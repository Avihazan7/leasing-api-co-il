# DIGITAL_CORE.md — Multi-Agent Super Skill · Digital Core Architecture

**Module:** `DIGITAL_CORE.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Doctrine + Architecture. השכבה הדיגיטלית/האגנטית שמריצה את ה-ULJ מקצה לקצה.
**Integrates with:** `LEASE_JOURNEY.md`, `AGENT_BLUEPRINT.md`, `N8N_AUTOMATION.md`, `COMMAND_API.md`, `power-bi-essential-concepts.md`, `BRANCH_KNOWLEDGE.md`, `LAUNCH.md`
**Thesis:** *ה-ULJ הוא ה"מה ולמה" (פסיכולוגיה). זה ה"איך": ארבעה סוכני AI על מרכז עצבים אחד, שהופכים את המכירה למדע מדויק — מקצה לקצה ברמת קצה.*

---

## 0. למה הקובץ הזה קיים

`LEASE_JOURNEY.md` נתן את הארכיטקטורה ההתנהגותית: 5 שלבים, 4 עקרונות-על, אקטים.
אבל הוא תיאר *מה* קורה ו*למה* — לא *איך* זה רץ דיגיטלית בקנה מידה.

המודול הזה הוא ה-**Digital Core**: התרגום של ה-ULJ ל-**Multi-Agent Super Skill** על
מרכז עצבים אחד (CRM), עם pipeline דיגיטלי מקצה לקצה (chatbot → KYC ביומטרי → חיתום
דינמי → מסירה). כל אקט פסיכולוגי מ-ULJ מקבל כאן **כלי דיגיטלי וסוכן AI** שמבצע אותו.

> **יעד סקייל:** הארכיטקטורה נבנתה לנפח — תמיכה נוחה ב-**130+ רכבים** כבר בשלבי ההשקה
> הראשונים, ועשרות-מאות עסקאות בחודש. ראה § 7.

**הזוג:** `LEASE_JOURNEY` (התנהגות) ⇄ `DIGITAL_CORE` (מימוש). קוראים אותם יחד.

---

## 1. שלוש השכבות + שכבת הבסיס

```
┌──────────────────────────────────────────────────────────────┐
│  שכבה 1 · מוח המערכת — CRM (Salesforce)                       │
│  מרכז עצבים: נתונים · סטטוסים · אוטומציות · ניצוח הסוכנים     │
└───────────────────────────▲──────────────────────────────────┘
                            │ context + מצב לקוח
┌───────────────────────────┴──────────────────────────────────┐
│  שכבה 2 · Multi-Agent Super Skill                            │
│  Profiler · Mediator · Strategist · Experience                │
└───────────────────────────▲──────────────────────────────────┘
                            │ פעולות לאורך המסע
┌───────────────────────────┴──────────────────────────────────┐
│  שכבה 3 · צינור ההמרה הדיגיטלי (E2E Pipeline)                │
│  Chatbot → TCO → KYC ביומטרי → CLM → Gap → מסירה             │
└───────────────────────────▲──────────────────────────────────┘
                            │
   שכבת בסיס · The ULease Edge:                                  
   שקיפות מוחלטת ◂ חיכוך אפסי ◂ סגירה מהירה ◂ פתרון הוליסטי     
```

---

## 2. שכבה 2 — ארבעת הסוכנים (Multi-Agent Super Skill)

| סוכן | טכנולוגיה | מטרה אסטרטגית | מתודולוגיה (ULJ) | טופולוגיה (`AGENT_BLUEPRINT § 9`) |
|------|-----------|----------------|-------------------|-----------------------------------|
| **The Profiler** | NLP / זיהוי שפה | אבחון הליד בזמן אמת → פרופיל פסיכולוגי | **Big Five** (P2) | Router/Classifier |
| **The Mediator** | עצי החלטה לוגיים | דחיפת הנחיות לנציג: מיקוד הלקוח, הורדת חרדה | **העשרה אינסטרומנטלית** (P1) | Reflexion / guidance |
| **The Strategist** | אלגוריתמים פיננסיים | חישוב BATNA מול השוק, הפקת חלופות Win-Win | **תורת המשחקים** (P3,P4) | Plan&Execute + Evaluator |
| **The Experience** | אוטומציית שיווק | ניהול ה-Gap + חוויית מסירה | **Peak-End Rule** (P1,P2) | Scheduled / Autonomous |

**הניצוח:** ה-CRM (שכבה 1) הוא ה-**Orchestrator**; ארבעת הסוכנים הם ה-**Workers**.
זוהי טופולוגיית Orchestrator-Worker (`AGENT_BLUEPRINT § 9`), שבה כל סוכן מופעל לפי
מצב הלקוח ב-pipeline. ב-`stage-a` כל סוכן הוא Skill עם Memory + Tools משלו.

---

## 3. שכבה 3 — צינור ההמרה הדיגיטלי, שלב-אחר-שלב

ה-pipeline מבצע את אותם 5 שלבי ULJ; ה-KYC והחיתום הם **הזרקה דיגיטלית** בתוך מעבר
מו"מ→סגירה. לכל שלב: ערוץ · פעולה דיגיטלית · הסוכן שפועל · סטטוס ב-CRM.

| # | שלב דיגיטלי | ערוץ | סוכן | סטטוס CRM (דוגמה) | ULJ |
|---|--------------|------|------|--------------------|-----|
| **1** | **Lead & Profiling** | Chatbot / אתר → CRM | Profiler + Mediator | `Personality_Profile__c`, `Risk_Aversion_Score__c` | שלב 1 |
| **2** | **Nurturing & Signaling** | נציג + דף נחיתה + סימולטור TCO + WhatsApp | Strategist | Lead→Opportunity · `Customer_Viewed_TCO_Calculator__t` | שלב 2 |
| **3** | **Biometric KYC** | זיהוי+חיתום בנייד (Liveness Check) | CLM/KYC Agent | `Identity_Verified__c=TRUE`, `KYC_Status__c=Approved` | שלב 3 |
| **4** | **Dynamic Contracting** | Docusign CLM ב-CRM Flow | Strategist | `Opportunity_Stage__c=Closed Won` · Audit Trail | שלב 3→4 |
| **5** | **Gap Management** | Marketing Cloud → WhatsApp | Experience | `Customer_Anxiety_Level__c` 9→2 · `Ready_for_Delivery` | שלב 4 |
| **6** | **The Grand Delivery** | אפליקציית מסירה (Mobile CRM) | Experience + Strategist | `Delivery_Status__c=Handed Over` · משימת חידוש +33 חודש | שלב 5 |

**עקרון ה-Signaling (שלב 2):** הסוכן חושף מידע "לרעתנו" (יקרים ב-20₪/חודש) כדי
לזכות באמון מלא (חוסכים 4,000₪ בהשתתפות עצמית) — מהלך Cooperative Game שמייצר
שיווי משקל של אמון. שקיפות כ-אות, לא כחולשה.

---

## 4. תרחיש-קנון — "אבי כהן" (Conscientious-Neurotic)

תרחיש המסירה המלא משמש כ-**eval scenario** (ראה `AGENT_BLUEPRINT` שכבת Evals):
פרסונה אחת, מקצה לקצה, שמודדת אם המערכת אבחנה והגיבה נכון.

**הפרסונה:** אבי — מונע מ**פחד מ"אותיות קטנות"** (Neurotic גבוה), אך מגיב מצוין
ל**מספרים, עובדות וסדר** (Conscientious גבוה). `Risk_Aversion_Score__c: 9/10`.

| שלב | מה אבי עושה | מה המערכת עושה (התאמה לפרופיל) |
|-----|-------------|-------------------------------|
| 1 | "מפחד שדוחפים עלויות... רוצה לדעת בדיוק על מה אני משלם" | Profiler מסמן N↑ C↑ · Mediator עובר ל**שקיפות מוחלטת** |
| 2 | שוהה 45ש' בטבלת השוואת ביטוחים | התראה לנציג: *"מחפש שקט נפשי — אל תוריד מחיר, הרחב אחריות"* + סימולטור TCO |
| 3 | סורק ת"ז + Liveness Check | סרגל התקדמות ירוק: *"המידע שלך מוצפן בתקן המחמיר ביותר"* (הרגעת N↑) |
| 4 | חותם Sign-on-Glass + MFA | חוזה דינמי: סעיפי החרדה מודגשים בצהוב + **נספח הגנת ערך** (מענה ל-BATNA) |
| 5 | מקבל עדכון כל 3 ימים בתקופת ההמתנה | Experience מיישם ויסות התנהגות → `Anxiety` 9→2, מנטרל חרטת קונה |
| 6 | מגיע למסירה | טאבלט לנציג: *"אל תציע טקסים רועשים — קפה, מתודי, סבלני, הסבר בטיחות אקטיבית"* |

**תוצאה:** `Customer_Satisfaction_Prediction__c: 9.8/10` · משימת חידוש אוטומטית
בעוד 33 חודשים (פתיחת ה"משחק החוזר"). **Success criteria של ה-eval:** המערכת
זיהתה N↑C↑, בחרה אסטרטגיית שקיפות, *לא* הורידה מחיר אלא הרחיבה ערך, ומנעה ביטול ב-Gap.

---

## 5. מודל הנתונים — שדות מותאמים ב-CRM

הפרופיל הפסיכולוגי הוא **first-class data**. השדות המרכזיים (custom fields):

| שדה | טיפוס | נכתב ע"י | תפקיד |
|-----|-------|----------|-------|
| `Personality_Profile__c` | Picklist | Profiler | טיפוס Big Five (e.g. Conscientious-Neurotic) |
| `Risk_Aversion_Score__c` | Number 0–10 | Profiler | עוצמת חרדה פיננסית → בוחר אסטרטגיה |
| `Customer_Anxiety_Level__c` | Number 0–10 | Experience | מנוטר לאורך ה-Gap (יעד: ↓) |
| `Identity_Verified__c` / `KYC_Status__c` | Bool / Picklist | KYC Agent | שער חיתום |
| `Opportunity_Stage__c` | Picklist | Strategist | מצב ה-funnel (→ Closed Won) |
| `Customer_Satisfaction_Prediction__c` | Number | Experience | מדד Peak-End → טריגר חידוש |

הפרופיל זורם ל-Power BI (`power-bi-essential-concepts.md`) כממד נוסף: המרה ו-NPS
**לפי טיפוס אישיות**, לא רק לפי רכב/אזור.

---

## 6. שילוב עם הסטאק הקיים — Salesforce כ-CRM (החלטה)

**החלטה (הוראת בעלים, 2026-06-03):** ה-CRM הוא **Salesforce**. הוא נכנס כ"מרכז עצבים"
של תהליך המכירה, **לצד** הסטאק הקיים (`leasing-api` + Supabase + n8n + Power BI) — לא במקומו.
הגבול:

| שכבה | תפקיד מוצע | מקור אמת |
|------|-----------|----------|
| **`leasing-api` + Supabase** | הליבה הטרנזקציונית: מלאי, settlements, ledger, Outbox | מקור האמת ל-**מוצר/כסף** |
| **Salesforce** | מוח ה-**מכירה**: ליד→עסקה, פרופיל, סטטוסים, ניצוח סוכנים | מקור האמת ל-**תהליך/לקוח** |
| **n8n** (`N8N_AUTOMATION`) | Glue: מסנכרן אירועי Outbox ⇄ Salesforce (HMAC+Webhook) | — |
| **stage-a** (`AGENT_BLUEPRINT`) | מימוש ה-Brain של 4 הסוכנים | — |
| **Power BI** | מדידה חוצת-מערכות | — |

### 6.1 חיבור Salesforce — תוכנית אינטגרציה

החיבור בפועל דורש **org + Connected App + OAuth credentials** שאינם בסביבה הזו. כשהם
יסופקו, זהו ה-blueprint (מיושר ל-`N8N_AUTOMATION` ול-`DEV_ENVIRONMENTS` MCP):

| כיוון | מנגנון | מה זורם |
|-------|--------|---------|
| **leasing-api → Salesforce** | Outbox event → n8n → Salesforce REST API (`sObject` upsert) | מלאי נשריין/נמכר, settlement → עדכון Opportunity |
| **Salesforce → leasing-api** | Platform Event / Outbound Message → n8n webhook (HMAC) | עסקה נסגרה (Closed Won) → יצירת הזמנה ב-API |
| **Claude ⇄ Salesforce** | Salesforce MCP server (חיבור ב-`DEV_ENVIRONMENTS`) | קריאה/כתיבת לידים, פרופילים, סטטוסים מתוך Skills |
| **אימות** | OAuth 2.0 (JWT Bearer / Connected App) · secrets ב-vault | — |

**מצב נוכחי:** ה-blueprint מתועד; אין חיבור חי עד שהאישורים יסופקו. ראה תשובה למשתמש.

---

## 7. סקייל ו-Rollout

| ציר | יעד |
|-----|-----|
| **נפח השקה** | 130+ רכבים בשלבים ראשונים · עשרות-מאות עסקאות/חודש |
| **Manual-first** | בדיוק כמו `LEASE_JOURNEY § 6`: הסוכנים הדיגיטליים נכנסים בהדרגה. עכשיו — עסקאות ידניות לפי ה-playbook; ה-CRM קולט ידנית את הפרופיל והסטטוסים |
| **Week 1** | Chatbot + Profiler חיים (שלב 1 אוטומטי); שאר השלבים — נציג אנושי ב-CRM |
| **Month 1** | Signaling (TCO) + Gap Management (Experience) אוטומטיים |
| **Quarter 1** | KYC ביומטרי + Dynamic CLM משולבים; eval "אבי כהן" רץ כ-regression |

**עיקרון:** הארכיטקטורה תומכת בסקייל מלמעלה, אבל מתחילים ידני מלמטה. הסוכנים
מגדילים throughput — לא תנאי להתחלה.

---

## גרסאות

| גרסה | תאריך | שינוי |
|------|--------|-------|
| 1.0.0 | 2026-06-03 | Initial — Digital Core: 3 שכבות (CRM מרכז עצבים · 4 סוכנים · pipeline דיגיטלי) + שכבת Edge. ארבעת הסוכנים (Profiler/Mediator/Strategist/Experience) ממופים ל-ULJ ול-AGENT_BLUEPRINT § 9. Pipeline 6-שלבי (כולל KYC ביומטרי + חיתום דינמי) ממופה ל-5 שלבי ULJ. תרחיש-קנון "אבי כהן" כ-eval. מודל נתונים (custom fields). § 6 נקודת החלטה פתוחה — CRM מול הסטאק הקיים (default: צד-לצד). יעד סקייל 130+ |

---

**Tie-back ל-OS:** `LEASE_JOURNEY` נתן את הנשמה (פסיכולוגיה), `AGENT_BLUEPRINT` את
מנוע הסוכנים, `N8N_AUTOMATION` את הצינורות, `power-bi` את המדידה. המודול הזה
**מרכיב אותם ללקוח אחד שזז ב-pipeline** — עם מוח (CRM), ארבע ידיים (סוכנים),
וגבול ברור מול הליבה הטרנזקציונית. *מקצה לקצה ברמת קצה — עכשיו עם תוכנית מימוש.*
