#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULease 🎯 Leasing.co.il — Pitch Deck Generator (13 slides)
מקור-אמת יחיד → מייצר Marp Markdown (.md) + HTML עצמאי (.html).
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
                    rows=[["עמלת עסקה", "3.33% ≈ ₪4,995"],
                          ["מכירת ליד", "₪150"],
                          ["מנוי Pro / Pro Max", "₪4,500 / ₪7,700"],
                          ["פרסום", "מימון · ביטוח · דרך"]]),
         note="ארבעה זרמים — גם ההיצע וגם הביקוש משלמים."),
    dict(title="הארכיטקטורה המתודולוגית 🧠",
         bullets=["**תורת המשחקים** — מכרז **מחיר-שני (Vickrey)**: תמחור יעיל וחשיפת-אמת",
                  "**העשרה אינסטרומנטלית (Feuerstein)** — שכבת החלטה/UX שמכוונת",
                  "**Big Five** — פרופיל לקוח להתאמה מדויקת",
                  "**Multi-agent: Ultra · Master · Max** — תזמור → מומחיות → ביצוע",
                  "**Deal Score** — ציון כדאיות לכל עסקה (IP)"],
         note="זה לא עוד אתר רכב. זו מערכת קבלת-החלטות."),
    dict(title="השקה 🚀",
         bullets=["הקמת חברה — השבוע · דומיין **ULease.co.il** — נרכש",
                  "אתר לאוויר — תוך שבועיים",
                  "**בסיס יוני 2026:** 26 עסקאות · 130 לידים · 15 מנויים · 7 ספקים"],
         note="עולים לאוויר עם עסקאות אמיתיות — לא הדגמה."),
    dict(title="תחזית פיננסית 📈",
         table=dict(headers=["", "2026 (יוני–דצמ')", "2027"],
                    rows=[["עסקאות", "314", "1,737"],
                          ["GMV", "₪47.1M", "₪260.5M"],
                          ["הכנסה", "₪2.79M", "₪15.14M"],
                          ["נטו", "₪2.23M", "₪13.05M"]]),
         note="Run-rate דצמבר 2027: ₪20.2M / שנה."),
    dict(title="Unit Economics 💎",
         bullets=["₪4,995 רווח לעסקה (3.33% × ₪150K)",
                  "מנויים חוזרים ₪4,500–7,700 / חודש",
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
          "  section::after { content: attr(data-marpit-pagination) ' / ' attr(data-marpit-pagination-total); }\n"
          "---\n")
    meta = ("<!-- Module: CASES/ULEASE_DECK.md | Version: 1.0.0 | "
            "Author: Avraham Bar Yochai Chazan — Claude OS | Status: Active (Pitch Deck, 13 slides) -->\n")
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

# ---------------- HTML עצמאי ----------------
def render_html():
    css = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#2a2622;font-family:Arial,'Helvetica Neue',sans-serif}}
.slide{{direction:rtl;text-align:right;width:100%;max-width:1000px;min-height:100vh;
  margin:0 auto;padding:8vh 9vw;display:flex;flex-direction:column;justify-content:center;
  background:{CREAM};color:#2a2622;border-bottom:1px solid #ddd;position:relative;
  scroll-snap-align:start}}
html{{scroll-snap-type:y mandatory}}
.kicker{{color:{ACCENT};font-weight:700;letter-spacing:.15em;font-size:.85rem;margin-bottom:1.2rem}}
.slide h2{{color:{ACCENT};font-size:2.6rem;line-height:1.15;margin-bottom:.4rem}}
.slide h3{{color:#2a2622;font-size:1.6rem;font-weight:400;margin-bottom:.8rem;opacity:.75}}
.lead{{font-size:1.5rem;font-weight:700;margin:.6rem 0 1.2rem}}
ul{{list-style:none}}
li{{font-size:1.3rem;line-height:1.9;padding-right:1.4rem;position:relative}}
li::before{{content:'';position:absolute;right:0;top:.85em;width:.5rem;height:.5rem;
  background:{ACCENT};border-radius:50%}}
strong{{color:{ACCENT}}}
table{{border-collapse:collapse;margin-top:.8rem;font-size:1.25rem;width:100%}}
th,td{{padding:.6rem 1rem;border-bottom:1px solid #ccc;text-align:right}}
th{{color:{ACCENT};border-bottom:2px solid {ACCENT}}}
.note{{margin-top:2rem;font-style:italic;font-size:1.15rem;opacity:.8;
  border-right:3px solid {ACCENT};padding-right:1rem}}
.page{{position:absolute;bottom:3vh;left:9vw;color:{ACCENT};font-weight:700;font-size:.9rem}}
.title-slide h2{{font-size:4rem}}
@media print{{
  html,body{{background:#fff}}
  .slide{{min-height:auto;height:100vh;page-break-after:always;border:none;max-width:none}}
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
        parts.append(f'<div class="page">ULease 🎯 · {i}</div>')
        secs.append(f'<section class="{cls}">' + "".join(parts) + "</section>")
    return ("<!doctype html><html lang='he' dir='rtl'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>ULease 🎯 — Pitch Deck</title>"
            f"<style>{css}</style></head><body>" + "".join(secs) + "</body></html>")

# ---------------- כתיבה ----------------
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "ULEASE_DECK.md"), "w", encoding="utf-8") as f:
    f.write(render_md())
with open(os.path.join(here, "ULEASE_DECK.html"), "w", encoding="utf-8") as f:
    f.write(render_html())
print(f"נוצרו {len(SLIDES)} שקפים → ULEASE_DECK.md (Marp) + ULEASE_DECK.html (עצמאי).")
