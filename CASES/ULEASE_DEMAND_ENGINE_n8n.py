#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULease 🎯 — Demand Engine · AI Receptionist (WhatsApp) · n8n workflow generator
מפיק קובץ JSON שניתן לייבא ישירות ל-n8n (Import from File).
תת-זרם דלת-הכניסה של מנוע הביקוש (ראו CASES/ULEASE_DEMAND_ENGINE.md §9):
  WhatsApp (טקסט + קול) → סיווג כוונה (Haiku) → אחזור מ-Sheets (FAQ/INVENTORY)
  → תשובה מעוגנת (Sonnet, עובדות מהכלי בלבד) → שער HITL לכל כתיבה (order) → שליחה.
המקור (תמונת n8n) רץ על OpenAI בלי HITL; כאן זה מתוקן ל-Claude + grounding + D-040.
הרצה:  python3 CASES/ULEASE_DEMAND_ENGINE_n8n.py
"""
import json, os

# I5 · ריכוז שמות המודלים במקום אחד — לא hard-coded בכל צומת (מונע drift).
# Haiku = שכבת הנפח (סיווג כוונה) · Sonnet = שכבת האיכות (ניסוח מעוגן).
HAIKU = "claude-haiku-4-5"
SONNET = "claude-sonnet-4-6"

nodes, conns = [], {}


def add(name, type_, tv, pos, params=None, extra=None):
    n = {"parameters": params or {}, "id": name.replace(" ", "-")[:60],
         "name": name, "type": type_, "typeVersion": tv, "position": pos}
    if extra: n.update(extra)
    nodes.append(n)
    return name


def link(src, dst, out=0):
    conns.setdefault(src, {}).setdefault("main", [])
    while len(conns[src]["main"]) <= out:
        conns[src]["main"].append([])
    conns[src]["main"][out].append({"node": dst, "type": "main", "index": 0})


def claude_body(model, prompt):
    return json.dumps({"model": model, "max_tokens": 400,
                       "messages": [{"role": "user", "content": prompt}]}, ensure_ascii=False)


def http_claude(name, pos, model, prompt):
    return add(name, "n8n-nodes-base.httpRequest", 4.2, pos, {
        "method": "POST", "url": "https://api.anthropic.com/v1/messages",
        "sendHeaders": True, "headerParameters": {"parameters": [
            {"name": "x-api-key", "value": "={{ $env.ANTHROPIC_API_KEY }}"},
            {"name": "anthropic-version", "value": "2023-06-01"},
            {"name": "content-type", "value": "application/json"}]},
        "sendBody": True, "specifyBody": "json", "jsonBody": claude_body(model, prompt),
        "options": {}})


# ---------- Intake · קליטת WhatsApp + ניתוב לפי סוג ----------
trig = add("Intake · WhatsApp Trigger (inbound)", "n8n-nodes-base.whatsAppTrigger", 1, [-220, 300],
           {"updates": ["messages"]}, {"webhookId": "ulease-wa-receptionist"})
sw_type = add("Intake · Switch — Text / Audio", "n8n-nodes-base.switch", 3, [0, 300],
              {"mode": "expression", "numberOutputs": 2,
               "output": "={{ $json.messages?.[0]?.type === 'audio' ? 1 : 0 }}", "options": {}})
link(trig, sw_type)

# מסלול קולי (out=1): הורדת המדיה → תמלול (ספק STT) → מתנקז ל-Normalize יחד עם הטקסט
dl = add("Audio · Download Media", "n8n-nodes-base.httpRequest", 4.2, [240, 520],
         {"method": "GET", "url": "={{ $json.messages?.[0]?.audio?.url }}", "options": {}})
link(sw_type, dl, out=1)
stt = add("Audio · Transcribe (STT provider)", "n8n-nodes-base.httpRequest", 4.2, [460, 520],
          {"method": "POST", "url": "https://STT_PROVIDER/transcribe", "options": {}})
link(dl, stt)

# ---------- Normalize · איחוד שני המסלולים לסוכן אחד (שיפור #4) ----------
norm = add("Normalize · Unify Text + Phone", "n8n-nodes-base.set", 3.4, [700, 300],
           {"assignments": {"assignments": [
               {"id": "txt", "name": "text",
                "value": "={{ $json.messages?.[0]?.text?.body ?? $json.text ?? '' }}", "type": "string"},
               {"id": "wa", "name": "wa_from",
                "value": "={{ $json.messages?.[0]?.from ?? $json.wa_from }}", "type": "string"}]},
            "options": {}})
link(sw_type, norm, out=0)   # מסלול טקסט
link(stt, norm)              # מסלול קול אחרי תמלול

# ---------- Lead upsert · "אין ליד מבוזבז" (שיפור #7) ----------
lead = add("Lead · Upsert by Phone (Sheets/CRM)", "n8n-nodes-base.googleSheets", 4, [700, 120],
           {"operation": "appendOrUpdate", "options": {}})
link(norm, lead)

# ---------- Classify · סיווג כוונה (Haiku) + ניקוד (שיפורים #8/#10) ----------
clf = http_claude("Classify · Intent — Claude Haiku", [920, 300], HAIKU,
    "You are the WhatsApp receptionist intent classifier for ULease 🎯 (car-leasing marketplace). "
    "Return ONLY JSON {\"intent\":\"faq|inventory|order|human\",\"intent_score\":0-100}. "
    "intent_score = buying intent. 'order' = place/change a leasing order (a WRITE action). "
    "Message: {{ $json.text }}")
link(norm, clf)
pintent = add("Classify · Parse Intent", "n8n-nodes-base.code", 2, [1140, 300],
    {"jsCode": "// חילוץ intent + score מתשובת Claude (fallback בטוח: human)\nconst out=[];\n"
               "for (const it of $input.all()){\n"
               "  const t = it.json?.content?.[0]?.text ?? '{}';\n"
               "  let intent='human', score=0;\n"
               "  try{const j=JSON.parse(t); intent=j.intent||'human'; score=j.intent_score??0;}catch(e){}\n"
               "  out.push({json:{...it.json, intent, intent_score:score}});\n}\nreturn out;"})
link(clf, pintent)
sw_intent = add("Route · Intent (4-way)", "n8n-nodes-base.switch", 3, [1360, 300],
    {"mode": "expression", "numberOutputs": 4,
     "output": "={{ ({faq:0, inventory:1, order:2, human:3})[$json.intent] ?? 3 }}", "options": {}})
link(pintent, sw_intent)

# ---------- Retrieval · אחזור עובדות מ-Sheets (ה-grounding) ----------
faq = add("FAQ · Read (Sheets)", "n8n-nodes-base.googleSheets", 4, [1600, 120],
          {"operation": "read", "options": {}})
link(sw_intent, faq, out=0)
inv = add("INVENTORY · Read (Sheets)", "n8n-nodes-base.googleSheets", 4, [1600, 280],
          {"operation": "read", "options": {}})
link(sw_intent, inv, out=1)

# ---------- HITL · שער אנושי לכל כתיבה (שיפור #1 · D-040) ----------
hitl = add("HITL · Approve Order (sendAndWait)", "n8n-nodes-base.noOp", 1, [1600, 460])
link(sw_intent, hitl, out=2)
order_w = add("Order · Create/Update (Sheets) — after approval", "n8n-nodes-base.googleSheets", 4,
              [1820, 460], {"operation": "appendOrUpdate", "options": {}})
link(hitl, order_w)

# ---------- Human · אסקלציה (תלונה / בקשת אדם) ----------
human = add("Human · Escalate", "n8n-nodes-base.noOp", 1, [1600, 660])
link(sw_intent, human, out=3)
hand = add("Human · Handoff Message", "n8n-nodes-base.set", 3.4, [1820, 660],
           {"assignments": {"assignments": [
               {"id": "h", "name": "reply",
                "value": "=קיבלנו 🙏 נציג/ה יחזרו אליך בהקדם.", "type": "string"}]}, "options": {}})
link(human, hand)

# ---------- Reply · ניסוח מעוגן (Sonnet) — עובדות מהכלי בלבד (שיפור #2 · SPEC §7.2) ----------
reply = http_claude("Reply · Grounded — Claude Sonnet", [1820, 240], SONNET,
    "You are ULease's WhatsApp assistant. Answer the customer in Hebrew using ONLY the DATA below "
    "(prices, availability, FAQ). If the answer is NOT in DATA, say you'll check and a human will follow up — "
    "NEVER invent prices, availability, monthly payments or any number (grounding: 100% factual). "
    "Keep it short and WhatsApp-friendly. CUSTOMER: {{ $json.text }} | DATA: {{ JSON.stringify($json) }}")
link(faq, reply)
link(inv, reply)
link(order_w, reply)

# ---------- Send + Measurement ----------
send = add("Send · WhatsApp Reply", "n8n-nodes-base.whatsApp", 1, [2060, 300],
           {"operation": "send", "options": {}})
link(reply, send)
link(hand, send)
log = add("Measurement · Log Outcome", "n8n-nodes-base.code", 2, [2280, 300],
    {"jsCode": "// לוג תוצאת השיחה לשכבת המדידה (answered/qualified/ordered/escalated/opt-out)\n"
               "const j=$json; return [{json:{wa_from:j.wa_from, intent:j.intent, "
               "intent_score:j.intent_score, ts:new Date().toISOString()}}];"})
link(send, log)


# ---------- Sticky notes ----------
def sticky(content, pos, w=360, h=240, color=4):
    nodes.append({"parameters": {"content": content, "height": h, "width": w, "color": color},
                  "id": "note-" + str(len(nodes)), "name": "Note " + str(len(nodes)),
                  "type": "n8n-nodes-base.stickyNote", "typeVersion": 1, "position": pos})


sticky("## ULease 🎯 — Demand Engine · AI Receptionist (WhatsApp)\n"
       "שלד n8n · דלת-הכניסה של מנוע הביקוש (DEMAND_ENGINE §9 · צומת 16).\n"
       "**הגדרות לפני הרצה:**\n"
       "- `ANTHROPIC_API_KEY` ב-Environment (או Credential ב-2 צמתי Claude).\n"
       "- WhatsApp Business Cloud + Google Sheets credentials.\n"
       "- ⚠️ ציות: inbound בלבד · חלון 24ש'/template-messages · opt-out בכל הודעה (תיקון 40).",
       [-260, 20], 470, 280, 5)
sticky("### Intake · טקסט + קול\nSwitch מנתב לפי סוג. קול → הורדת מדיה → STT → מתנקז ל-Normalize.\n"
       "**STT** = ספק תמלול נפרד (Whisper/אחר) — לא ה-agent LLM; D-022 חל על הסוכן, לא על ה-STT. לאישור.",
       [-40, 560], 420, 160)
sticky("### Classify (Haiku) → Route\nסיווג כוונה + intent_score → ניתוב 4-כיווני: FAQ · INVENTORY · order · human.\n"
       "**Lead upsert** בכל שיחה — \"אין ליד מבוזבז\" (₪150 לספק).", [900, 20], 420, 170)
sticky("### Grounding (Sonnet · SPEC §7.2)\nתשובה מעובדות ה-Sheet בלבד; אין דאטה → \"אבדוק + אדם יחזור\".\n"
       "אסור להמציא מחיר/זמינות/החזר. Sheets = MVP; ל-V1 מעבר ל-DB + Idempotency (Tech Lead).",
       [1760, 20], 420, 180)
sticky("### HITL (D-040) · שער כתיבה\nכל `order` עוצר לאישור אדם (`sendAndWait`) לפני כתיבה.\n"
       "ה-NoOp = placeholder — החלף ב-Send-and-Wait אמיתי. דגימת 10% באוטונומיה.",
       [1760, 640], 420, 160)

# ---------- Assemble ----------
workflow = {"name": "ULease 🎯 — Demand Engine · AI Receptionist v1 (skeleton)",
            "nodes": nodes, "connections": conns, "active": False,
            "settings": {"executionOrder": "v1"}, "pinData": {},
            "meta": {"templateCredsSetupCompleted": False}, "tags": []}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ULEASE_DEMAND_ENGINE.n8n.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(workflow, f, ensure_ascii=False, indent=2)
print(f"נוצר workflow עם {len([n for n in nodes if n['type']!='n8n-nodes-base.stickyNote'])} צמתים "
      f"(+{sum(1 for n in nodes if n['type']=='n8n-nodes-base.stickyNote')} sticky) → ULEASE_DEMAND_ENGINE.n8n.json")
