# ULease 🎯 — Outbound Engine (בלופרינט n8n + Claude)

**Module:** `CASES/ULEASE_OUTBOUND_ENGINE.md`
**Version:** 1.2.1
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — בלופרינט אוטומציה (Stage 2–3).
**Integrates with:** `CASES/ULEASE_OUTREACH_SCRIPTS.md`, `CASES/ULEASE_IMPORTER_PLAYBOOK.md`, `CASES/ULEASE_LEASING_PLAYBOOK.md`, `CASES/ULEASE_SPEC.md`, `AI_PROGRESSION_PLAN.md`, `AI_PROCESS_INTELLIGENCE.md`
**Inspiration:** ארכיטקטורת *Outbound Engine* (Quortihm · Usama Tanveer).

> מנוע אקווזיציה ל**צד ההיצע** — מאתר ומגייס את 4 הסגמנטים (יבואן רשמי · יבואן מקביל · חברת ליסינג · מימון/ביטוח, כמו ב-`ULEASE_OUTREACH_SCRIPTS.md`) ומזין את ה-Marketplace. משתמש בסקריפטים ובמודלי Claude.

---

## 1. 8 השכבות

| # | שכבה | מה היא עושה ל-ULease | כלי / מודל |
|---|------|----------------------|------------|
| 01 | **Sourcing** | איתור 4 הסגמנטים: יבואנים רשמיים · מקבילים · ליסינג · מימון/ביטוח | מאגרי חברות · LinkedIn · רישומי יבוא |
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

> ⚠️ **מצב השלד (W14):** בקובץ ה-n8n המיובא, שכבות 01–06 מחווטות; שכבה 07 (Measurement) קיימת כצומת קצה ושכבה 08 (Feedback Loop) **טרם ממומשת** — היא מופעלת ידנית (סקירה שבועית) עד V2.

---

## 2.5 היחס לארכיטקטורת המוצר (Ultra·Master·Max)

מנוע ה-outbound הוא **מערכת acquisition נפרדת** מהמנוע המוצרי (`ULEASE_SPEC.md` §7) — הוא רץ ב-n8n מחוץ לפלטפורמה, לא בתוכה. כשהפלטפורמה תבשיל (Phase 1+), המנוע ימופה ל-**Master "Content/Marketing"** וה-suppression list שלו תסתנכרן עם ישות ה-`Consent` (Guardian).

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
| **MVP** | חצי-ידני: סורסינג + פנייה ב-assist — **HITL מלא**: כל שליחה עוצרת לאישור אדם (`sendAndWait`) | אברהם (לומד n8n — שלב 2 במפה) |
| **V1** | אוטומציה מלאה של שכבות 01–06 — **בכפוף לשער הבגרות (§6.1)** | Tech Lead (מימוש, deliverability) |
| **V2** | feedback loop אוטומטי + scale | Tech Lead |

> תואם ל-`AI_PROGRESSION_PLAN.md`: זה **בדיוק** הפרויקט שבו אברהם לומד Stage 2 (n8n/Webhooks) ו-Stage 3 (סוכני Claude) — תוך כדי בנייה אמיתית.

### 6.1 שער הבגרות — מ-assist לאוטונומיה (D-040)

המעבר MVP→V1 הוא לא החלטת לוח-זמנים — הוא **שער שעוברים בהוכחה** (הדפוס המלא: `AI_PROCESS_INTELLIGENCE.md` §3.3):

| שלב | מה מאושר ידנית | קריטריון מעבר לשלב הבא |
|------|------------------|--------------------------|
| **1 · HITL מלא** (MVP) | כל מייל/וואטסאפ — לפני שליחה | **20 אישורים רצופים ללא תיקון** (טקסט, נמען, סגמנט) |
| **2 · HITL חלקי** | פניות ליבואנים רשמיים (הסגמנט הרגיש) + כל הודעה ראשונה לארגון חדש | חודש ללא תקרית: תלונה, טעות זיהוי או הפרת ציות |
| **3 · אוטונומיה מנוטרת** (V1) | כלום — אך **10% מהשליחות נדגמות** לבדיקה שבועית | קבוע. הניטור לא יורד לעולם |

> ⚠️ שכבה 06 (Reply Handling) כפופה לאותו שער: סיווג "הסרה→block" חייב **דיוק 100%** לפני אוטונומיה — טעות שם היא הפרת חוק הספאם, לא באג.

⚠️ **ציות:** outreach כפוף לחוק הספאם (תיקון 40) — opt-out, זיהוי שולח, ותדירות. לאמת לפני הפעלה בנפח.

---

## 7. קובץ n8n מוכן לייבוא

- **`CASES/ULEASE_OUTBOUND_ENGINE.n8n.json`** — workflow שלד (**25 צמתים**: 21 פונקציונליים + 4 הערות sticky) לייבוא ישיר ל-n8n (`Workflows → Import from File`).
- **`CASES/ULEASE_OUTBOUND_ENGINE_n8n.py`** — הגנרטור (מקור-אמת; משנים → מריצים → ה-JSON מתעדכן).

**לפני הרצה:**
1. הגדר `ANTHROPIC_API_KEY` ב-Environment של n8n (או החלף ל-Credential ב-3 צמתי Claude).
2. הוסף מפתחות/endpoints ל-Apollo (שכבה 01) ול-Smartlead (05).
3. כוונן ICP (צומת 02) וסף ניקוד (צומת 03 — כרגע ≥7).
4. מודלים: **Haiku 4.5** לניקוד/סיווג · **Sonnet 4.6** לפרסונליזציה. **(I5)** רכז את שמות המודלים בצומת Set/ENV אחד — לא hard-coded בכל צומת — כדי למנוע drift.
5. **(I4)** הוסף retry (×2, exponential backoff) + fallback לכל צומת Claude: כשל ניקוד → score 0 (suppress) · כשל סיווג → intent "hard" (לא שולחים) · כשל פרסונליזציה → תבנית גנרית מהסקריפטים.

> השלד מייבא as-is; חבר את ה-APIs האמיתיים שכבה-שכבה והעבר מ-assist לאוטומציה מלאה.

> **איך מייצרים את הטיוטה הראשונה מהר?** ה-n8n **AI Workflow Builder** (בנייה מ-Plain English) מייצר את השלד מתיאור באנגלית פשוטה — אך הטיוטה עוברת הקשחה (Claude · HITL · grounding) ומתקבעת **בגנרטור הזה** כמקור-אמת. הדוקטרינה המלאה: `AI_PROCESS_INTELLIGENCE.md` §6 — *Prompt-to-Prototype, Generator-to-Production*.

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | בלופרינט מנוע outbound — 8 שכבות, מודלי Claude, חיבור לסקריפטים, KPIs | 2026-05-31 |
| 1.1.0 | גל 3 של הביקורת: יישור 4 הסגמנטים לסקריפטים (W6), היחס ל-Ultra·Master·Max (W13), מצב השלד 07–08 (W14), ספירת צמתים (W18), retry/ENV למודלים (I4·I5) | 2026-06-01 |
| 1.2.0 | §6.1 חדש (D-040): שער הבגרות — שלושת שלבי HITL (`sendAndWait`) עם קריטריוני מעבר מדידים + דרישת דיוק 100% לסיווג הסרה | 2026-06-02 |
| 1.2.1 | הצלבה ל-`AI_PROCESS_INTELLIGENCE.md` §6 (D-065): ה-AI Workflow Builder מייצר את טיוטת השלד מ-Plain English; הגנרטור (§7) נשאר מקור-האמת — *Prompt-to-Prototype, Generator-to-Production* | 2026-06-08 |

**Confidentiality.** מסמך תפעולי חסוי — חלק מה-Claude OS של Avraham Bar Yochai Chazan.

— *End of CASES/ULEASE_OUTBOUND_ENGINE.md v1.2.1 —*
