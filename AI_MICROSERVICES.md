# Microservices — איך שירות אחד מתחבר לאחר

**Module:** `AI_MICROSERVICES.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — Knowledge layer (§3 שורה 30). מודול במשפחת ההנדסה (`AI_SYSTEM_DESIGN` · `KUBERNETES_101` · `CLOUD_ARCHITECT_SKILLS`) — שפת ה-microservices מול ה-Tech Lead.
**Source:** מבוסס על האינפוגרפיקה *"How One Service Connects to Another Service in Microservices"* (תרחיש E-Commerce: Order · Inventory · Payment).
**Integrates with:** `AI_SYSTEM_DESIGN.md` (§1 · §2 · §3 · §4.5), `KUBERNETES_101.md`, `AI_PROJECT_STRUCTURE.md`, `CASES/ULEASE_SPEC.md` (§3 · §8), `AI_DATA_BI.md`, `AI_CLAUDE_STACK_2026.md`

---

> איך שירותים מדברים זה עם זה ברשת — **sync** (REST/gRPC) מול **async** (message broker), service discovery, load balancing ו-API Gateway. אבל הערך האמיתי למייסד הוא דווקא **ההכרעה ההפוכה** (§6): *מתי לא לפצל* למיקרו-שירותים. זה ההמשך הטבעי של `AI_SYSTEM_DESIGN` — שם הבקשה נכנסה דרך ה-Gateway ועברה בשכבות בתוך אפליקציה אחת; כאן השאלה היא מה קורה כשיש **כמה אפליקציות (שירותים)** שצריכות לדבר. המסקנה ל-ULease: ב-MVP **לא בונים את זה** — בונים Modular Monolith ושומרים את המפה הזו ליום שבו ה-scale ידרוש.

---

## 1. שתי דרכים שירות מדבר עם שירות — Sync מול Async ⭐

זו ההבחנה שכל השאר נתלה עליה. כששירות A צריך משהו משירות B, יש שתי משפחות:

| ציר | **Sync** (בקשה-תשובה) | **Async** (אירועים) |
|-----|------------------------|----------------------|
| מי מחכה למי | A **חוסם** וממתין לתשובת B | A שולח אירוע ו**ממשיך**; B מעבד מתי שיכול |
| פרוטוקול | REST (HTTP/JSON) · gRPC (HTTP/2, בינארי) | Message Broker — Kafka · RabbitMQ · SNS/SQS |
| יתרון | פשוט, מיידי, קל לדבג | ניתוק (decoupling), עמידות, ספיגת עומסים |
| חיסרון | זיווג הדוק — אם B נופל, A נתקע | סיבוכיות: eventual consistency, סדר, כפילויות |
| 🎯 ב-ULease | קריאות הפורטל (לקוח/ספק) — REST | זרימת העסקה והלידים — **events** (`SPEC` §3) |

> **כלל האצבע:** *"אם הקורא צריך תשובה עכשיו כדי להמשיך — sync. אם זה 'תעדכן את השאר שקרה X' — async."* קניית רכב בחדר-העסקה צריכה אישור מיידי (sync), אבל "עסקה נסגרה → עדכן דשבורד, חייב עמלה, שלח התראה" הם async — בדיוק התורים מ-`AI_SYSTEM_DESIGN` §3.

---

## 2. ארכיטקטורת הדוגמה — ומה ממנה רלוונטי ל-ULease

האינפוגרפיקה מפרקת חנות E-Commerce לשירותים נפרדים, כל אחד עם ה-DB שלו:

```
Client → API Gateway → Order Service ─┬→ Inventory Service → Inventory DB
                                      └→ Payment Service   → Payment DB
                          (Service Discovery: Eureka/Consul מאחורי הקלעים)
```

| רכיב בדוגמה | מה הוא עושה | המקבילה ב-ULease | מתי? |
|--------------|--------------|-------------------|------|
| **API Gateway** | כניסה אחת: ניתוב, אימות, rate-limit | כבר ב-`AI_SYSTEM_DESIGN` §1 | **MVP** |
| **Order Service** | מנהל את מחזור-החיים של ההזמנה | "חדר-העסקה" — סגירת עסקת רכב | MVP (כמודול, לא שירות נפרד) |
| **Inventory Service** | בודק/שומר מלאי | קטלוג המלאי מהספקים (`SPEC` §8) | MVP (מודול) |
| **Payment Service** | מחייב/מחזיר תשלום | ניתוב מימון/עמלות (שותפים מורשים, D-009) | V1 (מודול) |
| **DB-per-service** | לכל שירות DB משלו | ❌ **לא ב-MVP** — PostgreSQL אחד (`SPEC` §8) | V2 בלבד |
| **Service Discovery** | שירותים מוצאים זה את זה לבד | רלוונטי רק במעבר ל-microservices | V2 (`SYSTEM_DESIGN` §4.5) |

> **התובנה הקריטית:** ב-ULease ה"שירותים" האלה הם **מודולים בתוך אפליקציה אחת**, לא תהליכים נפרדים ברשת. אותם גבולות לוגיים (Order/Inventory/Payment) — אבל בלי הרשת, ה-DB-per-service וה-discovery שביניהם. זו בדיוק ההבחנה Modular Monolith מול Microservices (§6).

---

## 3. חמש דרכי החיבור — וההכרעה לכל אחת

| דרך | מה זה | טכנולוגיה לדוגמה | ההכרעה ל-ULease |
|-----|--------|-------------------|------------------|
| **REST API** | משאבים על HTTP, JSON — הנפוץ ביותר | Spring Cloud Gateway · OpenFeign | ✅ **MVP** — הפורטלים וה-ingestion (`SYSTEM_DESIGN` §2) |
| **gRPC** | RPC בינארי מהיר עם סכמה (Protobuf), על HTTP/2 | gRPC / Protocol Buffers | ⏳ **V2** — תקשורת פנימית בין שירותי הסוכנים אם ה-scale ידרוש |
| **Message Broker** | pub/sub אסינכרוני — services מפרסמים/נרשמים לאירועים | Kafka · RabbitMQ · SNS/SQS | ✅ **MVP/V1** — מנוע ה-events (`SYSTEM_DESIGN` §3 · `SPEC` §3) |
| **Service Discovery** | שירותים נרשמים ומתגלים בשם במקום IP+פורט | Eureka · Consul · Zookeeper | ⏳ **V2** — רק כשיש ריבוי instances דינמי |
| **Load Balancing** | פיזור בקשות בין כמה instances של שירות | Ribbon · Spring Cloud LB | ✅ **MVP** — מאחורי ה-SLA (uptime, `PRICING_SLA` §4) |

> **הכלל (תאום ל-`SYSTEM_DESIGN` §4.5):** כל דרך מהטור הזה שה-Tech Lead רוצה להכניס ב-MVP מעבר ל-REST + broker אחד + LB — צריכה הצדקה בכתב. Discovery ו-gRPC הם פתרונות ל**בעיות של scale שעוד אין לנו**.

---

## 4. זרימת "סגירת עסקה" מקצה לקצה — Orchestration מול Choreography

האינפוגרפיקה מתארת *Create Order*: הלקוח מזמין → Gateway מאמת → Order קורא ל-Inventory (שמור מלאי) → Order קורא ל-Payment (חייב) → Order שומר ומחזיר תשובה. שרשרת כזו אפשר לתזמר בשתי דרכים — וזו הכרעה ארכיטקטונית, לא פרט מימוש:

| גישה | מי מנהל את הזרימה | יתרון | חיסרון |
|------|-------------------|--------|---------|
| **Orchestration** | רכיב מרכזי (כמו Order) מנצח את כל השאר בקריאות sync | זרימה גלויה במקום אחד, קל למעקב | נקודת-תלות מרכזית |
| **Choreography** | כל שירות מגיב לאירועים ופולט אירועים (async) | ניתוק מלא, עמידות | קשה לראות את "התמונה המלאה" |

> **החיבור ל-Ultra·Master·Max (D-008, `SPEC` §3):** מנוע הסוכנים של ULease הוא **orchestration** — Ultra מתזמר את ה-Masters וה-Max בדיוק כמו Order Service שמנצח את Inventory ו-Payment. ה-`AgentRun.eventId` (`SPEC` §8) הוא ה-**Correlation ID** מ-`SYSTEM_DESIGN` §3 — אותו מזהה שעובר בכל השרשרת ומאפשר traceability. עיקרון ה-**Idempotency** קריטי כאן: retry על "חייב תשלום" אסור שיחייב פעמיים (`SYSTEM_DESIGN` §3).

---

## 5. ריבוי instances — סקיילביליות אופקית

הדרך לשרת יותר תנועה: לא שרת גדול יותר (vertical), אלא **עוד עותקים** של אותו שירות מאחורי Load Balancer (horizontal):

```
            ┌→ Order Instance 1 ┐
Client → LB ┼→ Order Instance 2 ┼→ Order DB   (Service Discovery רושם/מסיר instances)
            └→ Order Instance N ┘
```

| מושג | מה זה | 🎯 ב-ULease |
|------|--------|--------------|
| **Stateless services** | השירות לא שומר state מקומי → כל instance מחליף כל instance | תנאי מקדים ל-scale; ה-state ב-DB/Redis, לא בזיכרון השרת |
| **Auto Scaling** | הוספת/הסרת instances לפי עומס | קמפיין ב-21:00 → גדל לבד; 02:00 → מתכווץ (`SYSTEM_DESIGN` §4.5) |
| **Service Discovery** | ה-LB יודע אילו instances חיים כרגע | V2 — נדרש רק כשה-scaling דינמי |

> ל-MVP: instance אחד או שניים מאחורי LB מנוהל בענן — זה כל ה-scale שצריך עד שיש תנועה אמיתית. ה-stateless-ness הוא ההחלטה היחידה שכן מקבלים מוקדם, כי קשה לתקן אותה אחר כך.

---

## 6. ⭐ ההכרעה ל-ULease: Modular Monolith קודם, Microservices אחר כך

זה הלב של המודול — והפער שהאינפוגרפיקה *לא* מכסה. היא מראה איך microservices מתחברים; היא לא שואלת **האם בכלל צריך אותם**. לסטארטאפ לפני השקה התשובה כמעט תמיד **לא**.

| | **Modular Monolith** (🎯 ULease ב-MVP) | **Microservices** (V2+, בתנאים) |
|---|------------------------------------------|----------------------------------|
| פריסה | אפליקציה אחת, deploy אחד | N שירותים, N pipelines |
| תקשורת פנימית | קריאת פונקציה (in-process) — אפס רשת | רשת: REST/gRPC/broker בין שירותים |
| דאטה | DB אחד, טרנזקציות ACID פשוטות | DB-per-service, eventual consistency, saga |
| מי צריך את זה | צוות קטן, מוצר שעוד מתגבש | צוותים מרובים, גבולות יציבים, scale מוכח |
| העלות הנסתרת | — | latency רשת, debugging מבוזר, DevOps כבד |

**למה monolith-first נכון ל-ULease דווקא:**
1. **צוות של אחד+שכירה** (D-012) — microservices פותרים בעיה *ארגונית* (צוותים שדורכים זה לזה), ולא בעיה טכנית. אין צוותים → אין את הבעיה.
2. **הגבולות עוד זזים** — לפני 1,000 עסקאות (D-022) עוד לא יודעים איפה באמת עובר הגבול בין "Order" ל-"Inventory". לפצל מוקדם = לתקוע את הגבול הלא-נכון בבטון של רשת.
3. **הזרימה החיובית** (D-011) תלויה בהשקה מהירה — כל שעה על Kubernetes/discovery/saga היא שעה שלא על המוצר. **Over-engineering ב-Phase 0 = השקה מאוחרת** (תאום ל-`SYSTEM_DESIGN` §4.5 ו-`KUBERNETES_101` §11 — אותו שער: K8s הוא V1+, לא MVP).

> **הדרך הנכונה (Modular Monolith):** מודול אחד פר תחום (Order/Inventory/Payment/Agents) עם **גבולות נקיים** בתוך אפליקציה אחת — בדיוק תקן 4/10 התיקיות ב-`AI_PROJECT_STRUCTURE`. כשתחום אחד באמת חונק את האחרים (scale מוכח במספרים) — מחלצים אותו לשירות נפרד **בלי לשכתב את הלוגיקה**, כי הגבול כבר נקי. זה "strangler" מסודר, לא ניתוח לב פתוח.

**שלושת הטריגרים שמצדיקים פיצול שירות (ולא לפני):**
- 📈 **Scale נקודתי** — תחום אחד צורך משאבים פי-כמה מהשאר וצריך לגדול לבד.
- 👥 **גבול צוותי** — שני צוותים נפרדים נתקעים זה לזה על אותו deploy.
- 🔌 **קצב/טכנולוגיה שונים** — תחום שצריך release נפרד או stack אחר (למשל שירות ML).

---

## 7. צ'קליסט Design Review מול ה-Tech Lead

- [ ] **Monolith או Microservices?** ל-MVP — Modular Monolith. אם ה-Tech Lead מציע microservices: איזה משלושת הטריגרים (§6) כבר מתקיים? (אם אף אחד → עצור)
- [ ] **Sync או Async?** לכל קריאה בין-תחומית — צריך תשובה עכשיו (sync) או "תעדכן שקרה X" (async)? (§1)
- [ ] **גבולות נקיים?** האם המודולים מופרדים מספיק כדי שאפשר יהיה לחלץ אחד לשירות בעתיד בלי שכתוב? (§6 + `AI_PROJECT_STRUCTURE`)
- [ ] **Stateless?** האם השירותים נטולי-state מקומי כדי לאפשר scale אופקי? (§5)
- [ ] **Idempotency + Correlation ID** בזרימת העסקה? (§4 + `SYSTEM_DESIGN` §3)
- [ ] **DB אחד או DB-per-service?** ל-MVP — אחד. פיצול DB הוא החלטה של V2 בלבד. (§2)

---

## 8. החיבור ל-OS

| איפה | מה |
|------|-----|
| `AI_SYSTEM_DESIGN.md` | המודול-אח: §1 (Gateway/LB) · §2 (REST/gRPC/Webhook) · §3 (תורים/Idempotency) · §4.5 (Service Discovery, Auto Scaling) — הרכיבים; **כאן** = איך הם מתחברים בין שירותים + מתי לא לפצל |
| `AI_PROJECT_STRUCTURE.md` | המבנה שמממש את ה-Modular Monolith — מודול פר תחום עם גבולות נקיים, מסלול הצמיחה MVP→Enterprise |
| `KUBERNETES_101.md` | השכבה שמתחת: כש-ULease *כן* תפצל לשירותים (V2), K8s מתזמר אותם (Pod · Service · HPA). §11 שם = אותה הכרעת MVP/V1/V2 ושער אנטי-over-engineering |
| `CASES/ULEASE_SPEC.md` §3 · §8 | ארכיטקטורת ה-events ו-Ultra·Master·Max (orchestration, §4) + מודל הנתונים (DB אחד, §2) |
| `AI_CLAUDE_STACK_2026.md` | Agent Teams כ-prototype לסוכנים (D-029) — orchestration לפני פיצול לשירותים אמיתיים |
| Learn-vs-Delegate | **אתה:** ההכרעה monolith-vs-microservices + הצ'קליסט · **Tech Lead:** המימוש והגבולות |

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | מודול ראשוני (D-062): חמש דרכי חיבור שירות-לשירות (REST · gRPC · Message Broker · Service Discovery · Load Balancing), sync מול async, orchestration מול choreography, ריבוי instances — וההכרעה המרכזית ל-ULease: **Modular Monolith קודם** (§6) + צ'קליסט design review | 2026-06-04 |

**Attribution.** המקור: האינפוגרפיקה *"How One Service Connects to Another Service in Microservices"* (תרחיש E-Commerce: Order · Inventory · Payment). העיבוד, ההכרעה monolith-first והמיפוי ל-ULease — חלק מה-Claude OS של Avraham Bar Yochai Chazan.

**Confidentiality.** קובץ זה הוא חלק מה-Claude Operating System האישי של Avraham Bar Yochai Chazan.

— *End of AI_MICROSERVICES.md v1.0.0 —*
