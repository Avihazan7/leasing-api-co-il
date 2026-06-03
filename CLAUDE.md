# CLAUDE.md — OS Entry Point

נקודת הכניסה הראשית של ה-Claude Operating System עבור הריפו.

## Active Modules
- `COMMAND_API.md` v1.1.0 — 100 slash commands (12 categories, native ⚙️ + behavioral 💬), composition operators, drop-in system prompt loaded.
- `WINDOWS_DEPLOYMENT.md` v1.0.0 — End-to-end Windows rollout for Claude in Microsoft 365 (Word/Excel/PowerPoint + Skills).
- `DEV_ENVIRONMENTS.md` v1.0.0 — End-to-end Claude dev environments: Desktop, VS Code, JetBrains, Cursor, Windsurf, Claude Code CLI + MCP + Computer Use.
- `LAUNCH.md` v1.0.0 — Master ignition file. ULease go-live playbook: Day 0 → Week 1 → Month 1 → Quarter 1, RACI, kill-switch, master switch.
- `AGENT_BLUEPRINT.md` v1.2.0 — System-first doctrine. הגשר בין ה-Docs OS ל-Agent Runtime (`stage-a/`): 8-module blueprint, coverage map, evals layer, governance-in-code, **+ § 9 Orchestration Patterns** (9 topologies · ULease Skills map · `stage-a`=Plan&Execute · Stage-B=P&E+Replan), **+ § 10 Coding Workflow Doctrine** (Karpathy's CLAUDE.md: 6 עקרונות workflow · Working Rules · mindset).
- `CASES/ROX_KEY.md` v1.0.0 — Vietnamese benchmark — ROX Key digital transformation. Direct parallel to ULease positioning; 5 operational lessons + 6 action items woven into LAUNCH and DEV_ENVIRONMENTS.
- `power-bi-essential-concepts.md` v1.1.0 — 10 מושגי יסוד ב-Power BI + **§ דשבורדים ל-ULease**: חיבור ל-Supabase, מודל Star Schema על `settlements`/`ledger_entries`/`vehicle_read_model`, מדדי DAX (מכירות, עמלות, המרה), RLS לסוכנויות.
- `N8N_AUTOMATION.md` v1.1.0 — שכבת האוטומציה התפעולית: n8n כ-Glue Layer בין ה-Outbox של `leasing-api` לעולם העסקי. חיבור HMAC+Webhook, קטלוג אירועים→workflows, 5 workflows מוכנים, מיפוי ל-AGENT_BLUEPRINT § 9 (n8n=Hands · stage-a=Brain), **+ § 7.3 אנטומיית AI Agent** (Form→Tools Agent→Switch→Slack ⇒ Dealer Onboarding), MCP דו-כיווני, ממשל ו-kill-switch.

## Module Load Order
1. `OPERATING_SYSTEM.md`      ← roadmap (ראה AGENT_BLUEPRINT § 7)
2. `MEMORY.md`                ← roadmap (ראה AGENT_BLUEPRINT § 7)
3. `COMMAND_API.md`           ← לפני הקטגוריות העסקיות
4. `WINDOWS_DEPLOYMENT.md`    ← הטמעת אופיס מקצה לקצה
5. `DEV_ENVIRONMENTS.md`      ← סביבות פיתוח מקצה לקצה
6. `LAUNCH.md`                ← Master Switch — Go-Live
7. `AGENT_BLUEPRINT.md`       ← Docs OS ⇄ Agent Runtime (stage-a/)
8. `power-bi-essential-concepts.md` ← BI ודשבורדים על נתוני ה-API
9. `N8N_AUTOMATION.md`        ← אוטומציה תפעולית על אירועי ה-API
10. `INVESTOR_RELATIONS.md`   ← roadmap
11. `CASES/*.md`

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
