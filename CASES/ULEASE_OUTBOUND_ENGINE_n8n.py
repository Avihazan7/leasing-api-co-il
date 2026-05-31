#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULease 🎯 — Outbound Engine · n8n workflow generator
מפיק קובץ JSON שניתן לייבא ישירות ל-n8n (Import from File).
8 שכבות עם צמתי Claude (Haiku לניקוד/סיווג, Sonnet לפרסונליזציה).
הרצה:  python3 CASES/ULEASE_OUTBOUND_ENGINE_n8n.py
"""
import json, os

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

# ---------- שכבה 01 · Sourcing ----------
s = add("01 · Sourcing — Schedule", "n8n-nodes-base.scheduleTrigger", 1.2, [-160, 320],
        {"rule": {"interval": [{"field": "cronExpression", "expression": "0 6 * * 1,3,5"}]}})
src = add("01 · Sourcing — Apollo/Crustdata", "n8n-nodes-base.httpRequest", 4.2, [60, 320],
          {"method": "GET", "url": "https://api.apollo.io/v1/mixed_people/search",
           "options": {}}, )
link(s, src)

# ---------- שכבה 02 · Quality Gate ----------
qg = add("02 · Quality Gate — Dedup + ICP", "n8n-nodes-base.code", 2, [280, 320],
         {"jsCode": "// סינון ל-ICP: יש מלאי? סגמנט נכון? dedupe לפי אימייל/דומיין.\n"
                    "for (const item of $input.all()) {\n"
                    "  const d = item.json;\n"
                    "  d.icp_pass = Boolean(d.email) && (d.segment ?? '') !== '';\n"
                    "}\nreturn $input.all();"})
link(src, qg)
icp = add("02 · ICP Pass?", "n8n-nodes-base.if", 2, [500, 320],
          {"conditions": {"options": {"caseSensitive": True, "typeValidation": "loose"},
           "conditions": [{"leftValue": "={{ $json.icp_pass }}", "rightValue": True,
            "operator": {"type": "boolean", "operation": "true", "singleValue": True}}],
           "combinator": "and"}, "options": {}})
link(qg, icp)
rej = add("02 · Rejected (log)", "n8n-nodes-base.noOp", 1, [740, 460])
link(icp, rej, out=1)

# ---------- שכבה 03 · Intelligence (Haiku) ----------
score = http_claude("03 · Intelligence — Claude Haiku (score)", [740, 200], "claude-haiku-4-5",
    "You score B2B supply prospects for ULease (car marketplace). "
    "Given the prospect JSON, return ONLY JSON {\"score\":0-10,\"reason\":\"...\"}. "
    "High = importer/leasing with stuck inventory and reachable. Prospect: {{ JSON.stringify($json) }}")
link(icp, score, out=0)
parse = add("03 · Parse Score", "n8n-nodes-base.code", 2, [960, 200],
    {"jsCode": "// חילוץ ציון מתשובת Claude\nconst out = [];\nfor (const it of $input.all()){\n"
               "  const txt = it.json?.content?.[0]?.text ?? '{}';\n  let s=0,r='';\n"
               "  try{const j=JSON.parse(txt); s=j.score; r=j.reason;}catch(e){}\n"
               "  out.push({json:{...it.json, score:s, reason:r}});\n}\nreturn out;"})
link(score, parse)
thr = add("03 · Score ≥ 7?", "n8n-nodes-base.if", 2, [1180, 200],
          {"conditions": {"options": {"caseSensitive": True, "typeValidation": "loose"},
           "conditions": [{"leftValue": "={{ $json.score }}", "rightValue": 7,
            "operator": {"type": "number", "operation": "gte"}}], "combinator": "and"}, "options": {}})
link(parse, thr)
nur = add("03 · Nurture Queue (score<7)", "n8n-nodes-base.noOp", 1, [1400, 340])
link(thr, nur, out=1)

# ---------- שכבה 04 · Personalization (Sonnet) ----------
ctx = add("04 · Build Context", "n8n-nodes-base.set", 3.4, [1400, 80],
    {"assignments": {"assignments": [
        {"id": "seg", "name": "segment", "value": "={{ $json.segment }}", "type": "string"},
        {"id": "hook", "name": "hook_variant", "value": "=A", "type": "string"}]}, "options": {}})
link(thr, ctx, out=0)
pers = http_claude("04 · Personalization — Claude Sonnet (A/B)", [1620, 80], "claude-sonnet-4-6",
    "Write a 60-120 word Hebrew outbound message for ULease 🎯 to a {{ $json.segment }} prospect. "
    "Lead with their pain, one low-risk ask (pilot of 10 cars). No AI slop. "
    "Use the segment hook from ULEASE_OUTREACH_SCRIPTS. Prospect: {{ JSON.stringify($json) }}")
link(ctx, pers)
send = add("05 · Send — Email/Smartlead", "n8n-nodes-base.httpRequest", 4.2, [1840, 80],
           {"method": "POST", "url": "https://server.smartlead.ai/api/v1/campaigns/CAMPAIGN_ID/leads",
            "options": {}})
link(pers, send)
meas = add("07 · Measurement — CPM Calc", "n8n-nodes-base.code", 2, [2060, 80],
    {"jsCode": "// reply rate, meeting rate, cost-per-meeting\nconst sent=$json.sent??0, replies=$json.replies??0, meetings=$json.meetings??0, spend=$json.spend??0;\n"
               "return [{json:{reply_rate: sent? replies/sent:0, meeting_rate: replies? meetings/replies:0, cpm: meetings? spend/meetings:0}}];"})
link(send, meas)

# ---------- שכבה 06 · Reply Handling (Haiku) ----------
hook = add("06 · Reply — Inbound (Webhook)", "n8n-nodes-base.webhook", 2, [-160, 860],
           {"httpMethod": "POST", "path": "ulease-reply", "options": {}},
           {"webhookId": "ulease-reply-hook"})
clf = http_claude("06 · Classify — Claude Haiku", [120, 860], "claude-haiku-4-5",
    "Classify the reply intent. Return ONLY JSON {\"intent\":\"interested|soft|hard|unsubscribe\"}. "
    "Reply: {{ JSON.stringify($json.body) }}")
link(hook, clf)
parse2 = add("06 · Parse Intent", "n8n-nodes-base.code", 2, [340, 860],
    {"jsCode": "const out=[];for(const it of $input.all()){const t=it.json?.content?.[0]?.text??'{}';let i='hard';try{i=JSON.parse(t).intent;}catch(e){}out.push({json:{...it.json,intent:i}});}return out;"})
link(clf, parse2)
sw = add("06 · Route Reply (4-way)", "n8n-nodes-base.switch", 3, [560, 860],
    {"mode": "expression", "numberOutputs": 4,
     "output": "={{ ({interested:0, soft:1, hard:2, unsubscribe:3})[$json.intent] ?? 2 }}", "options": {}})
link(parse2, sw)
for i, (nm, y) in enumerate([("→ Interested · Calendar", 680), ("→ Soft Objection · Reframe", 800),
                              ("→ Hard Objection · Suppress", 920), ("→ Unsubscribe · Block", 1040)]):
    o = add(nm, "n8n-nodes-base.noOp", 1, [820, y])
    link(sw, o, out=i)

# ---------- Sticky notes ----------
def sticky(content, pos, w=360, h=240, color=4):
    nodes.append({"parameters": {"content": content, "height": h, "width": w, "color": color},
                  "id": "note-" + str(len(nodes)), "name": "Note " + str(len(nodes)),
                  "type": "n8n-nodes-base.stickyNote", "typeVersion": 1, "position": pos})

sticky("## ULease 🎯 — Outbound Engine\nשלד n8n · 8 שכבות.\n**הגדרות לפני הרצה:**\n- `ANTHROPIC_API_KEY` ב-Environment (או החלף ל-Credential).\n- Apollo / Smartlead: הוסף מפתחות + endpoints.\n- ICP/threshold: כוונן בצמתי Code/IF.\n⚠️ outreach כפוף לחוק הספאם — opt-out + תדירות.", [-200, -40], 460, 300, 5)
sticky("### 01–02 · Sourcing + Quality Gate\nאיתור (Apollo/Crustdata) → dedupe + סינון ICP.\nReject → log.", [-200, 560], 360, 180)
sticky("### 03–05 · Score → Personalize → Send\nHaiku מנקד (זול/נפח) · Sonnet כותב (איכות) · שליחה + מדידה.\nScore<7 → Nurture.", [700, -120], 420, 180)
sticky("### 06 · Reply Handling\nWebhook → Haiku מסווג → ניתוב 4-כיווני:\nInterested→יומן · Soft→reframe · Hard→suppress · Unsub→block.", [-200, 1140], 420, 160)

# ---------- Assemble ----------
workflow = {"name": "ULease 🎯 — Outbound Engine v1 (skeleton)",
            "nodes": nodes, "connections": conns, "active": False,
            "settings": {"executionOrder": "v1"}, "pinData": {},
            "meta": {"templateCredsSetupCompleted": False}, "tags": []}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ULEASE_OUTBOUND_ENGINE.n8n.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(workflow, f, ensure_ascii=False, indent=2)
print(f"נוצר workflow עם {len([n for n in nodes if n['type']!='n8n-nodes-base.stickyNote'])} צמתים "
      f"(+{sum(1 for n in nodes if n['type']=='n8n-nodes-base.stickyNote')} sticky) → ULEASE_OUTBOUND_ENGINE.n8n.json")
