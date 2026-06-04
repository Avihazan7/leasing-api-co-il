# CLAUDE.md — OS Entry Point

נקודת הכניסה הראשית של ה-Claude Operating System עבור הריפו.

## Active Modules
- `OPERATING_SYSTEM.md` v1.0.0 — מסמך-העל. שכבות ה-OS, חוזה הטעינה, עקרון System-First. סוגר dangling ref #1.
- `MEMORY.md` v1.0.0 — דוקטרינת 4 ה-tiers (working/episodic/vector/SQL) + לולאת השיפור-העצמי (Card 1 §6). סוגר dangling ref #2 + מודול 5 ב-AGENT_BLUEPRINT.
- `COMMAND_API.md` v1.1.0 — 100 slash commands (12 categories, native ⚙️ + behavioral 💬), composition operators, drop-in system prompt loaded.
- `WINDOWS_DEPLOYMENT.md` v1.0.0 — End-to-end Windows rollout for Claude in Microsoft 365 (Word/Excel/PowerPoint + Skills).
- `DEV_ENVIRONMENTS.md` v1.1.0 — End-to-end Claude dev environments: Desktop, VS Code, JetBrains, Cursor, Windsurf, Claude Code CLI + MCP + Computer Use, **+ נספח ג'** מפת Anthropic Ecosystem (מיקום ULease) **+ נספח ד'** Setup סטנדרטי (Cowork folder-first, ABOUT-ME, Global Instructions).
- `LAUNCH.md` v1.1.0 — Master ignition file. ULease go-live playbook: Day 0 → Week 1 → Month 1 → Quarter 1, RACI, kill-switch, master switch, **+ § 3.1 מסלול הדרכה "Master Claude in a Week"** (7 ימים, deliverable יומי, ממופה ל-OS).
- `AGENT_BLUEPRINT.md` v1.3.0 — System-first doctrine. הגשר בין ה-Docs OS ל-Agent Runtime (`stage-a/`): 8-module blueprint, coverage map, evals layer, governance-in-code, **+ § 6.1 חיזוק Gartner** (5 misconceptions ⇄ הדוקטרינה), **+ § 9 Orchestration Patterns** (9 topologies · ULease Skills map · **§ 9.6 מיפוי הקנון** *Agentic Design Patterns*/Gulli), **+ § 10 Coding Workflow Doctrine** (Karpathy's CLAUDE.md: 6 עקרונות workflow · Working Rules · mindset).
- `CASES/ROX_KEY.md` v1.0.0 — Vietnamese benchmark — ROX Key digital transformation. Direct parallel to ULease positioning; 5 operational lessons + 6 action items woven into LAUNCH and DEV_ENVIRONMENTS.
- `power-bi-essential-concepts.md` v1.1.0 — 10 מושגי יסוד ב-Power BI + **§ דשבורדים ל-ULease**: חיבור ל-Supabase, מודל Star Schema על `settlements`/`ledger_entries`/`vehicle_read_model`, מדדי DAX (מכירות, עמלות, המרה), RLS לסוכנויות.
- `N8N_AUTOMATION.md` v1.1.0 — שכבת האוטומציה התפעולית: n8n כ-Glue Layer בין ה-Outbox של `leasing-api` לעולם העסקי. חיבור HMAC+Webhook, קטלוג אירועים→workflows, 5 workflows מוכנים, מיפוי ל-AGENT_BLUEPRINT § 9 (n8n=Hands · stage-a=Brain), **+ § 7.3 אנטומיית AI Agent** (Form→Tools Agent→Switch→Slack ⇒ Dealer Onboarding), MCP דו-כיווני, ממשל ו-kill-switch.
- `BRANCH_KNOWLEDGE.md` v1.0.0 — תשתית הידע לסניפים: ערוץ Slack פרטי + ספר ידע (`BRANCHES/`) לכל סניף/סוכנות, צינור דו-כיווני Edge⇄Core (תובנות 💡/⚠️ → W6 זיקוק שבועי → OS), הפרדת סניפים (RLS doctrine), rollout משולב ב-LAUNCH.
- `CTO_REVIEW.md` v1.0.0 — ביקורת CTO על ULease v1.2, תגובה מבוססת-קוד. הצלבת 10 נקודות הביקורת מול הקוד ב-`leasing-api`: תיקון 3 טענות (Event Bus / Data Warehouse / RLS קיימים כ-seams), scorecard מתוקן, מפת דרכים P0–P7 ל-Platform v2.0, ותיעוד הצעד הראשון (Decision Engine seam, 55/55 טסטים, תואם-לאחור).
- `SYSTEM_DESIGN_PATTERNS.md` v1.0.0 — 8 patterns (Ambassador/Circuit-Breaker/CQRS/Sharding/Sidecar/Pub-Sub/Leader-Election/Event-Sourcing) ⇄ הקוד האמיתי ב-`leasing-api`: מה מיושם, איפה, ואילו invariants אסור לשבור. ה-bridge ל-`leasing-api/CLAUDE.md § 3`.
- `AI_ENGINEER_STACK.md` v1.0.0 — 12 הכלים של AI Engineer (OpenAI/Claude/LangChain/LlamaIndex/CrewAI/vLLM/Ollama/Pinecone/Weaviate/W&B/FastAPI/Docker) ⇄ ה-tier וה-מצב ב-ULease (בשימוש/נשקל/roadmap).
- `INVESTOR_RELATIONS.md` v1.0.0 — narrative למשקיעים מבוסס-evidence: כל טענה ⇄ artifact בקוד/OS. סוגר dangling ref #3.
- `power-bi` ⬇ · `ai-product-strategy-framework.md` v1.0.0 — מסגרת אסטרטגיית מוצר-AI. · `marketing-strategy-framework.md` v1.0.0 — מסגרת אסטרטגיית שיווק.
- `BRANCHES/*.md` — ספרי ידע לסניפים (`_TEMPLATE.md`, `tel-aviv.md`). · `stage-a/` — Agent Runtime (manager · worker · shared-memory).

## Module Load Order
1. `OPERATING_SYSTEM.md`      ← מסמך-העל: שכבות + חוזה טעינה
2. `MEMORY.md`                ← 4 tiers + לולאת לקחים (קרא לפני עבודה חוזרת)
3. `COMMAND_API.md`           ← לפני הקטגוריות העסקיות
4. `WINDOWS_DEPLOYMENT.md`    ← הטמעת אופיס מקצה לקצה
5. `DEV_ENVIRONMENTS.md`      ← סביבות פיתוח מקצה לקצה
6. `LAUNCH.md`                ← Master Switch — Go-Live
7. `AGENT_BLUEPRINT.md`       ← Docs OS ⇄ Agent Runtime (stage-a/)
8. `SYSTEM_DESIGN_PATTERNS.md` ← 8 patterns ⇄ הקוד (bridge ל-leasing-api § 3)
9. `AI_ENGINEER_STACK.md`     ← 12 tools ⇄ tiers ULease
10. `CTO_REVIEW.md`           ← ביקורת CTO ⇄ קוד + מפת דרכים Platform v2.0
11. `power-bi-essential-concepts.md` ← BI ודשבורדים על נתוני ה-API
12. `N8N_AUTOMATION.md`       ← אוטומציה תפעולית על אירועי ה-API
13. `BRANCH_KNOWLEDGE.md`     ← תשתית הידע לסניפים (Edge⇄Core)
14. `INVESTOR_RELATIONS.md`   ← narrative למשקיעים מבוסס-evidence
15. `ai-product-strategy-framework.md` · `marketing-strategy-framework.md` ← מסגרות אסטרטגיה
16. `CASES/*.md`              ← בנצ'מארקים (ROX_KEY)
17. `BRANCHES/*.md`           ← ספרי הידע של הסניפים

## Working Rules
כללי עבודה מחייבים לכל agent שעובד על הריפו (מקור: `AGENT_BLUEPRINT.md § 10` — Karpathy doctrine):

1. **PLAN FIRST** — משימה לא-טריוויאלית מתחילה ב-plan, לא בקוד.
2. **ASK, DON'T ASSUME** — עמימות בדרישה? שאל. אל תנחש.
3. **SIMPLE** — הפתרון המינימלי שפותר את הבעיה. שום דבר ספקולטיבי.
4. **SURGICAL** — גע רק בקבצים שהמשימה דורשת. אל תשפץ מה שלא שבור.
5. **GOAL-DRIVEN** — הגדר success criteria (טסט/בדיקה) לפני הביצוע; איטרט עד שעובר.
6. **VERIFY** — הרץ את מה שכתבת. diff נסקר לפני commit. אין "אמור לעבוד".
7. **NO LAZINESS** — root cause, לא workaround. אם יש חוב — תעד אותו, אל תסתיר.
8. **SUBAGENTS** — exploration/research ב-subagent נפרד; שמור על context ראשי נקי.

## Activation
כדי להפעיל את ה-Command API, טען את בלוק ה-System Prompt מסעיף 7 ב-[`COMMAND_API.md`](./COMMAND_API.md)
אל ההקשר (`userPreferences` / system prompt / טעינת OS). זה מה שגורם ל-Claude לזהות תחביר `/command`.
