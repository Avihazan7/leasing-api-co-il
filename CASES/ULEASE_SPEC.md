# ULease 🎯 Leasing.co.il — איפיון מוצר ומערכת (End-to-End Spec)

**Module:** `CASES/ULEASE_SPEC.md`
**Version:** 1.1.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — איפיון (Product & System Spec), נספח ל-`CASES/ULEASE.md`.
**Integrates with:** `CASES/ULEASE.md`, `CASES/ULEASE_METHODOLOGY.md`, `INVESTOR_RELATIONS.md`, `OPERATING_SYSTEM.md`, `MEMORY.md`
**Confidentiality:** מנגנוני **Deal Score**, **Match** ו**תמחור** הם IP ליבה (§6). מסומן בהתאם.

---

## תוכן עניינים
1. [חזון והיקף](#1-חזון-והיקף)
2. [שחקנים ופרסונות](#2-שחקנים-ופרסונות)
3. [ארכיטקטורת-על](#3-ארכיטקטורת-על)
4. [מסעות משתמש מקצה-לקצה](#4-מסעות-משתמש-מקצה-לקצה)
5. [מודולים פונקציונליים](#5-מודולים-פונקציונליים)
6. [מנוע Match · Deal Score · מכרז מחיר-שני (IP)](#6-מנוע-match--deal-score--מכרז-מחיר-שני-ip)
7. [מנוע Multi-agent: Ultra · Master · Max](#7-מנוע-multi-agent-ultra--master--max)
8. [מודל נתונים](#8-מודל-נתונים)
9. [אינטגרציות](#9-אינטגרציות)
10. [דרישות לא-פונקציונליות (NFR)](#10-דרישות-לא-פונקציונליות-nfr)
11. [מסכים עיקריים](#11-מסכים-עיקריים)
12. [שלבי פיתוח (Roadmap)](#12-שלבי-פיתוח-roadmap)
13. [KPIs](#13-kpis)
14. [Document Control](#document-control)

---

## 1. חזון והיקף

**חזון:** לבצע עסקת רכב חדש **דיגיטלית, מקצה-לקצה**, בין יבואן/ליסינג/מימון לבין לקוח — תוך דקות במקום שבועות, עם תמחור יעיל מבוסס תורת-המשחקים.

**היקף (In-Scope):** ingestion מלאי מהספקים → הצגה לביקוש (פרטי/B2B) ולמפיצים → התאמה (Match) ודירוג (Deal Score) → הצעה/מכרז → חדר-עסקה דיגיטלי (חתימה + מקדמה + מימון) → התחשבנות → דאטה ומנויים.

**מחוץ להיקף (כרגע):** רכב יד-שנייה C2C, ייבוא אישי פרטי, ביטוח עצמאי (רק כשותף פרסום/עמלה).

---

## 2. שחקנים ופרסונות

| שחקן | תיאור | מה רוצה |
|------|--------|----------|
| **ספק** (יבואן / ליסינג / מימון) | מזרים מלאי ל-APIs | לפנות מלאי 0 ק"מ/גיולים במהירות ובמרווח מיטבי |
| **לקוח פרטי / B2B2C** | רוכש רכב | רכב נכון, מחיר הוגן, עסקה מהירה ודיגיטלית |
| **מפיץ/דילר (מנוי B2B)** | רוכש כמויות און-ליין | זרם עסקאות, דאטה, יתרון במכרז |
| **Ops/Admin (ULease)** | תפעול, KYC, מחלוקות, חיוב | שליטה, אכיפת מדיניות, אנליטיקה |
| **AI Agents** | Ultra/Master/Max (§7) | להריץ את כל הצינור אוטומטית |

---

## 3. ארכיטקטורת-על

```
            ┌─────────────────────────────────────────────┐
SUPPLY  →   │  INGESTION APIs  (יבואן · ליסינג · מימון)    │
            └───────────────┬─────────────────────────────┘
                            ▼
            ┌─────────────────────────────────────────────┐
            │  CORE  ·  Catalog ▸ Match/DealScore ▸ Auction │  ← IP (§6)
            │        ·  Deal Room ▸ Financing ▸ Settlement  │
            └───────────────┬─────────────────────────────┘
                 ▲          ▼            ▲
   DEMAND ───────┘   ┌────────────┐     └────── DISTRIBUTORS (מנויים)
   (web/app)         │ Multi-agent │
                     │ Ultra·Master│ (§7)
                     │ ·Max        │
                     └────────────┘
            ┌─────────────────────────────────────────────┐
            │  PLATFORM  ·  Auth/KYC · Billing · Data/BI · │
            │              Notifications · Audit/Compliance │
            └─────────────────────────────────────────────┘
```

**עקרון:** כל אירוע (ליד, בקשת עסקה, מכרז) הוא **event** שעובר ב-Core ומתוזמר ע"י שכבת ה-Multi-agent.

---

## 4. מסעות משתמש מקצה-לקצה

**4.1 ספק (היצע):** התחברות → חיבור API / העלאת מלאי (CSV fallback) → קביעת מחיר-רצפה ומרווח → המלאי עולה לקטלוג → קבלת לידים/עסקאות → התחשבנות אוטומטית (עמלה מדורגת 1.1%–2.2% + מקדמה).

**4.2 לקוח פרטי / B2B2C:** חיפוש/סינון → דף רכב עם **Deal Score** → "קבל הצעה" → KYC קצר → **חדר עסקה**: בחירת מימון/ליסינג → אישור מקדמה → **חתימה דיגיטלית** → אישור עסקה → מסירה. *(ליד שלא נחתם → נמכר לספק ב-₪150.)*

**4.3 מפיץ/דילר (מנוי):** מנוי Ultra/Max → בקשת כמות/דגם → השתתפות ב**מכרז מחיר-שני** → זכייה → חדר עסקה מרוכז → דאטה ותובנות בלוח הבקרה.

**4.4 Admin/Ops:** ניטור pipeline עסקאות → אישורי KYC → טיפול במחלוקות → חיוב מנויים → ניהול תוכן וקמפיינים → אנליטיקה.

---

## 5. מודולים פונקציונליים

| # | מודול | תיאור | שלב |
|---|--------|--------|-----|
| M1 | **Catalog & Inventory** | קליטת מלאי (API/CSV), נורמליזציה, תמונות, זמינות | MVP |
| M2 | **Search & Match** | חיפוש, סינון, התאמת רכב-לקוח (§6) | MVP |
| M3 | **Deal Score** | דירוג כדאיות עסקה ללקוח/לפלטפורמה (§6, IP) | MVP→V1 |
| M4 | **Leads Marketplace** | לכידת ליד, תמחור, מכירה לספקים (₪150) | MVP |
| M5 | **Deal Room** | חתימה דיגיטלית, מקדמה, סטטוס עסקה | MVP |
| M6 | **Financing/Leasing** | חיבור למימון/ליסינג, הגשת בקשה, אישור | MVP→V1 |
| M7 | **Auction (Second-Price)** | מכרז כמויות למפיצים (§6) | V1 |
| M8 | **Subscriptions & Billing** | Ultra ₪4,500 / Max ₪7,700, חיוב חוזר | MVP |
| M9 | **Data & Insights** | לוחות בקרה, דאטה למנויים, BI פנימי | V1 |
| M10 | **Advertising** | קידום מחברות מימון/ביטוח/שירותי דרך | V1 |
| M11 | **Admin/Ops Console** | pipeline, KYC, מחלוקות, תוכן | MVP |
| M12 | **Settlement** | התחשבנות ישירה בין צדדים + עמלות | MVP→V1 |

---

## 6. מנוע Match · Deal Score · מכרז מחיר-שני (IP)

> 🔒 **חסוי — IP ליבה.** מתואר ברמה פונקציונלית; פרמטרים ומשקלים פנימיים אינם מתועדים כאן.

- **Match:** מתאים רכב ↔ לקוח לפי צרכים, תקציב, מימון, זמינות והעדפות (מודל Big Five + העשרה אינסטרומנטלית כשכבת UX/החלטה).
- **Deal Score:** ציון 0–100 לכל זיווג עסקה — משקלל מרווח לספק, התאמה ללקוח, סבירות סגירה וזמן-לעסקה. מניע ranking והמלצות.
- **מכרז מחיר-שני (Second-Price / Vickrey):** במכרזי כמויות למפיצים — **המציע הגבוה זוכה ומשלם את הצעת המקום השני**. יוצר חשיפת-אמת ותמחור יעיל (תורת המשחקים). מונע over-bidding ושומר על שוק בריא.

---

## 7. מנוע Multi-agent: Ultra · Master · Max

ארכיטקטורת סוכנים תלת-שכבתית — "**Ultra Master Max**":

| שכבה | תפקיד | סוכנים לדוגמה |
|------|--------|----------------|
| **🛰️ Ultra** | **Orchestrator** — מקבל event, מנהל state של העסקה מקצה-לקצה, מנתב למומחים | Deal Orchestrator, Routing |
| **🧠 Master** | **Domain Masters** — מומחי-תחום שמחליטים | Pricing/Margin, Match, **Negotiation**, Financing, Compliance, Content/Marketing |
| **⚙️ Max** | **Execution** — מבצעים פעולות בעולם | Offer-Builder, Contract/e-Sign, Financing-Submit, Inventory-Sync, Billing |
| **🛡️ Guardian** | **Safety/IP** — אכיפת מדיניות, חיסיון IP, audit | Compliance Guard |

**זרימה:** event → **Ultra** מתזמר → **Master** מחליט (תמחור/Match/מימון) → **Max** מבצע (הצעה→חוזה→מימון→חיוב) → **Guardian** מאמת ציות ורושם audit.

> שלב MVP: Ultra + 2 Masters (Match, Pricing) במצב **assist** (אדם מאשר). אוטומציה מלאה מתרחבת ב-V1/V2.

---

## 8. מודל נתונים

| ישות | שדות-מפתח | קשרים |
|------|-----------|--------|
| **Supplier** | id, type(importer/leasing/finance), terms, fee% | →Vehicles, →Settlements |
| **Vehicle** | id, supplierId, make/model/trim, km(0), price_floor, status | →Listing |
| **Listing** | id, vehicleId, public_price, score, availability | →Deal/Lead |
| **Customer** | id, type(private/B2B2C), KYC, profile(Big5) | →Lead, →Deal |
| **Distributor** | id, subscriptionTier, dataAccess | →Bid, →Deal |
| **Lead** | id, customerId, vehicleId, status, price(₪150) | →Sold-to-Supplier |
| **Deal** | id, parties, amount(~150K), take(מדורג 1.1%–7.77% לפי סוג), advance, status | →Contract, →Settlement |
| **Auction/Bid** | id, lot, bids[], winner, clearing_price(2nd) | →Deal |
| **FinancingApp** | id, dealId, provider, amount, decision | →Deal |
| **Subscription** | id, distributorId, tier, price, cycle | →Invoice |
| **Invoice/Payment** | id, amount, method, status | — |
| **AuditLog** | id, actor(agent/user), action, ts | (כל הישויות) |

---

## 9. אינטגרציות

| קטגוריה | אינטגרציה | שלב |
|----------|-----------|-----|
| **Supply** | APIs יבואנים/ליסינג/מימון (מלאי, מחיר, זמינות) | MVP (CSV fallback) |
| **Identity/KYC** | אימות ת"ז/חברה ישראלי | MVP |
| **Vehicle data** | מחירון (לוי יצחק), נתוני משרד התחבורה | V1 |
| **e-Signature** | חתימה דיגיטלית על חוזה | MVP |
| **Payments/Escrow** | כרטיס אשראי, העברה, מקדמה | MVP |
| **Financing/Leasing** | handoff לחברות מימון/ליסינג | MVP→V1 |
| **Insurance / Road** | שותפי פרסום/עמלה | V1 |
| **Comms** | SMS, Email, WhatsApp Business | MVP |

---

## 10. דרישות לא-פונקציונליות (NFR)

- **אבטחה:** הצפנה in-transit/at-rest, PCI-DSS לתשלומים, הרשאות מבוססות-תפקיד (RBAC).
- **פרטיות:** עמידה בחוק הגנת הפרטיות (ישראל) + GDPR ללקוחות רלוונטיים; מינימיזציית מידע.
- **זמינות/ביצועים:** יעד 99.9% uptime; חיפוש < 500ms; חדר-עסקה responsive.
- **קנה-מידה:** תמיכה בעשרות-אלפי פריטי מלאי ובמכרזים מקבילים.
- **Audit:** כל פעולת סוכן/משתמש נרשמת (מי, מה, מתי) — לצורכי ציות ומחלוקות.
- **⚠️ רגולציה (לבדיקה משפטית):** תיווך מימון/ביטוח עשוי לדרוש רישוי; הגנת הצרכן בעסקאות און-ליין. **מומלץ ייעוץ משפטי לפני השקה.**

---

## 11. מסכים עיקריים

| פורטל | מסכים |
|--------|--------|
| **לקוח (web/app)** | חיפוש · דף רכב + Deal Score · חדר-עסקה · מימון · חתימה · סטטוס |
| **ספק** | סטטוס API/מלאי · לידים/עסקאות · התחשבנות |
| **מפיץ/דילר** | בקשת כמות · מכרז · לוח דאטה/תובנות · מנוי |
| **Admin/Ops** | pipeline עסקאות · KYC · מחלוקות · חיוב · תוכן · אנליטיקה |

---

## 12. שלבי פיתוח (Roadmap)

| שלב | יעד | תוכן | מיפוי לתחזית |
|------|-----|------|--------------|
| **Phase 0 — MVP** | ≤ שבועיים · חצי שני יוני 26 | M1·M2·M4·M5·M8·M11 + Ultra+2 Masters (assist) + CSV/API ingestion + e-sign + מקדמה | בסיס יוני: 26 עסקאות |
| **Phase 1 — Scale** | Q3–Q4 2026 | מכרז מחיר-שני (M7), מנוי Max, Financing מלא (M6), Data/Insights (M9), Advertising (M10), הרחבת agents | ראמפ H2-2026 |
| **Phase 2 — Automate** | 2027 | אוטומציה מלאה Multi-agent, Deal Score מתקדם, אינטגרציות נוספות, scale | צמיחת 2027 |

---

## 13. KPIs

GMV · עסקאות/חודש · take-rate בפועל · המרת ליד→עסקה (בסיס 20%) · ARPU מנויים · CAC · churn · time-to-deal · דיוק Match · Deal Score → סגירה.

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | איפיון מוצר ומערכת ראשוני — מקצה-לקצה, Ultra·Master·Max, MVP→V2 | 2026-05-30 |
| 1.1.0 | יישום D-015: מנויי **Ultra/Max** (M8), עמלות מדורגות 1.1%–7.77% במודל הנתונים ובזרימת הספק | 2026-06-01 |

**Confidentiality.** מסמך זה וכל מנגנוני הליבה (Deal Score, Match, Pricing, Auction) הם IP חסוי של ULease 🎯 — חלק מה-Claude OS של Avraham Bar Yochai Chazan.

— *End of CASES/ULEASE_SPEC.md v1.1.0 —*
