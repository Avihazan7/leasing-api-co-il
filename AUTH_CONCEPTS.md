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
| **Row-level access (ABAC)** | `rls.sql` — `tenant_isolation` על `app.current_tenant`, **מחווט end-to-end**: בקשה (`X-Tenant-Id` → `resolveTenant` → `db.asTenant`) ו-worker (`SYSTEM_TENANT`); **fail-closed** | ✅ AuthZ (tenant-level, e2e) |
| **403 Forbidden** | — אין endpoint שמחזיר 403; AuthZ הוא row-level (RLS מסתיר שורות), לא action-level | ⚠️ חוב |

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
            ▼  ③ AUTHORIZATION (row-level, request-scoped)
   ┌──────────────────────────┐
   │ X-Tenant-Id → asTenant   │  app.current_tenant per request
   │ rls.sql tenant_isolation │  WITH CHECK + USING; fail-closed
   │ cross-tenant read/write→✗│
   └────────────┬─────────────┘
            │ authorized rows only
            ▼
        domain logic
```

> **הקריאה:** ULease מיישם **AuthN חזק** (HMAC עם replay-guard + constant-time compare) ו-**AuthZ ברמת-שורה מחווט end-to-end** — הטננט של הבקשה (`X-Tenant-Id`) נקשר ל-connection דרך `db.asTenant`, וה-RLS אוכף בידוד (מאומת גם ברמת-SQL וגם דרך HTTP ב-`tenancy.test.ts`). מה שחסר הוא **AuthZ ברמת-פעולה** (role→action, ה-403 הקלאסי). זה תואם את `system-design-cheatsheet § 9` (Security).

---

## 4. למה זה לא תאוריה — ה-RLS כבר עובד

`tenancy.test.ts` מוכיח את שני חצאי ה-AuthZ ברמת-שורה (65/65 ירוקים):

1. **בידוד קריאה** — tenant-a רואה רק שורות tenant-a; tenant-b רק שלו.
2. **WITH CHECK** — כתיבה חוצת-tenant נדחית (`INSERT ... tenant_id='tenant-b'` תחת context של tenant-a → throws).
3. **Fail-closed** — חיבור ללא `app.current_tenant` רואה **0 שורות** (לא שגיאה — בטוח-כברירת-מחדל).
4. **Additive** — `tenant_id` ברירת-מחדל נגזרת מ-GUC, תואם-לאחור; RLS מאחורי flag `RLS_ENABLED`.
5. **End-to-end (HTTP)** — בקשה עם `X-Tenant-Id: tenant-a` שיוצרת רכב; בקשת `tenant-b` מקבלת **404** על אותו רכב (RLS מסתיר, לא דליפה). זה מוכיח שהחיווט עובד מקצה-לקצה, לא רק ברמת-SQL.

> זו בדיוק ה-**ABAC** (Attribute-Based Access Control) מהמדריך, ברמת ה-DB. ה-attribute הוא `tenant_id`; ה-policy אוכף ב-Postgres, לא באפליקציה — `FORCE ROW LEVEL SECURITY` כי האפליקציה מתחברת כ-owner. ה-worker רץ תחת `__system__` (bypass מבוקר) כדי לעבד אירועים על-פני כל הטננטים.

---

## 5. חוב פתוח (כנה)

> **נסגר:** חיווט RLS end-to-end (request `X-Tenant-Id` → `asTenant`, worker `SYSTEM_TENANT`, מאומת ב-HTTP). `RLS_ENABLED` נשאר כבוי כברירת-מחדל ל-rollout מבוקר — הפעלתו אוכפת בידוד ללא שינוי קוד.

1. **Action-level AuthZ (RBAC)** — אין מיפוי role→endpoint; כל בקשה מאומתת (HMAC) מורשית לכל פעולה. הצעד: middleware הרשאות שמחזיר **403** לפי role של ה-actor.
2. **Tenant authenticity (hardening)** — כיום `X-Tenant-Id` מהימן-בלבד (תחת secret משותף יחיד הוא ניתן-לזיוף). הקשחה: per-tenant API keys (key-id → tenant+secret) ב-`hmacAuth.ts`.
3. **ייחוד `vin` per-tenant** — ה-`vin` ייחודי גלובלית; שני טננטים לא יכולים לחלוק VIN. תיקון: PK מורכב `(tenant_id, vin)`.

---

*תומלל מ-"Authentication vs Authorization — Complete Guide for Beginners" (M-SoftTech), ומופה לשכבת האבטחה של `leasing-api` בהמשך ל-`system-design-cheatsheet.md § 9` ו-`CTO_REVIEW.md`.*
