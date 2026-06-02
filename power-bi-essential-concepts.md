# מושגי יסוד ב-Power BI

**10 מושגים חיוניים ב-Power BI שכל אנליסט חייב להכיר**

> לשלוט ביסודות. לבנות דשבורדים טובים יותר. פתרונות Power BI מעולים נבנים על דאטה נקי, מודל נתונים חזק, DAX יעיל והבנה ברורה של הדרישות העסקיות — לא רק על ויזואליזציות.

---

## 10 המושגים במבט-על

| # | מושג | בשורה אחת |
|---|------|-----------|
| 1 | **מקורות נתונים (Data Sources)** | חיבור ל-Excel, SQL Server, Web, SharePoint, CSV, APIs ועוד. |
| 2 | **Power Query (טרנספורמציית נתונים)** | ניקוי ועיצוב הדאטה לפני שהוא מגיע למודל. |
| 3 | **מודל נתונים (Data Model)** | קשרים בין טבלאות — הבסיס לכל דבר. |
| 4 | **DAX (Data Analysis Expressions)** | עמודות מחושבות, מדדים (Measures) וטבלאות לניתוח מתקדם. |
| 5 | **Slicers ופילטרים** | אינטראקטיביות ו-Drilldown למשתמשי הקצה. |
| 6 | **ויזואליזציות (Visualizations)** | עמודות, עוגות, טבלאות, מפות, KPI, כרטיסים, מטריצות. |
| 7 | **דוחות (Reports)** | תוצרים אינטראקטיביים, מרובי עמודים ועשירים בוויזואלים. |
| 8 | **דשבורדים מול דוחות** | להכיר את ההבדל — הם משרתים מטרות שונות. |
| 9 | **פרסום ושיתוף (Publishing & Sharing)** | Power BI Service, סביבות עבודה (Workspaces) ושיתוף פעולה. |
| 10 | **אבטחה ברמת שורה (RLS)** | הגבלת נראוּת הדאטה לפי תפקיד המשתמש. |

---

## 1. מקורות נתונים (Data Sources)

חיבור ל-Excel, SQL Server, Web, SharePoint, CSV, APIs ועוד.

- **איך:** Home → Get Data

## 2. Power Query (טרנספורמציית נתונים)

ניקוי ועיצוב מחדש של הדאטה באמצעות Power Query Editor.

- **דוגמאות:** הסרת עמודות, סינון שורות, פיצול טקסט, שינוי סוגי נתונים

## 3. מודל נתונים (Data Model)

יצירת קשרים בין טבלאות (אחד-לרבים, רבים-לאחד).

- **טיפ:** השתמשו ב-Star Schema לביצועים טובים יותר.

## 4. DAX (Data Analysis Expressions)

יצירת עמודות מחושבות, מדדים (Measures) וטבלאות לביצוע ניתוחים מתקדמים.

- **דוגמאות:** `SUM`, `CALCULATE`, `FILTER`, `VALUES`, `DATEADD`
- מדד לדוגמה: `Total Sales = SUM(Sales[Amount])`

> DAX הוא לרוב נקודת המפנה בין *בניית דוחות* לבין *הפקת תובנות עסקיות אמיתיות*.

## 5. Slicers ופילטרים

משמשים לאינטראקטיביות ו-Drilldown.

- **דוגמה:** הוספת Slicer לפי אזור או שנה.

## 6. ויזואליזציות (Visualizations)

עמודות, עוגה, טבלה, מפה, KPI, Slicers, כרטיסים, מטריצה ועוד רבים.

- גוררים שדות אל **Values**, **Axis**, **Legend** כדי להתאים אישית.

## 7. דוחות (Reports)

בניית דוחות אינטראקטיביים עם מספר עמודים וויזואלים עשירים.

- **טיפ:** לשמור על פשטות, בהירות ומיקוד.

## 8. דשבורדים מול דוחות

| | דוח (Report) | דשבורד (Dashboard) |
|---|--------------|---------------------|
| **עמודים** | מספר עמודים | קנבס אחד |
| **תוכן** | ויזואלים אינטראקטיביים | ויזואלים מוצמדים (Pinned) מדוחות |
| **מצב** | עריכה וחקירה | צפייה בלבד, משותף |

## 9. פרסום ושיתוף (Publishing & Sharing)

פרסום ל-Power BI Service (ענן), שיתוף דוחות או דשבורדים דרך Workspaces.

- **טיפ:** השתמשו ב-Workspaces לשיתוף פעולה ובקרת גישה.

## 10. אבטחה ברמת שורה (Row-Level Security — RLS)

הגבלת נראוּת הדאטה בהתאם לתפקיד המשתמש.

- **דוגמה:** איש מכירות רואה רק את הדאטה של האזור שלו.
- חוק לדוגמה: `[Region] = USERPRINCIPALNAME()`

---

## דשבורדים ל-ULease — מהתיאוריה לפרקטיקה

יישום 10 המושגים על נתוני ה-Leasing API (`stage-a`): Supabase/Postgres עם הטבלאות `vehicles`, `settlements`, `ledger_entries`, `payment_transfers` ו-`vehicle_read_model`.

### 1. מקור הנתונים (Data Source)

| מה | איך |
|----|-----|
| Supabase/Postgres (production) | Get Data → PostgreSQL database |
| טבלאות לחיבור | `vehicle_read_model` (קטלוג) · `settlements` (עסקאות) · `ledger_entries` (עמלות) · `payment_transfers` (תשלומים) |
| מצב רענון | Import + Scheduled Refresh (או DirectQuery לנתוני זמן-אמת) |

### 2. Power Query — טרנספורמציות נדרשות

- **המרת `amount_minor` (אגורות) לשקלים:** עמודה חדשה `Amount = amount_minor / 100`
- **המרת `status` לעברית:** `DRAFT` → טיוטה, `AVAILABLE` → זמין, `RESERVED` → שמור, `SOLD` → נמכר, `IN_SERVICE` → בטיפול, `WITHDRAWN` → הוסר
- **טיפוסי נתונים:** `created_at` / `updated_at` → Date/Time, `list_price` / `offer_price` → Decimal

### 3. מודל הנתונים — Star Schema

```
                    ┌──────────────────┐
                    │  DimDate (לוח)    │
                    └────────┬─────────┘
                             │
┌─────────────────┐   ┌──────┴──────────┐   ┌──────────────────┐
│ DimVehicle      │───│ FactSettlements │───│ DimDealer        │
│ (vehicle_read_  │   │ (settlements)   │   │ (מתוך ledger:    │
│  model)         │   │ deal_id, vin,   │   │  dealer account) │
│ vin, status,    │   │ amount, date    │   └──────────────────┘
│ list/offer price│   └──────┬──────────┘
└─────────────────┘          │
                    ┌────────┴─────────┐
                    │ FactLedger       │
                    │ (ledger_entries) │
                    │ commission/payout│
                    └──────────────────┘
```

- **Fact:** `settlements` + `ledger_entries`
- **Dim:** `vehicle_read_model`, טבלת תאריכים, טבלת סוכנויות (dealers)
- קשר אחד-לרבים: `vin` → עסקאות, `deal_id` → רישומי Ledger

### 4. מדדי DAX מרכזיים

```dax
-- סך מכירות (₪)
Total Sales = SUM(FactSettlements[Amount])

-- הכנסות פלטפורמה מעמלות (5% ברירת מחדל)
Platform Commission =
CALCULATE(SUM(FactLedger[Amount]), FactLedger[type] = "commission", FactLedger[party] = "platform")

-- שיעור המרה: RESERVED → SOLD
Conversion Rate =
DIVIDE(
    CALCULATE(COUNTROWS(DimVehicle), DimVehicle[status] = "SOLD"),
    CALCULATE(COUNTROWS(DimVehicle), DimVehicle[status] IN {"SOLD", "RESERVED", "AVAILABLE"})
)

-- מלאי זמין
Available Inventory = CALCULATE(COUNTROWS(DimVehicle), DimVehicle[status] = "AVAILABLE")

-- מכירות חודש קודם (להשוואה)
Sales Previous Month = CALCULATE([Total Sales], DATEADD(DimDate[Date], -1, MONTH))

-- ממוצע הנחה (Offer מול List)
Avg Discount % = AVERAGEX(DimVehicle, DIVIDE(DimVehicle[list_price] - DimVehicle[offer_price], DimVehicle[list_price]))
```

### 5–6. Slicers וויזואליזציות מומלצות

| ויזואל | שדות | מטרה |
|--------|------|------|
| **KPI Cards** | Total Sales · Platform Commission · Available Inventory · Conversion Rate | מבט-על ב-3 שניות |
| **Line Chart** | Total Sales לפי חודש | מגמת מכירות |
| **Funnel** | מספר רכבים לפי status (זמין → שמור → נמכר) | משפך ההמרה |
| **Bar Chart** | עמלות לפי סוכנות (dealer account) | ביצועי סוכנויות |
| **Matrix** | רכבים × סטטוס × חודש | תמונת מלאי |
| **Slicers** | חודש/רבעון · סטטוס · סוכנות | סינון אינטראקטיבי |

### 7–8. דוח מול דשבורד ב-ULease

- **דוח (Report):** "ביצועי מכירות ULease" — 3 עמודים: מכירות · מלאי · עמלות וסליקה
- **דשבורד (Dashboard):** הצמדת 4 ה-KPI Cards + מגמת המכירות — מסך אחד להנהלה (view-only)

### 9. פרסום ושיתוף

- Workspace ייעודי: **ULease Analytics**
- Scheduled Refresh יומי מ-Supabase
- שיתוף: הנהלה (Viewer) · אנליסטים (Contributor)

### 10. RLS — אבטחה ברמת שורה

```dax
-- Role: Dealer — כל סוכנות רואה רק את העסקאות שלה
[dealer_account] = USERPRINCIPALNAME()

-- Role: Management — ללא סינון (רואים הכל)
```

> **קשר ל-AGENT_BLUEPRINT:** ה-Outbox events (`outbox` table) הם המקור האמין ביותר ל-Audit Trail — דשבורד תפעולי יכול לנטר גם `published_at IS NULL` (אירועים שטרם פורסמו) כמדד בריאות המערכת.

---

## הרעיון הגדול

> רבים מתמקדים רק ביצירת ויזואליזציות, אבל פתרונות Power BI מעולים נבנים על **דאטה נקי**, **מודל נתונים חזק**, **DAX יעיל** ו**הבנה ברורה של הדרישות העסקיות**.
>
> **תובנות טובות יותר. החלטות טובות יותר. עסק טוב יותר.**

---

*תומלל מהאינפוגרפיקה "10 Essential Power BI Concepts".*
