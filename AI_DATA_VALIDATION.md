# ולידציית נתונים — Data Validation Techniques (שער האיכות של האנליסט)

**Module:** `AI_DATA_VALIDATION.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — מודול ידע/יסודות (Knowledge layer, §3 שורה 31). שער האיכות שלפני כל ניתוח, RAG או מודל.
**Source:** מבוסס על האינפוגרפיקה *"Data Validation Techniques Every Analyst Should Know"* (Poornachandra Kongara).
**Integrates with:** `AI_DATA_BI.md`, `AI_RAG_DESIGN.md`, `AI_SYSTEM_DESIGN.md`, `CASES/ULEASE_SPEC.md`, `CASES/ULEASE_PRICING_SLA.md`

---

> **"Bad data creates bad decisions."** זו לא סיסמה — זו **תזת ULease**: המוצר הוא *מערכת קבלת החלטות* (D-007), לא אתר רכב. Deal Score, Match API ו-Aging Predictor הם מנועי-החלטה שיושבים על **feed הספקים** ועל **קורפוס ה-RAG**. אם הנתון בכניסה שגוי — ההחלטה ביציאה שגויה, מהר ובביטחון. ולידציית נתונים היא **שער האיכות** בין raw data לבין ניתוח/RAG/מודל אמין. שש הטכניקות מהדף — וכל אחת: איזה כשל היא מונעת ב-ULease, ובאיזו שכבה היא חיה.

---

## 1. שש הטכניקות → מה הן בודקות ולמה זה חשוב

| # | טכניקה | מה היא בודקת | הכשל שהיא מונעת (לשון הדף) |
|---|--------|----------------|-----------------------------|
| 1 | **Data Type** | כל עמודה מאחסנת את הטיפוס הנכון (number/date/text) לפני ניתוח | "type שגוי → החישוב נשבר" |
| 2 | **Range** | ערכים נופלים בגבול עסקי/לוגי/תפעולי סביר (min–max) | "range שגוי → outliers מטעים" |
| 3 | **Mandatory Field** | שדות חיוניים אינם ריקים/חסרים/חלקיים | "שדות חסרים → דוחות חלקיים" |
| 4 | **Duplicate** | אין רשומות כפולות שמנפחות ספירות/הכנסה/עסקאות | "כפילויות → מספרים מנופחים" |
| 5 | **Format** | אימייל/תאריך/טלפון/ID/קוד עוקבים אחרי תבנית נדרשת | "format לא-אחיד → מערכות לא מצליבות רשומות" |
| 6 | **Consistency** | שדות קשורים אינם סותרים זה את זה (בין שורות/מערכות) | "חוסר עקביות → האמון נעלם" |

> כל טכניקה היא **flow של ~8 צעדים** בדף, וכולם חולקים אותו שלד: *הגדר כלל → סרוק → סמן חריגה → תקן → אמת*. ההבדל הוא **מה** נבדק, לא **איך**.

---

## 2. הגשר ל-ULease 🎯 — איזה כשל כל טכניקה מונעת

ב-ULease הנתון נכנס מ-**feed ספקים** (יבואנים, חברות ליסינג — API/webhook/CSV, ראו `CASES/ULEASE_SPEC.md`) ומוזרם לקטלוג, ל-RAG ולמנועי ההחלטה. כל טכניקה חוסמת כשל ספציפי:

| טכניקה | דוגמה אמיתית ב-ULease | מה נשבר בלי הוולידציה |
|--------|------------------------|------------------------|
| **Data Type** | מחיר מגיע כ-`"₪150,000"` (string) במקום `150000` (number) | חישוב ה-PMT/לוח הסילוקין (`AI_DATA_BI` §4.1) נופל — הלקוח רואה שגיאה בחדר-העסקה |
| **Range** | רכב ב-₪15 (חסרו אפסים) · ק"מ = ‎−5 · שנתון = 2099 | Deal Score מזדהם, "מבצע" מזויף עולה לראש, אמון נשבר |
| **Mandatory** | רכב בלי VIN / מחיר / זמינות | אי-אפשר להתאים, לנקד או למכור; ה-RAG מאחזר רשומה חלקית |
| **Duplicate** | אותו VIN משני ספקים · אותה עסקה נספרת פעמיים | מלאי מנופח לקונה · ספירת עסקאות מנופחת **למשקיע** · חיוב כפול |
| **Format** | לוחית רישוי / VIN / טלפון ישראלי / תאריך בפורמטים שונים | feed הספק ↔ CRM ↔ שותף המימון לא מצליחים להצליב רשומה |
| **Consistency** | `fuel=electric` אך `engine_cc=2000` · `lease_end < lease_start` · `payment×term ≠ total` | סתירה שמרעילה את המודל הפיננסי ואת ה-Q&A Bot |

**שתי נגיעות קריטיות:**
- **Duplicate = הסיכון הכפול.** "מספרים מנופחים" אינו רק קוסמטי — ספירת עסקאות מנופחת ב-**עדכון משקיע** היא חשיפת אמינות; וחיוב כפול הוא בדיוק מה ש-**Idempotency** (`AI_SYSTEM_DESIGN`, D-023) נועד למנוע. מפתח ייחודי (VIN+ספק) + idempotency key = שתי הפנים של אותה טכניקה.
- **שער ה-SLA חסר משמעות בלי ולידציה.** ה-SLA מבטיח ingestion ‎≤4h/24h (`CASES/ULEASE_PRICING_SLA`). אבל **ingestion מהיר של נתון פסול גרוע מ-ingestion איטי** — הוולידציה היא *תנאי מוקדם* ל-SLA, לא צעד נפרד אחריו.

---

## 3. איפה בסטאק הוולידציה חיה — הכרעת design-review

הטעות הנפוצה: "נוסיף ולידציה איפשהו". הנכון: לכל טכניקה יש **שכבה** במסלול הבקשה (`AI_SYSTEM_DESIGN` §1.5):

| שכבה | מה רץ שם | טכניקות | התנהגות בכשל |
|------|-----------|----------|---------------|
| **Edge** (Middleware/Controller) | בדיקה חסרת-הקשר, מהירה, stateless | Type · Format · Mandatory | דחייה בדלת — `400 Bad Request`, לא נכנס פנימה |
| **Service** (חוקי עסק) | בדיקה תלוית-הקשר עסקי | Range · Consistency | הפנייה ל-**HITL** (D-039) — אסור לפרסם ₪15 אוטומטית |
| **Repository/DB + batch** | בדיקה חוצת-רשומות | Duplicate | unique constraint (VIN+ספק) + dedup בצינור ה-ingestion |
| **Pre-RAG gate** | רק נתון תקין נכנס ל-embedding | כולן | קורפוס pgvector נקי → retrieval נקי (`AI_RAG_DESIGN`) |
| **Model / Monitoring** | ניטור איכות לאורך זמן | drift detection | drift שבועי (D-023) → התראה (`AI_DATA_BI` §6.ד) |

> **הקו המנחה:** Type/Format/Mandatory הם **stateless** → בדלת. Range/Consistency דורשים הקשר עסקי → ב-Service. Duplicate דורש מבט על פני שורות → ב-DB/batch. וזה גם **גבול אבטחה**: ספק שמזריק הוראות בשדה "תיאור רכב" הוא בו-זמנית כשל Format/Consistency וגם וקטור **Prompt Injection** (`AI_CLAUDE_STACK_2026` §5.6) — הוולידציה היא קו ההגנה הראשון של Guardian, לפני שה-LLM בכלל רואה את הקלט.

---

## 4. מה זה אומר לך (המייסד)

- **אוריינות design-review, לא יישום.** אתה לא כותב regex לוולידציה — אתה שואל את ה-Tech Lead את שש שאלות השער: *"מה קורה כשספק שולח feed בלי מחיר? עם מחיר ₪15? עם אותו VIN פעמיים? עם תאריך בפורמט אמריקאי?"* שש הטכניקות הן **הצ'קליסט** לשאלות האלה — תאום ל-`AI_RAG_DESIGN` (15 שאלות ה-retrieval) ולעיקרון של `AI_DATA_BI` ("ה-BI מנתח, ה-API מחשב"): **ה-Tech Lead מיישם, המייסד סוקר**.
- **זה שומר על עדכון המשקיע.** הטכניקה שנוגעת ישירות בגיוס היא **Duplicate**: מספר עסקאות מנופח בדוח השבועי = פגיעה באמינות מול משקיע. ה-QA על המודל הפיננסי (`COMMAND_API_TASKS` §4: ‎#29 reconcile · ‎#30 stress-test) הוא ולידציה בתחפושת.
- **למה מודול נפרד ולא הערה ב-`AI_DATA_BI`?** `AI_DATA_BI` מלמד את ה-**T** ב-ETL כחלק מצינור ה-BI; כאן זו **דיסציפלינה רוחבית** שחלה על ה-feed, על ה-RAG, על ה-API ועל המודל הפיננסי — לא רק על שכבת ה-BI. זהו שער האיכות שמגן על **כל** שכבת ההחלטה של ULease.

---

## 5. כלים ושורה תחתונה

**כלים (מהתחום):** Great Expectations / Pandera (Python) · Pydantic (ולידציית סכמה ב-API) · DB constraints (NOT NULL · UNIQUE · CHECK) · JSON Schema ל-feed הספק. ב-ULease הכל מופשט מאחורי שכבת ה-ingestion — אף אחד לא בודק ביד; הערך הוא לדעת ש**השער קיים**, באיזו שכבה, ומה הוא חוסם.

> **השורה התחתונה:** ולידציה אינה שלב ניקוי טכני — היא **שער האיכות בין raw data להחלטה אמינה**. ב-ULease, שבו ההחלטה *היא המוצר*, השער הזה הוא חלק מה-IP — לא overhead.

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | 6 טכניקות ולידציית נתונים (Type · Range · Mandatory · Duplicate · Format · Consistency) + עמודת הכשל הנמנע, הגשר ל-ULease (איזה כשל כל טכניקה מונעת ב-feed/RAG/מודל), הכרעת design-review "איפה בסטאק הוולידציה חיה" (Edge/Service/DB/Pre-RAG/Monitoring) ואוריינות המייסד | 2026-06-07 |

**Attribution.** מבוסס על האינפוגרפיקה *Data Validation Techniques Every Analyst Should Know* (Poornachandra Kongara). העיבוד, עמודת הכשל-הנמנע, הכרעת ה-design-review והמיפוי ל-OS/ULease הם חלק מה-Claude Operating System של Avraham Bar Yochai Chazan.

**Confidentiality.** קובץ זה הוא חלק מה-Claude Operating System האישי של Avraham Bar Yochai Chazan.

— *End of AI_DATA_VALIDATION.md v1.0.0 —*
