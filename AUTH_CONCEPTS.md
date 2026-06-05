# Authentication vs Authorization — המדריך ⇄ הקוד של ULease

**ההבחנה בין אימות (מי אתה) להרשאה (מה מותר לך), מוצלבת מול שכבת האבטחה בפועל ב-`leasing-api`.**

> AuthN ≠ AuthZ. **Authentication מאמת זהות** (*"are you really who you claim to be?"*) — קורה ראשון, כישלון = **401 Unauthorized**. **Authorization קובע הרשאות** (*"what can you do?"*) — קורה אחרי, כישלון = **403 Forbidden**. הסיסמה לזכור: **Authenticate first, authorize second.** המודול מצליב כל מושג מהמדריך מול ה-seam המקביל ב-ULease — ומסמן במפורש היכן AuthN חזק אך AuthZ עדיין חוב.

---

## 1. AuthN ⇄ AuthZ במבט-על

| | Authentication | Authorization |
|---|----------------|---------------|
| עונה על | מי אתה? | מה מותר לך? |
| מטרה | אימות זהות | אימות הרשאה |
| מתי | ראשון | אחרי האימות |
| דוגמה | login, password, OTP, **token** | roles, permissions, **row-level access** |
| קוד כישלון | **401 Unauthorized** | **403 Forbidden** |

---

## 2. שכבת האבטחה של ULease — מיפוי לקוד

| מושג מהמדריך | מימוש/Seam ב-`leasing-api` | סטטוס |
|--------------|---------------------------|--------|
| **Token-based auth (JWT/HMAC)** | `src/middleware/hmacAuth.ts` — `X-Signature` = hex(HMAC-SHA256(secret, `${timestamp}.${rawBody}`)) | ✅ AuthN |
| **Replay protection** | `X-Timestamp` + `MAX_SKEW_MS = 5min`; `timingSafeEqual` (constant-time) | ✅ |
| **401 Unauthorized** | חתימה/timestamp חסרים/לא תקפים → `401 { code: 'UNAUTHORIZED' }` | ✅ |
| **Provider signature** | `/webhooks/stripe` מאומת ב-Stripe signature על raw body (לא HMAC הפנימי) | ✅ |
| **Input validation** | `zod` (`schemas.ts`) → `400 VALIDATION_ERROR` (לפני authZ) | ✅ |
| **Authorization (RBAC/ABAC)** | — אין מודל role/permission ברמת ה-actor; ה-`actor` הוא string, לא נבדק מול הרשאות | ⚠️ חוב |
| **Row-level access (ABAC)** | `rls.sql` — `tenant_isolation` policy על `app.current_tenant` GUC; `setTenantContext` (`db/client.ts`); **fail-closed** | ✅ AuthZ (tenant-level) |
| **403 Forbidden** | — אין endpoint שמחזיר 403; AuthZ כיום הוא row-level (RLS מסתיר שורות), לא action-level | ⚠️ חוב |

---

## 3. הזרימה ב-ULease — Authenticate first, authorize second

```
  Request (X-Signature, X-Timestamp, body)
            │
            ▼  ① AUTHENTICATION
   ┌─────────────────────────┐
   │ hmacAuth (server.ts)    │  HMAC-SHA256 + replay guard
   │ fail → 401 UNAUTHORIZED  │
   └────────────┬────────────┘
            │ valid
            ▼  ② VALIDATION
   ┌─────────────────────────┐
   │ zod parseBody           │  fail → 400 VALIDATION_ERROR
   └────────────┬────────────┘
            │ valid
            ▼  ③ AUTHORIZATION (row-level)
   ┌─────────────────────────┐
   │ setTenantContext        │  app.current_tenant → RLS
   │ rls.sql tenant_isolation │  WITH CHECK + USING; fail-closed
   │ cross-tenant write → ✗   │
   └────────────┬────────────┘
            │ authorized rows only
            ▼
        domain logic
```

> **הקריאה:** ULease מיישם **AuthN חזק** (HMAC עם replay-guard + constant-time compare) ו-**AuthZ ברמת-שורה** (RLS tenant isolation, fail-closed, מאומת ב-4 טסטי `tenancy.test.ts`). מה שחסר הוא **AuthZ ברמת-פעולה** (role→action, ה-403 הקלאסי). זה תואם את `system-design-cheatsheet § 9` (Security) ואת חוב ה-Multi-Tenancy שנסגר חלקית ב-`CTO_REVIEW.md`.

---

## 4. למה זה לא תאוריה — ה-RLS כבר עובד

`tenancy.test.ts` מוכיח את שני חצאי ה-AuthZ ברמת-שורה (63/63 ירוקים):

1. **בידוד קריאה** — tenant-a רואה רק שורות tenant-a; tenant-b רק שלו.
2. **WITH CHECK** — כתיבה חוצת-tenant נדחית (`INSERT ... tenant_id='tenant-b'` תחת context של tenant-a → throws).
3. **Fail-closed** — חיבור ללא `app.current_tenant` רואה **0 שורות** (לא שגיאה — בטוח-כברירת-מחדל).
4. **Additive** — `tenant_id` ברירת-מחדל `'leasing-co-il'`, תואם-לאחור; RLS מאחורי flag `RLS_ENABLED`.

> זו בדיוק ה-**ABAC** (Attribute-Based Access Control) מהמדריך, ברמת ה-DB. ה-attribute הוא `tenant_id`; ה-policy אוכף ב-Postgres, לא באפליקציה — `FORCE ROW LEVEL SECURITY` כי האפליקציה מתחברת כ-owner.

---

## 5. חוב פתוח (כנה)

1. **Action-level AuthZ (RBAC)** — אין מיפוי role→endpoint; כל בקשה מאומתת (HMAC) מורשית לכל פעולה. הצעד: middleware הרשאות שמחזיר **403** לפי role של ה-actor.
2. **חיווט RLS end-to-end** — `setTenantContext` קיים אך `RLS_ENABLED` כבוי כברירת-מחדל; חיבור request→tenant בכל handler/worker הוא Stage הבא (`CTO_REVIEW` P0).

---

*תומלל מ-"Authentication vs Authorization — Complete Guide for Beginners" (M-SoftTech), ומופה לשכבת האבטחה של `leasing-api` בהמשך ל-`system-design-cheatsheet.md § 9` ו-`CTO_REVIEW.md`.*
