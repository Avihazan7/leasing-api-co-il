# תפקידי ה-AI החמים ב-2026 — ומי מכסה אותם ב-ULease

**Module:** `AI_ROLES_2026.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — Knowledge layer (§3 שורה 20).
**Source:** מבוסס על האינפוגרפיקה *"The Hottest AI Role in 2026"* (Ashish Joshi).
**Integrates with:** `CASES/ULEASE_HIRING.md`, `AI_SKILL_MAP.md`, `AI_PROGRESSION_PLAN.md`, `CASES/ULEASE_SPEC.md`, `AI_RAG_DESIGN.md`

> 21 תפקידי AI מגדירים את שוק העבודה של 2026. ב-ULease אין 21 משרות — יש **מייסד + Tech Lead אחד**. המודול ממפה אילו תפקידים כל אחד מכסה, ומוכיח למה הגדרת התפקיד ב-`ULEASE_HIRING.md` נכונה: ה-Tech Lead הוא בעצם 5 תפקידים בכובע אחד.

---

## 1. עשרים ואחד התפקידים

| # | תפקיד | מה הוא עושה |
|---|--------|---------------|
| 1 | **AI Solutions Architect** | מתכנן מערכות AI סקיילביליות ומשלב מודלים באפליקציות אמיתיות |
| 2 | **AI Knowledge Engineer** | בונה ומנהל בסיסי ידע למערכות AI (RAG, embeddings) |
| 3 | **AI Data Engineer** | מתכנן pipelines לאיסוף, ניקוי ועיבוד דאטה ל-AI |
| 4 | **AI Trainer / Annotator** | מכין, מתייג ומזקק דאטה לשיפור ביצועי מודלים |
| 5 | **AI/ML Engineer** | בונה, מאמן ומפרסם מודלי machine learning ל-production |
| 6 | **Prompt Engineer** | מנסח פרומפטים ממוטבים לשיפור איכות ואמינות הפלט |
| 7 | **MLOps Engineer** | מנהל deployment, ניטור ומחזור חיים של מודלים ב-production |
| 8 | **AI Ethics Specialist** | מוודא שמערכות AI הוגנות, שקופות ועומדות ברגולציה |
| 9 | **AI Research Scientist** | מפתח אלגוריתמים חדשים ומקדם את יכולות ה-AI |
| 10 | **AI Product Manager** | מגדיר אסטרטגיית מוצר AI, מקרי שימוש ואימפקט עסקי |
| 11 | **Data Scientist (AI)** | מחלץ תובנות ובונה מודלים חיזויים מדאטה |
| 12 | **LLM Engineer** | מתמחה ב-fine-tuning, אופטימיזציה ו-deployment של מודלי שפה |
| 13 | **AI Integration Engineer** | מחבר מודלי AI ל-APIs, כלים ומערכות ארגוניות |
| 14 | **AI Agent Engineer** | בונה סוכני AI אוטונומיים שמתכננים, פועלים ומשתמשים בכלים |
| 15 | **AI Cost Optimization Engineer** | מוריד עלויות inference תוך שמירה על ביצועים |
| 16 | **Reinforcement Learning Engineer** | בונה מודלים שלומדים דרך תגמולים וקבלת החלטות |
| 17 | **Speech Recognition Engineer** | מפתח מערכות שממירות דיבור לטקסט ולפקודות |
| 18 | **AI Security Specialist** | מגן על מערכות AI מהתקפות, שימוש לרעה ופרצות |
| 19 | **Computer Vision Engineer** | מפתח מערכות שמבינות תמונות ווידאו |
| 20 | **Robotics AI Engineer** | יוצר רובוטים חכמים לאוטומציה ושליטה |
| 21 | **NLP Engineer** | בונה מערכות שמבינות ומייצרות שפה אנושית |

---

## 2. המיפוי ל-ULease 🎯 — מי מכסה מה

### 🧑‍💼 המייסד (אברהם) — 3 תפקידים

| תפקיד | איך זה מתבטא |
|--------|----------------|
| **AI Product Manager** (#10) | הגדרת ה-roadmap, מקרי השימוש והאימפקט — האיפיון כולו (`ULEASE_SPEC.md`) |
| **Prompt Engineer** (#6) — רמת מוצר | `COMMAND_API.md` · skills · פרומפטי ה-Outbound (Learn-vs-Delegate: מושגים אצלך) |
| **AI Knowledge Engineer** (#2) — רמת תכנון | `AI_RAG_DESIGN.md` + צ'קליסט ה-design review של שכבת ה-RAG (§7.1) |

### 🤝 ה-Tech Lead — 5 תפקידים בכובע אחד

| תפקיד | מה הוא יבנה ב-ULease | איפה זה באיפיון |
|--------|------------------------|------------------|
| **AI Agent Engineer** (#14) | מנוע Ultra · Master · Max · Guardian | `ULEASE_SPEC.md` §7 |
| **AI Integration Engineer** (#13) | חיבורי API: ספקים, e-sign, סולק, מימון | `ULEASE_SPEC.md` §9 |
| **AI Knowledge Engineer** (#2) — מימוש | pgvector, chunking, hybrid retrieval | `ULEASE_SPEC.md` §7.1 + `AI_RAG_DESIGN.md` |
| **MLOps/LLMOps Engineer** (#7) | eval suite, ניטור הזיות, drift, CI | `ULEASE_SPEC.md` §7.2 (D-023) |
| **AI Cost Optimization** (#15) | עלות-לשאילתה, תקציבי latency, בחירת מודלים | `AI_RAG_DESIGN.md` §3 + unit economics |

> **המסקנה לגיוס:** מודעת הדרושים ב-`ULEASE_HIRING.md` (LLM/Agents · orchestration · RAG · vector DBs) מכסה בדיוק את חמשת התפקידים האלה. כשמועמד שואל "מה התפקיד?" — התשובה: *"חמשת התפקידים הכי מבוקשים של 2026, בסטארטאפ אחד, עם איפיון מוכן."* זו הצעת ערך לגיוס, לא רק דרישה.

### 🛡️ מכוסה ע"י הארכיטקטורה (לא משרה)

| תפקיד | מי מכסה |
|--------|----------|
| **AI Ethics Specialist** (#8) | **Guardian** — ציות, הסכמות, opt-out, audit (`ULEASE_SPEC.md` §7) |
| **AI Security Specialist** (#18) | Guardian (red team evals, §7.2) + NFR אבטחה (§10); מומחה ייעודי — בשלב scale |
| **AI Trainer/Annotator** (#4) | נדחה עם ה-fine-tuning ל-~1,000 עסקאות (D-022) |

### ⏳ לא רלוונטי בשלב הזה

Reinforcement Learning (#16) · Speech Recognition (#17) · Computer Vision (#19) · Robotics (#20) · AI Research Scientist (#9) — מחקר ותחומים שאינם ליבת marketplace. NLP (#21) ו-AI/ML (#5) מכוסים ע"י Claude כתשתית (לא בונים מודלים — צורכים אותם).

---

## 3. החיבור למפת המיומנויות

| מסלול | תפקידים | שלב במפה (`AI_SKILL_MAP.md`) |
|--------|----------|-------------------------------|
| המסלול שלך (מייסד) | Product Manager → Knowledge Engineer (תכנון) | שלב 3 → 4 (Agentic → Architect) |
| מסלול ה-Tech Lead | Agent + Integration + Knowledge (מימוש) | שלב 3 (Agentic) ב-production |
| מה שביניהם | Learn-vs-Delegate (`AI_PROGRESSION_PLAN.md`) | אתה מנהל, הוא בונה |

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | 21 תפקידי AI (2026) + מיפוי מלא: מייסד (3 תפקידים) · Tech Lead (5 בכובע אחד) · Guardian (2) · לא-רלוונטי (6) + הצעת ערך לגיוס | 2026-06-02 |

**Attribution.** רשימת התפקידים מבוססת על *The Hottest AI Role in 2026* (Ashish Joshi). העיבוד והמיפוי ל-ULease — חלק מה-Claude OS של Avraham Bar Yochai Chazan.

**Confidentiality.** קובץ זה הוא חלק מה-Claude Operating System האישי של Avraham Bar Yochai Chazan.

— *End of AI_ROLES_2026.md v1.0.0 —*
