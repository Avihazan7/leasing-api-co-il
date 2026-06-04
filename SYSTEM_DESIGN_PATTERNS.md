# SYSTEM_DESIGN_PATTERNS.md — 8 Patterns ⇄ ULease

**Module:** `SYSTEM_DESIGN_PATTERNS.md` · **Version:** 1.0.0
**מקור:** הכרטיס *System Design Patterns* (@cloud_x_berry) — 8 patterns.
**Thesis:** *Pattern הוא חוזה invariants, לא דיאגרמה. דע איזה pattern חל לפני שאתה נוגע.*

---

## 0. למה המודול קיים

הכרטיס מציג 8 patterns גנריים. מודול זה ממפה כל אחד למצב האמיתי ב-`leasing-api` —
מה כבר מיושם, איפה, ומה roadmap. זה ה-bridge בין תיאוריה ל-`CLAUDE.md § 3` של ריפו הקוד.

## 1. הטבלה — 8 Patterns ⇄ קוד

| # | Pattern | מהות | ב-ULease | היכן |
|---|---------|------|----------|------|
| 1 | **Ambassador** | proxy ל-logging/monitoring/retry | ❌ roadmap | — |
| 2 | **Circuit Breaker** | עצירת קריאות לשירות נופל | ❌ roadmap | רלוונטי ל-Stripe adapter |
| 3 | **CQRS** | הפרדת write/read | ✅ מיושם | `vehicles` ⇄ `vehicle_read_model` · `projection/vehicleProjection.ts` |
| 4 | **Sharding** | פיצול DB מונוליטי | ❌ לא נדרש בקנה-המידה הנוכחי | — |
| 5 | **Sidecar** | container עזר לצד השירות | ❌ roadmap | רלוונטי לפריסת worker |
| 6 | **Pub/Sub** | מפיצים/מנויים מנותקים | ✅ מיושם (in-proc) | `events/sink.ts` (`InMemoryEventSink`) → Kafka/PubSub בפרודקשן |
| 7 | **Leader Election** | בורר leader בין nodes | ⚠️ נעקף | `outboxRelay.ts` משתמש ב-`SKIP LOCKED` ⇒ ריבוי-workers בטוח בלי leader |
| 8 | **Event Sourcing** | האירועים הם source-of-truth | ⚠️ חלקי | `outbox` = CDC log; write model (`vehicles`) עדיין mutable |

**Bonus (מעבר לכרטיס, קיימים בקוד):** Transactional Outbox · Idempotency · Optimistic Locking.

## 2. Invariants שאסור לשבור

- **Outbox** — אירוע נכתב באותה טרנזקציה כמו ה-state change. כתיבה מחוץ = dual-write bug.
- **CQRS** — queries קוראות מה-read model בלבד; אל תקרא מה-write model ב-path של קריאה.
- **Leader-safe** — אל תסיר `FOR UPDATE SKIP LOCKED` מה-relay בלי נעילה חלופית.
- **Event Sourcing חלקי** — אל תניח replay מלא מה-outbox; הוא לא event store סמכותי.

## 3. מתי לאמץ pattern חדש

הוספת Circuit Breaker / Sidecar / Sharding = **שינוי ארכיטקטוני** → PLAN FIRST + תיעוד
ב-`leasing-api/MEMORY.md`. ממופה למפת הדרכים ב-`CTO_REVIEW.md` (Platform v2.0).
