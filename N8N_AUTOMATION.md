# N8N_AUTOMATION.md — שכבת האוטומציה התפעולית

**n8n כ-Glue Layer של ULease: מה-Outbox של ה-API ועד ל-CRM, ל-Slack ול-Power BI**

> [n8n](https://n8n.io/) היא פלטפורמת workflow automation בקוד-הוגן (fair-code): קנבס ויזואלי + קוד (JavaScript/Python)
> בכל צומת, 500+ אינטגרציות, AI-native (AI Agent nodes + MCP), וניתנת ל-self-hosting מלא.
> ב-ULease היא סוגרת את הפער בין **אירועי המערכת** (ה-Outbox של `leasing-api`) לבין **העולם העסקי**
> (סוכנויות, לקוחות, הנהלה) — בלי לכתוב microservice לכל התראה.

---

## 0. תוכן עניינים

1. [מה זה n8n ולמה עכשיו](#1-מה-זה-n8n-ולמה-עכשיו)
2. [מושגי יסוד](#2-מושגי-יסוד)
3. [Cloud מול Self-Hosted](#3-cloud-מול-self-hosted)
4. [חיבור ל-Leasing API](#4-חיבור-ל-leasing-api)
5. [קטלוג אירועים → Workflows](#5-קטלוג-אירועים--workflows)
6. [חמישה Workflows מוכנים ל-ULease](#6-חמישה-workflows-מוכנים-ל-ulease)
7. [AI Agents ב-n8n — היחס ל-AGENT_BLUEPRINT](#7-ai-agents-ב-n8n--היחס-ל-agent_blueprint)
8. [MCP — הגשר הדו-כיווני ל-Claude](#8-mcp--הגשר-הדו-כיווני-ל-claude)
9. [טופולוגיית פריסה](#9-טופולוגיית-פריסה)
10. [ממשל, אבטחה ו-Kill-Switch](#10-ממשל-אבטחה-ו-kill-switch)
11. [כלל בחירה: Skill · Workflow · Agent](#11-כלל-בחירה-skill--workflow--agent)

---

## 1. מה זה n8n ולמה עכשיו

| מאפיין | פירוט |
|--------|-------|
| **מודל** | Visual canvas של nodes; כל node הוא Trigger / Action / Logic; אפשר לכתוב JS/Python בכל נקודה |
| **רישוי** | Fair-code — Community Edition חינמית ל-self-hosting, ללא הגבלת workflows/executions |
| **אינטגרציות** | 500+ built-in (Slack, Gmail, Stripe, Postgres, WhatsApp, Google Sheets, HubSpot...) + HTTP Request לכל REST API |
| **AI** | AI Agent node (memory + tools + guardrails), תמיכה ב-Anthropic/OpenAI/Ollama, RAG, ו-MCP דו-כיווני |
| **n8n 2.0** | שכתוב 2025–2026: Task Runners (בידוד הרצת קוד), ביצועים, אבטחה |
| **תמחור Cloud** | Starter €24/חודש (2,500 executions) · Pro €60 (10,000) · Business €800 (40,000 + SSO) |

**למה ULease צריך את זה:** ה-API כבר פולט אירועים אמינים (Transactional Outbox + Relay).
מה שחסר זה הצד השני — מי *מגיב* לאירועים: מי שולח ווטסאפ לסוכן כשרכב נמכר, מי מרענן את
דשבורד ה-Power BI אחרי סליקה, מי מתריע כששריון פג. לכתוב worker ייעודי לכל תגובה כזו =
שבועות פיתוח. ב-n8n זה workflow של 20 דקות, עם audit מלא.

---

## 2. מושגי יסוד

| מושג | בשורה אחת | המקבילה אצלנו |
|------|-----------|----------------|
| **Workflow** | גרף של nodes שרץ מ-Trigger עד תוצאה | המקבילה הוויזואלית ל-`worker.ts` |
| **Trigger Node** | מה שמעיר את ה-workflow: Webhook, Schedule, Postgres Trigger, Stripe... | `outboxRelay` poller |
| **Action Node** | פעולה: שליחת מייל, INSERT ל-DB, קריאת API | `EventSink.publish` |
| **Expression** | `{{ $json.vin }}` — גישה לדאטה שזורם בין nodes | template strings |
| **Credentials** | סודות מוצפנים (API keys, DB) מנוהלים מחוץ ל-workflow | `config.ts` (zod, fail-fast) |
| **Execution** | ריצה אחת של workflow שלם (לא per-step כמו Zapier) | request lifecycle |
| **Error Workflow** | workflow ייעודי שרץ כשאחר נכשל | DLQ / retry logic |
| **Queue Mode** | main instance + N workers + Redis — סקיילינג אופקי | בדיוק הטופולוגיה של `api` + `worker` שלנו |

---

## 3. Cloud מול Self-Hosted

| | n8n Cloud | Self-Hosted (Community) |
|---|-----------|--------------------------|
| **עלות** | €24–800/חודש לפי executions | חינם; רק תשתית (VPS ~$10/חודש) |
| **תפעול** | אפס | Docker Compose, עדכונים, גיבויים |
| **דאטה** | עובר דרך שרתי n8n (EU) | נשאר אצלנו — ליד ה-Postgres |
| **SSO / Git sync** | Business ומעלה | בתשלום (Self-Hosted Business) |
| **AI nodes** | חינם בכל תוכנית (משלמים רק ל-LLM provider) | חינם |

**המלצה ל-ULease:** **Self-hosted** לצד ה-stack הקיים.

1. ה-`docker-compose.yml` של `leasing-api` כבר מריץ Postgres + api + worker — n8n מצטרף כשירות רביעי.
2. נתוני עסקאות, עמלות ולקוחות לא יוצאים מהתשתית (עיקרון החיסיון — ראה `AGENT_BLUEPRINT § 6`).
3. מודל ה-executions של Cloud מעניש אוטומציה event-driven אינטנסיבית; self-hosted אין מגבלה.
4. Pilot מהיר אפשר להתחיל ב-Cloud Starter ולהגר — workflows מיוצאים כ-JSON.

---

## 4. חיבור ל-Leasing API

שלושה ערוצי חיבור, מהקל לכבד:

### 4.1 יוצא: n8n → API (HTTP Request + HMAC)

ה-API מאומת ב-HMAC (`X-Signature` = HMAC-SHA256 על `${timestamp}.${rawBody}`, ראה `src/middleware/hmacAuth.ts`).
ב-n8n: **Code node** שמחשב את החתימה → **HTTP Request node** שקורא ל-endpoint.

```javascript
// n8n Code node — לפני ה-HTTP Request
const crypto = require('crypto');
const body = JSON.stringify($json.payload);
const timestamp = Date.now().toString();
const signature = crypto
  .createHmac('sha256', $env.ULEASE_HMAC_SECRET)
  .update(`${timestamp}.`)
  .update(Buffer.from(body))
  .digest('hex');

return [{ json: { body, headers: { 'X-Signature': signature, 'X-Timestamp': timestamp } } }];
```

| Endpoint | שימוש מ-n8n |
|----------|--------------|
| `POST /v1/deal-score` | ניקוד ליד שנכנס מטופס אתר/פייסבוק |
| `POST /v1/inventory/:vin/reserve` | שריון אוטומטי אחרי אישור לקוח (עם `Idempotency-Key`!) |
| `GET /v1/catalog?status=AVAILABLE` | פיד יומי לערוצי שיווק |
| `POST /v1/deals/:dealId/settle` | סליקה כחלק מ-workflow אישור עסקה |

### 4.2 נכנס: Outbox → n8n (הערוץ המרכזי)

ל-`EventSink` (כיום `InMemoryEventSink`, "production wires Kafka/PubSub here" — `src/events/sink.ts`) מתווסף
יעד שלישי, הפשוט מכולם: **`WebhookEventSink`** שעושה POST לכתובת ה-Webhook Trigger של n8n.

```
outbox (Postgres) → outboxRelay → WebhookEventSink → POST https://n8n.ulease.internal/webhook/outbox
                                                          │
                                                          ▼
                                            n8n Switch node לפי event.type
                                            ├─ vehicle.sold        → Workflow W1
                                            ├─ deal.settled        → Workflow W2
                                            ├─ vehicle.reservation_released → Workflow W3
                                            └─ default             → Log only
```

at-least-once נשמר: ה-Relay כבר עובד עם `SKIP LOCKED` ו-retry; ה-workflows ב-n8n חייבים להיות
**אידמפוטנטיים** (בדיקת `event_id` מול טבלת `processed_events` ב-Postgres node) — אותו חוזה שכבר
מוטל על `vehicleProjection.ts`.

### 4.3 חלופה ללא שינוי קוד: Postgres Trigger node

אם לא רוצים לגעת בקוד ה-API בכלל: n8n Postgres Trigger node מאזין ל-INSERT על טבלת `outbox`
(או על `vehicle_read_model`). דורש הרשאת `TRIGGER` על הסכמה — מתאים ל-pilot, פחות לפרודקשן
(עוקף את ה-Relay ואת סמנטיקת ה-at-least-once שלו).

### 4.4 Stripe

n8n **Stripe Trigger node** מאזין ישירות לאירועי Stripe (`payout.paid`, `charge.refunded`...) —
משלים את `POST /webhooks/stripe` הקיים: ה-API מטפל בהתאמה החשבונאית, n8n מטפל בהתראות ובדוחות.

---

## 5. קטלוג אירועים → Workflows

כל אירוע שה-API פולט (ראה `src/inventory/repository.ts`, `src/commission/settlementService.ts`) ומה עושים איתו:

| Event type | Payload | תגובה אוטומטית ב-n8n |
|------------|---------|------------------------|
| `vehicle.added` | `vin, listPrice, offerPrice` | פרסום לערוצי שיווק, עדכון פיד קטלוג |
| `vehicle.reserved` | `vin, actor, reservedUntil` | אישור ללקוח (מייל/SMS) + תזכורת לסוכן + timer לקראת פקיעה |
| `vehicle.sold` | `vin, actor` | 🎉 חבילת מכירה: חשבונית, ברכה ללקוח, עדכון CRM, Slack להנהלה |
| `vehicle.reservation_released` | `vin, actor, reason` | החזרה לקטלוג, הודעה לרשימת המתנה, ניתוח סיבת נטישה |
| `deal.settled` | פירוט עמלות וחלוקה | דוח סליקה לסוכנות, רענון Power BI, רישום ב-ERP |

---

## 6. חמישה Workflows מוכנים ל-ULease

### W1 · רכב נמכר — חבילת Post-Sale
**Trigger:** Webhook (`vehicle.sold`) →
**Steps:** שליפת פרטי רכב מ-`/v1/inventory/:vin` → יצירת חשבונית (Stripe/iCount) → מייל ללקוח →
WhatsApp לסוכן → הודעת Slack `#sales` → רישום ב-CRM.
**ROI:** חוסך ~20 דקות עבודה ידנית לכל מכירה.

### W2 · עסקה נסלקה — דוח וסנכרון
**Trigger:** Webhook (`deal.settled`) →
**Steps:** שליפת `ledger_entries` (Postgres node) → בניית דוח עמלות → מייל לסוכנות →
טריגר רענון Power BI dataset (REST API) → אם עמלה > סף: התראת הנהלה.
**קשר:** סוגר את הלולאה עם `power-bi-essential-concepts.md § 9` (Scheduled Refresh → רענון מבוסס-אירוע).

### W3 · שריון פג — Recovery
**Trigger:** Webhook (`vehicle.reservation_released` כאשר `reason != 'released'`) →
**Steps:** Router לפי סיבה → אם פקיעה: מייל "הרכב עדיין כאן" ללקוח + הצעת ניקוד מחדש (`/v1/deal-score`) →
הודעה לרשימת המתנה על הרכב שהשתחרר.
**ROI:** הופך נטישה לערוץ remarketing.

### W4 · דייג'סט יומי — קטלוג ומלאי
**Trigger:** Schedule (כל יום 07:00) →
**Steps:** `GET /v1/catalog?status=AVAILABLE` → Code node לפורמט → פרסום לערוצים (טלגרם/וואטסאפ קבוצות סוכנים) →
שורת סיכום ל-Slack הנהלה (כמה זמין/שמור/נמכר אתמול).

### W5 · ליד נכנס — Score & Route
**Trigger:** Webhook מטופס אתר / Facebook Lead Ads →
**Steps:** ולידציה (Code node) → `POST /v1/deal-score` (עם HMAC) → **Switch node** לפי score:
- ≥ 80 ("חם") → התראה מיידית לסוכן + יצירת משימה ב-CRM
- 50–79 → רצף nurturing במייל
- < 50 → מאגר remarketing

**זה Router pattern (#5 מ-`AGENT_BLUEPRINT § 9.1`) — ממומש ב-n8n בלי שורת קוד.**

---

## 7. AI Agents ב-n8n — היחס ל-AGENT_BLUEPRINT

n8n כוללת **AI Agent node**: LLM (Anthropic Claude) + Memory + Tools על אותו קנבס.
זה מציב שאלה דוקטרינרית: מתי agent ב-n8n ומתי `stage-a`?

### 7.1 מיפוי ל-9 ה-patterns (`AGENT_BLUEPRINT § 9.1`)

| Pattern | מימוש ב-n8n | מתאים? |
|---------|-------------|--------|
| Chaining (1) | שרשרת nodes — זה כל הרעיון של n8n | ✅ מצוין |
| Parallelization (2) | פיצול branches + Merge node | ✅ מצוין |
| Router (5) | Switch node / Text Classifier node | ✅ מצוין |
| Evaluator (4) | Loop של Generator→IF→חזרה | ⚠️ אפשרי, מסורבל |
| Orchestrator-Worker (3) | AI Agent + Sub-workflow Tools | ⚠️ חלקי |
| Reflexion (7) / ReWOO (8) / Plan&Execute (9) | דורש state ו-replan דינמי | ❌ לא הכלי |

### 7.2 חלוקת העבודה

> **n8n = ה-Hands. `stage-a` = ה-Brain.**

- **n8n מצטיין ב-patterns דטרמיניסטיים** (1, 2, 5): אירוע נכנס → תגובה ידועה. בלי LLM בכלל, או עם
  LLM כצומת בודד (סיכום, סיווג, ניסוח מייל).
- **`stage-a` (Plan & Execute) נשאר הבית של reasoning רב-שלבי**: ממשל אכוף בקוד, `evidence[]` חובה,
  step ceiling, append-only memory. ל-n8n אין את שכבת ה-evals וה-governance של `AGENT_BLUEPRINT § 5–6`.
- **השילוב:** workflow ב-n8n יכול לקרוא ל-`stage-a` (Execute Command / HTTP) כשנדרש reasoning,
  ו-`stage-a` יכול להפעיל workflows ב-n8n כ-tools דרך MCP (ראה § 8). כל שכבה עושה את מה שהיא טובה בו.

### 7.3 אנטומיה של AI Agent על הקנבס — דוגמה חיה

כך נראה Tools Agent ב-n8n בפועל (מבוסס על ה-workflow הרשמי של n8n לקליטת משתמש חדש):

```
⚡ On 'Create User'          ┌──────────────────────┐         ┌─────────────┐    true   Slack:
   form submission  ───────► │      AI Agent        │ ──────► │ Is manager? │ ───────►  Add to channel
                             │     (Tools Agent)    │         └─────────────┘
                             └──┬───────┬───────┬───┘                │ false     Slack:
                                ┆       ┆       ┆                    └────────►  Update profile
                          Chat Model  Memory   Tools
                                ┆       ┆       ┆
                         ┌──────┴─┐ ┌───┴────┐ ┌┴──────────────┬─────────────┐
                         │Anthropic│ │Postgres│ │Microsoft Entra│    Jira     │
                         │  Claude │ │  Chat  │ │ID (getAll:user)│(create:user)│
                         └─────────┘ │ Memory │ └───────────────┴─────────────┘
                                     └────────┘
```

ארבעת אבני הבניין של כל AI Agent ב-n8n:

| רכיב | בתרשים | התפקיד |
|------|---------|--------|
| **Trigger** | Form submission | האירוע שמעיר את הסוכן — אצלנו: Webhook מה-Outbox או טופס ליד |
| **Chat Model** | Anthropic Claude | המוח — מקבל את הקלט ומחליט אילו tools להפעיל ובאיזה סדר |
| **Memory** | Postgres Chat Memory | הקשר בין הרצות — נשמר באותו Postgres של ה-stack |
| **Tools** | Entra ID + Jira | הידיים — הסוכן קורא להם *לפי שיקול דעתו*, לא לפי סדר קבוע |

אחרי הסוכן: **Switch node** (`Is manager?`) מפצל לשני ענפי Slack — כלומר הסוכן עושה את החלק
ה"חכם", וההמשך חוזר להיות דטרמיניסטי. **זה בדיוק העיקרון מ-§ 7.2** — LLM רק איפה שצריך שיקול דעת.

**ההתאמה ל-ULease — קליטת סוכנות חדשה (Dealer Onboarding):**

| בתרשים המקורי | בגרסת ULease |
|----------------|---------------|
| On 'Create User' form | טופס "הצטרפות סוכנות" באתר |
| Anthropic Chat Model | Claude (אותו דבר) |
| Postgres Chat Memory | אותו Postgres של `leasing-api`, schema `n8n` |
| Tool: Microsoft Entra ID | Tool: `GET /v1/catalog` — שליפת מלאי רלוונטי לאזור הסוכנות |
| Tool: Jira (create user) | Tool: CRM — יצירת רשומת סוכנות + Commission Plan |
| Is manager? | Is fleet dealer? (סוכנות ציי רכב או פרטית?) |
| Slack: Add to channel | Slack: צירוף ל-`#dealers-fleet` + הודעת ברכה |
| Slack: Update profile | Slack: צירוף ל-`#dealers-retail` + שליחת ערכת onboarding |


---

## 8. MCP — הגשר הדו-כיווני ל-Claude

n8n תומכת ב-Model Context Protocol **בשני הכיוונים** — וזה מה שמחבר אותה ל-`DEV_ENVIRONMENTS.md` (שכבת ה-MCP):

### 8.1 n8n כ-MCP Server (Claude קורא ל-n8n)

**MCP Server Trigger node** חושף workflows כ-tools לכל MCP client — Claude Desktop, Claude Code, Cursor.

```jsonc
// claude_desktop_config.json / .mcp.json בפרויקט
{
  "mcpServers": {
    "ulease-automations": {
      "url": "https://n8n.ulease.internal/mcp/ulease",
      "headers": { "Authorization": "Bearer ${N8N_MCP_TOKEN}" }
    }
  }
}
```

ואז בשיחת Claude: *"שלח דוח מלאי לסוכנות X"* → Claude קורא ל-tool `send-inventory-report` שהוא
בעצם workflow W4 — עם כל ה-credentials מאוחסנים ב-n8n, לא אצל Claude.

### 8.2 n8n כ-MCP Client (n8n קורא ל-Claude tools)

**MCP Client Tool node** בתוך AI Agent node — סוכן שרץ ב-n8n יכול לצרוך MCP servers חיצוניים
(למשל ה-MCP servers שהוגדרו ב-`DEV_ENVIRONMENTS § MCP`).

### 8.3 התמונה המלאה

```
Claude Code / Desktop ──(MCP client)──► n8n MCP Server Trigger ──► Workflows W1–W5 ──► Leasing API
        ▲                                                                                  │
        └───────────────────────── Outbox events ◄────────────────────────────────────────┘
```

הסוכן מדבר, n8n מבצעת, ה-API שומר על האמת. **שלוש שכבות, אחריות אחת לכל שכבה.**

### 8.4 MCP ≠ Skill — מה ה-MCP הזה כן ומה הוא לא

ה-MCP בסעיף הזה הוא שכבת ה-**חיבור** בלבד (Connect), לא שכבת ה-**workflow** (Learn).
ההבחנה המלאה ב-`AGENT_BLUEPRINT § 11`, וכאן בקצרה כי קל לבלבל:

| | 🟢 MCP (מה שיש כאן) | 🔵 Agent Skill |
|---|---------------------|------------------|
| **התפקיד** | חושף את workflows W1–W5 כ-tools; מחבר ל-DB/Stripe/Slack | מלמד *מתי* ובאיזה סדר לקרוא להם, באיזה פורמט, לפי איזה policy |
| **מודל מנטלי** | AI-native API — מערכת העצבים | AI-native SOP — ספר הנהלים |
| **אצלנו** | `MCP Server Trigger` (§ 8.1) + ה-Webhook/Postgres nodes | פקודות `COMMAND_API` שמתזמרות את הקריאות |

**המסקנה התפעולית:** חשיפת workflow כ-MCP tool **לא** מייתרת Skill. ה-tool נותן ל-Claude
את הידיים (`send-inventory-report`); ה-Skill נותן לו את הנוהל (למי, מתי, עם איזה אישור).
שניהם נדרשים — ראה כלל הבחירה ב-§ 11.

---

## 9. טופולוגיית פריסה

הרחבת ה-`docker-compose.yml` הקיים של `leasing-api` (Postgres + api + worker):

```yaml
  n8n:
    image: docker.n8n.io/n8nio/n8n
    environment:
      DB_TYPE: postgresdb
      DB_POSTGRESDB_HOST: db                # אותו Postgres, schema נפרד: n8n
      DB_POSTGRESDB_DATABASE: n8n
      N8N_ENCRYPTION_KEY: ${N8N_ENCRYPTION_KEY}   # חובה! מצפין credentials
      WEBHOOK_URL: https://n8n.ulease.internal/
      GENERIC_TIMEZONE: Asia/Jerusalem
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      db:
        condition: service_healthy
```

| שלב | טופולוגיה |
|-----|-----------|
| **Pilot (עכשיו)** | קונטיינר n8n יחיד, SQLite פנימי או schema ב-Postgres הקיים |
| **Production (Month 1)** | n8n + Postgres schema נפרד + `N8N_ENCRYPTION_KEY` ב-secrets + HTTPS מאחורי reverse proxy |
| **Scale (Quarter 1)** | Queue mode: main + webhook processors + N workers + Redis — אותו מודל בדיוק כמו `api`/`worker` שלנו |

---

## 10. ממשל, אבטחה ו-Kill-Switch

עקרונות `AGENT_BLUEPRINT § 6` חלים גם כאן — אוטומציה בלי ממשל היא סיכון, לא נכס:

| עיקרון | מימוש ב-n8n |
|--------|--------------|
| **Human-in-command** | n8n Wait/Approval nodes — כל פעולה כספית (settle, refund) עוצרת לאישור אנושי בסלאק/מייל |
| **שקיפות** | Execution log מלא לכל ריצה (input/output של כל node) — ה-audit trail המקביל ל-shared memory של stage-a |
| **חיסיון** | Self-hosted; credentials מוצפנים ב-`N8N_ENCRYPTION_KEY`; ה-LLM היחיד שרואה דאטה הוא Claude דרך API מאובטח |
| **עצירה בטוחה** | Error Workflow ייעודי: כל כשל → Slack `#claude-os` + השבתת ה-workflow האוטומטית אחרי N כשלים |
| **Kill-Switch** | `LAUNCH § 8`: השבתת כל ה-workflows = כיבוי קונטיינר אחד (או Deactivate All ב-UI). ה-API ממשיך לעבוד — n8n היא שכבה נתיקה |

**כלל ברזל:** n8n לעולם לא כותבת ישירות לטבלאות הליבה (`vehicles`, `settlements`, `ledger_entries`).
כל שינוי state עובר דרך ה-API עם HMAC. קריאה (SELECT) — מותרת. כתיבה — רק דרך החוזה.

---

## 11. כלל בחירה: Skill · Workflow · Agent

הרחבת כלל הבחירה מ-`AGENT_BLUEPRINT § 9.5`:

```
המשימה היא שיחה/ניתוח חד-פעמי?            → Skill (COMMAND_API)
המשימה היא תגובה קבועה לאירוע מערכת?       → n8n Workflow
המשימה היא תגובה לאירוע + שיקול דעת קל?    → n8n Workflow + צומת LLM בודד
המשימה דורשת תכנון, איטרציה, evidence?      → stage-a Agent (Plan & Execute)
המשימה דורשת גם וגם?                       → stage-a Agent שקורא ל-n8n Workflows דרך MCP
```

**הכלל הראשון נשאר:** הכלי הפשוט ביותר שעושה את העבודה. רוב התפעול השוטף של ULease —
התראות, דוחות, סנכרונים — הוא n8n Workflows, לא agents.

---

## גרסאות

| גרסה | תאריך | שינוי |
|------|--------|-------|
| 1.0.0 | 2026-06-02 | Initial — מושגי יסוד, חיבור ל-Leasing API (HMAC + Outbox→Webhook), קטלוג אירועים, 5 workflows, מיפוי ל-AGENT_BLUEPRINT § 9, MCP דו-כיווני, טופולוגיית פריסה, ממשל |
| 1.1.0 | 2026-06-02 | + § 7.3 אנטומיה של AI Agent על הקנבס — פירוק ה-workflow הרשמי (Form → Tools Agent → Switch → Slack) והתאמתו ל-Dealer Onboarding של ULease |
| 1.2.0 | 2026-06-05 | + § 8.4 MCP ≠ Skill — הבהרה שה-MCP כאן הוא שכבת חיבור (Connect) בלבד; חשיפת workflow כ-tool לא מייתרת Skill. מצביע ל-`AGENT_BLUEPRINT § 11` |

---

*מקורות: [n8n.io](https://n8n.io/) · [docs.n8n.io](https://docs.n8n.io/) — Webhook, Postgres Trigger, Stripe, MCP Server Trigger, Queue Mode.*
