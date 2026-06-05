# AI SDLC Orchestration — מ-"כלים" ל-"תזמור כוונה"

**מפת כלי ה-AI על פני מחזור חיי הפיתוח (SDLC) — ולמה ULease לא אוסף כלים אלא בונה שכבת-תזמור אחת.**

> הטענה המרכזית (Ashish Sahu / השיח התעשייתי 2026): כלי ה-AI **לא** משנים את ה-SDLC באופן אחיד — הם **מפצלים אותו לכיסי-אינטליגנציה** שכמעט לא מתחברים. רוב הצוותים חושבים שהם בונים *"AI-enabled delivery"*; בפועל הם מרכיבים שכבות קוגניטיביות מנותקות. **השינוי האמיתי אינו הכלים — הוא תזמור הכוונה (orchestration of intent) על-פני המערכות.** המודול הזה לוקח את מפת הכלים, מצליב אותה מול הסטאק של ULease, ומראה היכן ה-event backbone + `stage-a` + n8n כבר מהווים את שכבת-התזמור הזו.

---

## 1. מפת ה-SDLC במבט-על — 6 השלבים

האינפוגרפיקה מחלקת את ה-SDLC ל-6 שלבים, כל אחד עם "כיס אינטליגנציה" משלו:

| שלב | כלי AI מייצגים (מהמפה) | הכאב | הזדמנות התזמור |
|-----|------------------------|------|----------------|
| 🔵 **Requirement Gathering & Analysis** | ChatGPT Enterprise (PRD), Claude Projects (long-context), ClickUp AI (meeting→task), Otter AI, Notion AI | דרישות חיות ב-5 כלים שונים | מקור-אמת אחד ל-intent (spec) |
| 🔴 **UI / UX Design** | Figma AI, Galileo AI, Uizard, Framer AI, Locofy (design→code) | מעצב ⇄ קוד = תרגום ידני | design-to-code אוטומטי |
| 🔵 **Coding & Development** | Cursor AI, GitHub Copilot X, Codeium, CodeWhisperer, Gemini Code | suggestion ≠ execution | context-aware IDE על קוד אמיתי |
| 🟣 **Quality & Testing** | Testim, Functionize, Applitools, Mabl, LambdaTest | טסטים שבירים | continuous verification |
| 🔴 **Project Planning** | Jira AI, Linear AI, Asana Intelligence, Monday AI, Motion AI | תכנון ידני, לא צפוי | workload balancing מבוסס-AI |
| 🟠 **Monitoring & Maintenance** | Datadog AI, Dynatrace, New Relic, Sentry AI, BigPanda | התראות מנותקות | system-wide reasoning על incidents |

> **הדפוס:** כל שלב הופך לאינטליגנטי **בבידוד**. מעט מאוד מערכות אינטליגנטיות **end-to-end**. הפער הזה — בין כיסים נבונים למערכת נבונה — הוא היתרון התפעולי של 2026.

---

## 2. מ-6 השלבים אל הקוד — מיפוי ל-ULease

ULease אינו "צרכן כלים" — הוא **המערכת שמתוזמרת**. הטבלה מצליבה כל שלב מול הראיה בקוד של `leasing-api` ומול מודול ה-OS שמכסה אותו.

| שלב SDLC | מימוש/Seam ב-ULease | מודול OS אחראי | סטטוס |
|----------|---------------------|----------------|--------|
| Requirement Gathering | `docs/specs/*.md` (spec לפני קוד: `deal-score-engine.md`, `commission-and-settlement.md`…) | `system-design-cheatsheet § 1` · Working Rules #1 PLAN FIRST | ✅ |
| UI / UX | Demo storefront + ops dashboard ב-`public/` (`/ui`, CSP נפרד ב-`server.ts`) | שכבה נפרדת מה-API | 🟡 demo |
| Coding & Development | Claude Code CLI + MCP על הריפו; `tsx`, `typecheck` (tsc) | `DEV_ENVIRONMENTS.md` · `AGENT_BLUEPRINT § 10` | ✅ |
| Quality & Testing | `vitest` — **63/63 ✅** ב-14 קבצים (api/inventory/settlement/commission/decisionEngine/projection/biViews/**tenancy**) | `BACKEND_ROADMAP § Testing` · Working Rules #6 VERIFY | ✅ |
| Project Planning | `LAUNCH.md` playbook (Day 0→Quarter 1, RACI) · `COMMAND_API` slash commands | `LAUNCH.md` · `COMMAND_API.md` | ✅ |
| Monitoring & Maintenance | `/health` (liveness) · `/ready` (DB check→503) · `logger.ts` structured logs · `sweeperRunner` (self-healing reservations) | `system-design-cheatsheet § 6-7` · `N8N_AUTOMATION` (alerting) | 🟡 חלקי |

> **הקריאה:** ULease חזק ב-Requirements (spec-first), Coding, ו-Testing; שכבת ה-UI היא demo; ה-Monitoring קיים כ-seams (health/ready/logs) אך עדיין ללא APM מלא (חוב מתועד — ראה `CTO_REVIEW` P-Ops).

---

## 3. שכבת-התזמור של ULease — Brain · Hands · Backbone

כאן ULease עונה על הטענה המרכזית. **התזמור אינו עוד כלי — הוא שלוש שכבות מחוברות** שכבר חיות בקוד:

```
        INTENT (spec / slash-command / event)
                       │
        ┌──────────────┴───────────────────────────────┐
        │  BRAIN — stage-a (Plan & Execute agent)       │  AGENT_BLUEPRINT § 9.3
        │  decision-making, orchestration topology      │
        └──────────────┬───────────────────────────────┘
                       │ decisions
        ┌──────────────┴───────────────────────────────┐
        │  BACKBONE — Transactional Outbox + Relay      │  src/events/outbox.ts
        │  + EventSink (Kafka/PubSub seam)              │  outboxRelay.ts · sink.ts
        │  אפס אובדן אירועים · at-least-once · ordered   │
        └──────────────┬───────────────────────────────┘
                       │ events
        ┌──────────────┴───────────────────────────────┐
        │  HANDS — n8n workflows (Glue Layer)           │  N8N_AUTOMATION.md
        │  Post-Sale · Settlement · Recovery · Digest   │
        └───────────────────────────────────────────────┘
```

- **Brain (`stage-a`)** — agent מסוג Plan & Execute; קובע *מה* לעשות (`AGENT_BLUEPRINT § 9.3`).
- **Backbone (Outbox+Relay+Sink)** — ה-event backbone שמחבר את הכיסים: כל decision שמשנה state כותב ל-`outbox` **באותה טרנזקציה** (אפס אובדן), וה-`OutboxRelay` מפרסם ב-`ORDER BY occurred_at, version` עם `FOR UPDATE SKIP LOCKED`. ה-`EventSink` הוא נקודת-ההחלפה ל-Kafka/PubSub.
- **Hands (n8n)** — מתרגם אירועים לפעולות עסקיות (`N8N_AUTOMATION § 7`).

> זה בדיוק ה-*"connecting their decision logic"* מהטענה המרכזית: לא עוד כלי ל-monitoring או ל-planning, אלא **decision-logic אחד שזורם דרך backbone אחד**. ה-`EventSink` הוא הסיבה ש-ULease הוא end-to-end ולא 6 כיסים מנותקים.

---

## 4. אנטומיית ה-Enterprise AI Agent — 8 השכבות (M-SoftTech) ⇄ ULease

הפוסט השני מפרק *enterprise AI agent* ל-8 שכבות, עם האזהרה: **"agent קורס תחת עומס אמיתי כי שכבה אחת הוזנחה"**. כל שכבה מוצלבת מול ה-seam המקביל ב-ULease.

| # | שכבה (מהפוסט) | העיקרון | המקביל ב-ULease |
|---|---------------|---------|-----------------|
| 1 | **Task Entry & Microservices Gate** | משימות נכנסות דרך APIs מאובטחים; חוסם flood; ה-core מוגן | `src/routes/api.ts` (`/v1`) + `hmacAuth` (HMAC-SHA256 + replay guard) + `zod` validation → 400/401 |
| 2 | **AI Agent Core Loop** | מחזור מנוהל, לא prompt בודד; controller על lifecycle+state; cache | `stage-a` core loop · `AGENT_BLUEPRINT § 9.3` (Plan & Execute) |
| 3 | **Context-Aware Task Breakdown** | מנתח state/history/tools/cache לפני פעולה; מונע loops | Working Rules #1 PLAN FIRST · `AGENT_BLUEPRINT § 10` (plan mode) |
| 4 | **MCP Tools Execution Layer** | agents עוברים דרך MCP server בלבד; interfaces סטנדרטיים, retries | `AGENT_BLUEPRINT § 11` (MCP=Connect) · `DEV_ENVIRONMENTS § 10` · `N8N § 8` |
| 5 | **Response with Confidence Guardrails** | generate→score confidence→retry; אין failures שקטים | `scoring/decisionEngine.ts` — normalized weights, abstain=null, `Decision.score` 0..100 |
| 6 | **Specialized LLM Routing** | route לפי task: domain/external/local-privacy | `AGENT_BLUEPRINT § 9` Router pattern (#5) · model selection ב-`DEV_ENV` |
| 7 | **External Data Isolation** | משימות web רצות בנפרד, מוזנות דרך MCP; core נשאר טהור | RLS tenant isolation (`rls.sql`, fail-closed) · `setTenantContext` · `EventSink` decoupling |
| 8 | **MVP Reality Check** | אל תדלג על logging, human oversight, data pipelines | `logger.ts` · kill-switch (`LAUNCH`/`N8N § ממשל`) · 63/63 tests · `bi_views.sql` |

> **המסר המאוחד:** *"AI agents are distributed control systems. Miss the layers, face chaos."* — ULease בנוי בדיוק כך: gate (#1) → core (#2) → backbone → tools (#4) → guardrails (#5). השכבה שהכי קל "להזניח" — #8 (logging/oversight/tests) — היא בדיוק ה-Working Rule #6 VERIFY ו-#7 NO LAZINESS שאוכפים ב-`CLAUDE.md`.

---

## 5. שני חובות פתוחים (כנה)

בהמשך לדוקטרינת `CTO_REVIEW.md` — מה שעדיין **לא** end-to-end:

1. **Observability מלא (#8 / Monitoring)** — קיימים `/health`, `/ready`, ו-structured `logger`, אך **אין APM/anomaly-detection** (Datadog/Sentry מהמפה). חוב P-Ops.
2. **LLM Routing חי (#6)** — ה-Router pattern מתועד ב-`AGENT_BLUEPRINT § 9` אך טרם מיושם כ-runtime ב-`stage-a`. חוב Stage-B.

> שאר ה-backbone (Outbox/Relay/Sink), ה-gate (hmacAuth/zod), וה-guardrails (decisionEngine) — **קיימים ומאומתים (63/63)**.

---

*תומלל מ-"AI Tool Map for the Software Development Lifecycle" (Ashish Sahu) ומ-"Enterprise AI Agent Architecture" (M-SoftTech), ומופה ל-codebase של `leasing-api` בהמשך ל-`AGENT_BLUEPRINT.md` ו-`CTO_REVIEW.md`.*
