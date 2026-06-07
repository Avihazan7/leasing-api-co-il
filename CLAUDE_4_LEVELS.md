# The 4 Levels of Claude — הסולם ⇄ היכן ULease עומדת

**ארבע רמות הבגרות בשימוש ב-Claude (i just vibe coded this): היכן רוב המייסדים מתחילים, והיכן ULease כבר נמצאת.**

> הטענה (מהאינפוגרפיקה): רוב המייסדים תקועים ב-Level 1 (Claude כ-search bar). הקפיצה לא קשה כמו שנדמה — אבל היא דורשת מעבר מ-prompts בודדים ל**מערכות**. *"Systems run the show."* המודול מצליב את 4 הרמות מול ה-OS וה-codebase של ULease, ומראה ש-ULease אינה משתמשת ב-Claude — היא **בנויה כ-Level 4**.

---

## 1. ארבע הרמות במבט-על

| רמה | שם | Goal | Mindset | המנוף |
|-----|-----|------|---------|--------|
| **1** | **The Beginner** — Claude Chat | לקבל תשובה | ask, read, close | כלום לא נשמר; כל שיחה מאפס |
| **2** | **The Context Builder** — Projects & Skills | פלט שנשמע כמוך | context-first, repeatable | Projects טוענים הקשר; Skills הופכים משימה חוזרת לפקודה אחת |
| **3** | **The Operator** — Cowork & Connectors | deliverables, לא תגובות | Claude = עובד בעסק | Cowork בונה קבצים/decks; Connectors מזרימים דאטה |
| **4** | **The Architect** — Code & Agents | compound leverage | systems over hustle | agents שרצים מעצמם; כל משימה חוזרת = משהו ש-Claude "מחזיק" |

> **הקפיצה הקריטית:** מ-Level 3 (Operator — Claude מבצע משימות) ל-Level 4 (Architect — Claude **מריץ מערכת שמריצה את עצמה**). זה ההבדל בין "להריץ prompts" ל"לבנות עסק שרץ לבד".

---

## 2. מ-4 הרמות אל ה-OS — היכן ULease עומדת

| רמה | המקבילה ב-ULease / בקוד | סטטוס |
|-----|------------------------|--------|
| 1 · Chat | baseline — לא שם. שיחה חד-פעמית = אנטי-תזה ל-OS | — |
| 2 · Context Builder | **ה-OS עצמו** — `CLAUDE.md` + מכלול המודולים = ה-Project/Context; **Skills** = `AGENT_BLUEPRINT § 11` (`/code-review`, `/security-review`); `MASTER_CLAUDE_58` אשכול PROJECTS | ✅ תשתית |
| 3 · Operator | Connectors: `N8N_AUTOMATION` (Glue Layer), `DEV_ENVIRONMENTS § 10` (MCP). Cowork = doctrine (טרם בריפו הזה) | 🟡 חלקי |
| 4 · Architect | **`leasing-api`** (פלטפורמה רצה: 65/65 טסטים, RLS end-to-end, Outbox+Relay backbone) + **`stage-a`** (Agent Runtime, Plan & Execute) + n8n agents | ✅ זה הבית |

> **הקריאה:** ULease **כבר Level 4 על ציר ההנדסה** — יש קוד רץ, agents, ו-event backbone ("systems run the show"). הפער היחיד הוא ב-Level 3 (Operator): שכבת ה-Cowork/Connectors היא עדיין doctrine בריפו הזה. כלומר הקפיצה לא לפנינו — היא **מאחורינו**; מה שנותר הוא להשלים את שכבת ה-Operator שמתחתיה.

---

## 3. הקשר למודולים האחים (Skill Map · Stack 2026)

ה-4 Levels הם ניסוח עממי של מה שכבר ממופה ב-OS:

- **`AI_SKILL_MAP`** — המסע בן 4 השלבים (Tools → Workflows → Agentic → Architect) = בדיוק Beginner → Context Builder → Operator → Architect.
- **`AI_CLAUDE_STACK_2026`** — סולם ה-7 רמות של Claude Code (ULease ב-6/7), הגרסה ההנדסית-עמוקה של אותו רעיון.
- **`MASTER_CLAUDE_58`** — אשכולות PROJECTS ו-PRO LEVEL = המנופים של Level 2 ו-Level 4.

> ⚠️ **הערת סנכרון:** שני המודולים `AI_SKILL_MAP` ו-`AI_CLAUDE_STACK_2026` **קיימים ב-OS המלא (Cowork/Projects) אך לא בריפו הגיט הזה** (21 מודולים בלבד מול ~50). המודול הזה הוא הראשון בקבוצה הזו שנכנס לגיט — ראה "חוב הסנכרון" למטה.

---

## 4. החוב הפתוח (כנה)

1. **חוב סנכרון OS↔גיט** — ה-OS המלא (~50 מודולים: `OPERATING_SYSTEM`, `MEMORY`, `DECISION_LOG`, `AI_SKILL_MAP`, `AI_CLAUDE_STACK_2026`, `COWORK/`…) חי ב-Cowork/Projects ולא בריפו הגיט. הגיט מכיל 21 מודולים. **משימה נפרדת:** הבאת התוכן לגיט (דורש את קבצי-המקור).
2. **Level 3 — Operator** — שכבת Cowork/Connectors היא doctrine; אין `COWORK/` workspace בריפו זה. הצעד: לעגן את ה-Connectors (`.mcp.json` מ-`CLAUDE_CODE_PROJECT_STRUCTURE § 5.3`) כקבצים ממשיים.

---

*תומלל מ-"The 4 Levels of Claude" (i just vibe coded this), ומופה ל-OS וה-codebase של ULease בהמשך ל-`MASTER_CLAUDE_58.md` ו-`AGENT_BLUEPRINT.md`; אח מושגי ל-`AI_SKILL_MAP`/`AI_CLAUDE_STACK_2026` (ב-OS המלא).*
