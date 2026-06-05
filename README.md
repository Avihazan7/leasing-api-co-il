# leasing-api-co-il
פלטפורמת מסחר, שיווק ומכירת רכבים חדשים — Leasing.co.il

## Active Modules
- [`LAUNCH.md`](./LAUNCH.md) v1.0.0 — **Master ignition file.** ULease Go-Live playbook: Day 0 → Week 1 → Month 1 → Quarter 1, RACI, kill-switch, master switch. הקובץ שמפעיל את כל היתר.
- [`COMMAND_API.md`](./COMMAND_API.md) v1.1.0 — CLAUDE Command API: **100 slash commands** ב-12 קטגוריות, עם הבחנה מפורשת בין Native Claude Code primitives (⚙️) ל-Behavioral prompts (💬). Composition operators ו-drop-in system prompt לטעינה ב-OS.
- [`WINDOWS_DEPLOYMENT.md`](./WINDOWS_DEPLOYMENT.md) v1.0.0 — הטמעת Claude לאופיס מקצה לקצה על Windows: התקנה, חיווט M365/OneDrive/SharePoint, playbooks ל-Word/Excel/PowerPoint, בניית Skills, ו-rollout ארגוני (Intune/GPO/PowerShell).
- [`DEV_ENVIRONMENTS.md`](./DEV_ENVIRONMENTS.md) v1.0.0 — סביבות פיתוח של Claude מקצה לקצה: Desktop, VS Code, JetBrains, Cursor, Windsurf, ו-Claude Code CLI; שכבות MCP ו-Computer Use; אינטגרציה מלאה ל-COMMAND_API; rollout צוותי, secrets, ו-checklist בגרות.
- [`AGENT_BLUEPRINT.md`](./AGENT_BLUEPRINT.md) v1.1.0 — **System-first doctrine.** הגשר בין ה-Docs OS ל-Agent Runtime (`stage-a/`): 8-module blueprint (Purpose → Prompt → LLM → Tools → Memory → Orchestration → UI → Evals), coverage map כן, שכבת Evals, governance שנאכף בקוד, **ו-§ 9 Orchestration Patterns** — 9 topologies (Chaining · Parallel · Orchestrator-Worker · Evaluator · Router · Autonomous · Reflexion · ReWOO · Plan&Execute), מיפוי ה-Skills של ULease, ו-זיהוי `stage-a` כ-Plan&Execute עם Stage-B = +Replan.
- [`N8N_AUTOMATION.md`](./N8N_AUTOMATION.md) v1.1.0 — **שכבת האוטומציה התפעולית.** [n8n](https://n8n.io/) כ-Glue Layer בין אירועי ה-Outbox של `leasing-api` לעולם העסקי: חיבור HMAC+Webhook, קטלוג אירועים→workflows, 5 workflows מוכנים (Post-Sale, Settlement, Recovery, Digest, Lead Scoring), אנטומיית AI Agent על הקנבס (Claude + Memory + Tools ⇒ Dealer Onboarding), חלוקת עבודה מול `stage-a` (n8n=Hands · stage-a=Brain), MCP דו-כיווני ל-Claude, טופולוגיית Docker, וממשל עם kill-switch.

- [`CTO_REVIEW.md`](./CTO_REVIEW.md) v1.0.0 — **ביקורת CTO על ULease v1.2 — תגובה מבוססת-קוד.** הצלבת 10 נקודות הביקורת מול הקוד בפועל ב-`leasing-api`: תיקון 3 טענות (Event Bus / Data Warehouse / RLS — כולן כבר קיימות כ-seams), scorecard מתוקן מבוסס-ראיות, ומפת דרכים מתועדפת P0–P7 ל-Platform v2.0 (Multi-Tenant → Decision Engine → Event Backbone → Data Platform → Matching). הצעד הראשון (Decision Engine seam) כבר נחת בקוד, מאומת (55/55) ותואם-לאחור.

## Cheat Sheets & Concepts
- [`system-design-cheatsheet.md`](./system-design-cheatsheet.md) v1.0.0 — **15 מושגי הליבה בעיצוב מערכות** ב-4 אשכולות (Design 🟧 · NFRs 🟦 · Build/Quality 🟩 · Ops/Lifecycle 🟪). לא תיאוריה: כל אחד מ-15 המושגים מוצלב מול **ראיה בקוד** ב-`leasing-api` (Outbox+EventSink, CQRS `vehicle_read_model`, `hmacAuth`, 55/55 טסטים), כולל שני חובות פתוחים מתועדים — RLS בצד DB ו-Multi-Tenancy — בהמשך ישיר ל-[`CTO_REVIEW.md`](./CTO_REVIEW.md).

## Strategic Benchmarks
- [`CASES/ROX_KEY.md`](./CASES/ROX_KEY.md) v1.0.0 — Case study וייטנאמי: ROX Key, קונגלומרט שעבר טרנספורמציה דיגיטלית מבוססת-נתונים בענף ניהול הנכסים. **Direct parallel ל-ULease.** 5 לקחים אופרטיביים + 6 action items שכבר משולבים ב-`LAUNCH.md` וב-`DEV_ENVIRONMENTS.md`.
