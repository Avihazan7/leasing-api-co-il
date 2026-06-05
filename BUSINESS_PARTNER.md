# Claude as Business Partner — 9 צעדים ⇄ ה-OS של ULease

**מ-chatbot ל-co-founder: 9 הצעדים להפוך את Claude לשותף עסקי, מוצלבים מול מה שכבר בנוי ב-OS של ULease.**

> הטענה (מהאינפוגרפיקה): Claude מפסיק להתנהג כ-chatbot ומתחיל לחשוב כשותף עסקי — אבל רק אם נותנים לו **role, זיכרון עסקי, ושגרה**. זה בדיוק מה שה-OS של ULease כבר עושה ברמת-מערכת: ה-`CLAUDE.md` + מכלול המודולים **הם** ה-"Business Brain". המודול הזה ממפה כל אחד מ-9 הצעדים למקבילה שכבר קיימת, ומסמן היכן זו פרקטיקה אישית ולא תשתית.

---

## 1. תשעת הצעדים במבט-על

| # | צעד | מה זה עושה | ה-prompt המרכזי |
|---|-----|-----------|------------------|
| 1 | **Set Claude's Role** | מ-chatbot ל-co-founder | *"Act as my business partner. My business is […]. Help me think, plan, execute."* |
| 2 | **Build Your Business Brain** | זיכרון על העסק לאורך כל session | Project עם overview/audience/offer/pricing — reference בכל chat |
| 3 | **Daily Business Briefing** | להתחיל כל יום עם פוקוס | *"Prioritize my to-do list by what moves the business forward most today."* |
| 4 | **Stress-Test Every Idea** | לאתגר רעיון לפני שמשקיעים בו | *"Give me 5 reasons this will fail and how to fix each."* |
| 5 | **Write All Your Sales Copy** | ads/emails/DMs/landing | *"Write a [ad/DM/email] for [offer]. Audience […]. Tone: direct, conversational."* |
| 6 | **Handle Customer Objections** | להתכונן לכל "לא" מראש | *"My offer is […]. Give me 10 objections + the perfect response to each."* |
| 7 | **Analyze Your Competition** | לזהות פערים בשוק | *"Here are 3-5 competitor posts — what are they missing, how do I differentiate?"* |
| 8 | **Build Your SOPs** | לתעד תהליכים כדי לסקייל/לדלגייט | *"Turn this repeated task into a step-by-step SOP for a team member."* |
| 9 | **Monthly Business Review** | accountability + אסטרטגיה חודשית | *"Here's what worked/didn't + my numbers. Analyze and plan next month."* |

---

## 2. מ-9 הצעדים אל ה-OS — מיפוי ל-ULease

| צעד | המקבילה ב-OS / בקוד | סטטוס |
|-----|---------------------|--------|
| 1 · Role | `COMMAND_API.md` (System Prompt block) · `AGENT_BLUEPRINT` persona — ULease = שותף ל-marketplace ליסינג רכב | ✅ תשתית |
| 2 · Business Brain | **ה-OS עצמו** — `CLAUDE.md` (entry point) + מכלול המודולים = הזיכרון העסקי; `MASTER_CLAUDE_58` אשכול PROJECTS | ✅ תשתית |
| 3 · Daily Briefing | `LAUNCH.md` (Day-0→Quarter ops) · `COMMAND_API` slash commands לתעדוף | ✅ |
| 4 · Stress-Test | `CTO_REVIEW.md` (קרא את הקוד, אתגר טענות) · `AGENT_BLUEPRINT` Evals · Working Rule #5 GOAL-DRIVEN / #7 NO LAZINESS | ✅ דוקטרינה |
| 5 · Sales Copy | `marketing-strategy-framework.md` · `N8N_AUTOMATION` (Lead workflows) | ✅ |
| 6 · Objections | Dealer/Customer Onboarding (`N8N § 7.3`) · `BRANCH_KNOWLEDGE` (ידע סניפים) | 🟡 חלקי |
| 7 · Competition | `CASES/ROX_KEY.md` (benchmark) · `ai-product-strategy-framework.md` | ✅ |
| 8 · SOPs | **Skills = SOPs** (`AGENT_BLUEPRINT § 11` — Learn) · `COMMAND_API` repeatable workflows | ✅ תשתית |
| 9 · Monthly Review | `CTO_REVIEW.md` (scorecard) · `power-bi-essential-concepts` (מדדים) · `INVESTOR_RELATIONS` | ✅ |

> **הקריאה:** 8 מתוך 9 הצעדים כבר קיימים כ**תשתית** ב-OS, לא כפרקטיקה אישית — וזה ההבדל בין "משתמש ש-prompt-ים את Claude כשותף" ל"**ארגון שבנה את השותפות לתוך המערכת**". ה-9 צעדים הם המבחן; ה-OS הוא התשובה.

---

## 3. הצעד הקריטי — #4 Stress-Test כ-DNA של הריפו

האינפוגרפיקה ממליצה stress-test לפני כל launch. ב-ULease זה לא best-practice — זה **כלל-עבודה מחייב**:

- **Working Rule #5 (GOAL-DRIVEN)** — הגדר success criteria (טסט) לפני הביצוע.
- **Working Rule #7 (NO LAZINESS)** — root cause, ותעד חוב במקום להסתיר.
- **`CTO_REVIEW.md`** — הדוגמה החיה: ביקורת חיצונית הוצלבה מול הקוד, 3 טענות תוקנו, חוב תועד בכנות.

> זה ה-*"5 reasons this will fail"* ברמת-הנדסה: לא שואלים את Claude לאשר — נותנים לו success criteria ונותנים לו לאתגר. שותף אמיתי אומר "זה לא יעבוד כי…".

---

## 4. החוב הפתוח (כנה)

1. **#6 Objections כ-asset** — אין מאגר תשובות-להתנגדויות מובנה ל-dealers/לקוחות. הצעד: ספריית objection→response ב-`BRANCH_KNOWLEDGE` (ניתנת לשימוש-חוזר ב-DMs/שיחות).
2. **#9 Review אוטומטי** — ה-Monthly Review הוא ידני. ה-seam: דשבורד Power BI על `settlements`/`ledger_entries` (`power-bi-essential-concepts`) שמזין את הסקירה במספרים אמיתיים במקום paste ידני.

---

*תומלל מ-"How to Turn Claude into a Business Partner in 9 Steps", ומופה ל-OS של `leasing-api-co-il` בהמשך ל-`COMMAND_API.md`, `CTO_REVIEW.md` ו-`MASTER_CLAUDE_58.md`.*
