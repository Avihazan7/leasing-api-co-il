# leasing-api-co-il
פלטפורמת מסחר, שיווק ומכירת רכבים חדשים — Leasing.co.il

## Active Modules
- [`LAUNCH.md`](./LAUNCH.md) v1.1.0 — **Master ignition file.** ULease Go-Live playbook: Day 0 → Week 1 → Month 1 → Quarter 1, RACI, kill-switch, master switch. הקובץ שמפעיל את כל היתר.
- [`COMMAND_API.md`](./COMMAND_API.md) v1.1.0 — CLAUDE Command API: **100 slash commands** ב-12 קטגוריות, עם הבחנה מפורשת בין Native Claude Code primitives (⚙️) ל-Behavioral prompts (💬). Composition operators ו-drop-in system prompt לטעינה ב-OS.
- [`WINDOWS_DEPLOYMENT.md`](./WINDOWS_DEPLOYMENT.md) v1.0.0 — הטמעת Claude לאופיס מקצה לקצה על Windows: התקנה, חיווט M365/OneDrive/SharePoint, playbooks ל-Word/Excel/PowerPoint, בניית Skills, ו-rollout ארגוני (Intune/GPO/PowerShell).
- [`DEV_ENVIRONMENTS.md`](./DEV_ENVIRONMENTS.md) v1.1.0 — סביבות פיתוח של Claude מקצה לקצה: Desktop, VS Code, JetBrains, Cursor, Windsurf, ו-Claude Code CLI; שכבות MCP ו-Computer Use; אינטגרציה מלאה ל-COMMAND_API; rollout צוותי, secrets, ו-checklist בגרות.
- [`AGENT_BLUEPRINT.md`](./AGENT_BLUEPRINT.md) v1.5.0 — **System-first doctrine.** הגשר בין ה-Docs OS ל-Agent Runtime (`stage-a/`): 8-module blueprint (Purpose → Prompt → LLM → Tools → Memory → Orchestration → UI → Evals), coverage map כן, שכבת Evals, governance שנאכף בקוד, **§ 9 Orchestration Patterns** — 9 topologies (Chaining · Parallel · Orchestrator-Worker · Evaluator · Router · Autonomous · Reflexion · ReWOO · Plan&Execute), מיפוי ה-Skills של ULease, זיהוי `stage-a` כ-Plan&Execute עם Stage-B = +Replan, **ו-§ 11 MCP vs. Agent Skills** — Connect (MCP=AI-native APIs) ⇄ Learn (Skills=AI-native SOPs): 5 ממדים ⇄ ULease, הבהרת מינוח, ודוקטרינת Use-Both.
- [`N8N_AUTOMATION.md`](./N8N_AUTOMATION.md) v1.2.0 — **שכבת האוטומציה התפעולית.** [n8n](https://n8n.io/) כ-Glue Layer בין אירועי ה-Outbox של `leasing-api` לעולם העסקי: חיבור HMAC+Webhook, קטלוג אירועים→workflows, 5 workflows מוכנים (Post-Sale, Settlement, Recovery, Digest, Lead Scoring), אנטומיית AI Agent על הקנבס (Claude + Memory + Tools ⇒ Dealer Onboarding), חלוקת עבודה מול `stage-a` (n8n=Hands · stage-a=Brain), MCP דו-כיווני ל-Claude (**§ 8.4: MCP=שכבת חיבור, לא Skill** — מצביע ל-`AGENT_BLUEPRINT § 11`), טופולוגיית Docker, וממשל עם kill-switch.

- [`CTO_REVIEW.md`](./CTO_REVIEW.md) v1.2.0 — **ביקורת CTO על ULease — תגובה מבוססת-קוד.** הצלבת 10 נקודות הביקורת מול הקוד בפועל ב-`leasing-api`: תיקון 3 טענות (Event Bus / Data Warehouse / BI — כבר קיימות כ-seams), scorecard מתוקן מבוסס-ראיות, ומפת דרכים מתועדפת P0–P7 ל-Platform v2.0. **שני צעדי P0 נחתו**: Decision Engine seam + Multi-Tenancy/RLS **מחווט end-to-end** (request `X-Tenant-Id`→`asTenant` · worker `SYSTEM_TENANT`), מאומתים ב-HTTP (**65/65**) ותואמי-לאחור; נותר action-level RBAC.

## Cheat Sheets & Concepts
- [`BACKEND_ROADMAP.md`](./BACKEND_ROADMAP.md) v1.0.0 — **Backend Developer Roadmap ⇄ ULease.** האינפוגרפיקה הפופולרית של Shishir Pant, אבל לא גנרית: 6 שלבי המסלול (🟢 Foundations · 🔵 Backend Core · 🟣 Databases · 🟠 Performance · 🔴 Cloud/Deploy · ⭐ Advanced Engineering) מוצלבים **כל אחד מול ראיה בקוד** ב-`leasing-api` (state machine, HMAC auth, Outbox+ledger, CQRS read model, Docker/CI, domain modules), עם סטטוס STRONG/PARTIAL/GAP לכל שלב, ריכוז החובות הפתוחים (Multi-Tenancy/RLS — מחווט end-to-end ✅, נותר action-level RBAC) בהמשך ל-[`CTO_REVIEW.md`](./CTO_REVIEW.md), ו-§ "אם הייתי מתחיל מחדש היום".
- [`system-design-cheatsheet.md`](./system-design-cheatsheet.md) v1.0.0 — **15 מושגי הליבה בעיצוב מערכות** ב-4 אשכולות (Design 🟧 · NFRs 🟦 · Build/Quality 🟩 · Ops/Lifecycle 🟪). לא תיאוריה: כל אחד מ-15 המושגים מוצלב מול **ראיה בקוד** ב-`leasing-api` (Outbox+EventSink, CQRS `vehicle_read_model`, `hmacAuth`, **65/65 טסטים**); P0 Multi-Tenancy/RLS נחת כ-first increment (`tenant_id` additive + `rls.sql` fail-closed מאחורי flag, מאומת ב-`tenancy.test.ts`), נותר action-level RBAC — בהמשך ישיר ל-[`CTO_REVIEW.md`](./CTO_REVIEW.md).
- [`AI_SDLC_ORCHESTRATION.md`](./AI_SDLC_ORCHESTRATION.md) v1.0.0 — **מפת כלי ה-AI על פני ה-SDLC ⇄ ULease.** הטענה *"orchestration of intent, not tools"*: 6 שלבי ה-SDLC מוצלבים מול ראיה בקוד, ושכבת-התזמור של ULease מוצגת כ-**Brain** (`stage-a`) · **Backbone** (Transactional Outbox + Relay + `EventSink`) · **Hands** (n8n). § 4 ממפה את אנטומיית ה-Enterprise AI Agent (8 שכבות: gate→core→MCP→guardrails→routing→isolation→MVP) מול ה-seams (`hmacAuth`, `decisionEngine`, RLS, **65/65 טסטים**).
- [`CLAUDE_CODE_PROJECT_STRUCTURE.md`](./CLAUDE_CODE_PROJECT_STRUCTURE.md) v1.1.0 — **מבנה פרויקט Claude Code ⇄ ה-OS בפועל.** 8 אבני-הבניין (van Vlijmen) ממופות למקבילה בריפו (COMMAND_API=commands · `stage-a`=agents · AGENT_BLUEPRINT § 11=skills/MCP), ההבחנה בין 4 הפרימיטיבים, וחוב P-Tooling — **+ § 5 (Jamie AI Empire)**: drop-in קונקרטי שסוגר אותו (`.claude/settings.json` permissions+hook · `.mcp.json` github+postgres · Hook Events ⇄ Working Rules · Context Management).
- [`AUTH_CONCEPTS.md`](./AUTH_CONCEPTS.md) v1.1.0 — **Authentication vs Authorization ⇄ שכבת האבטחה.** AuthN חזק (`hmacAuth.ts` — HMAC-SHA256 + replay guard + `timingSafeEqual` → 401) ו-AuthZ ברמת-שורה **מחווט end-to-end** (`X-Tenant-Id`→`asTenant` · worker `SYSTEM_TENANT` · `rls.sql` fail-closed, מאומת ב-HTTP ב-`tenancy.test.ts`), כולל חוב פתוח: action-level RBAC/403 + hardening (per-tenant keys · `(tenant_id, vin)` PK).
- [`MASTER_CLAUDE_58.md`](./MASTER_CLAUDE_58.md) v1.0.0 — **58 Ways to Master Claude ⇄ מודולי ה-OS.** 8 אשכולות (SETUP·MODELS·PROMPTING·ASK·CONNECTORS·PROJECTS·ARTIFACTS·PRO LEVEL) כל אחד ⇄ המודול שמיישם אותו (ASK ⇄ Working Rule #2 · PROJECTS ⇄ ה-OS עצמו · PRO LEVEL ⇄ `stage-a`+orchestration), מיפוי ל-[`LAUNCH.md`](./LAUNCH.md) § 3.1, ו-self-audit בגרות.
- [`BUSINESS_PARTNER.md`](./BUSINESS_PARTNER.md) v1.0.0 — **Claude כשותף עסקי ב-9 צעדים ⇄ ה-OS.** כל צעד (Role · Business Brain · Daily Briefing · Stress-Test · Sales Copy · Objections · Competition · SOPs · Monthly Review) ⇄ תשתית קיימת (Business Brain ⇄ ה-OS עצמו · SOPs ⇄ Skills · Stress-Test ⇄ `CTO_REVIEW`+Working Rules · Review ⇄ Power BI) — 8/9 כבר תשתית, לא פרקטיקה אישית.
- [`CLAUDE_DESIGN.md`](./CLAUDE_DESIGN.md) v1.0.0 — **Claude Design (`claude.ai/design`) ב-8 צעדים ⇄ שכבת ה-UI.** format · `DESIGN.md` · prompt · video→slides · iterate · WCAG validate · export → ה-storefront/dashboard ב-`public/` (מוגש מ-`/ui` ב-`server.ts`); חוב: אין `DESIGN.md` ו-WCAG validation שיטתי.
- [`CLAUDE_4_LEVELS.md`](./CLAUDE_4_LEVELS.md) v1.0.0 — **4 רמות הבגרות של Claude ⇄ היכן ULease עומדת.** Beginner→Context Builder→Operator→Architect; ULease כבר **Level 4** (`leasing-api` רץ + `stage-a` agents + Outbox backbone — "systems run the show"), הפער היחיד ב-Level 3 (Operator/Cowork). אח מושגי ל-`AI_SKILL_MAP`/`AI_CLAUDE_STACK_2026`, **+ חוב הסנכרון OS↔גיט** (~50 מודולים ב-Cowork/Projects מול 21 בגיט).

## Strategic Benchmarks
- [`CASES/ROX_KEY.md`](./CASES/ROX_KEY.md) v1.0.0 — Case study וייטנאמי: ROX Key, קונגלומרט שעבר טרנספורמציה דיגיטלית מבוססת-נתונים בענף ניהול הנכסים. **Direct parallel ל-ULease.** 5 לקחים אופרטיביים + 6 action items שכבר משולבים ב-`LAUNCH.md` וב-`DEV_ENVIRONMENTS.md`.

## Imported OS Modules
מודולים שיובאו מענף ה-OS (אוחדו ל-main):

- [`AI_7_SKILLS.md`](./AI_7_SKILLS.md) v1.0.0 — 7 מיומנויות לשליטה ב-AI ב-2026
- [`AI_AGENTIC_WORKFLOWS.md`](./AI_AGENTIC_WORKFLOWS.md) v1.0.0 — 100 Agentic Claude Workflows mapped to ULease (application + priority per workflow, cross-ref to AUTOMATION_MAP)
- [`AI_CLAUDE_ENGINEER_ROADMAP.md`](./AI_CLAUDE_ENGINEER_ROADMAP.md) v1.0.0 — Claude AI Engineer Roadmap — 15 שלבים, ואיפה אתה עליהם
- [`AI_CLAUDE_GLOSSARY.md`](./AI_CLAUDE_GLOSSARY.md) v1.1.0 — מילון Claude — 30 מונחים שחייבים להכיר
- [`AI_CLAUDE_STACK_2026.md`](./AI_CLAUDE_STACK_2026.md) v1.8.0 — Claude Stack 2026 — How to use Claude in 2026
- [`AI_CLAUDE_TOOL_SELECTOR.md`](./AI_CLAUDE_TOOL_SELECTOR.md) v1.3.0 — איזה Claude לבחור? — Which Claude Should You Use?
- [`AI_DATA_BI.md`](./AI_DATA_BI.md) v1.5.0 — יסודות BI ומידול נתונים — Power BI כמקרה לימוד
- [`AI_DATA_VALIDATION.md`](./AI_DATA_VALIDATION.md) v1.0.0 — ולידציית נתונים — Data Validation Techniques (שער האיכות של האנליסט)
- [`AI_LEARNING_RESOURCES.md`](./AI_LEARNING_RESOURCES.md) v1.0.0 — משאבי למידה — קוריקולום AI לפי המפה
- [`AI_LINEAR_ALGEBRA.md`](./AI_LINEAR_ALGEBRA.md) v1.0.0 — יסודות אלגברה לינארית — Linear Algebra Foundations (Cheat Sheet)
- [`AI_MICROSERVICES.md`](./AI_MICROSERVICES.md) v1.0.0 — Microservices — איך שירות אחד מתחבר לאחר
- [`AI_PROCESS_INTELLIGENCE.md`](./AI_PROCESS_INTELLIGENCE.md) v1.1.0 — מודיעין תהליכים ובקרת הטמעת AI — Process Intelligence & Human-in-the-Loop
- [`AI_PROFICIENCIES_2026.md`](./AI_PROFICIENCIES_2026.md) v1.0.0 — מיומנויות ה-AI החיוניות ל-2026 — Essential AI Proficiencies for the 2026 Landscape
- [`AI_PROGRESSION_PLAN.md`](./AI_PROGRESSION_PLAN.md) v1.0.0 — תוכנית התקדמות אישית — מ-AI Tools ל-Automation Architect
- [`AI_PROJECT_STRUCTURE.md`](./AI_PROJECT_STRUCTURE.md) v1.1.0 — מבנה פרויקט AI — ארבע תיקיות, אפס בלגן
- [`AI_RAG_DESIGN.md`](./AI_RAG_DESIGN.md) v1.0.0 — תכנון RAG — 15 הטעויות ששוברות Retrieval
- [`AI_ROLES_2026.md`](./AI_ROLES_2026.md) v1.0.0 — תפקידי ה-AI החמים ב-2026 — ומי מכסה אותם ב-ULease
- [`AI_SKILLS_ACQUISITION.md`](./AI_SKILLS_ACQUISITION.md) v1.0.0 — תוכנית רכישת מיומנויות — Build to Learn
- [`AI_SKILL_MAP.md`](./AI_SKILL_MAP.md) v1.0.0 — מפת מיומנויות ה-AI — The AI Skill Map
- [`AI_SYSTEM_DESIGN.md`](./AI_SYSTEM_DESIGN.md) v1.3.0 — יסודות System Design — ארכיטקטורת הפלטפורמה
- [`AI_TYPES.md`](./AI_TYPES.md) v1.1.0 — סוגי AI — Traditional · Generative · Agentic
- [`BRANCH_KNOWLEDGE.md`](./BRANCH_KNOWLEDGE.md) v1.0.0 — BRANCH_KNOWLEDGE.md — תשתית הידע לסניפים
- [`CASES/ULEASE.md`](./CASES/ULEASE.md) v1.5.0 — ULease 🎯 Leasing.co.il — Business Case & Forecast
- [`CASES/ULEASE_AUDIT.md`](./CASES/ULEASE_AUDIT.md) v1.4.0 — ביקורת מקצה-לקצה — תיק ULease 🎯 Leasing.co.il
- [`CASES/ULEASE_AUTOMATION_MAP.md`](./CASES/ULEASE_AUTOMATION_MAP.md) v1.5.0 — ULease 🎯 — מפת אוטומציות AI לפי פונקציה עסקית
- [`CASES/ULEASE_DECK.md`](./CASES/ULEASE_DECK.md) v1.2.0 — ULEASE_DECK.md
- [`CASES/ULEASE_DEMAND_ENGINE.md`](./CASES/ULEASE_DEMAND_ENGINE.md) v1.2.1 — ULease 🎯 — Demand Engine (בלופרינט n8n: אוטופיילוט צד-הביקוש)
- [`CASES/ULEASE_DEMAND_PLAYBOOK.md`](./CASES/ULEASE_DEMAND_PLAYBOOK.md) v1.2.0 — ULease 🎯 — Playbook צד-הביקוש (Demand Generation)
- [`CASES/ULEASE_FINANCE_INSURANCE.md`](./CASES/ULEASE_FINANCE_INSURANCE.md) v1.1.0 — ULease 🎯 — מימון, ביטוח וחיתום דיגיטלי
- [`CASES/ULEASE_HIRING.md`](./CASES/ULEASE_HIRING.md) v1.1.0 — ULease 🎯 — ערכת גיוס (Hiring Kit)
- [`CASES/ULEASE_IMPORTER_PLAYBOOK.md`](./CASES/ULEASE_IMPORTER_PLAYBOOK.md) v1.1.0 — ULease 🎯 — Playbook מו"מ מול יבואני רכב
- [`CASES/ULEASE_LAUNCH_CHECKLIST.md`](./CASES/ULEASE_LAUNCH_CHECKLIST.md) v1.3.0 — ULease 🎯 — צ'קליסט השקה (שבועיים)
- [`CASES/ULEASE_LEASING_PLAYBOOK.md`](./CASES/ULEASE_LEASING_PLAYBOOK.md) v1.1.0 — ULease 🎯 — Playbook מו"מ: יבואנים מקבילים וחברות ליסינג
- [`CASES/ULEASE_LEGAL_BRIEF.md`](./CASES/ULEASE_LEGAL_BRIEF.md) v1.0.0 — ULease 🎯 — תדריך משפטי לעו"ד (Legal Brief)
- [`CASES/ULEASE_METHODOLOGY.md`](./CASES/ULEASE_METHODOLOGY.md) v1.1.0 — ULease 🎯 — הארכיטקטורה המתודולוגית
- [`CASES/ULEASE_OUTBOUND_ENGINE.md`](./CASES/ULEASE_OUTBOUND_ENGINE.md) v1.2.1 — ULease 🎯 — Outbound Engine (בלופרינט n8n + Claude)
- [`CASES/ULEASE_OUTREACH_SCRIPTS.md`](./CASES/ULEASE_OUTREACH_SCRIPTS.md) v1.3.0 — ULease 🎯 — סקריפטים לפנייה (שיחה · מייל · וואטסאפ)
- [`CASES/ULEASE_PRICING_SLA.md`](./CASES/ULEASE_PRICING_SLA.md) v1.1.0 — ULease 🎯 — מחירון רשמי + SLA ספקים
- [`CASES/ULEASE_SPEC.md`](./CASES/ULEASE_SPEC.md) v1.5.0 — ULease 🎯 Leasing.co.il — איפיון מוצר ומערכת (End-to-End Spec)
- [`CASES/ULEASE_TECH_ONBOARDING.md`](./CASES/ULEASE_TECH_ONBOARDING.md) v1.2.0 — ULease 🎯 — Onboarding למנהל מערכות הטכנולוגיה
- [`CLOUD_ARCHITECT_SKILLS.md`](./CLOUD_ARCHITECT_SKILLS.md) v1.0.0 — כישורי ארכיטקט ענן — The Key Cloud Architect Skills
- [`COMMAND_API_TASKS.md`](./COMMAND_API_TASKS.md) v1.1.0 — ספריית פקודות משימה — Task Commands & Spreadsheet Prompts
- [`COWORK/TEMPLATES/os-module-header.md`](./COWORK/TEMPLATES/os-module-header.md) v1.0.0 — תבנית: Header למודול OS חדש
- [`COWORK_SETUP.md`](./COWORK_SETUP.md) v1.2.0 — CLAUDE COWORK — מדריך הגדרה ואונבורדינג
- [`DECISION_LOG.md`](./DECISION_LOG.md) v1.57.0 — DECISION_LOG.md — יומן החלטות
- [`INVESTOR_RELATIONS.md`](./INVESTOR_RELATIONS.md) v1.2.0 — CLAUDE INVESTOR RELATIONS — ULease 🎯
- [`KUBERNETES_101.md`](./KUBERNETES_101.md) v1.1.0 — קוברנטיס 101 — Kubernetes (K8s) Orchestration Foundations
- [`MEMORY.md`](./MEMORY.md) v1.1.0 — CLAUDE MEMORY — Persistent Memory Layer
- [`OPERATING_SYSTEM.md`](./OPERATING_SYSTEM.md) v1.17.0 — CLAUDE OPERATING SYSTEM — Kernel
- [`PROJECTS_SETUP.md`](./PROJECTS_SETUP.md) v1.0.0 — CLAUDE PROJECTS — הגדרת פרויקטים
