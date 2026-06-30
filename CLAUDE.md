# CLAUDE.md — OS Entry Point

נקודת הכניסה הראשית של ה-Claude Operating System עבור הריפו.

## Active Modules
- `COMMAND_API.md` v1.1.0 — 100 slash commands (12 categories, native ⚙️ + behavioral 💬), composition operators, drop-in system prompt loaded.
- `WINDOWS_DEPLOYMENT.md` v1.0.0 — End-to-end Windows rollout for Claude in Microsoft 365 (Word/Excel/PowerPoint + Skills).
- `DEV_ENVIRONMENTS.md` v1.1.0 — End-to-end Claude dev environments: Desktop, VS Code, JetBrains, Cursor, Windsurf, Claude Code CLI + MCP + Computer Use, **+ נספח ג'** מפת Anthropic Ecosystem (מיקום ULease) **+ נספח ד'** Setup סטנדרטי (Cowork folder-first, ABOUT-ME, Global Instructions).
- `LAUNCH.md` v1.1.0 — Master ignition file. ULease go-live playbook: Day 0 → Week 1 → Month 1 → Quarter 1, RACI, kill-switch, master switch, **+ § 3.1 מסלול הדרכה "Master Claude in a Week"** (7 ימים, deliverable יומי, ממופה ל-OS).
- `AGENT_BLUEPRINT.md` v1.5.0 — System-first doctrine. הגשר בין ה-Docs OS ל-Agent Runtime (`stage-a/`): 8-module blueprint, coverage map, evals layer, governance-in-code, **+ § 6.1 חיזוק Gartner** (5 misconceptions ⇄ הדוקטרינה), **+ § 9 Orchestration Patterns** (9 topologies · ULease Skills map · **§ 9.6 מיפוי הקנון** *Agentic Design Patterns*/Gulli), **+ § 10 Coding Workflow Doctrine** (Karpathy's CLAUDE.md: 6 עקרונות workflow · Working Rules · mindset), **+ § 11 MCP vs. Agent Skills** (Connect⇄Learn: 5 ממדים ⇄ ULease · הבהרת מינוח · דוקטרינת Use-Both), **+ § 12 אימות חיצוני** ("How to Actually Build an AI Agent" — 7 צעדים ⇄ 8 מודולים · טקסונומיית LRM/LLM/SLM · build-not-buy · 3⇄4 memory tiers).
- `ULEASE_OS_X.md` v1.0.0 — **כתב-העל / capstone**: *ULease OS X — The Autonomous Mobility Economy Engine*. מתודולוגיית **UDM** (5 שכבות: Data→Behavior→Cognitive→Game-Theory→Execution + Governance spine + Web Intelligence), העיקרון המכונן **"ULease לא מחזיקה כסף"** (שכבת תיווך/החלטה/ביצוע בין יבואנים·דילרים·ליסינג·בנקים·ביטוח·לקוחות, B2B2C&B2B), Big-Five Decision Engine, Instrumental Enrichment/Cognitive Friction, Game-Theory (Nash/cooperative + Utility), **ADS** + Decision Protocol, ו-Governance (Identity·Audit·Kill-Switch). **+ § 4 מיפוי קיים/חלקי/חסר** מול `leasing-api` (Entity-Graph 🟡 · Big-Five ❌ · Game-Theory ❌ · Governance 🟡 · Agents ❌), ו-Moat = Data+Behavior+GameTheory+Governance+Network-Effects (לא AI). בהמשך ל-`AGENT_BLUEPRINT` ו-`CTO_REVIEW`.
- `CASES/ROX_KEY.md` v1.0.0 — Vietnamese benchmark — ROX Key digital transformation. Direct parallel to ULease positioning; 5 operational lessons + 6 action items woven into LAUNCH and DEV_ENVIRONMENTS.
- `system-design-cheatsheet.md` v1.0.0 — 15 מושגי הליבה בעיצוב מערכות (4 אשכולות: Design 🟧 · NFRs 🟦 · Build/Quality 🟩 · Ops/Lifecycle 🟪) + **§ מיפוי ל-ULease**: כל מושג מוצלב מול ראיה בקוד ב-`leasing-api` (Outbox+EventSink, `vehicle_read_model`, `hmacAuth`, **65/65 טסטים**); P0 Multi-Tenancy/RLS נחת כ-first increment (`tenant_id` additive + `rls.sql` fail-closed), נותר action-level RBAC, בהמשך ל-`CTO_REVIEW.md`.
- `BACKEND_ROADMAP.md` v1.0.0 — Backend Developer Roadmap (Shishir Pant) מוצלב מול ULease: 6 שלבי המסלול (🟢 Foundations · 🔵 Backend Core · 🟣 Databases · 🟠 Performance · 🔴 Cloud/Deploy · ⭐ Advanced) כל אחד ⇄ ראיה בקוד (`stateMachine.ts`, `hmacAuth.ts`, `schema.sql`+ledger, Outbox/EventSink, Dockerfile/CI, domain modules) עם סטטוס STRONG/PARTIAL/GAP, ריכוז החובות הפתוחים (Multi-Tenancy/RLS — מחווט end-to-end ✅, נותר action-level RBAC · Event Backbone P2 · Data Platform P3 · Rate-limit/Redis) בהמשך ל-`CTO_REVIEW.md`, ו-§8 "אם הייתי מתחיל מחדש".
- `power-bi-essential-concepts.md` v1.1.0 — 10 מושגי יסוד ב-Power BI + **§ דשבורדים ל-ULease**: חיבור ל-Supabase, מודל Star Schema על `settlements`/`ledger_entries`/`vehicle_read_model`, מדדי DAX (מכירות, עמלות, המרה), RLS לסוכנויות.
- `N8N_AUTOMATION.md` v1.2.0 — שכבת האוטומציה התפעולית: n8n כ-Glue Layer בין ה-Outbox של `leasing-api` לעולם העסקי. חיבור HMAC+Webhook, קטלוג אירועים→workflows, 5 workflows מוכנים, מיפוי ל-AGENT_BLUEPRINT § 9 (n8n=Hands · stage-a=Brain), **+ § 7.3 אנטומיית AI Agent** (Form→Tools Agent→Switch→Slack ⇒ Dealer Onboarding), MCP דו-כיווני, **+ § 8.4 MCP ≠ Skill** (MCP=שכבת חיבור · מצביע ל-AGENT_BLUEPRINT § 11), ממשל ו-kill-switch.
- `BRANCH_KNOWLEDGE.md` v1.0.0 — תשתית הידע לסניפים: ערוץ Slack פרטי + ספר ידע (`BRANCHES/`) לכל סניף/סוכנות, צינור דו-כיווני Edge⇄Core (תובנות 💡/⚠️ → W6 זיקוק שבועי → OS), הפרדת סניפים (RLS doctrine), rollout משולב ב-LAUNCH.
- `CTO_REVIEW.md` v1.2.0 — ביקורת CTO על ULease, תגובה מבוססת-קוד. הצלבת 10 נקודות הביקורת מול הקוד ב-`leasing-api`: תיקון 3 טענות (Event Bus / Data Warehouse / BI קיימים כ-seams), scorecard מתוקן, מפת דרכים P0–P7 ל-Platform v2.0; **שני צעדי P0 נחתו** (Decision Engine seam + Multi-Tenancy/RLS **מחווט end-to-end**: request `X-Tenant-Id`→`asTenant`, worker `SYSTEM_TENANT`, מאומת ב-HTTP, **65/65 טסטים**), נותר action-level RBAC.
- `AI_SDLC_ORCHESTRATION.md` v1.0.0 — מפת כלי ה-AI על פני ה-SDLC (Ashish Sahu) + הטענה *"orchestration of intent, not tools"*: 6 שלבי ה-SDLC ⇄ ראיה ב-`leasing-api`, שכבת-התזמור של ULease (Brain=`stage-a` · Backbone=Outbox+Relay+Sink · Hands=n8n), **+ § 4** אנטומיית Enterprise AI Agent (8 שכבות M-SoftTech: gate→core→MCP→guardrails→routing→isolation) ⇄ seams בקוד (`hmacAuth`, `decisionEngine`, RLS, 65/65 טסטים), בהמשך ל-`AGENT_BLUEPRINT § 9` ו-`CTO_REVIEW`.
- `CLAUDE_CODE_PROJECT_STRUCTURE.md` v1.1.0 — מבנה פרויקט Claude Code (Robbert van Vlijmen) **+ אנטומיה מפורטת (Jamie AI Empire)** ⇄ ה-OS בפועל: 8 אבני-בניין ממופות למקבילה בריפו, ההבחנה בין 4 הפרימיטיבים, **§ 4** חוב P-Tooling, **+ § 5** drop-in קונקרטי שסוגר אותו (`.claude/settings.json` permissions+PostToolUse hook · `.mcp.json` github+postgres · Hook Events ⇄ Working Rules · Context Management thresholds).
- `AUTH_CONCEPTS.md` v1.1.0 — Authentication vs Authorization (M-SoftTech) ⇄ שכבת האבטחה של `leasing-api`: AuthN חזק (`hmacAuth.ts` — HMAC-SHA256 + replay guard + constant-time → 401) · AuthZ ברמת-שורה **מחווט end-to-end** (`X-Tenant-Id`→`asTenant` · worker `SYSTEM_TENANT` · `rls.sql` fail-closed, מאומת ב-HTTP ב-`tenancy.test.ts`), **+ § 5** חוב פתוח (action-level RBAC/403 + hardening: per-tenant keys · `(tenant_id, vin)` PK), בהמשך ל-`system-design-cheatsheet § 9`.
- `MASTER_CLAUDE_58.md` v1.0.0 — 58 Ways to Master Claude (@coder_surya): 8 אשכולות (SETUP·MODELS·PROMPTING·ASK·CONNECTORS·PROJECTS·ARTIFACTS·PRO LEVEL) כל אחד ⇄ המודול שמיישם ב-OS (ASK ⇄ Working Rule #2 · PROJECTS ⇄ ה-OS עצמו · PRO LEVEL ⇄ `stage-a`+`AGENT_BLUEPRINT § 9`), מיפוי ל-`LAUNCH § 3.1` (Master Claude in a Week), ו-self-audit בגרות.
- `BUSINESS_PARTNER.md` v1.0.0 — Claude כשותף עסקי ב-9 צעדים: כל צעד (Role · Business Brain · Daily Briefing · Stress-Test · Sales Copy · Objections · Competition · SOPs · Monthly Review) ⇄ תשתית קיימת ב-OS (Business Brain ⇄ ה-OS עצמו · SOPs ⇄ Skills `§ 11` · Stress-Test ⇄ `CTO_REVIEW`+Working Rule #5/#7 · Review ⇄ Power BI), 8/9 כבר תשתית; חוב: ספריית objections + Monthly Review אוטומטי.
- `CLAUDE_DESIGN.md` v1.0.0 — Claude Design (`claude.ai/design`) ב-8 צעדים ⇄ שכבת ה-UI של ULease: format · `DESIGN.md` · prompt (Goal/layout/content/constraints) · video→slides · iterate · WCAG validate · export → `public/index.html`+`dashboard.html` (מוגש מ-`/ui` ב-`server.ts`); חוב: אין `DESIGN.md` ו-WCAG validation.
- `CLAUDE_4_LEVELS.md` v1.0.0 — 4 רמות הבגרות של Claude (Beginner→Context Builder→Operator→Architect) ⇄ היכן ULease עומדת: כבר **Level 4** (`leasing-api` רץ + `stage-a` agents + Outbox backbone), פער ב-Level 3 (Operator/Cowork). אח מושגי ל-`AI_SKILL_MAP`/`AI_CLAUDE_STACK_2026` (ב-OS המלא), **+ חוב סנכרון OS↔גיט** (~50 מודולים ב-Cowork מול 21 בגיט).

## Module Load Order
1. `OPERATING_SYSTEM.md`      ← roadmap (ראה AGENT_BLUEPRINT § 7)
2. `MEMORY.md`                ← roadmap (ראה AGENT_BLUEPRINT § 7)
3. `COMMAND_API.md`           ← לפני הקטגוריות העסקיות
4. `WINDOWS_DEPLOYMENT.md`    ← הטמעת אופיס מקצה לקצה
5. `DEV_ENVIRONMENTS.md`      ← סביבות פיתוח מקצה לקצה
6. `LAUNCH.md`                ← Master Switch — Go-Live
7. `AGENT_BLUEPRINT.md`       ← Docs OS ⇄ Agent Runtime (stage-a/)
7a. `ULEASE_OS_X.md`          ← capstone: UDM 5 שכבות + Governance + ADS + Moat (חזון-העל)
8. `CTO_REVIEW.md`            ← ביקורת CTO ⇄ קוד + מפת דרכים Platform v2.0
8a. `AI_SDLC_ORCHESTRATION.md` ← מפת SDLC ⇄ שכבת-התזמור (Brain/Backbone/Hands) + אנטומיית Agent
8b. `CLAUDE_CODE_PROJECT_STRUCTURE.md` ← מבנה Claude Code סטנדרטי ⇄ ה-OS בפועל
8c. `AUTH_CONCEPTS.md`        ← AuthN vs AuthZ ⇄ hmacAuth + RLS
8d. `MASTER_CLAUDE_58.md`     ← 58 Ways ⇄ מודולי ה-OS + LAUNCH § 3.1
8e. `BUSINESS_PARTNER.md`     ← Claude כשותף עסקי (9 צעדים) ⇄ תשתית ה-OS
8f. `CLAUDE_DESIGN.md`        ← Claude Design (8 צעדים) ⇄ שכבת ה-UI (`public/`)
8g. `CLAUDE_4_LEVELS.md`      ← 4 רמות Claude ⇄ ULease ב-Level 4 + חוב סנכרון OS↔גיט
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

## Imported OS Modules
מודולים שיובאו מענף ה-OS (אוחדו ל-main; ראו DECISION_LOG). מצוטטים כאן לעקביות-אינדקס:

- `AI_7_SKILLS.md` v1.0.0 — 7 מיומנויות לשליטה ב-AI ב-2026
- `AI_AGENTIC_WORKFLOWS.md` v1.0.0 — 100 Agentic Claude Workflows ממופים ל-ULease (יישום + תעדוף, cross-ref ל-AUTOMATION_MAP)
- `AI_CLAUDE_ENGINEER_ROADMAP.md` v1.0.0 — Claude AI Engineer Roadmap — 15 שלבים, ואיפה אתה עליהם
- `AI_CLAUDE_GLOSSARY.md` v1.1.0 — מילון Claude — 30 מונחים שחייבים להכיר
- `AI_CLAUDE_STACK_2026.md` v1.8.0 — Claude Stack 2026 — How to use Claude in 2026
- `AI_CLAUDE_TOOL_SELECTOR.md` v1.3.0 — איזה Claude לבחור? — Which Claude Should You Use?
- `AI_DATA_BI.md` v1.5.0 — יסודות BI ומידול נתונים — Power BI כמקרה לימוד
- `AI_DATA_VALIDATION.md` v1.0.0 — ולידציית נתונים — Data Validation Techniques (שער האיכות של האנליסט)
- `AI_LEARNING_RESOURCES.md` v1.0.0 — משאבי למידה — קוריקולום AI לפי המפה
- `AI_LINEAR_ALGEBRA.md` v1.0.0 — יסודות אלגברה לינארית — Linear Algebra Foundations (Cheat Sheet)
- `AI_MICROSERVICES.md` v1.0.0 — Microservices — איך שירות אחד מתחבר לאחר
- `AI_PROCESS_INTELLIGENCE.md` v1.1.0 — מודיעין תהליכים ובקרת הטמעת AI — Process Intelligence & Human-in-the-Loop
- `AI_PROFICIENCIES_2026.md` v1.0.0 — מיומנויות ה-AI החיוניות ל-2026 — Essential AI Proficiencies for the 2026 Landscape
- `AI_PROGRESSION_PLAN.md` v1.0.0 — תוכנית התקדמות אישית — מ-AI Tools ל-Automation Architect
- `AI_PROJECT_STRUCTURE.md` v1.1.0 — מבנה פרויקט AI — ארבע תיקיות, אפס בלגן
- `AI_RAG_DESIGN.md` v1.0.0 — תכנון RAG — 15 הטעויות ששוברות Retrieval
- `AI_ROLES_2026.md` v1.0.0 — תפקידי ה-AI החמים ב-2026 — ומי מכסה אותם ב-ULease
- `AI_SKILLS_ACQUISITION.md` v1.0.0 — תוכנית רכישת מיומנויות — Build to Learn
- `AI_SKILL_MAP.md` v1.0.0 — מפת מיומנויות ה-AI — The AI Skill Map
- `AI_SYSTEM_DESIGN.md` v1.3.0 — יסודות System Design — ארכיטקטורת הפלטפורמה
- `AI_TYPES.md` v1.1.0 — סוגי AI — Traditional · Generative · Agentic
- `BRANCH_KNOWLEDGE.md` v1.0.0 — BRANCH_KNOWLEDGE.md — תשתית הידע לסניפים
- `CASES/ULEASE.md` v1.5.0 — ULease 🎯 Leasing.co.il — Business Case & Forecast
- `CASES/ULEASE_AUDIT.md` v1.4.0 — ביקורת מקצה-לקצה — תיק ULease 🎯 Leasing.co.il
- `CASES/ULEASE_AUTOMATION_MAP.md` v1.5.0 — ULease 🎯 — מפת אוטומציות AI לפי פונקציה עסקית
- `CASES/ULEASE_DECK.md` v1.2.0 — ULEASE_DECK.md
- `CASES/ULEASE_DEMAND_ENGINE.md` v1.2.1 — ULease 🎯 — Demand Engine (בלופרינט n8n: אוטופיילוט צד-הביקוש)
- `CASES/ULEASE_DEMAND_PLAYBOOK.md` v1.2.0 — ULease 🎯 — Playbook צד-הביקוש (Demand Generation)
- `CASES/ULEASE_FINANCE_INSURANCE.md` v1.1.0 — ULease 🎯 — מימון, ביטוח וחיתום דיגיטלי
- `CASES/ULEASE_HIRING.md` v1.1.0 — ULease 🎯 — ערכת גיוס (Hiring Kit)
- `CASES/ULEASE_IMPORTER_PLAYBOOK.md` v1.1.0 — ULease 🎯 — Playbook מו"מ מול יבואני רכב
- `CASES/ULEASE_LAUNCH_CHECKLIST.md` v1.3.0 — ULease 🎯 — צ'קליסט השקה (שבועיים)
- `CASES/ULEASE_LEASING_PLAYBOOK.md` v1.1.0 — ULease 🎯 — Playbook מו"מ: יבואנים מקבילים וחברות ליסינג
- `CASES/ULEASE_LEGAL_BRIEF.md` v1.0.0 — ULease 🎯 — תדריך משפטי לעו"ד (Legal Brief)
- `CASES/ULEASE_METHODOLOGY.md` v1.1.0 — ULease 🎯 — הארכיטקטורה המתודולוגית
- `CASES/ULEASE_OUTBOUND_ENGINE.md` v1.2.1 — ULease 🎯 — Outbound Engine (בלופרינט n8n + Claude)
- `CASES/ULEASE_OUTREACH_SCRIPTS.md` v1.3.0 — ULease 🎯 — סקריפטים לפנייה (שיחה · מייל · וואטסאפ)
- `CASES/ULEASE_PRICING_SLA.md` v1.1.0 — ULease 🎯 — מחירון רשמי + SLA ספקים
- `CASES/ULEASE_SPEC.md` v1.5.0 — ULease 🎯 Leasing.co.il — איפיון מוצר ומערכת (End-to-End Spec)
- `CASES/ULEASE_TECH_ONBOARDING.md` v1.2.0 — ULease 🎯 — Onboarding למנהל מערכות הטכנולוגיה
- `CLOUD_ARCHITECT_SKILLS.md` v1.0.0 — כישורי ארכיטקט ענן — The Key Cloud Architect Skills
- `COMMAND_API_TASKS.md` v1.1.0 — ספריית פקודות משימה — Task Commands & Spreadsheet Prompts
- `COWORK/TEMPLATES/os-module-header.md` v1.0.0 — תבנית: Header למודול OS חדש
- `COWORK_SETUP.md` v1.2.0 — CLAUDE COWORK — מדריך הגדרה ואונבורדינג
- `DECISION_LOG.md` v1.57.0 — DECISION_LOG.md — יומן החלטות
- `INVESTOR_RELATIONS.md` v1.2.0 — CLAUDE INVESTOR RELATIONS — ULease 🎯
- `KUBERNETES_101.md` v1.1.0 — קוברנטיס 101 — Kubernetes (K8s) Orchestration Foundations
- `MEMORY.md` v1.1.0 — CLAUDE MEMORY — Persistent Memory Layer
- `OPERATING_SYSTEM.md` v1.18.0 — CLAUDE OPERATING SYSTEM — Kernel
- `PROJECTS_SETUP.md` v1.0.0 — CLAUDE PROJECTS — הגדרת פרויקטים
