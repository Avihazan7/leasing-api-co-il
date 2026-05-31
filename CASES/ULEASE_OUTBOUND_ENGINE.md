# ULease 🎯 — Outbound Engine (בלופרינט n8n + Claude)

**Module:** `CASES/ULEASE_OUTBOUND_ENGINE.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — בלופרינט אוטומציה (Stage 2–3).
**Integrates with:** `CASES/ULEASE_OUTREACH_SCRIPTS.md`, `CASES/ULEASE_IMPORTER_PLAYBOOK.md`, `CASES/ULEASE_LEASING_PLAYBOOK.md`, `CASES/ULEASE_SPEC.md`, `AI_PROGRESSION_PLAN.md`
**Inspiration:** ארכיטקטורת *Outbound Engine* (Quortihm · Usama Tanveer).

> מנוע אקווזיציה ל**צד ההיצע** — מאתר ומגייס יבואנים/מקבילים/ליסינג/דילרים אוטומטית, ומזין את ה-Marketplace. משתמש בסקריפטים (`ULEASE_OUTREACH_SCRIPTS.md`) ובמודלי Claude.

---

## 1. 8 השכבות

| # | שכבה | מה היא עושה ל-ULease | כלי / מודל |
|---|------|----------------------|------------|
| 01 | **Sourcing** | איתור יבואנים/מקבילים/ליסינג/דילרים | מאגרי חברות · LinkedIn · רישומי יבוא |
| 02 | **Quality Gate** | סינון ל-ICP (יש מלאי? סגמנט?), dedupe, אימות איש קשר | כללים + אימות אימייל |
| 03 | **Intelligence** | ניקוד פרוספקט: גודל מלאי, כאב (0 ק"מ תקוע?), reachability | **Claude Haiku 4.5** (ניקוד מהיר/זול) |
| 04 | **Personalization** | חיבור הפנייה לפי סגמנט + A/B (ערך מול סקרנות), 60–120 מילים, בלי "AI slop" | **Claude Sonnet 4.6** + Quality Gate |
| 05 | **Send Infra** | שליחה (אימייל/וואטסאפ), deliverability, ניטור bounce/spam | פלטפורמת שליחה + Health Monitor |
| 06 | **Reply Handling** | סיווג תגובה ל-4: מעוניין→יומן · התנגדות רכה→reframe · קשה→suppress · הסרה→block | **Claude Haiku 4.5** (classify) |
| 07 | **Measurement** | reply rate, meeting rate, עלות לפגישה (CPM), דשבורד חי | מחשבון + דשבורד |
| 08 | **Feedback Loop** | בחירת variants מנצחים, חידוד פרומפטים, דוח שבועי | Cron + refine |

---

## 2. הזרימה

```
Sourcing → Quality Gate → Intelligence(score) → Personalization(A/B) → Send
                                                                          ↓
   Feedback ← Measurement ← Reply Handling(classify → route) ←──────────┘
```

**עיקרון:** כל ליד עובר ניקוד → אם עובר סף, מקבל פנייה מותאמת → תגובה מסווגת ומנותבת → המדדים מזינים את שיפור הפרומפטים.

---

## 3. למה שני מודלים של Claude

- **Haiku 4.5** — לשכבות ה**נפח** (ניקוד 03, סיווג תגובות 06): מהיר, זול, "2-line reasoning". מריצים על כל ליד.
- **Sonnet 4.6** — לשכבת ה**איכות** (פרסונליזציה 04): כתיבה משכנעת, A/B hooks. מריצים רק על מי שעבר סף.

> חיסכון: ניקוד/סיווג ב-Haiku, כתיבה ב-Sonnet — איכות גבוהה בעלות נמוכה.

---

## 4. חיבור לסקריפטים ולפלייבוקים

- שכבה 04 (Personalization) שולפת את ה-hook לפי סגמנט מ-`ULEASE_OUTREACH_SCRIPTS.md`.
- שכבה 06 (Reply Handling) משתמשת בטבלאות ההתנגדויות מ-`ULEASE_IMPORTER_PLAYBOOK.md` / `ULEASE_LEASING_PLAYBOOK.md` כדי לנסח reframe.
- כל "מעוניין" → פיילוט (10 רכבים / 15 החזרות / חבילת רכש) לפי הסגמנט.

---

## 5. KPIs (כמו בדשבורד)

לידים מעובדים · אימיילים שנשלחו · תגובות · **פגישות שנקבעו** · **Reply Rate** · **Meeting Rate** · **עלות לפגישה (CPM)** · Health Score.
🎯 יעד התחלתי סביר: reply rate 15–25% · meeting rate (מתוך תגובות) 30–45%.

---

## 6. הקמה — מי, מתי, ואיך

| שלב | מצב | מי |
|-----|------|-----|
| **MVP** | חצי-ידני: סוגרסינג + פנייה ב-assist (אדם מאשר שליחה) | אברהם (לומד n8n — שלב 2 במפה) |
| **V1** | אוטומציה מלאה של שכבות 01–06 | Tech Lead (מימוש, deliverability) |
| **V2** | feedback loop אוטומטי + scale | Tech Lead |

> תואם ל-`AI_PROGRESSION_PLAN.md`: זה **בדיוק** הפרויקט שבו אברהם לומד Stage 2 (n8n/Webhooks) ו-Stage 3 (סוכני Claude) — תוך כדי בנייה אמיתית.

⚠️ **ציות:** outreach כפוף לחוק הספאם (תיקון 40) — opt-out, זיהוי שולח, ותדירות. לאמת לפני הפעלה בנפח.

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | בלופרינט מנוע outbound — 8 שכבות, מודלי Claude, חיבור לסקריפטים, KPIs | 2026-05-31 |

**Confidentiality.** מסמך תפעולי חסוי — חלק מה-Claude OS של Avraham Bar Yochai Chazan.

— *End of CASES/ULEASE_OUTBOUND_ENGINE.md v1.0.0 —*
