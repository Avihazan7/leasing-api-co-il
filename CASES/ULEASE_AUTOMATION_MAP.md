# ULease 🎯 — מפת אוטומציות AI לפי פונקציה עסקית

**Module:** `CASES/ULEASE_AUTOMATION_MAP.md`
**Version:** 1.5.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — Backlog אוטומציות מתועדף (Business layer, תחת CASES).
**Source:** מבוסס על מסגרת *"546 AI Automation Ideas"* (AI Matt · Next Step Agents) + *"31 Claude Skills For Small Businesses"* (Anthropic plugin pack) + *"10 Claude Skills Every Professional Needs"* (Hamza Khalid) + *"Claude Skills That Replace a Full Operations Team"* (25 ops skills) — מסונן ומותאם ל-ULease.
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

### 11.1 חבילה שנייה: 10 ה-Skills המקצועיים (authoring)

לצד חבילת ה-31 לעסקים-קטנים (שמתחברת לכלים), Anthropic מציעה גם **Skills מקצועיים לעבודת-ידע** שרצים על **הקול, התבנית והסטנדרטים שלך** — לא על אינטגרציות חיצוניות. מותקנים בקליק מ-`github.com/anthropics/skills`. חלקם נופלים ישירות על עבודות ההשקה:

| Skill | מה עושה | עבודת ULease שזה משרת | מתי |
|-------|----------|------------------------|:---:|
| `cold-outreach` | פנייה מותאמת בטון שלך (לא AI-copy) | **אקווזיציית היצע** — יבואנים/ליסינג (D-045 white-glove · `OUTREACH_SCRIPTS`); עובד הכי טוב עם `about-me.md` (כבר קיים ב-OS) | עכשיו |
| `weekly-report` | ממלא תבנית דוח מ-notes גולמיים | **עדכון משקיעים שבועי** (תוכנית הביצוע, כלל 5) — מגשר/משלים את ה-skill `investor-update` | עכשיו |
| `email-rewriter` | טיוטה גסה → מייל send-ready | תקשורת יומיומית + follow-ups (`OUTREACH_SCRIPTS`) | עכשיו |
| `meeting-notes` | transcript → סיכום מובנה | ראש המטה "Meetings" (`COWORK_SETUP` §9) — פגישות ספקים/משקיעים | עכשיו |
| `linkedin-post-writer` | פוסט בקול המדויק שלך | נוכחות מייסד + תוכן אורגני לצד-הביקוש (`DEMAND_ENGINE` פאזה 2) | השקה+ |
| `brand-guidelines` | נועל צבעים/פונטים/טון | **מותג צרכני** — סוגר את דגל D-024 (האתר חייב פלטת מותג מכוונת) | השקה+ |
| `data-analyst` | מחיל את מסגרת המדדים שלך על כל dataset | QA למודל הפיננסי (`ULEASE_FORECAST.csv`) + KPIs ל-M9 | V1 |
| `research-summary` | מאמר צפוף → אנגלית פשוטה | מודיעין שוק/רגולציה + ניתוח מתחרים | V1 |
| `docx-builder` | Word מעוצב בלי לחזור על הפורמט | one-pagers · טיוטות הסכמי ספק/SLA | לפי צורך |
| `code-reviewer` | סקירת קוד מול סטנדרט הצוות | משימת ה-Tech Lead — סקירה עקבית | פוסט-גיוס |

**ארבעה Stacks (combo) מהמקור → ל-ULease:**
- `cold-outreach` + `about-me.md` → פנייה אישית להיצע (ה-`about-me.md` כבר בנוי).
- `weekly-report` + `meeting-notes` → דיווח אוטומטי: פגישה → דוח.
- `linkedin-post-writer` + `brand-guidelines` → פוסטים zero-edit בקול המותג.
- `research-summary` + `data-analyst` → אנליסט מחקר אישי (מודיעין שוק).

> 💡 **העיקרון — "skill אחד, job אחד · לעולם לא לשלב שני workflows":** בדיוק למה ארבעת ה-skills של ה-OS (`os-module` · `os-decision` · `ulease-refresh` · `investor-update`) מוגדרים צר. workflow מורכב? **לערום** skills (combo), לא לנפח אחד. בונים משלכם? **Skill Creator** — 5 דקות (כך נולדו ארבעת ה-skills שלנו).

> ⚠️ **אותה הסתייגות, רובד אישי:** החבילה הזו פותרת **פרודוקטיביות מקצועית** (כתיבה, סיכום, ניתוח) — משלימה את חבילת התפעול, לא מחליפה את המוצר. שים לב לכפילות מכוונת: `weekly-report` ו-`cold-outreach` חופפים ל-skills/scripts קיימים (`investor-update`, `OUTREACH_SCRIPTS`) — הם **מגשרים** עד שהגרסה המותאמת שלנו בשלה.

### 11.2 חבילה שלישית: אשכול ה-Ops התפעולי ("25 skills שמריצות ops בלי לגייס")

מקור: אינפוגרפיקת *Claude Skills That Replace a Full Operations Team* (25 skills · 6 קטגוריות: COMMS · DOCS · DATA · PLANNING · QUALITY · SYSTEMS). המקבילה התפעולית ל-§11/§11.1 — נופלת בדיוק על המציאות של ULease: **סולו/דואו עד ה-Tech Lead** (אברהם + שירי).

**~14/25 כבר מכוסים** (לא ממפים מחדש): inbox-triage→`/lead-triage`+ראש המטה "Inbox" · slack-digest/pipeline-report→`/sales-brief` · client-update→`weekly-report` · meeting-recap→`meeting-notes`+"Meetings" · escalation-draft→`/handle-complaint` · kpi-snapshot→`/business-pulse` · expense-scan→`/month-end-prep` · friday-wrap→`/friday-brief` · week-plan/morning-brief→`/monday-brief`+"Briefer" · onboard-checklist→Onboarding Coach (§2).

**הדלתא — האשכול התפעולי החדש (אימות grep: 0 בריפו):**

| Skill חדש | מה הוא עושה ל-ULease | בעלים | מתי |
|-----------|----------------------|:-----:|:---:|
| `/time-audit` | סורק יומן 30 יום → איפה השעות באמת הלכו מול התכנון; חושף את דליפת-הזמן הגדולה | אברהם | עכשיו |
| `/capacity-check` | משימות מול שעות פנויות → דגל over-commit לפני Deadline שנשבר | אברהם | עכשיו |
| `/sprint-scope` | מפרק את ההשקה ל-milestones שבועיים + שעות לכל אבן-דרך | אברהם | עכשיו |
| `/risk-flag` | סורק פרויקטים פעילים לאיתותי-סיכון (deadline · scope gap · מייל ללא מענה) → מרשם סיכונים | אברהם | עכשיו (שער Go-Live) |
| `/deliverable-check` | QA לתוצר לפני שיוצא ללקוח/משקיע (פורמט · מותג · טון) → pass/fail | שירי | השקה+ |
| `/process-audit` | SOP מול ה-workflow בפועל → צעדים מיושנים/חסרים/לא-מבוצעים | שירי | V1 |
| `/vendor-compare` | 3 הצעות ספק/כלי → השוואת מחיר/היקף/תנאים + המלצה בשורה | אברהם | עכשיו |
| `/access-audit` | כל כלי/login/מנוי → חשבונות לא-בשימוש + חידושים מתקרבים | שירי | חודשי (עלויות) |
| `/file-cleanup` | סורק תיקיות → כפילויות, קבצים מיושנים, שמות חסרי-משמעות → צ'קליסט | שירי | לפי צורך |
| `/sop-draft` · `/policy-writer` · `/changelog` | תהליך חוזר → SOP ממוספר · מדיניות פנימית · יומן שינויים | שירי | V1 (לפני הרחבת צוות) |

**אותם 3 עקרונות (§11/§11.1):** skill אחד-job אחד (combo, לא ניפוח) · כפילות מכוונת = גשר (תפעול-העסק, לא המוצר) · **שער המדידה §12** — time-audit/capacity-check הם ה-baseline עצמו.

> **למה זה מחזק את הארכיטקטורה:** עד ה-Tech Lead הצוואר הוא **זמן המייסד**. אשכול ה-DATA+PLANNING+QUALITY (time-audit · capacity-check · risk-flag · deliverable-check) הוא שכבת ה-chief-of-staff התפעולית **on-demand** שמגנה על המשאב הזה — משלים את 5 התפקידים המתוזמנים של `COWORK_SETUP` §9 בכלים נקודתיים.

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
| 1.4.0 | §11.1 חדש (D-051): חבילה שנייה — 10 ה-Skills המקצועיים (authoring) ממופים לעבודות ההשקה (cold-outreach→היצע · weekly-report→משקיעים · brand→מותג) + 4 stacks + עקרון "skill אחד, job אחד" | 2026-06-03 |
| 1.5.0 | §11.2 חדש (D-067): חבילה שלישית — אשכול ה-Ops התפעולי ("25 skills שמריצות ops בלי לגייס"); ~14/25 כבר מכוסים, הדלתא = 10 יכולות חדשות (time-audit · capacity-check · process-audit · risk-flag · access-audit · file-cleanup · vendor-compare · sprint-scope · deliverable-check · sop/policy/changelog) ממופות למי-עושה-מה (אברהם/שירי) + שער המדידה §12 | 2026-06-08 |

**Attribution.** המסגרות: *546 AI Automation Ideas* (AI Matt · Next Step Agents) · *31 Claude Skills For Small Businesses* (Anthropic) · *10 Claude Skills Every Professional Needs* (Hamza Khalid) · *Claude Skills That Replace a Full Operations Team* (25 ops skills). הסינון, המיפוי והתעדוף ל-ULease — חלק מה-Claude OS של Avraham Bar Yochai Chazan.

— *End of CASES/ULEASE_AUTOMATION_MAP.md v1.5.0 —*
