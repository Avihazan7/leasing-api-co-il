# System Design Cheat Sheet — 15 מושגי הליבה

**מפת דרכים לעיצוב מערכות: 15 מושגים שכדאי להחזיק בהישג יד בכל פעם שמתכננים מערכת.**

> עיצוב מערכת טוב לא מתחיל בבחירת טכנולוגיה — הוא מתחיל בהבנת **הדרישות**, מתקדם דרך **הארכיטקטורה והנתונים**, נשען על **תכונות איכות** (Scalability/Reliability/Availability/Performance), ונסגר ב**תפעול ומחזור-חיים** (Cost/Docs/Migration). 15 המושגים האלה הם רשימת-בדיקה, לא רשימת-קניות.

---

## 15 המושגים במבט-על

האינפוגרפיקה מחלקת את 15 המושגים ל-4 אשכולות צבע — וזה בדיוק זרימת התכנון:

| אשכול | שלב | מושגים |
|-------|-----|--------|
| 🟧 כתום | **תכנון (Design)** | Requirement Gathering · System Architecture · Data Design · Domain Design |
| 🟦 כחול | **תכונות איכות (NFRs)** | Scalability · Reliability · Availability · Performance |
| 🟩 ירוק | **בנייה ואיכות** | Security · Maintainability · Testing · User Experience Design |
| 🟪 סגול | **תפעול ומחזור-חיים** | Cost Estimation · Documentation · Migration Plan |

| # | מושג | בשורה אחת |
|---|------|-----------|
| 1 | **Requirement Gathering** | מה המערכת צריכה לעשות, מי ישתמש בה, ואיזו בעיה היא פותרת. |
| 2 | **System Architecture** | המבנה הכולל: איך הרכיבים מתחברים, מתקשרים ומתרחבים. |
| 3 | **Data Design** | איך הנתונים נשמרים, מאורגנים ונגישים. |
| 4 | **Domain Design** | פירוק לדומיינים עסקיים, היגיון עסקי ומינימום תלויות. |
| 5 | **Scalability** | שהמערכת תגדל בצורה חלקה ככל שהביקוש עולה. |
| 6 | **Reliability** | שתעבוד באופן עקבי ותתאושש כשמשהו משתבש. |
| 7 | **Availability** | שהשירות יישאר זמין — גם בזמן תקלות. |
| 8 | **Performance** | latency נמוך, תגובה מהירה, throughput גבוה. |
| 9 | **Security** | אימות, הרשאות, הצפנה ושמירה על מידע רגיש. |
| 10 | **Maintainability** | קל לעדכן, לדבג ולשפר לאורך זמן. |
| 11 | **Testing** | unit / integration / system — לתפוס באגים מוקדם. |
| 12 | **User Experience Design** | ממשק אינטואיטיבי, ידידותי ורספונסיבי. |
| 13 | **Cost Estimation** | תקצוב חומרה, רישוי, תשתית והפעלה שוטפת. |
| 14 | **Documentation** | תיעוד טכני, מדריכי משתמש ותיעוד API חיצוני. |
| 15 | **Migration Plan** | מעבר ממערכות ישנות בשיבוש מינימלי. |

---

## 🟧 תכנון (Design)

### 1. Requirement Gathering
להבין מה המערכת צריכה לעשות, מי ישתמש בה, ואילו בעיות היא פותרת.

- **Functional vs Non-Functional** — מה המערכת עושה מול כמה טוב היא עושה את זה.
- **Define user stories** — תרחישי שימוש קונקרטיים.
- **Set priority** — לא הכול P0; תיעדוף הוא חלק מהדרישות.

### 2. System Architecture
לשרטט את המבנה הכולל: איך הרכיבים מתחברים, מתקשרים ומתרחבים.

- **Define system components** — שירותים, מסדי נתונים, תורים, gateways.
- **Choose architectural styles** — monolith / modular monolith / microservices / event-driven.
- **Consider scalability, maintainability** — ארכיטקטורה היא סדרת trade-offs, לא "הנכון".

### 3. Data Design
לתכנן איך הנתונים נשמרים, מאורגנים ונגישים.

- **Define data models and schemas** — entities, relationships, invariants.
- **Choose proper database** — SQL מול NoSQL לפי דפוסי הגישה, לא לפי טרנד.
- **Define retention target** — כמה זמן שומרים, ומתי מארכבים/מוחקים.

### 4. Domain Design
לפרק את המערכת לדומיינים עסקיים ולמפות אותם לתהליכים בעולם האמיתי.

- **Break down system into business domains** — bounded contexts.
- **Encapsulate functionality within modules** — היגיון עסקי חי בתוך הדומיין שלו.
- **Minimize dependencies among domains** — קישוריות נמוכה (low coupling), לכידות גבוהה (high cohesion).

---

## 🟦 תכונות איכות (NFRs)

### 5. Scalability
שהמערכת תגדל בצורה חלקה ככל שהביקוש עולה.

- **Horizontal & vertical scaling** — להוסיף מכונות מול להגדיל מכונה.
- **Load balancing** — לפזר עומס בין instances.
- **Cold start-up** — זמן ההתחממות של שירותים serverless/אוטו-סקיילינג.

### 6. Reliability
שהמערכת תעבוד באופן עקבי ותתאושש כשמשהו משתבש.

- **Fault tolerance** — כשל ברכיב אחד לא מפיל את המערכת.
- **Monitoring and alerting** — לדעת על תקלה לפני שהלקוח מדווח.
- **Recovery plans** — runbooks, retries, idempotency.

### 7. Availability
לשמור על השירות זמין — גם בזמן כשלים.

- **Data replication** — עותקים מרובים, אין single point of failure.
- **Minimize system downtime** — deploys ללא-downtime, health checks.
- **Disaster recovery** — RTO/RPO, גיבויים נבדקים (לא רק קיימים).

### 8. Performance
לתכנן לזמני טעינה מהירים, תגובה מהירה ו-latency נמוך.

- **Define latency and throughput target** — מספר, לא "מהר".
- **Optimize data structures and encoding** — אינדקסים, סריאליזציה, payload sizes.
- **Caching strategies** — read models, CDN, מטמון בזיכרון.

---

## 🟩 בנייה ואיכות

### 9. Security
להגן על המערכת מאיומים — אימות, הרשאות ושיטות בטוחות.

- **Authentication & Authorization** — מי אתה, ומה מותר לך.
- **Data encryption** — at-rest ו-in-transit.
- **Sensitive data storage** — סודות ב-secret manager, לא בקוד.

### 10. Maintainability
שיהיה קל לעדכן, לדבג ולשפר עם הזמן.

- **Clear code structure and documentation** — קוד שנקרא כמו הקוד שמסביבו.
- **SDLC management** — ניהול מחזור-חיי פיתוח.
- **Evolvable architecture** — Strangler Fig על Big-Bang refactor.

### 11. Testing
שיטות מגוונות (unit, integration, system) כדי לתפוס באגים מוקדם.

- **Define unit, integration, system tests** — פירמידת הטסטים.
- **Define acceptance tests with the users** — מה זה "עובד" מבחינת הלקוח.
- **Define performance and security tests** — load tests, scans.

### 12. User Experience Design
ליצור ממשק אינטואיטיבי וידידותי.

- **Intuitive, user-friendly user interface design**
- **Design usability tests**
- **Responsiveness** — מובייל-first, נגישות.

---

## 🟪 תפעול ומחזור-חיים

### 13. Cost Estimation
לתקצב משאבים, אירוח, כוח-אדם והפעלה שוטפת.

- **Evaluate hardware TCO** — עלות בעלות כוללת, לא רק מחיר רכישה.
- **Evaluate licensing and subscription fees** — SaaS, רישיונות, third-party.
- **Plan for future scalability costs** — עלות ה-scale שתכננת בסעיף 5.

### 14. Documentation
לכתוב מדריכים, דיאגרמות והערות inline לצוותים עתידיים.

- **Clear technical documentation** — ADRs, specs, דיאגרמות.
- **User manuals** — לקצה.
- **External API design and documentation** — חוזה ה-API הוא ממשק ציבורי.

### 15. Migration Plan
להכין אסטרטגיות למעבר ממערכות ישנות בשיבוש מינימלי.

- **Technical stack compatibility** — תאימות מחסנית.
- **System interoperability** — שתי המערכות חיות יחד בתקופת המעבר.
- **Data migration** — backfill, dual-write, cutover מתוכנן.

---

## מ-15 המושגים אל הקוד — מיפוי ל-ULease (`leasing-api`)

15 המושגים אינם תיאוריה מופשטת עבורנו — כל אחד מהם כבר נגזר (במלואו או כ-seam) בקוד של `leasing-api`. הטבלה מצליבה כל מושג מול **ראיה בקוד**, בהמשך ישיר ל-`CTO_REVIEW.md`:

| # | מושג | מימוש/Seam ב-`leasing-api` | סטטוס |
|---|------|---------------------------|--------|
| 1 | Requirement Gathering | `docs/specs/` (למשל `bi-analytics-layer.md`) — spec לפני קוד | ✅ |
| 2 | System Architecture | Event-driven: Transactional **Outbox + Relay** (`src/events/outbox.ts`, `outboxRelay.ts`) + `EventSink` (`src/events/sink.ts`); מודולים `inventory`/`payments`/`commission`/`scoring` | ✅ seam |
| 3 | Data Design | `src/db/schema.sql` (פורטבילי) · כסף ב-`amount_minor` (יחידות מינור, ללא float) · `ledger_entries` append-only ושומר-כסף | ✅ |
| 4 | Domain Design | Bounded contexts: `inventory/` עם `service`/`repository`/`stateMachine` נקיים; חילוץ הדרגתי (Strangler Fig, CTO_REVIEW §3) | ✅ חלקי |
| 5 | Scalability | `EventSink` seam מתועד *"Production wires Kafka/PubSub here"*; חסר broker אמיתי + `tenant_id` sharding | 🟡 seam (P0/P2) |
| 6 | Reliability | Transactional Outbox = אפס אובדן אירועים; `worker.ts` relay; idempotency; `inventory.concurrency.test.ts` | ✅ |
| 7 | Availability | Supabase/Postgres עם replication; relay worker נפרד מה-API (`start:api` / `start:worker`) | ✅ |
| 8 | Performance | CQRS read-model `vehicle_read_model` (projection) · composite indexes · Postgres FTS (מספיק עד עשרות אלפי רכבים, CTO_REVIEW P7) | ✅ |
| 9 | Security | `hmacAuth.ts` (HMAC על webhooks) · `helmet` · **RLS בצד DB = חוב פתוח** (כיום RLS בצד Power BI לפי `dealer_account`) | ⚠️ חוב מתועד (P0) |
| 10 | Maintainability | `typecheck` (tsc) · מודולריות · `Working Rules` ב-`CLAUDE.md`; Decision Engine נוסף **additive** ולא rewrite | ✅ |
| 11 | Testing | `vitest`: `api`/`inventory.lifecycle`/`inventory.concurrency`/`settlement`/`commission`/`decisionEngine`/`projection`/`biViews` — **55/55 ✅** | ✅ |
| 12 | UX Design | מחוץ ל-scope של ה-API; חי בשכבת ה-frontend וב-Dealer Onboarding (ראו `N8N_AUTOMATION.md` §7.3) | ↗️ שכבה אחרת |
| 13 | Cost Estimation | Serverless deploy (`vercel.json`) · Supabase — עלות נשלטת; scale-cost ממופה במפת הדרכים (CTO_REVIEW P2–P3) | ✅ |
| 14 | Documentation | `docs/specs/` · `COMMAND_API.md` · ה-OS docs כולו · README כחוזה API | ✅ |
| 15 | Migration Plan | `schema.sql` פורטבילי · `tenant_id TEXT NOT NULL DEFAULT 'leasing-co-il'` (additive, תואם-לאחור) · backfill ל-P0 (CTO_REVIEW §2) | 🟡 מתוכנן (P0) |

> **הקריאה החשובה:** מתוך 15 המושגים, ULease חזקה ב-🟧 (Design) וב-🟩 (Build/Quality), בעלת seams מוכנים ל-🟦 (NFRs), ועם **שני חובות פתוחים מתועדים** — RLS בצד DB (#9) ו-Multi-Tenancy (#5/#15). זה בדיוק מה ש-`CTO_REVIEW.md` ממפה כ-P0. המושגים האלה הם המסגרת; מפת הדרכים היא הביצוע.

---

## הרעיון הגדול

> מהנדסים רבים קופצים ישר ל-System Architecture (#2) ול-Scalability (#5). אבל מערכות מעולות נבנות על **דרישות ברורות** (#1), **מודל נתונים נכון** (#3), **גבולות דומיין** (#4) ו**תכונות איכות מדידות** (#5–8) — לפני שורת קוד אחת.
>
> שמרו את הרשימה בהישג יד. תחזרו אל 15 הנקודות האלה בכל עיצוב מערכת רציני.

---

*תומלל מהאינפוגרפיקה "15 System Design Core Concepts" (Paras Mayur), ומופה ל-codebase של `leasing-api` בהמשך ל-`CTO_REVIEW.md`.*
