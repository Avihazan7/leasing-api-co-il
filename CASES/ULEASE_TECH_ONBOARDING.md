# ULease 🎯 — Onboarding למנהל מערכות הטכנולוגיה

**Module:** `CASES/ULEASE_TECH_ONBOARDING.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — קליטת Tech Lead.
**Integrates with:** `CASES/ULEASE_HIRING.md`, `CASES/ULEASE_SPEC.md`, `CASES/ULEASE_OUTBOUND_ENGINE.md`, `CASES/ULEASE_LAUNCH_CHECKLIST.md`, `DECISION_LOG.md`

> מטרה: שה-Tech Lead יבין את המערכת, יקבל גישות, **וישגר את ה-MVP תוך שבועיים**.

---

## 1. יום 0 — גישות והקמה
- [ ] חשבון Git + גישה לריפו (ה-OS הזה)
- [ ] גישת n8n + `ANTHROPIC_API_KEY` (Claude) + חשבונות Apollo/Smartlead
- [ ] גישת hosting + דומיינים (ULease.co.il, Leasing.co.il)
- [ ] סביבת dev מקומית + Cowork (ראו `COWORK_SETUP.md`)
- [ ] NDA + הבנת חיסיון IP (Deal Score / Match / תמחור)

## 2. יום 1 — רשימת קריאה ב-OS (לפי סדר)
1. `CLAUDE.md` — מפת המודולים · 2. `OPERATING_SYSTEM.md` — חוקים, ארכיטקטורה, היררכיית הכרעה
3. **`CASES/ULEASE_SPEC.md`** — האיפיון (הכי חשוב לך) · 4. `CASES/ULEASE.md` — עסקי + תחזית
5. `CASES/ULEASE_OUTBOUND_ENGINE.md` + שלד ה-n8n · 6. `CASES/ULEASE_FINANCE_INSURANCE.md` — חיתום + רגולציה
7. `CASES/ULEASE_METHODOLOGY.md` — המנגנון מאחורי Match/Deal Score · 8. `DECISION_LOG.md` — החלטות ורציונל

> בסוף יום 1: פגישת יישור עם אברהם (מוצר) ושירי (COO) — מה ה-MVP, מה הפער, מה דחוף.

---

## 3. תוכנית 30·60·90

| תקופה | מיקוד | יעדים |
|--------|--------|--------|
| **0–30 · MVP** | לאוויר! | אתר/אפליקציה · ingestion (CSV/API) · חדר-עסקה (e-sign + מקדמה) · מנויי Ultra · admin בסיסי · Ultra + 2 Masters (Match, Pricing) ב-assist |
| **31–60 · Scale** | אוטומציה | סוכנים ב-production (Financing, Negotiation, Guardian) · ניתוב מימון/ביטוח · חיווט מנוע ה-n8n · דשבורדים · מנוי Max |
| **61–90 · Harden** | יציבות | מכרז מחיר-שני (M7) · אבטחה/PCI · monitoring/audit · ביצועים/scale · error handling |

---

## 4. נורמות עבודה
- **כפיפות:** אברהם (מוצר/מו"פ) + שירי (COO).
- **Learn-vs-Delegate:** אברהם בעל החלטות מוצר + "החיבורים" + עיצוב סוכנים (מוצר); **אתה** בעל המימוש, infra, אבטחה, scale.
- **קצב:** demo שבועי (ship-before-perfect) · החלטות → `DECISION_LOG.md`.
- **חיסיון:** Deal Score / Match / תמחור = IP.

## 5. הגדרת הצלחה (90 יום)
MVP לאוויר ב-2 שבועות · עסקה דיגיטלית עובדת מקצה-לקצה · סוכנים assist→auto · מערכת יציבה ומנוטרת. (פירוט תפקיד: `ULEASE_HIRING.md`.)

## 6. העדיפות המיידית
👉 **צ'קליסט ההשקה** — `CASES/ULEASE_LAUNCH_CHECKLIST.md`. זה ה-30 הראשונים שלך, יום-אחר-יום.

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | Onboarding ראשוני — יום 0/1, רשימת קריאה, 30·60·90, נורמות | 2026-05-31 |

**Confidentiality.** מסמך פנימי חסוי — חלק מה-Claude OS של Avraham Bar Yochai Chazan.

— *End of CASES/ULEASE_TECH_ONBOARDING.md v1.0.0 —*
