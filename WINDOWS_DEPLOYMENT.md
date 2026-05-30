# WINDOWS_DEPLOYMENT.md — הטמעת Claude לאופיס מקצה לקצה (Windows)

**Module:** `WINDOWS_DEPLOYMENT.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Production-ready. End-to-end Windows rollout.
**Integrates with:** `CLAUDE.md`, `COMMAND_API.md`, `MEMORY.md`
**Target:** Microsoft 365 — Word, Excel, PowerPoint + Claude Skills (2026)

---

## 0. תוכן עניינים

1. [סקירה ומטרות](#1-סקירה-ומטרות)
2. [Prerequisites — דרישות מקדימות](#2-prerequisites)
3. [שלב 1 — התקנת התוסף הרשמי של Claude לאופיס](#3-שלב-1)
4. [שלב 2 — חיווט נכון של תיקיות, OneDrive ו-SharePoint](#4-שלב-2)
5. [שלב 3 — עבודה מתוך סרגל הצד של Claude בכל קובץ](#5-שלב-3)
6. [שלב 4 — Skills לתהליכים קבועים שחוזרים על עצמם](#6-שלב-4)
7. [Word — playbook מפורט](#7-word-playbook)
8. [Excel — playbook מפורט](#8-excel-playbook)
9. [PowerPoint — playbook מפורט](#9-powerpoint-playbook)
10. [Verification — איך יודעים שזה עובד](#10-verification)
11. [Troubleshooting — תקלות נפוצות](#11-troubleshooting)
12. [Rollout ארגוני — Group Policy & Intune](#12-rollout-ארגוני)
13. [Security & Compliance](#13-security--compliance)
14. [Checklist סופי](#14-checklist-סופי)

---

## 1. סקירה ומטרות

המסמך הזה הופך את האינפוגרפיקה של "4 התוספים של Claude לאופיס" למערכת הטמעה ארגונית מלאה על Windows. אחרי שעוברים את כל השלבים, כל משתמש בארגון מקבל:

| יכולת | מה זה נותן |
|-------|------------|
| **Claude בתוך Word** | כתיבה, עריכה ועיצוב מסמכים בלי לעבור בין דפדפן לקובץ |
| **Claude בתוך Excel** | בניית גיליונות, נוסחאות, גרפים — וגם הסבר של מה הקובץ עושה |
| **Claude בתוך PowerPoint** | מצגות נבנות לפי brief קצר, עם עיצוב עקבי לרשת |
| **Skills קבועים** | תהליכים שחוזרים על עצמם הופכים לפקודה אחת |

**עקרון מנחה:** לא להעתיק-להדביק בין דפדפן לקובץ. אם הצוות עדיין עושה את זה — הטמעה לא הושלמה.

---

## 2. Prerequisites

### 2.1 מערכת הפעלה ורישוי

| רכיב | דרישה מינימלית | מומלץ |
|------|----------------|--------|
| Windows | Windows 10 22H2 | Windows 11 23H2+ |
| Microsoft 365 | Apps for Business | Apps for Enterprise / E3 / E5 |
| Office build | 16.0.17000+ | Current Channel האחרון |
| Claude account | Pro / Team | Team / Enterprise (לשליטה מרכזית) |
| חיבור רשת | HTTPS יוצא ל-`*.anthropic.com` ו-`*.claude.ai` | + רשת ארגונית עם split tunnel |

בדיקת build של Office:
```
File → Account → About <App> → גרסה ובילד
```

### 2.2 הרשאות מנהל

לפני התחלה:

```powershell
# בדיקה שאתה Admin (אם רוצים התקנה ארגונית)
([Security.Principal.WindowsPrincipal] `
 [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(
   [Security.Principal.WindowsBuiltInRole]::Administrator)
```

ערך `True` = יש הרשאות. `False` = התקנה per-user בלבד.

### 2.3 פתיחת רשת (Firewall / Proxy)

יש לוודא שהדומיינים הבאים פתוחים מה-Endpoint:

```
*.anthropic.com           HTTPS/443
*.claude.ai               HTTPS/443
api.anthropic.com         HTTPS/443
console.anthropic.com     HTTPS/443
*.office.com              HTTPS/443  (כבר פתוח לרוב)
*.microsoft.com           HTTPS/443  (כבר פתוח לרוב)
```

אם יש Web Filter (Zscaler / Netskope / Palo Alto) — להוסיף ל-allowlist.

---

## 3. שלב 1 — התקנת התוסף הרשמי של Claude לאופיס

### 3.1 התקנה דרך AppSource (משתמש בודד)

1. פתח את **Word / Excel / PowerPoint**.
2. `Insert` → `Get Add-ins` (או `Office Add-ins`).
3. בחיפוש: `Claude`.
4. ודא שהמפרסם הוא **Anthropic, PBC** — אל תתקין clone-ים.
5. לחץ `Add` → אשר את ה-License.
6. התוסף יופיע ב-`Home` tab בצד ימין.

### 3.2 התקנה ארגונית (Microsoft 365 Admin Center)

עבור מנהל ארגון שרוצה לדחוף לכולם:

1. `admin.microsoft.com` → `Settings` → `Integrated apps`.
2. `Get apps` → חפש `Claude for Office`.
3. `Deploy` → בחר:
   - **Assign users**: All users / Specific users / Groups
   - **Deployment method**: `Fixed (default)` (מומלץ) או `Available`
4. `Next` → `Finish deployment`.
5. ההפצה לוקחת עד 12 שעות לכל המשתמשים.

### 3.3 וידוא התקנה

בכל אחת מאפליקציות Office, בלשונית `Home`:

```
[ Claude ]  ← אייקון בקצה הימני של ה-Ribbon
```

לחיצה פותחת Task Pane בצד ימין. אם לא רואים — Restart לאפליקציה.

---

## 4. שלב 2 — חיווט תיקיות, OneDrive ו-SharePoint

המטרה: להפסיק להעתיק-להדביק בין דפדפן לקבצים. Claude צריך גישה ישירה לקבצים שלך.

### 4.1 הגדרת OneDrive סנכרון

```powershell
# וודא ש-OneDrive פועל ומסונכרן
Get-Process OneDrive -ErrorAction SilentlyContinue

# נתיב ברירת מחדל
$env:OneDrive
```

תיקיות שחייבות להיות מסונכרנות:
- `Documents`
- `Desktop` (אופציונלי, אבל מומלץ)
- כל תיקייה שמכילה תבניות חוזרות

### 4.2 חיבור Claude ל-OneDrive / SharePoint

ב-Task Pane של Claude:

1. סמל גלגל שיניים → `Connections`.
2. `Add connection` → `Microsoft 365` → `Sign in`.
3. אשר scopes:
   - `Files.Read.All`
   - `Sites.Read.All` (אם רוצים SharePoint)
4. בחר תיקיות לאינדקס (אל תבחר את כל הדיסק — רק תיקיות עבודה רלוונטיות).

### 4.3 מבנה תיקיות מומלץ

```
OneDrive\
├── 00_Templates\        ← תבניות שמשמשות בסקילים
├── 01_Active_Deals\
├── 02_Reports\
├── 03_Investor_Relations\
├── 04_Marketing\
└── 99_Archive\
```

עקביות במבנה = Claude מבין מהר יותר מה אתה מחפש.

---

## 5. שלב 3 — סרגל צד של Claude בכל קובץ

### 5.1 פתיחת ה-Task Pane

| פעולה | קיצור |
|--------|-------|
| פתיחת/סגירת Claude pane | `Alt + H, C` (לאחר התקנה) |
| Focus ל-Claude input | `Ctrl + Shift + L` |
| הזנת prompt + שליחה | `Ctrl + Enter` |

### 5.2 מצבי עבודה (Context Modes)

ה-Task Pane של Claude עובד בשלושה מצבי הקשר:

| Mode | מה Claude רואה | מתי להשתמש |
|------|----------------|-------------|
| **Document** | כל המסמך הפתוח | סיכום, ניתוח, עריכה גלובלית |
| **Selection** | הסלקציה שלך בלבד | שכתוב פסקה, נוסחה ספציפית, שקופית אחת |
| **Sheet/Slide** | הגיליון / השקופית הנוכחית | עבודה ממוקדת בלי "להפריע" לשאר |

החלפה בין מצבים: ה-dropdown בראש ה-Pane.

### 5.3 הזרמת פלט חזרה למסמך

3 דרכים לקבל את התוצאה לתוך הקובץ:

1. **Insert at cursor** — הכי נפוץ. הופך טקסט / נוסחה / טבלה לעריכה במקום.
2. **Replace selection** — מחליף את מה שמסומן.
3. **Copy to clipboard** — אם אתה רוצה לשלוט בעצמך איפה להדביק.

**Tip:** ב-Excel, "Insert as formula" שונה מ-"Insert as value". שים לב מה אתה רוצה.

---

## 6. שלב 4 — Skills לתהליכים קבועים

### 6.1 מה זה Skill

Skill הוא תהליך מוגדר שחוזר על עצמו — נכתב פעם אחת, רץ במספר קליקים. דוגמאות מהעולם של Leasing.co.il:

- **`/deal-summary`** — סוכם עסקת ליסינג ל-PDF לקוח.
- **`/monthly-pnl`** — בונה דוח P&L חודשי מ-3 גיליונות.
- **`/investor-update`** — מצגת רבעונית למשקיעים.

### 6.2 בניית Skill ב-Claude

1. `claude.ai` → `Skills` → `Create skill`.
2. שדות חובה:
   - **Name** (kebab-case, באנגלית): `deal-summary`
   - **Description**: שורה אחת ברורה — Claude משתמש בה כדי להחליט מתי להפעיל
   - **Instructions**: ה-prompt המלא, כולל פורמט פלט וכללי קצה
3. הוסף **Resources**:
   - תבניות (`.docx`, `.xlsx`, `.pptx`)
   - דוגמאות פלט מוצלחות
   - מסמכי policy רלוונטיים
4. `Save` → ה-Skill זמין בכל אפליקציית אופיס דרך ה-Task Pane.

### 6.3 קישור Skills ל-Command API של הריפו

אנחנו כבר מחזיקים [`COMMAND_API.md`](./COMMAND_API.md) עם 89 פקודות. כדי שהן יעבדו גם בתוך Office:

1. בקובץ ה-Skill ב-Claude, ב-Instructions, הוסף:

   ```
   טען את כללי הפלט מ-COMMAND_API.md
   (נמצא ב-repo: avihazan7/leasing-api-co-il, branch: main).
   זהה תחביר /command בכל input מהמשתמש.
   ```

2. כך כל פקודה `/tldr`, `/bullet`, `/focus` וכו' עובדת באופן זהה ב-Word, Excel, PowerPoint וב-claude.ai.

### 6.4 Skills מומלצים לארגון Leasing

| Skill | תרחיש שימוש | פלט |
|-------|-------------|------|
| `/deal-quote` | יצירת הצעת מחיר ללקוח | Word + PDF |
| `/fleet-report` | דוח צי חודשי | Excel |
| `/board-deck` | מצגת דירקטוריון | PowerPoint |
| `/competitor-scan` | סריקת מתחרים שבועית | Word |
| `/inventory-aging` | התיישנות מלאי | Excel + טבלה ב-Word |

---

## 7. Word playbook

### 7.1 פקודות יומיומיות

| מטרה | Prompt | מצב מומלץ |
|------|--------|------------|
| שכתוב פסקה לסגנון משפטי | "/lawyerize" + select | Selection |
| הרחבת bullet לפסקה | "הרחב לפסקה של 80 מילים" | Selection |
| סיכום של מסמך ארוך | "/tldr" | Document |
| עיצוב — כותרות + TOC | "הוסף כותרות H1-H3 ו-Table of Contents" | Document |

### 7.2 דוגמת flow — חוזה ליסינג חדש

```
1. פתח template ריק:    OneDrive\00_Templates\lease-agreement.docx
2. Task Pane → /deal-quote
3. הזן בלחיצה אחת:
   - שם לקוח
   - דגם רכב
   - תקופה
   - מקדמה
4. Claude מחזיר חוזה מלא → "Insert at cursor"
5. עבור על השדות הצהובים (placeholders שנשארו)
6. Save As → 01_Active_Deals\<customer>-<date>.docx
```

### 7.3 כללי זהב ב-Word

- **לעולם לא לתת ל-Claude לסיים מסמך משפטי בלי קריאה אנושית**.
- מעצב כותרות, bullets, פרקים — אבל הניסוח הסופי באחריות עורך-דין/מנהל.
- שמור גרסאות (`Ctrl+S` + Version History ב-OneDrive).

---

## 8. Excel playbook

### 8.1 פקודות יומיומיות

| מטרה | Prompt | מצב |
|------|--------|------|
| בניית טבלה מ-CSV מודבק | "המר את הסלקציה לטבלה עם כותרות" | Selection |
| נוסחה מורכבת | "תן לי נוסחה ל-IRR עם תזרים לא-קבוע" | Sheet |
| הסבר נוסחה קיימת | "מה הנוסחה ב-K42 עושה?" | Selection |
| יצירת PivotTable | "בנה Pivot של מכירות לפי דגם וחודש" | Sheet |
| בדיקת שגיאות | "מצא חריגות בטור F" | Sheet |

### 8.2 דוגמת flow — דוח חודשי

```
1. פתח: 02_Reports\monthly-fleet-template.xlsx
2. Sheet "Raw" — הדבק את ה-export מהמערכת
3. Task Pane → /fleet-report
4. Claude:
   - מנקה duplicates
   - מחשב KPIs (utilization, downtime, revenue/unit)
   - בונה Pivot ו-Charts ב-Sheet "Dashboard"
5. בדוק את ה-Dashboard
6. Export → PDF → שלח להנהלה
```

### 8.3 כלל זהב ב-Excel

**Always validate the math.** Claude מצוין בנוסחאות, אבל לפני שמסתמכים על מספר ל-decision — תבצע sanity check ידני על שורה אחת. במיוחד בנוסחאות פיננסיות (IRR, NPV, amortization).

---

## 9. PowerPoint playbook

### 9.1 פקודות יומיומיות

| מטרה | Prompt | מצב |
|------|--------|------|
| מצגת מ-brief | "מצגת 8 שקופיות על Q4 sales" | Document |
| שיפור שקופית קיימת | "/rewrite פחות מילים, יותר ויזואל" | Slide |
| הוספת שקופית | "הוסף Case Study אחרי שקופית 5" | Document |
| התאמת עיצוב | "החל את ה-color palette של החברה" | Document |

### 9.2 דוגמת flow — מצגת משקיעים

```
1. פתח template:  03_Investor_Relations\board-template.pptx
2. Task Pane → /board-deck
3. הזן:
   - רבעון
   - 3 KPIs מובילים
   - הצלחה לתת דגש
   - אתגר עיקרי
4. Claude:
   - בונה 10-12 שקופיות
   - שומר על template + צבעים
   - יוצר charts מהנתונים
5. עבור שקופית-אחר-שקופית — וודא שאין "AI-isms"
6. Save → שלח ל-CEO ו-CFO
```

### 9.3 כלל זהב ב-PowerPoint

מצגת לוקחת 90% מהזמן בעריכה, לא ביצירה. אל תצפה שה-Skill ייתן deck מושלם — הוא נותן draft מוצק שחוסך 2-3 שעות.

---

## 10. Verification — איך יודעים שזה עובד

### 10.1 רשימה לבדיקה (per user)

```
□ Claude מופיע ב-Ribbon של Word
□ Claude מופיע ב-Ribbon של Excel
□ Claude מופיע ב-Ribbon של PowerPoint
□ Sign in הצליח
□ Connections → Microsoft 365 מחובר
□ Skill דמו (/tldr על מסמך) רץ ומחזיר פלט
□ "Insert at cursor" עובד
□ אין שגיאות ב-Event Viewer\Application
```

### 10.2 בדיקת telemetry בארגון

ב-Microsoft 365 Admin Center:

```
Reports → Usage → Integrated apps → Claude for Office
```

KPIs לעקוב אחריהם בחודש הראשון:
- **Active users / Licensed users** — יחס אימוץ
- **Prompts per active user / week** — עומק השימוש
- **Top Skills used** — מה באמת רץ
- **Errors** — אם יותר מ-2% — לחקור

---

## 11. Troubleshooting

### 11.1 התוסף לא מופיע

```powershell
# Reset של Office Add-ins cache
Remove-Item "$env:LOCALAPPDATA\Microsoft\Office\16.0\Wef\*" -Recurse -Force
```

הפעל מחדש את Word/Excel/PowerPoint.

### 11.2 Sign-in נכשל

1. בדוק שעון מערכת — סטייה > 5 דקות שוברת OAuth.
2. נסה incognito ב-Edge → התחבר ל-claude.ai → נסה שוב באופיס.
3. אם Proxy ארגוני — וודא ש-`*.anthropic.com` ב-allowlist.

### 11.3 "Connection failed" אחרי שעבד

```powershell
# בדוק קישוריות
Test-NetConnection api.anthropic.com -Port 443
Test-NetConnection claude.ai -Port 443
```

ערך `TcpTestSucceeded : True` — הרשת בסדר.

### 11.4 פלט איטי / timeouts

- בדוק שלא טענת מסמך ענק (> 200 עמודים) ב-Document mode → עבור ל-Selection mode.
- ב-Excel, מסמכים עם > 100K שורות — סנן או סמן טווח לפני שאתה שואל.

### 11.5 Skill לא מופיע ב-Task Pane

1. `claude.ai` → `Skills` → ודא שה-Skill ב-status `Published`.
2. Refresh ה-Task Pane (3 נקודות → `Reload`).
3. ודא שהמשתמש באותו workspace של ה-Skill (Team / Enterprise).

---

## 12. Rollout ארגוני — Group Policy & Intune

### 12.1 Intune — Configuration Profile

לדחיפת ההגדרות לכל endpoint:

```json
{
  "ClaudeForOffice": {
    "AutoEnable": true,
    "DefaultConnection": "Microsoft365",
    "AllowedSkillScopes": ["Workspace", "Personal"],
    "TelemetryLevel": "Basic"
  }
}
```

נתיב: `Intune → Devices → Configuration → Add → Templates → Office`.

### 12.2 Group Policy (AD מסורתי)

עבור ארגונים שעדיין על AD:

```
Computer Configuration
└── Administrative Templates
    └── Microsoft Office 2016
        └── Security Settings
            └── Trust Center
                └── Trusted Add-in Catalogs
                    [Add] https://addins.officecdn.microsoft.com/...
```

### 12.3 PowerShell — bulk enable per tenant

```powershell
# חיבור ל-Exchange Online (לניהול Add-ins)
Connect-ExchangeOnline -UserPrincipalName admin@leasing.co.il

# הצגת תוספים מותקנים
Get-App -OrganizationApp | Where-Object { $_.DisplayName -like "*Claude*" }

# הפעלה לכל המשתמשים
Enable-App -Identity "Claude for Office" -DefaultStateForUser Enabled
```

---

## 13. Security & Compliance

### 13.1 איזה Data יוצא ל-Anthropic

| Mode | מה נשלח |
|------|----------|
| Document mode | תוכן המסמך הפתוח (טקסט בלבד, לא קבצים מקושרים) |
| Selection mode | רק הסלקציה |
| Sheet mode | הגיליון הנוכחי (ערכים + נוסחאות) |

**מה לא נשלח:** מאקרו, comments פרטיים שלא בסלקציה, file metadata רגיש.

### 13.2 הגדרות לחברה תחת רגולציה

עבור Leasing.co.il (תחת פיקוח רשות שוק ההון):

1. **Anthropic Team / Enterprise plan** — מבטיח Zero Data Retention על prompts.
2. ב-`claude.ai` → `Settings` → `Privacy`:
   - `Improve Claude for everyone` → `Off`
   - `Skill data sharing` → `Workspace only`
3. תיעוד DPO — שמור עותק של ה-DPA של Anthropic.

### 13.3 PII / מידע לקוח

עקרון: **אין להעלות ת"ז מלא, מספרי כרטיסי אשראי, או נתוני בריאות**.

יצירת Skill `/scrub-pii`:
```
Description: מסיר/ממסך PII לפני שליחה ל-Claude.
Instructions:
- ת"ז (9 ספרות) → "XXX-XX-XXXX"
- כרטיס אשראי (16 ספרות) → "XXXX-XXXX-XXXX-NNNN"
- אימייל → "user@example.com"
- שמור על המבנה הסמנטי של המסמך
```

הפעל את `/scrub-pii` *לפני* כל פקודה אחרת על מסמכים עם נתוני לקוח.

---

## 14. Checklist סופי

### 14.1 לפני הכרזה ש"ההטמעה הושלמה"

```
□ כל endpoint בארגון על Windows 10 22H2+ או Windows 11
□ Office build עדכני (Current Channel)
□ Claude add-in מופץ דרך M365 Admin Center
□ Microsoft 365 connection פעיל בכל user
□ מבנה תיקיות OneDrive סטנדרטי הוטמע
□ Skills ארגוניים נוצרו ו-published:
   □ /deal-quote
   □ /fleet-report
   □ /board-deck
   □ /scrub-pii
□ הדרכת משתמשים — 1 שעה לפחות, לכל צוות
□ Power-users הוגדרו בכל מחלקה (1-2 לצוות של 10)
□ Telemetry baseline נמדד (שבוע 0)
□ Security review הושלם (DPO + IT)
□ Backup של תבניות ב-`00_Templates` תקין
```

### 14.2 שבוע 4 — ביקורת

```
□ Adoption rate > 70% מבעלי הרישיון
□ ירידה של 30%+ בפעולות copy-paste בין דפדפן לקובץ (סקר)
□ לפחות 3 Skills בשימוש יומי
□ אפס אירועי DLP פתוחים
□ NPS פנימי על הכלי > +30
```

### 14.3 חודש 3 — בגרות

```
□ כל Skill ארגוני מתועד ב-COMMAND_API.md
□ playbooks לכל מחלקה (מכירות, פיננסים, IR, שיווק)
□ צמצום זמן הכנת דוחות חודשיים ב-50%+
□ צמצום זמן הכנת מצגות משקיעים ב-60%+
□ Skills חדשים נוצרים על ידי משתמשים, לא רק IT
```

---

## נספח א' — סקריפט אוטומציה מלא (PowerShell)

```powershell
<#
    Deploy-ClaudeForOffice.ps1
    הפעלה אחת על endpoint חדש = מוכן לעבודה
#>

#Requires -RunAsAdministrator

$ErrorActionPreference = "Stop"

Write-Host "==> Claude for Office — Endpoint Deployment" -ForegroundColor Cyan

# 1) בדיקת מערכת
$os = (Get-CimInstance Win32_OperatingSystem).Caption
Write-Host "OS: $os"

# 2) בדיקת Office
$officeVer = (Get-ItemProperty `
    "HKLM:\SOFTWARE\Microsoft\Office\ClickToRun\Configuration" `
    -ErrorAction SilentlyContinue).VersionToReport
Write-Host "Office: $officeVer"

if (-not $officeVer) {
    throw "Microsoft 365 לא נמצא. התקן לפני שתמשיך."
}

# 3) ניקוי cache של Add-ins
$wefPath = "$env:LOCALAPPDATA\Microsoft\Office\16.0\Wef"
if (Test-Path $wefPath) {
    Write-Host "מנקה Add-ins cache..."
    Remove-Item "$wefPath\*" -Recurse -Force -ErrorAction SilentlyContinue
}

# 4) רישום ה-Trusted Catalog (אם נדרש)
$trustedKey = "HKCU:\Software\Microsoft\Office\16.0\WEF\TrustedCatalogs"
if (-not (Test-Path $trustedKey)) {
    New-Item -Path $trustedKey -Force | Out-Null
}

# 5) פתיחת רשת — בדיקה
$endpoints = @("api.anthropic.com", "claude.ai", "console.anthropic.com")
foreach ($e in $endpoints) {
    $r = Test-NetConnection -ComputerName $e -Port 443 -InformationLevel Quiet
    Write-Host "$e : $(if($r){'OK'}else{'BLOCKED'})" `
        -ForegroundColor $(if($r){'Green'}else{'Red'})
}

# 6) הצגת הוראות סיום
Write-Host @"

ההטמעה ברמת מערכת ההפעלה הושלמה.

צעדים אחרונים שהמשתמש עושה:
  1. פתח Word.
  2. Home → Claude (אייקון בקצה).
  3. Sign in עם חשבון @leasing.co.il.
  4. רוץ /tldr על מסמך כלשהו לבדיקה.

"@ -ForegroundColor Green
```

שמור בנתיב `\\fileserver\IT\Deployment\Deploy-ClaudeForOffice.ps1` והפעל דרך
Intune script או GPO logon script.

---

## נספח ב' — מטריצת אחריות (RACI)

| משימה | IT | Power User | משתמש קצה | DPO | מנכ"ל |
|--------|----|-----------|------------|-----|--------|
| התקנת תוסף | R | I | I | I | I |
| הגדרת Skills ארגוניים | C | R | I | C | A |
| הדרכה | C | R | R | I | A |
| יצירת Skill אישי | I | C | R | I | I |
| Security review | C | I | I | R | A |
| ביקורת חודשית | R | C | I | C | A |

`R`=Responsible · `A`=Accountable · `C`=Consulted · `I`=Informed

---

## גרסאות

| גרסה | תאריך | שינוי |
|------|--------|-------|
| 1.0.0 | 2026-05-28 | Initial release — Windows end-to-end deployment |

---

**נקודת קישור ל-OS:** המסמך הזה נטען אוטומטית כשמופעל `COMMAND_API.md` ופקודות
`/install-office`, `/deploy-skill`, `/audit-office` יזהו אותו כמקור האמת
להטמעה על Windows.
