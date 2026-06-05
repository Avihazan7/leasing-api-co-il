# CLAUDE.md — OS Entry Point

נקודת הכניסה הראשית של ה-Claude Operating System עבור הריפו.

## Active Modules
- `COMMAND_API.md` v1.1.0 — 100 slash commands (12 categories, native ⚙️ + behavioral 💬), composition operators, drop-in system prompt loaded.
- `WINDOWS_DEPLOYMENT.md` v1.0.0 — End-to-end Windows rollout for Claude in Microsoft 365 (Word/Excel/PowerPoint + Skills).
- `DEV_ENVIRONMENTS.md` v1.1.0 — End-to-end Claude dev environments: Desktop, VS Code, JetBrains, Cursor, Windsurf, Claude Code CLI + MCP + Computer Use, **+ נספח ג'** מפת Anthropic Ecosystem (מיקום ULease) **+ נספח ד'** Setup סטנדרטי (Cowork folder-first, ABOUT-ME, Global Instructions).
- `LAUNCH.md` v1.1.0 — Master ignition file. ULease go-live playbook: Day 0 → Week 1 → Month 1 → Quarter 1, RACI, kill-switch, master switch, **+ § 3.1 מסלול הדרכה "Master Claude in a Week"** (7 ימים, deliverable יומי, ממופה ל-OS).
- `AGENT_BLUEPRINT.md` v1.4.0 — System-first doctrine. הגשר בין ה-Docs OS ל-Agent Runtime (`stage-a/`): 8-module blueprint, coverage map, evals layer, governance-in-code, **+ § 6.1 חיזוק Gartner** (5 misconceptions ⇄ הדוקטרינה), **+ § 9 Orchestration Patterns** (9 topologies · ULease Skills map · **§ 9.6 מיפוי הקנון** *Agentic Design Patterns*/Gulli), **+ § 10 Coding Workflow Doctrine** (Karpathy's CLAUDE.md: 6 עקרונות workflow · Working Rules · mindset), **+ § 11 MCP vs. Agent Skills** (Connect⇄Learn: 5 ממדים ⇄ ULease · הבהרת מינוח · דוקטרינת Use-Both).
- `CASES/ROX_KEY.md` v1.0.0 — Vietnamese benchmark — ROX Key digital transformation. Direct parallel to ULease positioning; 5 operational lessons + 6 action items woven into LAUNCH and DEV_ENVIRONMENTS.
- `system-design-cheatsheet.md` v1.0.0 — 15 מושגי הליבה בעיצוב מערכות (4 אשכולות: Design 🟧 · NFRs 🟦 · Build/Quality 🟩 · Ops/Lifecycle 🟪) + **§ מיפוי ל-ULease**: כל מושג מוצלב מול ראיה בקוד ב-`leasing-api` (Outbox+EventSink, `vehicle_read_model`, `hmacAuth`, **65/65 טסטים**); P0 Multi-Tenancy/RLS נחת כ-first increment (`tenant_id` additive + `rls.sql` fail-closed), נותר action-level RBAC, בהמשך ל-`CTO_REVIEW.md`.
- `BACKEND_ROADMAP.md` v1.0.0 — Backend Developer Roadmap (Shishir Pant) מוצלב מול ULease: 6 שלבי המסלול (🟢 Foundations · 🔵 Backend Core · 🟣 Databases · 🟠 Performance · 🔴 Cloud/Deploy · ⭐ Advanced) כל אחד ⇄ ראיה בקוד (`stateMachine.ts`, `hmacAuth.ts`, `schema.sql`+ledger, Outbox/EventSink, Dockerfile/CI, domain modules) עם סטטוס STRONG/PARTIAL/GAP, ריכוז החובות הפתוחים (Multi-Tenancy/RLS — מחווט end-to-end ✅, נותר action-level RBAC · Event Backbone P2 · Data Platform P3 · Rate-limit/Redis) בהמשך ל-`CTO_REVIEW.md`, ו-§8 "אם הייתי מתחיל מחדש".
- `power-bi-essential-concepts.md` v1.1.0 — 10 מושגי יסוד ב-Power BI + **§ דשבורדים ל-ULease**: חיבור ל-Supabase, מודל Star Schema על `settlements`/`ledger_entries`/`vehicle_read_model`, מדדי DAX (מכירות, עמלות, המרה), RLS לסוכנויות.
- `N8N_AUTOMATION.md` v1.2.0 — שכבת האוטומציה התפעולית: n8n כ-Glue Layer בין ה-Outbox של `leasing-api` לעולם העסקי. חיבור HMAC+Webhook, קטלוג אירועים→workflows, 5 workflows מוכנים, מיפוי ל-AGENT_BLUEPRINT § 9 (n8n=Hands · stage-a=Brain), **+ § 7.3 אנטומיית AI Agent** (Form→Tools Agent→Switch→Slack ⇒ Dealer Onboarding), MCP דו-כיווני, **+ § 8.4 MCP ≠ Skill** (MCP=שכבת חיבור · מצביע ל-AGENT_BLUEPRINT § 11), ממשל ו-kill-switch.
- `BRANCH_KNOWLEDGE.md` v1.0.0 — תשתית הידע לסניפים: ערוץ Slack פרטי + ספר ידע (`BRANCHES/`) לכל סניף/סוכנות, צינור דו-כיווני Edge⇄Core (תובנות 💡/⚠️ → W6 זיקוק שבועי → OS), הפרדת סניפים (RLS doctrine), rollout משולב ב-LAUNCH.
- `CTO_REVIEW.md` v1.2.0 — ביקורת CTO על ULease, תגובה מבוססת-קוד. הצלבת 10 נקודות הביקורת מול הקוד ב-`leasing-api`: תיקון 3 טענות (Event Bus / Data Warehouse / BI קיימים כ-seams), scorecard מתוקן, מפת דרכים P0–P7 ל-Platform v2.0; **שני צעדי P0 נחתו** (Decision Engine seam + Multi-Tenancy/RLS **מחווט end-to-end**: request `X-Tenant-Id`→`asTenant`, worker `SYSTEM_TENANT`, מאומת ב-HTTP, **65/65 טסטים**), נותר action-level RBAC.
- `AI_SDLC_ORCHESTRATION.md` v1.0.0 — מפת כלי ה-AI על פני ה-SDLC (Ashish Sahu) + הטענה *"orchestration of intent, not tools"*: 6 שלבי ה-SDLC ⇄ ראיה ב-`leasing-api`, שכבת-התזמור של ULease (Brain=`stage-a` · Backbone=Outbox+Relay+Sink · Hands=n8n), **+ § 4** אנטומיית Enterprise AI Agent (8 שכבות M-SoftTech: gate→core→MCP→guardrails→routing→isolation) ⇄ seams בקוד (`hmacAuth`, `decisionEngine`, RLS, 65/65 טסטים), בהמשך ל-`AGENT_BLUEPRINT § 9` ו-`CTO_REVIEW`.
- `CLAUDE_CODE_PROJECT_STRUCTURE.md` v1.0.0 — מבנה פרויקט Claude Code סטנדרטי (Robbert van Vlijmen) ⇄ ה-OS בפועל: 8 אבני-בניין (`CLAUDE.md`/`.mcp.json`/`settings.json`/`rules`/`commands`/`skills`/`agents`/`hooks`) ממופות למקבילה בריפו (CLAUDE.md ✅ · COMMAND_API=commands · stage-a=agents · AGENT_BLUEPRINT § 11=skills/MCP), ההבחנה בין 4 הפרימיטיבים, **+ § 4** חוב P-Tooling (אין `hooks/`·`.claude/settings.json`·`.mcp.json` כקבצים ניתנים-להרצה).
- `AUTH_CONCEPTS.md` v1.1.0 — Authentication vs Authorization (M-SoftTech) ⇄ שכבת האבטחה של `leasing-api`: AuthN חזק (`hmacAuth.ts` — HMAC-SHA256 + replay guard + constant-time → 401) · AuthZ ברמת-שורה **מחווט end-to-end** (`X-Tenant-Id`→`asTenant` · worker `SYSTEM_TENANT` · `rls.sql` fail-closed, מאומת ב-HTTP ב-`tenancy.test.ts`), **+ § 5** חוב פתוח (action-level RBAC/403 + hardening: per-tenant keys · `(tenant_id, vin)` PK), בהמשך ל-`system-design-cheatsheet § 9`.
- `MASTER_CLAUDE_58.md` v1.0.0 — 58 Ways to Master Claude (@coder_surya): 8 אשכולות (SETUP·MODELS·PROMPTING·ASK·CONNECTORS·PROJECTS·ARTIFACTS·PRO LEVEL) כל אחד ⇄ המודול שמיישם ב-OS (ASK ⇄ Working Rule #2 · PROJECTS ⇄ ה-OS עצמו · PRO LEVEL ⇄ `stage-a`+`AGENT_BLUEPRINT § 9`), מיפוי ל-`LAUNCH § 3.1` (Master Claude in a Week), ו-self-audit בגרות.

## Module Load Order
1. `OPERATING_SYSTEM.md`      ← roadmap (ראה AGENT_BLUEPRINT § 7)
2. `MEMORY.md`                ← roadmap (ראה AGENT_BLUEPRINT § 7)
3. `COMMAND_API.md`           ← לפני הקטגוריות העסקיות
4. `WINDOWS_DEPLOYMENT.md`    ← הטמעת אופיס מקצה לקצה
5. `DEV_ENVIRONMENTS.md`      ← סביבות פיתוח מקצה לקצה
6. `LAUNCH.md`                ← Master Switch — Go-Live
7. `AGENT_BLUEPRINT.md`       ← Docs OS ⇄ Agent Runtime (stage-a/)
8. `CTO_REVIEW.md`            ← ביקורת CTO ⇄ קוד + מפת דרכים Platform v2.0
8a. `AI_SDLC_ORCHESTRATION.md` ← מפת SDLC ⇄ שכבת-התזמור (Brain/Backbone/Hands) + אנטומיית Agent
8b. `CLAUDE_CODE_PROJECT_STRUCTURE.md` ← מבנה Claude Code סטנדרטי ⇄ ה-OS בפועל
8c. `AUTH_CONCEPTS.md`        ← AuthN vs AuthZ ⇄ hmacAuth + RLS
8d. `MASTER_CLAUDE_58.md`     ← 58 Ways ⇄ מודולי ה-OS + LAUNCH § 3.1
9. `power-bi-essential-concepts.md` ← BI ודשבורדים על נתוני ה-API
9a. `system-design-cheatsheet.md` ← 15 מושגי עיצוב מערכות ⇄ מיפוי ל-codebase
9b. `BACKEND_ROADMAP.md`       ← Backend Developer Roadmap ⇄ ULease (6 שלבים, ראיות בקוד, חובות)
10. `N8N_AUTOMATION.md`       ← אוטומציה תפעולית על אירועי ה-API
11. `BRANCH_KNOWLEDGE.md`     ← תשתית הידע לסניפים (Edge⇄Core)
12. `INVESTOR_RELATIONS.md`   ← roadmap
13. `CASES/*.md`
14. `BRANCHES/*.md`           ← ספרי הידע של הסניפים

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
