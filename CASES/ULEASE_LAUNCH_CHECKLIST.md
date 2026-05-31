# ULease 🎯 — צ'קליסט השקה (שבועיים)

**Module:** `CASES/ULEASE_LAUNCH_CHECKLIST.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — צ'קליסט השקה תפעולי.
**Integrates with:** `CASES/ULEASE_SPEC.md` (Phase 0), `CASES/ULEASE_TECH_ONBOARDING.md`, `CASES/ULEASE_FINANCE_INSURANCE.md`, `CASES/ULEASE_OUTREACH_SCRIPTS.md`

> **יעד:** לאוויר עם עסקאות אמיתיות ב**חצי השני של יוני 2026**. בעלים: A=אברהם · S=שירי · T=Tech Lead.

---

## 1. דומיין ומותג
- [ ] רכישת **ULease.co.il** (S) · חיבור **Leasing.co.il** (redirect/branding) (T)
- [ ] DNS + SSL + אימייל (MX, כתובות @ULease) (T)
- [ ] לוגו: ULease 🎯 + Leasing.co.il כדומיין-מאסטר בגלישה (A)

## 2. חברה ומשפטי
- [ ] הקמת חברה — **השבוע** (S) · חשבון בנק + סליקה
- [ ] תקנון, מדיניות פרטיות, תנאי שימוש (חוק הגנת הפרטיות + הגנת הצרכן)
- [ ] 🔴 **ייעוץ משפטי** למודל החיתום (מימון/ביטוח דרך שותפים מורשים — `FINANCE_INSURANCE.md` §8)
- [ ] עמידה בחוק הספאם לפני outreach בנפח

## 3. טק / MVP (Phase 0)
- [ ] אתר + אפליקציה לאוויר (T)
- [ ] **Ingestion** מספקים — API + נפילה ל-CSV (T)
- [ ] קטלוג + חיפוש + דף רכב עם **Deal Score** (T)
- [ ] **חדר-עסקה:** חתימה דיגיטלית + מקדמה + handoff מימון (T)
- [ ] לכידת ליד + מכירת ליד (₪150) (T)
- [ ] מנויי **Pro** + חיוב (T)
- [ ] קונסולת **Admin** בסיסית (pipeline, KYC) (T)
- [ ] **Ultra + 2 Masters** (Match, Pricing) ב-assist (T)

## 4. תוכן והיצע
- [ ] Landing + הצעת ערך (A) · עמוד מנויים לדילרים (A)
- [ ] **מלאי 7 הספקים** טעון ומאומת (A + T)
- [ ] תמחור גלוי: עסקה / ליד / מנוי (A)

## 5. Outreach מוכן
- [ ] סקריפטים מותאמים לכל סגמנט (`ULEASE_OUTREACH_SCRIPTS.md`) (A)
- [ ] שלד ה-n8n מיובא ורץ ב-**assist** (אדם מאשר שליחה) (A + T)

## 6. מדידה
- [ ] Analytics בסיסי + מעקב funnel (T)
- [ ] דשבורד KPIs: עסקאות · לידים · reply/meeting rate · CPM (T)

## 7. שערי Go-Live (QA לפני שמפעילים)
- [ ] עסקה אחת **מקצה-לקצה** עברה בהצלחה (חיפוש→חתימה→מקדמה)
- [ ] תשלום/מקדמה נבדק בסביבת אמת
- [ ] מובייל responsive · זמני טעינה סבירים
- [ ] גיבוי + מנגנון rollback
- [ ] פרטיות/תנאים מפורסמים

---

## 8. לוח שבועיים

| שבוע | מוקד | בעלים |
|------|------|--------|
| **שבוע 1** | חברה + דומיינים + תשתית + ingestion + שלד אתר | S (חברה/דומיין) · T (תשתית) |
| **שבוע 2** | חדר-עסקה + מנויים + admin + טעינת מלאי + QA → **Go-Live** | T (טק) · A (תוכן/מלאי) |

> עיקרון (מיומנות #6): **שגר את ה-MVP, אל תחכה לשלמות.** עסקה אמיתית אחת > הדגמה מושלמת.

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | צ'קליסט השקה ראשוני — דומיין, משפטי, MVP, תוכן, outreach, QA, לוח שבועיים | 2026-05-31 |

**Confidentiality.** מסמך תפעולי חסוי — חלק מה-Claude OS של Avraham Bar Yochai Chazan.

— *End of CASES/ULEASE_LAUNCH_CHECKLIST.md v1.0.0 —*
