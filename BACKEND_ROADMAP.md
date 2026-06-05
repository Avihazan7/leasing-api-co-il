# BACKEND_ROADMAP.md — Backend Developer Roadmap ⇄ ULease

**גרסה:** v1.0.0
**מקור:** "The Complete Backend Developer Roadmap" (Shishir Pant) — אינפוגרפיקה פופולרית של מסלול ההתפתחות למפתח Backend.
**מטרת המודול:** לא עוד roadmap גנרי. כאן אנחנו לוקחים את 6 שלבי המסלול ו**מצליבים כל אחד מהם מול ראיה בקוד** ב-`leasing-api` ומול המודולים הקיימים ב-OS — איפה ULease כבר חזקה, איפה הכיסוי חלקי (seam מוכן), ואיפה יש **חוב פתוח מתועד**. בהמשך ישיר ל-[`CTO_REVIEW.md`](./CTO_REVIEW.md) ו-[`system-design-cheatsheet.md`](./system-design-cheatsheet.md).

> **התזה של הפוסט:** "ה-tech stack ישתנה. היסודות לא." ULease היא ההוכחה: מערכת קטנה אחת (Express + Postgres + worker) שכבר נוגעת בכל שלב במסלול — חלקם בשלות מלאה, חלקם כ-seam מתוכנן.

---

## 0. מפה מהירה — 6 השלבים בעין ULease

| שלב | מהות | סטטוס ב-ULease | ראיה מרכזית |
|-----|------|----------------|-------------|
| 🟢 **Foundations** | Programming · DS&A · Git/GitHub | ✅ STRONG | `AGENT_BLUEPRINT.md §10` · `tsconfig.json` (strict) · `stateMachine.ts` · `.github/workflows/ci.yml` |
| 🔵 **Backend Core** | HTTP/S · REST · AuthN · AuthZ | ✅ STRONG (AuthZ = חוב) | `src/routes/api.ts` · `src/middleware/hmacAuth.ts` · `helmet`/`cors`/`zod` |
| 🟣 **Databases** | SQL · NoSQL · DB Design · Migrations | ✅ STRONG | `src/db/schema.sql` · `src/db/migrate.ts` · `src/db/bi_views.sql` |
| 🟠 **Performance** | Caching · Redis · Jobs · Queues · Rate-limit | 🟡 PARTIAL | `src/events/outbox.ts` · `src/events/sink.ts` · `src/inventory/sweeperRunner.ts` |
| 🔴 **Cloud & Deploy** | Docker · CI/CD · Cloud | ✅ STRONG | `Dockerfile` · `docker-compose.yml` · `vercel.json` · health checks |
| ⭐ **Advanced Eng** | Monitoring · Logging · System Design · Scale · Microservices | ✅ STRONG (+roadmap) | `system-design-cheatsheet.md` · `CTO_REVIEW.md` P0–P7 · domain modules |

**ספירת אמת:** 55/55 טסטים (`vitest run`, 12 קבצי טסט), build ✅, typecheck ✅ — נכון ל-v1.2.

---

## 🟢 1. Foundations — Programming · Data Structures & Algorithms · Git/GitHub

**מה השלב:** משמעת הנדסית בסיסית. הכול נשען על זה.

**איפה ULease מכסה:**
- **Programming fundamentals + Typing:** כל הקוד TypeScript עם `strict` (`tsconfig.json`). `npm run typecheck` ב-CI.
- **Data Structures & Algorithms (יישומי, לא לראיונות):** מכונת מצבים סופית למחזור חיי רכב — `src/inventory/stateMachine.ts` (`DRAFT → AVAILABLE → RESERVED → SOLD`), עם טבלת מעברים מפורשת שאוסרת מעברים לא-חוקיים. Optimistic locking דרך עמודת `version` (MVCC) ב-`schema.sql`.
- **Git & GitHub:** שני הריפו ב-Git; pipeline מלא ב-`.github/workflows/ci.yml` (checkout → node 22 → `npm ci` → typecheck → test).
- **משמעת תהליך (מעבר לקוד):** [`AGENT_BLUEPRINT.md` §10](./AGENT_BLUEPRINT.md) — דוקטרינת ה-Working Rules (Karpathy): PLAN FIRST · GOAL-DRIVEN · VERIFY · NO LAZINESS. זה ה-"Foundations" של *איך עובדים*, לא רק *מה כותבים*.

**סטטוס: ✅ STRONG.**

---

## 🔵 2. Backend Core — HTTP/HTTPS · REST APIs · Authentication · Authorization

**מה השלב:** הליבה — איך לקוח מדבר עם שרת ואיך מאבטחים את זה.

**איפה ULease מכסה:**
- **REST API:** `src/routes/api.ts` — 8 endpoints (`POST /v1/deal-score`, `POST /v1/vehicles`, `GET /v1/inventory/:vin`, reserve/confirm/release, `POST /v1/deals/:dealId/settle`, `GET /v1/catalog`). מפת ה-endpoints מלאה ב-README של `leasing-api`.
- **HTTP/HTTPS hygiene:** `helmet()` ל-security headers, `cors()`, ו-`GET /health` (liveness) + `GET /ready` (readiness, בודק DB) ב-`src/server.ts`.
- **Authentication:** `src/middleware/hmacAuth.ts` — `X-Signature = HMAC-SHA256(\`${timestamp}.${rawBody}\`, secret)`, השוואה timing-safe (`timingSafeEqual`), הגנת replay דרך `X-Timestamp` עם סבילות ±5 דקות. (אם `HMAC_SECRET` לא מוגדר → no-op ל-dev מקומי.)
- **Input validation:** סכמות Zod ב-`src/schemas.ts`, אכיפה דרך `parseBody()` בכל handler.

**חוב פתוח — Authorization:**
> **RLS בצד ה-DB** עדיין לא נאכף בסכמה הפורטבילית — כיום ה-RLS קיים רק בשכבת ה-BI/Power BI (`dealer_account` filter), לא ב-Postgres. ראה [`CTO_REVIEW.md` §1](./CTO_REVIEW.md) (P0) ו-[`system-design-cheatsheet.md`](./system-design-cheatsheet.md) (מושג #9, מסומן ⚠️).

**סטטוס: ✅ STRONG** ל-AuthN ול-API; 🟡 **AuthZ ברמת ה-DB = חוב P0**.

---

## 🟣 3. Databases — SQL · NoSQL · Database Design · Migrations & Seeding

**מה השלב:** אחסון, ארגון וניהול נתונים ביעילות.

**איפה ULease מכסה:**
- **SQL Schema (פורטבילי):** `src/db/schema.sql` — `vehicles` (VIN כ-PK, סטטוס=state machine, מחירים כ-`NUMERIC` בלי float, `version` ל-optimistic locking, TTL לשמירת רכב).
- **Database Design מתקדם:**
  - **Transactional Outbox** — כתיבת אירוע באותה טרנזקציה כמו שינוי המצב (אין dual-write). אינדקס `(occurred_at) WHERE published_at IS NULL` לסריקת relay יעילה.
  - **Append-only ledger** — `ledger_entries` שומר-כסף; כסף ב-`amount_minor` (BIGINT, יחידות מינור, בלי float drift). אינווריאנט: סכום כל הרשומות = סכום העסקה.
  - **Idempotency keys** — מניעת כפילויות ברמת בקשה.
  - **CQRS read model** — `vehicle_read_model`, projection מנורמל-לאחור עם `last_version` ל-dedup.
- **Migrations & Seeding:** `src/db/migrate.ts` — runner אידמפוטנטי (`IF NOT EXISTS`), רץ ב-bootstrap בכל boot.
- **DB abstraction (NoSQL-ready seam):** `src/db/client.ts` — interface מינימלי `SqlClient` (query + transaction). `PgClient` בפרודקשן, pglite בטסטים (בלי תלות ענן).
- **BI / Analytics:** `src/db/bi_views.sql` — Star Schema (dims: date/vehicle/dealer, facts: settlements/ledger/transfers). מפורט ב-[`power-bi-essential-concepts.md`](./power-bi-essential-concepts.md).

**סטטוס: ✅ STRONG.** זה החלק הבשל ביותר של המערכת.

---

## 🟠 4. Performance & Caching — Caching · Redis · Background Jobs · Message Queues · Rate Limiting

**מה השלב:** להפוך את האפליקציה למהירה וניתנת-לסקייל.

**איפה ULease מכסה:**
- **Caching (CQRS):** `vehicle_read_model` הוא בפועל cache מטריאליזד של מצב הרכב — משרת את `GET /v1/catalog` בלי join-ים יקרים. עקביות eventual דרך אירועים.
- **Background Jobs:**
  - `src/inventory/sweeperRunner.ts` — משחרר שמירות שפג תוקפן באינטרוול מתצורה.
  - `src/events/outboxRelay.ts` — worker שמושך מה-outbox, **at-least-once**, עם `FOR UPDATE SKIP LOCKED` לריבוי instances. API ו-worker הם תהליכים נפרדים (`start:api` / `start:worker`).
- **Message Queue / Event Bus:** `src/events/outbox.ts` (single-writer) + `src/events/sink.ts` — interface `EventSink` עם `InMemorySink` ל-MVP. בקוד מסומן במפורש: *"Production wires Kafka/PubSub here"*.

**חובות פתוחים:**
> - **Redis / cache חיצוני:** אין — ה-cache כיום in-process בלבד.
> - **Broker אמיתי:** ה-`EventSink` הוא seam; טרם חובר Kafka/NATS/PubSub. ראה [`CTO_REVIEW.md` §P2](./CTO_REVIEW.md) — מימוש `KafkaEventSink`/`NatsEventSink` כנגד ה-interface הקיים, additive, בלי שינוי בשכבת ה-domain.
> - **Rate Limiting:** לא ממומש. נוסף בעתיד ב-middleware (`express-rate-limit`) או ב-reverse proxy.

**סטטוס: 🟡 PARTIAL — הדפוסים (Outbox/CQRS/Workers) קיימים ובשלים; ה-infra החיצוני (Redis/broker/rate-limit) הוא seam מתוכנן.**

---

## 🔴 5. Cloud & Deployment — Docker · CI/CD · AWS/Azure/GCP

**מה השלב:** להעלות לאוויר ולהפוך production-ready.

**איפה ULease מכסה:**
- **Docker:** `Dockerfile` multi-stage (build → deps → runtime, Node 22-slim). תמונה אחת ל-API ול-worker; פקודת ההרצה בוחרת מי.
- **Topology:** `docker-compose.yml` — Postgres 16 (health checks) + API + worker, כל אחד scalable בנפרד. משקף את טופולוגיית הפרודקשן.
- **CI/CD:** `.github/workflows/ci.yml` — על PR ו-push ל-main: typecheck + 55 טסטים, בלי DB ענן (pglite מוטמע).
- **Cloud (agnostic):** `api/index.ts` + `vercel.json` ל-serverless; Supabase כ-DB פרודקשן בספקים. הקוד עומד מול Postgres סטנדרטי — נייד לכל ענן (אין דוגמת AWS/Azure/GCP ייעודית, וזה במכוון).
- **Config:** `src/config.ts` — env vars מאומתי-Zod, fail-fast על חוסר (`DATABASE_URL` חובה).
- **Dev environments:** [`DEV_ENVIRONMENTS.md`](./DEV_ENVIRONMENTS.md) + playbook ה-Go-Live ב-[`LAUNCH.md`](./LAUNCH.md).

**סטטוס: ✅ STRONG.**

---

## ⭐ 6. Advanced Engineering — Monitoring · Logging · System Design · Scalability · Microservices

**מה השלב:** מה שמבדיל "כותב קוד" מ-"בונה מערכות אמינות".

**איפה ULease מכסה:**
- **System Design:** [`system-design-cheatsheet.md`](./system-design-cheatsheet.md) — 15 מושגי ליבה, כל אחד מוצלב מול קובץ קוד וסטטוס. ULease חזקה ב-🟧 Design וב-🟩 Build/Quality, עם seams מוכנים ל-🟦 NFRs.
- **Roadmap הנדסי:** [`CTO_REVIEW.md`](./CTO_REVIEW.md) — scorecard מבוסס-ראיות + מפת דרכים מתועדפת **P0–P7** ל-Platform v2.0 (Multi-Tenant → Decision Engine → Event Backbone → Data Platform → Matching → Anti-Fraud → Billing → Search).
- **Logging & Observability:** `src/lib/logger.ts` (logger מרכזי), `logger.error` עם stack traces ב-relay, health/ready endpoints, ו-`outbox_health` view (עוקב אחרי אירועים לא-published והגיל שלהם).
- **Scalability (seams):** API stateless (Nx instances), worker עם `SKIP LOCKED` (Nx workers על אותו Postgres), `EventSink` pluggable, tenant sharding מתוכנן ב-P0.
- **Microservices / Domain modules:** `src/inventory/`, `src/commission/`, `src/payments/`, `src/scoring/` — כל אחד עם `service`/`repository` ו-bounded context נקי. ([`CTO_REVIEW.md` §3](./CTO_REVIEW.md): "המבנה כבר חצי-שם".)
- **Reliability patterns:** Outbox (zero event loss), Idempotency keys, at-least-once, MVCC, append-only ledger, eventual-consistency read model. נבדק ב-`inventory.concurrency.test.ts` (25 ניסיונות מקבילים → בדיוק 1 מצליח).
- **Automation layer:** [`N8N_AUTOMATION.md`](./N8N_AUTOMATION.md) — n8n כ-Glue Layer מעל ה-Outbox; ו-`stage-a/` כ-Agent Runtime ([`AGENT_BLUEPRINT.md`](./AGENT_BLUEPRINT.md)).

**סטטוס: ✅ STRONG, עם roadmap מתועד להעמקה.**

---

## 7. החובות הפתוחים — מרוכזים (לא מוסתרים)

לפי Working Rule 7 (*NO LAZINESS — אם יש חוב, תעד אותו*):

| # | חוב | עדיפות | מקור | תיקון מתוכנן |
|---|-----|--------|------|--------------|
| 1 | **Multi-Tenancy** — אין `tenant_id` באף טבלה | **P0** | `CTO_REVIEW.md` §P0 | `tenant_id TEXT NOT NULL DEFAULT 'leasing-co-il'` additive + composite indexes + API-key→tenant resolver |
| 2 | **RLS בצד DB** — כיום רק ב-Power BI | **P0** | cheatsheet #9 ⚠️ | policies על כל הטבלאות, אחרי Multi-Tenancy |
| 3 | **Event Backbone** — broker אמיתי | **P2** | `CTO_REVIEW.md` §P2 | `KafkaEventSink`/`NatsEventSink` כנגד `src/events/sink.ts` |
| 4 | **Data Platform** — CDC→OLAP + Feature Store | **P3** | `CTO_REVIEW.md` §P3 | Debezium/CDC → BigQuery/ClickHouse |
| 5 | **Rate Limiting + Redis** | post-P2 | מודול זה §4 | middleware / reverse proxy + cache חיצוני |

---

## 8. "אם הייתי מתחיל מחדש היום" — התשובה של ULease

השאלה בפוסט: *מה הייתם לומדים קודם, ומה הייתם מדלגים עליו?* התשובה לפי איך ULease נבנתה בפועל:

1. **קודם כול — Data Modeling + Transactions.** רוב הבאגים היקרים הם באינטגריטי של נתונים, לא בסינטקס. ב-ULease, ה-`schema.sql` עם append-only ledger ו-`amount_minor` הוא הלב — הוא מה ששומר על "כסף לא נעלם".
2. **אחר כך — Idempotency + Concurrency.** לפני קנה-מידה. `inventory.concurrency.test.ts` (anti-overselling) שווה יותר מ-10 שכבות caching.
3. **מה לדלג עליו (בהתחלה):** Microservices מוקדם, Redis לפני שצריך, ו-broker חיצוני לפני שיש load. ULease השאירה את כולם כ-**seams** ולא בנתה אותם בטרם עת — וזה במכוון.
4. **התוספת המודרנית שהמסלול לא מראה:** שכבת ה-**Agent/Automation** מעל ה-API (n8n = Hands · `stage-a` = Brain). זה ה-"backend" של 2026 — ה-API לא רק משרת UI, הוא מזין agents.

---

## נספח — Module Registration

מודול זה רשום ב-[`CLAUDE.md`](./CLAUDE.md) וב-[`README.md`](./README.md). מיקום מומלץ ב-Load Order: אחרי `system-design-cheatsheet.md` (9a) — שניהם מצליבים תיאוריה ⇄ קוד, וזה ה-roadmap שמסגר אותם.
