# ULease 🎯 — מפת אוטומציות AI לפי פונקציה עסקית

**Module:** `CASES/ULEASE_AUTOMATION_MAP.md`
**Version:** 1.3.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — Backlog אוטומציות מתועדף (Business layer, תחת CASES).
**Source:** מבוסס על מסגרת *"546 AI Automation Ideas"* (AI Matt · Next Step Agents) + *"31 Claude Skills For Small Businesses"* (Anthropic plugin pack) — מסונן ומותאם ל-ULease.
**Integrates with:** `CASES/ULEASE_SPEC.md`, `CASES/ULEASE_OUTBOUND_ENGINE.md`, `AI_TYPES.md`, `AI_PROCESS_INTELLIGENCE.md`, `CASES/ULEASE_DASHBOARD.html`

> **הפילוסופיה:** רוב האנשים עוצרים בפרומפטים. מעטים בונים את **המערכת שמריצה את העסק**. Build systems · Own value · **Owned, not rented** — זה בדיוק מה ש-ULease בונה.

---

## מקרא
✅ **בנוי/מאופיין** (והיכן) · 🔜 **MVP** (עד ההשקה) · **V1** (Q3–Q4 26) · **V2** (2027)

---

## 1. 📈 מכירות ושיווק

| אוטומציה | מה היא עושה ל-ULease | סטטוס |
|-----------|----------------------|--------|
| Lead Scoring Agent | ניקוד לידים (Haiku) | ✅ מנוע n8n שכבה 03 |
| AI SDR / Outreach Agent | פנייה אוטומטית לספקים | ✅ מנוע n8n + סקריפטים |
| Deal Desk Assistant | חדר-עסקה דיגיטלי | ✅ איפיון M5 |
| Competitive Pricing Assistant | תמחור מול מחירון/שוק | 🔜 MVP (Deal Score) |
| Churn Prediction | חיזוי נטישת מנויים | V1 |
| ROI Calculator for Prospects | מחשבון חיסכון לקונה (כמה חסכת מול מחירון) | V1 — כלי שיווקי חזק |
| A/B Testing Recommendations | אופטימיזציית הודעות | ✅ מנוע n8n שכבה 04 |
| Deal-to-Content Generator | עסקה סגורה → סיפור עסקה אנונימי (Sonnet) → SEO + GEO — הדלק של הלופ האורגני | V1 — מנוע הביקוש צמתים 10–12 |
| SEO/GEO Rank Monitor | ניטור יומי: דירוגי גוגל + ציטוט בתשובות AI (Claude/ChatGPT/Perplexity) | V1 — מנוע הביקוש צומת 13 |

## 2. 🤝 קליטת לקוחות (Onboarding)

| אוטומציה | ל-ULease | סטטוס |
|-----------|----------|--------|
| Eligibility & KYC Checker | אימות זהות וזכאות | ✅ חיתום דיגיטלי שלב 1 |
| Application Guidance Bot | ליווי בקשת מימון | ✅ חיתום שלב 3 |
| Document Collection Assistant | איסוף מסמכי עסקה | 🔜 MVP |
| Welcome Journey Orchestrator | מסע קליטת דילר/מנוי חדש | V1 |

## 3. 🎧 שירות לקוחות

| אוטומציה | ל-ULease | סטטוס |
|-----------|----------|--------|
| Knowledge-base Q&A Bot | שאלות על רכבים/תהליך/מימון; משמש גם כ-**AI Receptionist** במנוע הביקוש (צומת 16) — עונה, מסנן וקובע פגישה | V1 (RAG) |
| Order Status Tracker | סטטוס עסקה ומסירה | 🔜 MVP (חדר-עסקה) |
| Sentiment & Escalation Monitor | ניטור תגובות והסלמה | ✅ Reply Handling (שכבה 06) |
| Complaint Trend Analyzer | מגמות תלונות | V2 |

## 4. ⚙️ תפעול

| אוטומציה | ל-ULease | סטטוס |
|-----------|----------|--------|
| Fraud Detection Agent | זיהוי הונאות בעסקאות | ✅ Guardian (איפיון §7) |
| Workflow Automation Designer | תכנון תהליכים | ✅ n8n |
| Compliance Reporting Copilot | ציות: ספאם/פרטיות/רישוי | 🔜 MVP (דגלים קיימים) |
| Incident Investigation Assistant | תחקור תקלות | V1 |

## 5. 💰 כספים

| אוטומציה | ל-ULease | סטטוס |
|-----------|----------|--------|
| Loan Underwriting Agent | חיתום מימון | ✅ ULEASE_FINANCE_INSURANCE |
| Deal Analyzer Modeler | ניתוח כדאיות עסקה | ✅ Deal Score |
| Cash Flow Monitor | מעקב תזרים | ✅ דשבורד |
| Payment Reconciliation Bot | התאמת תשלומים ועמלות (1%, origination) | V1 |
| Invoice Extraction Bot | קליטת חשבוניות ספקים | V1 |
| P&L Commentary Drafter | פרשנות דוחות אוטומטית | V2 |

## 6. 👥 משאבי אנוש

| אוטומציה | ל-ULease | סטטוס |
|-----------|----------|--------|
| Job Description Generator | תיאורי תפקיד | ✅ ערכת הגיוס |
| Onboarding Coach | קליטת עובד | ✅ Tech Lead Onboarding |
| Interview Scheduler Bot | תיאום ראיונות | V1 |

## 7. 💻 IT

| אוטומציה | ל-ULease | סטטוס |
|-----------|----------|--------|
| System Health Monitor | ניטור בריאות המערכת | ✅ מנוע n8n (Health) |
| Security Alert Triage Bot | טריאז' התראות אבטחה | V1 (Guardian) |
| Backup & DR Monitor | גיבוי והתאוששות | 🔜 MVP (שער Go-Live) |

## 8. 📦 שרשרת אספקה (= צד ההיצע/מלאי)

| אוטומציה | ל-ULease | סטטוס |
|-----------|----------|--------|
| Inventory Management Agent | ניהול מלאי ספקים | ✅ Ingestion (M1) |
| Demand Sensing Assistant | חיזוי ביקוש לדגמים | V1 — מזין את המכרז |
| Stock-out / Aging Risk Predictor | חיזוי התיישנות מלאי (0 ק"מ!) | **V1 — קריטי לארביטראז'** |
| Supplier Risk Insight Agent | סיכון ריכוז ספקים | V1 |

## 9. 🤝 ספקים ושותפים

| אוטומציה | ל-ULease | סטטוס |
|-----------|----------|--------|
| Vendor Qualification Agent | סינון ICP ספקים | ✅ מנוע n8n שכבה 02 |
| Vendor Onboarding Assistant | קליטת ספק White-Glove | ✅ Playbooks |
| Vendor Scorecard Analyzer | דירוג ביצועי ספקים | V1 |
| Partner Contract / SLA Monitor | מעקב חוזים ו-SLA | V2 |

## 10. 🔗 רוחבי (Cross-Function)

| אוטומציה | ל-ULease | סטטוס |
|-----------|----------|--------|
| Dashboard Builder Agent | דשבורד מנהלים | ✅ ULEASE_DASHBOARD |
| Forecasting Copilot | תחזית פיננסית | ✅ ULEASE_FORECAST |
| KPI Tracking Assistant | מעקב מדדים | ✅ דשבורד |
| Executive Briefing Bot | תקציר מנהלים שבועי אוטומטי | **V1 — קל ושווה** |
| Trend & Anomaly Detector | זיהוי מגמות/חריגות בשוק | V2 |
| Compliance Monitor | ניטור ציות שוטף | V1 |

---

## 11. 🔌 קיצור הדרך: 31 ה-Skills המוכנים של Anthropic

Anthropic שחררה חבילת **31 Claude Skills לעסקים קטנים** שמתחברת ל-12 כלים (Gmail · QuickBooks · HubSpot · Stripe · Slack · Calendar · Canva · PayPal · Drive · Microsoft 365 · DocuSign · Square). חלק מהאוטומציות שתוכננו כ-V1/V2 במפה **ניתנות להתקנה היום** — בלי לבנות:

| אוטומציה מהמפה | סטטוס קודם | ה-Skill המוכן | מתחבר ל־ |
|------------------|:-----------:|----------------|-----------|
| Executive Briefing Bot (רוחבי) | V1 | `/business-pulse` · `/monday-brief` · `/friday-brief` | Gmail · Calendar · QuickBooks |
| Cash Flow Monitor (כספים) | ✅ דשבורד | `/cash-flow-forecast` — תחזית 30/60/90 יום מהסליקה | Stripe · PayPal |
| Payment Reconciliation (כספים) | V1 | `/month-end-prep` · `/close-month` | QuickBooks · Stripe |
| Invoice Extraction (כספים) | V1 | `/invoice-chase` — מעקב חייבים ותזכורות | QuickBooks |
| P&L Commentary (כספים) | V2 | `/close-month` — סוגר חודש וכותב נרטיב רווח/הפסד | QuickBooks |
| Margin Analyser (תמחור) | 🔜 MVP | `/margin-analyser` · `/price-check` | Stripe |
| CRM Cleanup + Lead Triage (מכירות) | ✅ n8n | `/lead-triage` · `/crm-cleanup` · `/sales-brief` | HubSpot |
| Complaint Trend Analyzer (שירות) | V2 | `/customer-pulse` · `/handle-complaint` · `/ticket-deflector` | Gmail · Slack |
| Job Description Generator (HR) | ✅ ערכה | `/job-post-builder` — מודעה + שאלות סינון | DocuSign |
| Partner Contract / SLA Monitor (ספקים) | V2 | `/contract-review` — דגלים אדומים בחוזי ספקים | Drive · DocuSign |
| קמפיינים (שיווק) | 🔜 | `/content-strategy` · `/run-campaign` | Canva · HubSpot |

**המשמעות לרודמאפ:** לפחות **5 אוטומציות V1/V2 הופכות ל"התקן עכשיו"** — בעיקר בכספים ובחוזים. ההמלצה: שירי (Ops) מתקינה את חבילת ה-Briefings + Money בשבוע ההשקה; ה-Skills מגשרים עד שהפלטפורמה מחליפה אותם.

> ⚠️ **הסתייגות:** ה-Skills רצים על הכלים העסקיים (QuickBooks, Stripe…) — הם פותרים את **התפעול של ULease כעסק**, לא את המוצר. את המוצר (Deal Score, מכרז, חדר-עסקה) בונה ה-Tech Lead.

---

## 12. 📏 שכבת המדידה — ROI לכל אוטומציה (D-040)

> **מלכודת ה-56%** (`AI_PROCESS_INTELLIGENCE.md` §1): רוב המנהלים *מאמינים* שה-AI שלהם מחזיר את ההשקעה — ולא מודדים. המפה הזו לא עוצרת ברשימת אוטומציות; כל אוטומציה שעולה לאוויר נמדדת.

**הנוסחה לכל אוטומציה:**

| צד | מה נספר | דוגמה (Lead Scoring, מנוע n8n שכבה 03) |
|-----|----------|------------------------------------------|
| **עלות** | שעות בנייה (חד-פעמי, מופחת על 6 חודשים) + טוקנים/תשתית (חודשי) | הקמה + ~₪40/חודש Haiku |
| **תשואה** | שעות שנחסכו · לידים שהומרו · עסקאות שנוספו — **במספרים, לא בתחושה** | ~3 שעות סינון ידני בשבוע |
| **ROI** | תשואה חודשית ÷ עלות חודשית | נמדד מהשקה |

**שלושת הכללים:**

1. **אין עלייה לאוויר בלי baseline** — לפני שהאוטומציה רצה, מתעדים כמה זמן/כסף התהליך עולה ידנית. בלי baseline אין השוואה.
2. **כלל 90 הימים** — אוטומציה שלא החזירה את עלותה תוך 90 יום: מושהית, מתוקנת או נמחקת. אין "אולי בהמשך".
3. **המדידה בדשבורד, לא בזיכרון** — מדדי ה-ROI מצטרפים לשכבת ה-Measurement (מנוע n8n שכבה 07) ומדווחים בדשבורד המנהלים.

> ⚠️ **הדרישה החדשה:** שלוש ההזדמנויות הבאות (Aging Predictor · ROI Calculator · Briefing Bot) נכנסות לבנייה **רק עם אומדן ROI כתוב מראש** — עלות צפויה, תשואה צפויה, ותאריך בדיקת 90 הימים.

---

## סיכום: איפה אנחנו על המפה

| | כמות |
|---|------|
| ✅ **כבר בנוי/מאופיין** | **18 אוטומציות** — בעיקר Sales, Onboarding, Finance, Cross |
| 🔜 **MVP** (עד ההשקה) | 5 |
| **V1** (Q3–Q4 26) | 14 |
| **V2** (2027) | 5 |

**3 ההזדמנויות הבולטות הבאות:**
1. **Aging Risk Predictor** (שרשרת אספקה) — חיזוי התיישנות 0 ק"מ = הלב של הארביטראז'.
2. **ROI Calculator** (שיווק) — "כמה חסכת מול מחירון" = כלי המרה ללקוח קצה.
3. **Executive Briefing Bot** (רוחבי) — תקציר שבועי אוטומטי לאברהם+שירי, קל לבנות ב-n8n.

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | מפת אוטומציות מסוננת ל-ULease — 10 פונקציות, 40 אוטומציות, סטטוס ועדיפות | 2026-06-01 |
| 1.1.0 | §11 חדש (D-035): 31 ה-Skills של Anthropic ממופים למפה — לפחות 5 אוטומציות V1/V2 הופכות ל"התקן עכשיו" (כספים, חוזים, briefings) | 2026-06-02 |
| 1.2.0 | §12 חדש (D-040): שכבת המדידה — baseline חובה, עלות-מול-תשואה, כלל 90 הימים, ואומדן ROI כתוב כתנאי לבניית ההזדמנויות הבאות | 2026-06-02 |
| 1.3.0 | שתי אוטומציות מהלופ האורגני (D-047): Deal-to-Content Generator + SEO/GEO Rank Monitor (§1, V1) + סימון ה-Q&A Bot כ-AI Receptionist (§3) — סה"כ 40→42 | 2026-06-03 |

**Attribution.** המסגרות: *546 AI Automation Ideas* (AI Matt · Next Step Agents) · *31 Claude Skills For Small Businesses* (Anthropic). הסינון, המיפוי והתעדוף ל-ULease — חלק מה-Claude OS של Avraham Bar Yochai Chazan.

— *End of CASES/ULEASE_AUTOMATION_MAP.md v1.3.0 —*
