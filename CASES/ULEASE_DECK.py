#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULease 🎯 Leasing.co.il — Pitch Deck Generator (13 slides)
מקור-אמת יחיד → מייצר Marp Markdown (.md) + HTML אינטראקטיבי עצמאי (.html).
ה-HTML: מצגת עם הקשה/החלקה/חיצים + כפתורים; נפילה-לאחור לגלילה ללא JS.
הרצה:  python3 CASES/ULEASE_DECK.py
"""
import os, html

ACCENT = "#c0532b"
CREAM  = "#f5f1e8"

SLIDES = [
    dict(title="ULease 🎯", subtitle="Leasing.co.il",
         lead="עסקת רכב חדש — דיגיטלית, מקצה-לקצה",
         bullets=["Marketplace תלת-צדדי · תורת המשחקים · Multi-agent"],
         note="מצגת השקעה · 2026"),
    dict(title="הבעיה 🔥",
         bullets=["שוק רכב חדש בכאוס תמחורי — מלאי **0 ק\"מ** תקוע מאמצע 2025",
                  "עשרות אלפי **גיולים** ב-2026 + דגמים חדשים נכנסים",
                  "שקל מתחזק → מרווחי יבואנים גדלים, מחירים נלחצים",
                  "עסקאות איטיות, אופליין, חוסר מקצועיות ושקיפות"],
         note="המלאי קיים. הביקוש קיים. אין מי שמחבר אותם דיגיטלית."),
    dict(title="הפתרון ✅",
         lead="ULease מחברת את שלושת הצדדים בפלטפורמה אחת:",
         bullets=["**היצע:** יבואנים · ליסינג · מימון → API",
                  "**ביקוש:** לקוחות פרטיים · B2B2C",
                  "**מפיצים:** דילרים/ליסינג קטנים (מנויים)"],
         note="→ חתימת עסקה דיגיטלית מקצה-לקצה."),
    dict(title="איך זה עובד",
         bullets=["① ספק מזרים מלאי (API / CSV)",
                  "② הלקוח מחפש → רואה **Deal Score**",
                  "③ חדר-עסקה: מימון/ליסינג → מקדמה → **חתימה דיגיטלית**",
                  "④ התחשבנות ישירה + עמלה"],
         note="ליד שלא נסגר → נמכר לספק (₪150). שום דבר לא מתבזבז."),
    dict(title="השוק 📊",
         bullets=["רכב חדש בישראל — שוק של מיליארדים בשנה",
                  "גל **0 ק\"מ + גיולים** ב-2026 = היצע עודף שמחפש ערוץ",
                  "שקל חזק = רוח גבית למרווחים וליבוא"],
         note="חלון הזדמנות נדיר — ULease ממקסמת אותו."),
    dict(title="המודל העסקי 💰",
         table=dict(headers=["מנוע הכנסה", "תמחור"],
                    rows=[["עמלת עסקה B2B (מהספק)", "1.1%–2.2%"],
                          ["עמלת עסקה B2B2C (עסקי)", "1.1%–3.33%"],
                          ["עמלת עסקה B2C (פרטי)", "3.33%–7.77%"],
                          ["מכירת ליד", "₪150"],
                          ["מנוי Ultra / Max (B2B)", "₪4,500 / ₪7,700"],
                          ["עמלת מימון (מחברת המימון)", "1% מערך העסקה"],
                          ["פרסום", "מימון · ביטוח · דרך"]]),
         note="עמלות מדורגות לפי סוג עסקה — גם ההיצע וגם הביקוש משלמים."),
    dict(title="הארכיטקטורה המתודולוגית 🧠",
         bullets=["**תורת המשחקים** — מכרז **מחיר-שני (Second-Price)**: המציע הגבוה זוכה ומשלם את הצעת המקום השני",
                  "**העשרה אינסטרומנטלית (Feuerstein)** — שכבת החלטה/UX שמכוונת",
                  "**Big Five** — פרופיל לקוח להתאמה מדויקת",
                  "**משא-ומתן מבוסס-אינטרסים** — BATNA שקוף + Win-Win",
                  "**Multi-agent: Ultra · Master · Max** — תזמור → מומחיות → ביצוע",
                  "**Deal Score** — ציון כדאיות לכל עסקה (IP)"],
         note="זה לא עוד אתר רכב. זו מערכת קבלת-החלטות."),
    dict(title="השקה 🚀",
         bullets=["הקמת חברה — השבוע · דומיין **ULease.co.il** — בתהליך רכישה",
                  "אתר לאוויר — תוך שבועיים",
                  "**בסיס יוני 2026:** 26 עסקאות · 130 לידים · 15 מנויים · 7 ספקים"],
         note="עולים לאוויר עם עסקאות אמיתיות — לא הדגמה."),
    dict(title="תחזית פיננסית 📈",
         table=dict(headers=["", "2026 (יוני–דצמ')", "2027"],
                    rows=[["עסקאות", "314", "1,737"],
                          ["GMV", "₪47.1M", "₪260.5M"],
                          ["הכנסה", "₪2.29M", "₪12.98M"],
                          ["נטו (תפעולי)", "₪1.74M", "₪10.89M"]]),
         note="Base Case v1.4 (עמלות מדורגות) · Run-rate דצמבר 2027: ₪17.4M / שנה · נטו לפני מס."),
    dict(title="Unit Economics 💎",
         bullets=["₪3,001 הכנסה משוקללת לעסקה (עמלות מדורגות 1.1%–7.77%)",
                  "עמלת מימון: 1% מערך העסקה מחברת המימון",
                  "מנויים חוזרים Ultra/Max ₪4,500–7,700 / חודש",
                  "צוות רזה (שלב 1: ₪30K / חודש)",
                  "→ **תזרים חיובי כבר מחודש ההשקה**"],
         note="הגיוס = הון צמיחה, לא runway להישרדות."),
    dict(title="הצוות 👥",
         bullets=["**שירי הלפישטיין** — Super COO · פיקוח, ריכוז, מחזיקת מניות",
                  "**אברהם בר יוחאי חזן** — מו\"פ ושיווק · 21 שנות ענף, Leasing.co.il",
                  "**מגייסים:** מנהל מערכות טכנולוגיה"],
         note="ידע ענף עמוק + ביצוע + מתודולוגיה."),
    dict(title="הגיוס 🤝",
         lead="₪150,000",
         bullets=["40% — טכנולוגיה והקמת פלטפורמה",
                  "35% — שיווק דיגיטלי",
                  "15% — הקמה משפטית / תשתית",
                  "10% — כרית ביטחון"],
         note="להאיץ צמיחה ולקצר time-to-scale."),
    dict(title="החזון 🎯",
         lead="ULease 🎯 Leasing.co.il",
         bullets=["התשתית הדיגיטלית של עסקת הרכב החדש בישראל.",
                  "מקצה-לקצה. ברמת קצה."],
         note="בואו נבנה את זה יחד · avihazan112@gmail.com"),
]

# ---------------- בולד **טקסט** ----------------
def md_bold_to_html(s):
    out, i, b = [], 0, False
    s = html.escape(s)
    while i < len(s):
        if s[i:i+2] == "**":
            out.append("<strong>" if not b else "</strong>"); b = not b; i += 2
        else:
            out.append(s[i]); i += 1
    return "".join(out)

# ---------------- Marp Markdown ----------------
def render_md():
    fm = ("---\n"
          "marp: true\n"
          "paginate: true\n"
          "style: |\n"
          "  section { direction: rtl; text-align: right; font-family: Arial, \"Helvetica Neue\", sans-serif; }\n"
          f"  h1, h2 {{ color: {ACCENT}; }}\n"
          f"  strong {{ color: {ACCENT}; }}\n"
          "---\n")
    meta = ("<!-- Module: CASES/ULEASE_DECK.md | Version: 1.2.0 | "
            "Author: Avraham Bar Yochai Chazan — Claude OS | Status: Active (Pitch Deck, 13 slides) | "
            "Interactive build: CASES/ULEASE_DECK.html (generated together by ULEASE_DECK.py) -->\n")
    parts = [fm + meta]
    for s in SLIDES:
        blk = [f"## {s['title']}"]
        if s.get("subtitle"): blk.append(f"### {s['subtitle']}")
        if s.get("lead"):     blk.append(f"**{s['lead']}**")
        for b in s.get("bullets", []): blk.append(f"- {b}")
        t = s.get("table")
        if t:
            blk.append("| " + " | ".join(t["headers"]) + " |")
            blk.append("|" + "|".join(["---"]*len(t["headers"])) + "|")
            for r in t["rows"]: blk.append("| " + " | ".join(r) + " |")
        if s.get("note"): blk.append(f"\n> *{s['note']}*")
        parts.append("\n".join(blk))
    return "\n\n---\n\n".join(parts) + "\n"

# ---------------- HTML אינטראקטיבי עצמאי ----------------
def render_html():
    css = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#2a2622;font-family:Arial,'Helvetica Neue',sans-serif}}
.slide{{direction:rtl;text-align:right;width:100%;max-width:1000px;min-height:100vh;
  margin:0 auto;padding:8vh 9vw;display:flex;flex-direction:column;justify-content:center;
  background:{CREAM};color:#2a2622;border-bottom:1px solid #ddd;position:relative}}
.kicker{{color:{ACCENT};font-weight:700;letter-spacing:.15em;font-size:.85rem;margin-bottom:1.2rem}}
.slide h2{{color:{ACCENT};font-size:2.5rem;line-height:1.15;margin-bottom:.4rem}}
.slide h3{{color:#2a2622;font-size:1.6rem;font-weight:400;margin-bottom:.8rem;opacity:.75}}
.lead{{font-size:1.5rem;font-weight:700;margin:.6rem 0 1.2rem}}
ul{{list-style:none}}
li{{font-size:1.25rem;line-height:1.85;padding-right:1.4rem;position:relative}}
li::before{{content:'';position:absolute;right:0;top:.8em;width:.5rem;height:.5rem;background:{ACCENT};border-radius:50%}}
strong{{color:{ACCENT}}}
table{{border-collapse:collapse;margin-top:.8rem;font-size:1.2rem;width:100%}}
th,td{{padding:.55rem 1rem;border-bottom:1px solid #ccc;text-align:right}}
th{{color:{ACCENT};border-bottom:2px solid {ACCENT}}}
.note{{margin-top:1.8rem;font-style:italic;font-size:1.1rem;opacity:.8;border-right:3px solid {ACCENT};padding-right:1rem}}
.hint{{margin-top:1.6rem;color:{ACCENT};font-weight:700;font-size:1rem}}
.page{{position:absolute;bottom:3vh;left:9vw;color:{ACCENT};font-weight:700;font-size:.9rem}}
.title-slide h2{{font-size:3.6rem}}
/* --- ניווט (מצב JS) --- */
.deck-nav,.progress,.hint{{display:none}}
.deck-nav{{position:fixed;bottom:0;left:0;right:0;z-index:10;align-items:center;
  justify-content:space-between;padding:.55rem 1rem;background:rgba(42,38,34,.92);direction:rtl}}
.deck-nav button{{background:{ACCENT};color:#fff;border:none;border-radius:8px;
  padding:.65rem 1.3rem;font-size:1.05rem;font-weight:700;cursor:pointer}}
.deck-nav .counter{{color:#fff;font-weight:700;font-size:1rem}}
.progress{{position:fixed;top:0;right:0;height:4px;background:{ACCENT};z-index:11;width:0;transition:width .25s}}
.js .deck-nav{{display:flex}}
.js .progress{{display:block}}
.js .hint{{display:block}}
.js .page{{display:none}}
.js .slide{{position:fixed;inset:0;max-width:none;min-height:0;opacity:0;pointer-events:none;
  transition:opacity .25s ease;overflow:auto;justify-content:safe center;padding-bottom:12vh}}
.js .slide.active{{opacity:1;pointer-events:auto;z-index:1}}
@media print{{
  html,body{{background:#fff}}
  .deck-nav,.progress,.hint{{display:none!important}}
  .slide,.js .slide{{position:static;opacity:1;pointer-events:auto;min-height:auto;
    height:100vh;page-break-after:always;border:none;max-width:none}}
}}
"""
    secs = []
    n = len(SLIDES)
    for i, s in enumerate(SLIDES, 1):
        cls = "slide title-slide" if i == 1 else "slide"
        parts = [f'<div class="kicker">{i:02d} / {n}</div>',
                 f'<h2>{md_bold_to_html(s["title"])}</h2>']
        if s.get("subtitle"): parts.append(f'<h3>{md_bold_to_html(s["subtitle"])}</h3>')
        if s.get("lead"):     parts.append(f'<div class="lead">{md_bold_to_html(s["lead"])}</div>')
        if s.get("bullets"):
            lis = "".join(f"<li>{md_bold_to_html(b)}</li>" for b in s["bullets"])
            parts.append(f"<ul>{lis}</ul>")
        t = s.get("table")
        if t:
            head = "".join(f"<th>{html.escape(h)}</th>" for h in t["headers"])
            body = "".join("<tr>" + "".join(f"<td>{md_bold_to_html(c)}</td>" for c in r) + "</tr>"
                           for r in t["rows"])
            parts.append(f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>")
        if s.get("note"): parts.append(f'<div class="note">{md_bold_to_html(s["note"])}</div>')
        if i == 1: parts.append('<div class="hint">הקש · החלק · או מקשי ←/→ למעבר בין שקפים</div>')
        parts.append(f'<div class="page">ULease 🎯 · {i}</div>')
        secs.append(f'<section class="{cls}">' + "".join(parts) + "</section>")

    nav = ('<div class="progress"></div>'
           '<div class="deck-nav">'
           '<button id="btnPrev">›&nbsp;הקודם</button>'
           f'<span class="counter">1 / {n}</span>'
           '<button id="btnNext">הבא&nbsp;‹</button>'
           '</div>')

    js = """
<script>
(function(){
  var slides=[].slice.call(document.querySelectorAll('.slide'));
  var n=slides.length,i=0;
  document.body.classList.add('js');
  var counter=document.querySelector('.counter'), bar=document.querySelector('.progress');
  function show(k){
    i = k<0?0:(k>n-1?n-1:k);
    for(var j=0;j<n;j++) slides[j].classList.toggle('active', j===i);
    if(counter) counter.textContent=(i+1)+' / '+n;
    if(bar) bar.style.width=((i+1)/n*100)+'%';
    if(slides[i]) slides[i].scrollTop=0;
  }
  function next(){show(i+1);} function prev(){show(i-1);}
  document.addEventListener('keydown',function(e){
    var k=e.key;
    if(k==='ArrowLeft'||k==='ArrowDown'||k==='PageDown'||k===' '||k==='Spacebar'){next();e.preventDefault();}
    else if(k==='ArrowRight'||k==='ArrowUp'||k==='PageUp'){prev();e.preventDefault();}
    else if(k==='Home'){show(0);} else if(k==='End'){show(n-1);}
  });
  document.addEventListener('click',function(e){
    if(e.target.closest && e.target.closest('.deck-nav')) return;
    next();
  });
  var x0=null,y0=null;
  document.addEventListener('touchstart',function(e){x0=e.touches[0].clientX;y0=e.touches[0].clientY;},{passive:true});
  document.addEventListener('touchend',function(e){
    if(x0===null) return;
    var dx=e.changedTouches[0].clientX-x0, dy=e.changedTouches[0].clientY-y0;
    if(Math.abs(dx)>40 && Math.abs(dx)>Math.abs(dy)){ if(dx<0) next(); else prev(); }
    x0=null; y0=null;
  },{passive:true});
  var bn=document.getElementById('btnNext'), bp=document.getElementById('btnPrev');
  if(bn) bn.addEventListener('click',function(e){e.stopPropagation();next();});
  if(bp) bp.addEventListener('click',function(e){e.stopPropagation();prev();});
  show(0);
})();
</script>
"""
    return ("<!doctype html><html lang='he' dir='rtl'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>ULease 🎯 — Pitch Deck</title>"
            f"<style>{css}</style></head><body>"
            + "".join(secs) + nav + js + "</body></html>")

# ---------------- כתיבה ----------------
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "ULEASE_DECK.md"), "w", encoding="utf-8") as f:
    f.write(render_md())
with open(os.path.join(here, "ULEASE_DECK.html"), "w", encoding="utf-8") as f:
    f.write(render_html())
print(f"נוצרו {len(SLIDES)} שקפים → ULEASE_DECK.md (Marp) + ULEASE_DECK.html (אינטראקטיבי).")
