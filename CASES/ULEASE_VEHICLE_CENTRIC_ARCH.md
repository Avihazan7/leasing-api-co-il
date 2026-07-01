# ULease 🎯 Leasing.co.il — ארכיטקטורת "רכב במרכז" (Vehicle-Centric Architecture)

**Module:** `CASES/ULEASE_VEHICLE_CENTRIC_ARCH.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — פסק-דין ארכיטקטוני (Architecture-of-Record), נספח-אב ל-`CASES/ULEASE_SPEC.md`.
**Integrates with:** `CASES/ULEASE_SPEC.md` (§3 · §5 · §8 · §12), `CASES/ULEASE.md`, `AI_SYSTEM_DESIGN.md`, `AI_DATA_VALIDATION.md`, `AI_MICROSERVICES.md`, `leasing-api/docs/specs/*` (הקוד)
**Confidentiality:** מנגנוני **Deal Score**, **Match**, **Supplier Trust** ותמחור הם IP ליבה — מתוארים כאן ברמה פונקציונלית בלבד (ראו `ULEASE_SPEC.md` §6).

> **פסק הדין בשורה אחת:** ULease לא נבנית סביב "לידים". היא נבנית סביב **רכב חדש כיחידת אמת**, ו**כרטיס רכב כיחידת המרה**. כל היתר — ספקים, מימון, ביטוח, GitHub, Vercel, Supabase, OpenAI, Airtable, Canva, Aris — מסתדרים סביב זה.

---

## תוכן עניינים

1. [השלד הקנוני](#1-השלד-הקנוני)
2. [המשולש הקדוש הכפול](#2-המשולש-הקדוש-הכפול)
3. [ארבע שכבות הקטלוג + מקור-אמת MOT](#3-ארבע-שכבות-הקטלוג--מקור-אמת-mot)
4. [כרטיס הרכב — חוזה האמון](#4-כרטיס-הרכב--חוזה-האמון)
5. [חלוקת אחריות בין המערכות](#5-חלוקת-אחריות-בין-המערכות)
6. [סכמת נתונים (ממופה לקוד הקיים)](#6-סכמת-נתונים-ממופה-לקוד-הקיים)
7. [זרימת מידע (Event-Driven)](#7-זרימת-מידע-event-driven)
8. [מפת ההתאמה — Conformance Map (דוקטרינה ↔ קוד קיים)](#8-מפת-ההתאמה--conformance-map)
9. [ביקורת סיכונים — אדום · צהוב · ירוק](#9-ביקורת-סיכונים)
10. [מה נבנה עכשיו — Backlog מתועדף](#10-מה-נבנה-עכשיו)

---

## 1. השלד הקנוני

המהלך הנכון הוא ציר יחיד, שכל אירוע במרקטפלייס זורם דרכו:

```
Vehicle Master Catalog OS → Vehicle Card → Offer Engine → DealIQ / Score Deal → Deal Room → Delivery Loop
```

1. **קטלוג רכבים חדשים** הוא בסיס האמון — מה קיים בשוק, מדויק ורשמי.
2. **כרטיס הרכב** הוא המקום שבו הלקוח מבין, משווה ומחליט (יחידת ההמרה).
3. **הצעה ≠ רכב.** רכב הוא אובייקט קטלוגי; **הצעה** היא יחידת המסחר: מחיר, ספק, זמינות, מימון, ק״מ, מקדמה, תוקף, SLA.
4. **DealIQ / Score Deal** מדרג את **ההצעה**, לא רק את הרכב.
5. **Deal Room** סוגר את העסקה: מסמכים, מימון, ספק, מסירה, שביעות רצון.
6. **Delivery Loop** — מסירה → משוב → תוכן → אמון חוזר.

מתיישב עם `ULEASE_SPEC.md`: ULease היא **שכבת אמון וטרנזקציה**, לא "עוד אתר לידים" — הלקוח בוחר רכב לפי צורך ותשלום חודשי, מקבל Score Deal מוסבר, וסוגר בדיל-רום דיגיטלי עד מסירה.

---

## 2. המשולש הקדוש הכפול

### משולש ההנדסה

| צלע | תפקיד | הגבול האסור |
|------|--------|--------------|
| **GitHub** | מקור-אמת לקוד, migrations, policies, CI/CD, CODEOWNERS | לא ניהול עסקי ידני |
| **Vercel** | שכבת ריצה: Frontend, API routes, Preview/Production | לא מקור נתונים · לא מחזיק state |
| **Supabase** | זיכרון המערכת: Postgres, RLS, Storage, Events, Audit | לא חושף service-role או טבלאות רגישות ללקוח |

**למה נכון:** Vercel מפרידה Preview (נוצר אוטומטית ב-PR/branch) מ-Production (הסביבה החיה); Supabase Branching מריצה clone/migrate/seed/deploy על כל commit לענף; GitHub Branch Protection מחייב reviews + status checks לפני merge לענף מוגן. שלושתן יחד = SDLC בטוח מקצה לקצה.

### משולש המסחר

| צלע | תפקיד |
|------|--------|
| **Catalog** | מה קיים בשוק: יצרן, דגם, גימור, שנה, הנעה, WLTP, קטגוריה |
| **Vehicle Card** | איך הלקוח מבין את הרכב והעסקה תוך 5–10 שניות |
| **Deal Room** | איך הופכים עניין לעסקה סגורה, מתועדת ומדידה |

זה המשולש שמייצר את ה"איך לא חשבו על זה קודם": לא עוד אתר שמציג רכבים, אלא **מערכת הפעלה שמנהלת את האמת סביב רכב חדש בישראל**.

---

## 3. ארבע שכבות הקטלוג + מקור-אמת MOT

מקור הבסיס: **משרד התחבורה / data.gov.il** — "תוצרים ודגמים של כלי רכב פרטי ומסחרי" (פרטי מ-1996, מסחרי מ-1998) + נתוני WLTP. אבל זהו **raw registry, לא קטלוג מסחרי** — אסור להציגו ללקוח כמות-שהוא. לכן ארבע שכבות:

| # | שכבה | תפקיד | ישויות |
|---|-------|--------|---------|
| 1 | **Raw MOT** | שומר בדיוק את מה שהגיע ממשה"ת, ללא פרשנות | `raw_mot_json` (payload גולמי) |
| 2 | **Normalization** | מנקה שמות, מאחד יצרנים, מפריד דגם/גימור/הנעה | makes · models · trims · specs |
| 3 | **Commercial Catalog** | רק רכבים רלוונטיים למכירה/ליסינג בישראל עכשיו | commercial entry: שנה · גימור · קטגוריה · תמונות · SEO |
| 4 | **Offer** | הצעות ספקים מעל הרכב | price · monthly · down · km · availability · valid_until · DealIQ |

**עקרון ברזל (`ULEASE_SPEC.md` §8, מחודד):** **Offer ≠ Vehicle.** רכב אחד נושא N הצעות שונות מספקים שונים. ערבוב שתי הישויות = שגיאת-שורש ארכיטקטונית.

---

## 4. כרטיס הרכב — חוזה האמון

כרטיס הרכב הוא **מפקד המחלקה** של כל המסע. הוא לא UI — הוא **חוזה אמון** שעונה על ארבע שאלות:

> **כמה זה עולה לי בחודש? · מתי אני מקבל את הרכב? · למה זו עסקה טובה? · מי עומד מאחורי ההצעה?**

| אזור בכרטיס | תוכן חובה |
|--------------|-----------|
| **Hero** | תמונה/וידאו/360/3D · יצרן · דגם · גימור · שנה |
| **מחיר** | מחיר מחירון · מחיר ספק · חיסכון מוערך |
| **תשלום** | תשלום חודשי · מקדמה · תקופה · ק״מ שנתי |
| **זמינות** | אספקה מיידית / עד 14 יום / מלאי מוגבל / הזמנה + **freshness** ("עודכן לפני…") |
| **DealIQ** | ציון 0–100 + **הסבר אנושי קצר** |
| **אמון ספק** | דירוג ספק · SLA תגובה · שיעור מסירות בזמן |
| **מימון** | זכאות משוערת · מסמכים נדרשים · הערת אי-התחייבות |
| **CTA** | כפתור אחד: "בדוק התאמה וסגור דיל-רום" |

**כלל הברזל (Rule of Iron):**
- `VehicleCard` **לא** מחשב מחיר.
- `DealScoreBadge` **לא** מחשב Score.
- `page.tsx` **לא** מדבר ישירות עם service-role.
- כל חישוב מסחרי עובר דרך `/lib/scoring` או API server-side (מקור-אמת אחד, auditable).

הטעות הקריטית שיש להימנע ממנה: להפוך את הכרטיס לקטלוג-תמונות. הכרטיס עונה על ארבע השאלות — לא מציג גלריה.

---

## 5. חלוקת אחריות בין המערכות

| מערכת | אחריות נכונה | הגבול האסור |
|--------|--------------|--------------|
| **GitHub** | קוד, PR, CODEOWNERS, migrations, reviews, CI | ניהול ספקים/הצעות ידני |
| **Vercel** | ריצה, Preview, Production, Edge/API, ENV | אינו מחזיק state |
| **Supabase** | DB, RLS, Storage, Auth, Audit, Outbox | לא חושף service-role ללקוח |
| **OpenAI / LLM** | הסברי DealIQ, ניסוח SEO, סיווג קטגוריות, זיהוי חריגות, עוזרי תפעול | **לא קובע מחיר סופי · לא חותם · לא מחייב ספק** |
| **Airtable** | Backoffice קל: ספקים, תוכן, בקרת קטלוג, רשימות עבודה | לא source-of-truth לעסקאות |
| **Canva** | תבניות מותג, מודעות, באנרים, כרטיסי-דגם, קמפיינים | לא מחזיק נתוני מחיר חיים (הקטלוג מזין את Canva, לא להפך) |
| **Aris** | מיפוי תהליכים, Digital Twin, Process Mining, SOP | לא מחליף את המערכת התפעולית |
| **U.M.M OS** | Orchestrator, Events, Agents, Governance | לא עוקף Human-in-the-Loop |

**עקרון:** OpenAI/LLM הוא שכבת **Agent/Tool** (Function Calling + Structured Outputs) — מצוין להסבר, סיווג, SEO וזיהוי חריגות; **אף פעם** לא לקביעת עסקה מחייבת. זה בדיוק הגבול שאוכף `dealExplainer` בקוד (ראו §8).

---

## 6. סכמת נתונים (ממופה לקוד הקיים)

הדוקטרינה כבר ממומשת ברובה במיגרציית `supabase/migrations/202607010001_vehicle_catalog_2026.sql`. המיפוי הקנוני דוקטרינה → טבלה בפועל:

| ישות דוקטרינרית | טבלה/אובייקט בפועל (leasing-api) | הערה |
|------------------|-----------------------------------|------|
| Raw MOT | `vehicle_master_2026.raw_mot_json` (jsonb + GIN) | payload גולמי נשמר בשלמותו |
| Normalization (makes/models/trims/specs) | `vehicle_master_2026` + `vehicle_specs_2026` + `vehicle_brands_2026` | `motNormalizer.ts` — ~50+ aliases, נרמול דלק/הנעה |
| Commercial Catalog | שדות מסחריים ב-`vehicle_master_2026` (`canonical_slug`, `hero_image_url`, `category`) | model_year מוגבל ל-2026 |
| **Offer** | **`supplier_offers_2026`** (offer_type · offer_price · monthly · down · km · `valid_until` · status · `deal_score`) | 8 סוגי הצעה · lifecycle draft→active→expired/sold_out |
| Media | `vehicle_media_assets_2026` (14 סוגים: hero · 360 · `3d_model_glb`… · `license_status` · attribution) | `202607050001_media_attribution.sql` |
| Suppliers | `suppliers_2026` (`supplier_type` · `verification_status`) | public-read רק ל-`verified` |
| Inventory (VIN) | `vehicle_inventory_units_2026` + `zero_km_disclosures_2026` | הפרדת דגם (קטלוג) מ-VIN (מלאי) |
| **Read Model** | **`vehicle_page_projection_2026`** (`active_offers_count` · `lowest_monthly_payment` · `best_offer_id` · `payload_json`) | ציבורי, PII-free, secret-free |
| Audit | `catalog_audit_log_2026` + `audit_log` | after_json; **חסר pre-image snapshot** (ראו §9) |

**הטבלה החשובה ביותר ל-frontend היא `vehicle_page_projection_2026`** — מהירה, ציבורית, נקייה, בלי PII ובלי סודות מסחריים.

---

## 7. זרימת מידע (Event-Driven)

```
data.gov.il (CKAN / MOT)
        ↓  src/sync/ckanClient.ts
raw_mot_json  (vehicle_master_2026)
        ↓  src/sync/motNormalizer.ts
makes / models / trims / specs
        ↓  media enrichment + supplier offers
supplier_offers_2026
        ↓  src/offers2026/dealScore.ts + best_offer selection
vehicle_page_projection_2026   ← src/events/outbox.ts → outboxRelay → projection
        ↓
Vehicle Card / Catalog Grid   (public read via API, RLS-scoped)
        ↓
Lead / Deal Room
        ↓
Events / Outbox / Analytics / Supplier Billing
```

כל פעולה (לקוח, ספק, מימון, מסירה) היא **event** שנרשם, מפעיל סוכן, מעדכן סטטוס ומייצר אנליטיקה. המימוש: `src/events/outbox.ts` (כתיבה טרנזקציונית עם version), `src/events/outboxRelay.ts` (at-least-once, version-ordered), `src/projection/vehicleProjection.ts` (בונה את ה-read model מ-`vehicle.*` events).

---

## 8. מפת ההתאמה — Conformance Map

> מיפוי כן ומגובה-קוד בין הדוקטרינה לבין מה שכבר קיים ב-`leasing-api` (נכון ל-1.7.2026). **~75% מהדוקטרינה כבר בנוי.** זה לא greenfield — זה יישור והשלמה.

### 🟢 ירוק — קיים ומבוסס

| אלמנט בדוקטרינה | מימוש קיים |
|------------------|------------|
| מקור-אמת MOT (לא demo) | `src/sync/ckanClient.ts` — fetch חי מ-data.gov.il · `raw_mot_json` נשמר · `motNormalizer.ts` דטרמיניסטי. **אין demo-data fallback.** |
| Offer ≠ Vehicle | `supplier_offers_2026` ישות נפרדת · `src/offers2026/offerTypes.ts` (8 סוגים · lifecycle) · `valid_until` + בדיקת חלון-תוקף (`offers2026Repository.ts`) |
| DealIQ דטרמיניסטי שמדרג את ה**הצעה** | `src/offers2026/dealScore.ts` — `calculateDealScore2026` (discount 35 + completeness 15 + supplier-trust 15 + delivery 10 + zero-km 10 + freshness 10 + media 5) · פונקציה טהורה · `deal_score` נשמר |
| Rule of Iron (AI לא ממציא מספרים) | `src/explain/dealExplainer.ts` — LLM מנסח בלבד ו**מאמת כל מספר** מול המנוע (fallback קשיח אם ה-LLM המציא מחיר/APR/score) · `sealDealScore()` מסיר breakdown לצרכן |
| אמון ספק (doctrine "צהוב" → בפועל ירוק) | `src/engines/supplierTrust.engine.ts` — כיווץ בייסיאני, 0–100 + confidence + reasons |
| Read Model ציבורי · PII-free | `vehicle_page_projection_2026` · rebuild אירועי (`POST /api/catalog/2026/rebuild-projections`) · רק אגרגטים (lowest_monthly, best_offer_id) |
| RLS / בידוד-tenant / אין חשיפת service-role | RLS enabled על כל טבלאות `*_2026` · policies public-read מסוננות ל-`active`/`verified` · `20260630120000_consolidate_vehicle_read_model_rls.sql` |
| Media + רישוי | `vehicle_media_assets_2026` (hero/360/glb) · `license_status` · `license_name`/`attribution` |
| Events / Outbox / Audit | `src/events/outbox.ts` · `outboxRelay.ts` · `catalog_audit_log_2026` + `audit_log` (SECURITY DEFINER trigger) |
| מבנה-עסקה (win-win-win) | `src/engines/structureDeal.engine.ts` — מדרג 5 מבנים, שער Pareto לפני המלצה · `src/contracts/*` יומן חוזים append-only |

### 🟡 צהוב — חלקי, לשיפור לפני Scale

| אלמנט | מצב | הפער |
|-------|-----|------|
| `offer_history` — ראיית "מה בדיוק ראה הלקוח כשפנה" | חלקי | `catalog_audit_log_2026` מתעד מוטציות (after_json) אך **אין pre-image snapshot** ברמת-שדה בזמן הפנייה |
| HITL — שער-אדם לפני פעולה מחייבת | חלקי | `governance.guard()` + kill-switches קיימים, וה-AI advisory (orchestrator מחזיר המלצות) — אך **אין gate מפורש לאישור-אדם** לפני שספק מחייב מחיר/חותם |
| הסבר אנושי ל-DealIQ 2026 | חלקי | ל-`scoreDeal` הישן יש `reasons[]` בעברית; ל-`calculateDealScore2026` אין עדיין מערך reasons |
| Match-score / ranking-policy מתועד | חלקי | דירוג קיים (`best_offer_id`: deal_score DESC, monthly ASC) אך **אין מנוע match מפורש או מסמך ranking-policy** |
| Deal-lifecycle events | חלקי | `vehicle.*` events מחוברים ל-projection; אירועי supplier-commit / finance / delivery **טרם נצפו** |

### 🔴 אדום — חסר (הבידול עצמו)

| אלמנט | מצב | משמעות |
|-------|-----|--------|
| **Deal Room** | **חסר לגמרי** — אפס hits בקוד/מיגרציות | ה"מיני-Deal-Room" של כל כרטיס — timeline · checklist · מסמכים · מימון · מסירה · שביעות-רצון — הוא **הבידול**. `structureDeal` + `dealContractRepository` צמודים אך אינם ה-Deal-Room. |
| **Vehicle Card / קטלוג ציבורי (Frontend)** | **חסר** — קיים רק `app/brain/page.tsx` (קונסולת ops פנימית) | יחידת ההמרה אין לה חזית. ה-read model וה-API הציבורי כבר מזינים אותה — צריך לבנות את `VehicleCard`/`DealScoreBadge`/`CatalogGrid`. |

---

## 9. ביקורת סיכונים

### אדום — חוסם עלייה רצינית
1. **Demo data ב-Production** — *לא רלוונטי כרגע:* המקור חי (data.gov.il). לשמור כך.
2. **Vehicle ו-Offer מעורבבים** — *נמנע:* `supplier_offers_2026` ישות נפרדת. לשמר את ההפרדה בכל פיצ'ר חדש.
3. **service-role/טבלאות רגישות חשופות** — *מבוקר:* RLS על הכל + public-read מסונן. לאכוף RLS על כל טבלה/view חדשים ולהגביל `EXECUTE` לפונקציות.
4. **אין `offer_history`** — 🟡 **פער פתוח:** יש audit-log אך אין snapshot ברמת-שדה בזמן הפנייה. תשתית ראייתית = חובה לפני scale.
5. **AI בלי Human-in-the-Loop** — 🟡 **פער פתוח:** ה-AI advisory ומגודר, אך שער-אדם מפורש לפני חיוב/חתימה טרם קיים.

### צהוב — לשפר לפני Scale
מספיק תמונות איכותיות לכל דגם · הסבר DealIQ 2026 · availability freshness בחזית · הפרדת public מ-supplier/private (קיימת ב-RLS, חסרה בחזית) · canonical SEO מלא לכל יצרן/דגם/גימור.

### ירוק — הכיוון נכון
GitHub/Vercel/Supabase = בסיס נכון · U.M.M Marketplace OS = חזון נכון · ההתעקשות על קטלוג רכבים חדשים = נכונה אסטרטגית · כרטיס רכב + Deal Room = הבידול האמיתי.

---

## 10. מה נבנה עכשיו

Backlog מתועדף שנגזר ישירות מ-§8–§9. **הבנייה בפועל היא הכרעת Tech Lead + אישור מייסד — לא נכללת במודול התיעוד הזה.**

| # | פריט | סוג | עדיפות | סיכון |
|---|------|-----|---------|--------|
| 1 | **Deal Room** — טבלה + מודול (`deal_rooms`, timeline, checklist, מסמכים, מימון, מסירה) | migration + code | 🔴 גבוהה | בינוני |
| 2 | **Vehicle Card / CatalogGrid** — חזית ציבורית מעל `vehicle_page_projection_2026` | frontend | 🔴 גבוהה | נמוך (ה-API קיים) |
| 3 | **`offer_history`** — snapshot ברמת-שדה בזמן הפנייה (תשתית ראייתית) | migration | 🟡 בינונית | נמוך (אדיטיבי) |
| 4 | **HITL gate** — אישור-אדם מפורש לפני חיוב/חתימה/commit-ספק | code (governance) | 🟡 בינונית | בינוני |
| 5 | **`ranking-policy` + match-score** — לתעד ולחלץ את הדירוג למנוע מפורש | code + doc | 🟡 בינונית | נמוך |
| 6 | **DealIQ 2026 `reasons[]`** — הסבר אנושי בעברית ל-`calculateDealScore2026` | code | 🟡 נמוכה | נמוך |

**מסקנת רמטכ״ל:** השלב הבא של Leasing.co.il אינו עוד UI ואינו עוד AI. הוא **להפוך את קטלוג הרכבים החדשים בישראל ל-Source-of-Truth מסחרי, ולהפוך כל כרטיס רכב למיני-Deal-Room.** לא "מצאתי רכב" — אלא: *מצאתי רכב, הבנתי כמה הוא באמת עולה לי בחודש, ראיתי למה העסקה טובה, מי הספק, מתי האספקה, מה המימון, ופתחתי דיל-רום לסגירה.* זה ה"איך לא חשבו על זה קודם": החיבור — קטלוג-אמת + כרטיס-עסקה + דירוג-אמון + דיל-רום + ספקים + מימון + מסירה — במערכת OS אחת.

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | רישום ראשוני (D-070): דוקטרינת "רכב במרכז" כ-Architecture-of-Record — 10 סעיפים כולל **מפת התאמה מגובת-קוד** (§8) בין הדוקטרינה ל-`leasing-api` (🟢 ~75% בנוי · 🟡 5 פערים חלקיים · 🔴 Deal Room + Vehicle Card חסרים) | 2026-07-01 |

**Confidentiality.** מסמך פנימי חסוי — חלק מה-Claude OS של Avraham Bar Yochai Chazan.

— *End of CASES/ULEASE_VEHICLE_CENTRIC_ARCH.md v1.0.0 —*
