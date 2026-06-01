# CLAUDE COWORK — תוכנית מיגרציה מעשית (Claude OS → Cowork)

**Module:** `COWORK_MIGRATION.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — תוכנית ביצוע ידנית ב-Claude Desktop. אף שלב מחיקה אינו מבוצע על הריפו הזה — הריפו נשאר מקור-אמת מגובה-git.
**Integrates with:** `CLAUDE.md`, `OPERATING_SYSTEM.md`, `MEMORY.md`, `DECISION_LOG.md`, `COWORK_SETUP.md`, `COMMAND_API.md`, `INVESTOR_RELATIONS.md`, `CASES/*.md`

> **מצב Cowork:** GA מלא (macOS + Windows), קונקטורי Google פעילים. **תאריך:** 1 ביוני 2026.

---

## הקדמה — ההמשך של COWORK_SETUP

| מודול | תפקיד |
|--------|--------|
| `COWORK_SETUP.md` | **אונבורדינג** — איך מתחברים ל-Cowork (7 שלבי הגדרה, Global Instructions) |
| `COWORK_MIGRATION.md` (זה) | **מיגרציה** — איך עוברים אליו במלואו: מה נמחק, מה נשמר, באיזה סדר, ועם אילו שערי-אימות |

המסמך מנוסח ברמת **סביבת העבודה המלאה** (כל ה-workspace האישי), וכולל **מיפוי ייעודי לריפו הזה** (§5) — כך שכל הפניה במערכת מובילה לגוף אמיתי (No Dangling Modules).

---

## תוכן עניינים

1. [עיקרון מנחה](#1-עיקרון-מנחה)
2. [מבנה התיקייה היעד ב-Cowork](#2-מבנה-התיקייה-היעד-ב-cowork)
3. [טבלת הכרעה — סביבת העבודה המלאה](#3-טבלת-הכרעה--סביבת-העבודה-המלאה)
4. [רצף שלבים (7 שלבים)](#4-רצף-שלבים-7-שלבים-מהבטוח-למסוכן)
5. [מיפוי הריפו הזה ל-workspace היעד](#5-מיפוי-הריפו-הזה-ל-workspace-היעד)
6. [נקודות אימות קריטיות (gates)](#6-נקודות-אימות-קריטיות-gates)
7. [טיוטת Global Instructions (שלב 1)](#7-טיוטת-global-instructions-שלב-1)
8. [אזהרות וסיכונים](#8-אזהרות-וסיכונים-שיש-לתעד)
9. [Document Control](#document-control)

---

## 1. עיקרון מנחה

המעבר אינו "זריקת Claude OS" אלא **הפשטה (stripping)**: מוחקים את שכבת התשתית שנבנתה ביד (loader, registry, memory plumbing, Drive workflow) כי Cowork עושה אותה native — ומשמרים את שכבת ה-IP (סקילז, מסמכי תיקים, לוגיקה משפטית, data-quality) שאין ל-Cowork מקביל לה.

> **כלל בטיחות מקדים:** אל תמחק שום קובץ לפני שווידאת שהמערכת החדשה עובדת מקצה לקצה. כל מחיקה מתועדת ב-`DECISION_LOG.md` לפני ביצוע.

| שכבה | מה זה | גורל |
|------|--------|------|
| **תשתית (plumbing)** | loader, registry, memory plumbing, Drive workflow, רישום פקודות ידני | 🗑️ נמחקת — Cowork עושה זאת native (זיכרון, Projects, קונקטורים, slash commands) |
| **IP** | תיקים, playbooks, מתודולוגיה, לוגיקה משפטית, data-quality, יומן החלטות | 📌 נשמרת — אין ל-Cowork מקביל; זה הנכס |

---

## 2. מבנה התיקייה היעד ב-Cowork

כך ייראה ה-folder המקומי ש-Cowork יעבוד בו. ה-workspace נבנה **מחוץ לריפו הזה** (שלב 0); הסימונים מציינים מאיפה מגיע כל פריט:

- ✓ — קיים בריפו הזה (מקור: `leasing-api-co-il`)
- 🔜 — נוצר בזמן המיגרציה, או מגיע מהסביבה האישית הרחבה (מחוץ לריפו הזה)

```
ABRAHAM-WORKSPACE/                    ← folder ראשי שנותנים ל-Cowork גישה אליו (🔜 נבנה בשלב 0)
│
├── .global-instructions.md           ← 🔜 מחליף את CLAUDE.md — נטען כ-Global Instructions (טיוטה: §7 כאן)
│
├── skills/                           ← 🔜 חיצוני — 11 סקילז מהסביבה האישית הרחבה (drop-in, ללא שינוי)
│   ├── legal-automation/
│   ├── council-of-sages/
│   ├── leasing-platform/
│   └── ... (8 נוספים)
│
├── data-quality/                     ← 🔜 חיצוני — נשמר as-is (אין מקביל ב-Cowork)
│   ├── checks.ts
│   ├── runner.ts
│   └── edge.ts
│
├── architecture/                     ← מסמכי הכוונה (reference בלבד)
│   ├── OPERATING_SYSTEM.md           ← ✓ מהריפו הזה
│   ├── AGENTIC_SYSTEM.md             ← 🔜 חיצוני
│   └── AGENT_PIPELINE.md             ← 🔜 חיצוני
│
├── DECISION_LOG.md                   ← ✓ מהריפו הזה — append אמיתי (לא עוד עותקים מגרסאים)
│
└── projects/                         ← כל תיק = Cowork Project נפרד
    ├── ulease/                       ← ✓ מ-CASES/ בריפו הזה (כל תיק ULease)
    ├── ulease-seed/                  ← ✓ מ-INVESTOR_RELATIONS.md בריפו הזה
    ├── kapsula/                      ← 🔜 חיצוני
    ├── irusha-59951/                 ← 🔜 חיצוני (תיק משפטי)
    ├── bituach-leumi-42375/          ← 🔜 חיצוני (תיק משפטי)
    └── sheba-41802/                  ← 🔜 חיצוני (תיק משפטי)
```

---

## 3. טבלת הכרעה — סביבת העבודה המלאה

> טבלת המאסטר לכל סביבת העבודה האישית. העמודה **"בריפו הזה?"** מבהירה מה חי כאן ומה בסביבה הרחבה — להפניות שבריפו ראו את המיפוי המלא ב-§5.

| קובץ נוכחי | פעולה | יעד | מתי לבצע | בריפו הזה? |
|---|---|---|---|---|
| `CLAUDE.md` | 🔀 **למזג** | → `.global-instructions.md` | שלב 1 | ✓ |
| `MEMORY.md` | 🗑️ **למחוק** | זיכרון native + Projects | שלב 7 (אחרון) | ✓ |
| `OPERATING_SYSTEM.md` | 📌 **לשמור** | `architecture/` (reference) | שלב 2 | ✓ |
| `AGENTIC_SYSTEM.md` | 📌 **לשמור** | `architecture/` (reference) | שלב 2 | ❌ חיצוני |
| `AGENT_PIPELINE.md` | 🔀 **למזג** | תבנית תפקידים → Global Instructions; שאר → `architecture/` | שלב 1+2 | ❌ חיצוני |
| 11 הסקילז | 📌 **לשמור** | `skills/` (drop-in) | שלב 2 | ❌ חיצוני |
| `COMMAND_CENTER.md` | 🔀 **למזג** | פקודות → slash commands; לוגיקה → סקילז | שלב 5 | ❌ (המקבילה כאן: `COMMAND_API.md`) |
| `MCP_REGISTRY` module | 🗑️ **למחוק** | קונקטורים native של Cowork | שלב 4 | ❌ חיצוני |
| `DATA_QUALITY` (3 קבצי ts) | 📌 **לשמור** | `data-quality/` (as-is) | שלב 2 | ❌ חיצוני |
| `CASES/Kapsula-CASE.md` | 🔀 **למזג** | → `projects/kapsula/` | שלב 3 | ❌ (המקבילה כאן: `CASES/ULEASE*.md`) |
| `INVESTOR_RELATIONS.md` | 🔀 **למזג** | → `projects/ulease-seed/` | שלב 3 | ✓ |
| `DECISION_LOG.md` | 📌 **לשמור ולשפר** | append מקומי במקום עותקים | שלב 2 | ✓ |
| Google Drive workflow | 🗑️ **למחוק** | File System + Drive connector | שלב 4 | — (זרימת עבודה, לא קובץ) |

**סיכום מספרי (מאסטר):** 4 למחיקה · 5 לשמירה · 4 למיזוג.

---

## 4. רצף שלבים (7 שלבים, מהבטוח למסוכן)

### שלב 0 — הכנה (לפני נגיעה בכלום)
- [ ] התקן Claude Desktop ל-Windows מ-claude.com/download
- [ ] אם אתה על Windows Home: הפעל Virtual Machine Platform מלוח הבקרה + restart
- [ ] צור גיבוי מלא של Claude OS הנוכחי — נקודת שחזור (לריפו הזה: ה-git history הוא הגיבוי; ודא push עדכני)
- [ ] צור את תיקיית `ABRAHAM-WORKSPACE/` המקומית לפי המבנה ב-§2

### שלב 1 — Global Instructions (הלב)
- [ ] הטמע את `.global-instructions.md` (טיוטה מוכנה לריפו הזה: §7)
- [ ] הגדר אותו כ-Global Instructions ב-Cowork (Customize → Instructions)
- [ ] בדיקת אימות: פתח סשן ריק ושאל "מי אני ומה הכללים שלי" — ודא שהזהות נטענה

### שלב 2 — העתקת הנכסים שנשמרים (אפס סיכון, רק העתקה)
- [ ] העתק את הסקילז ל-`skills/` (מהסביבה הרחבה)
- [ ] העתק את קבצי ה-data-quality ל-`data-quality/` (מהסביבה הרחבה)
- [ ] העתק מסמכי ארכיטקטורה ל-`architecture/` (מהריפו הזה: `OPERATING_SYSTEM.md`, מודולי `AI_*`)
- [ ] העתק `DECISION_LOG.md` והמר לפורמט append יחיד
- [ ] בדיקת אימות: בקש מ-Cowork להריץ סקיל/פקודה אחת — ודא שנקלט

### שלב 3 — בניית ה-Projects
- [ ] צור Cowork Project לכל תיק (לריפו הזה: `projects/ulease/` + `projects/ulease-seed/`)
- [ ] מזג כל תיק ל-Project folder המתאים (`CASES/ULEASE*.md` → `projects/ulease/`)
- [ ] הגדר folder-specific instructions לכל Project (לריפו הזה: סטנדרט עברית/RTL, מקור לכל מספר פיננסי)
- [ ] בדיקת אימות: בקש טיוטה קצרה בתיק — ודא שהסטנדרט מיושם

### שלב 4 — חיבור קונקטורים והשבתת ה-plumbing הישן
- [ ] חבר Google Drive, Calendar, Gmail (Customize → Connectors → +)
- [ ] בדיקת אימות: בקש מ-Cowork לקרוא קובץ מ-Drive ולסכם — ודא גישה
- [ ] **רק לאחר אימות:** סמן את ה-Drive workflow הישן (`COWORK_SETUP.md` §2 שלב 3) כ-deprecated ב-`DECISION_LOG.md`

### שלב 5 — Slash Commands והחלפת ממשק הפקודות
- [ ] הגדר את הפקודות היומיומיות מ-`COMMAND_API.md` כ-slash commands
- [ ] בדיקת אימות: הרץ פקודה יומיומית דרך slash — ודא תוצאה זהה
- [ ] **רק לאחר אימות:** סמן את `COMMAND_API.md` כ-superseded ב-`DECISION_LOG.md` (הלוגיקה עברה ל-slash commands; הקובץ נשאר בריפו כ-reference)

### שלב 6 — תקופת הרצה מקבילה (2 שבועות)
- [ ] עבוד במקביל: Cowork כראשי, Claude OS הישן כגיבוי בלבד
- [ ] תעד כל פער/בעיה ב-`DECISION_LOG.md`
- [ ] אל תמחק את `MEMORY.md` בשלב זה

### שלב 7 — סגירה (רק אחרי שבועיים נקיים)
- [ ] סמן כ-deprecated את כל ה-plumbing (registry, Drive workflow, ממשק פקודות ידני)
- [ ] הוצא את `MEMORY.md` משימוש (זיכרון native + Projects החליפו אותו) — בריפו: עדכון סטטוס, לא מחיקה
- [ ] עדכן `DECISION_LOG.md`: "מיגרציה הושלמה"
- [ ] שמור את הגיבוי המלא לארכיון (לריפו הזה: ה-repo נשאר חי כארכיון מגובה-git — אל תמחק)

---

## 5. מיפוי הריפו הזה ל-workspace היעד

הכרעה לכל קובץ ב-`leasing-api-co-il` (43 קבצים). **אף קובץ לא נמחק מהריפו** — "מחיקה" משמעה שהקובץ לא עובר ל-workspace והתפקיד שלו עובר ליכולת native.

### 5.1 מודולי השורש

| קובץ בריפו | פעולה | יעד ב-workspace | שלב |
|---|---|---|---|
| `CLAUDE.md` | 🔀 למזג | → `.global-instructions.md` (טיוטה: §7) | 1 |
| `OPERATING_SYSTEM.md` | 📌 לשמור | → `architecture/` (reference) | 2 |
| `MEMORY.md` | 🗑️ לא עובר | זיכרון native + Projects מחליפים; בריפו — עדכון סטטוס בלבד | 7 |
| `DECISION_LOG.md` | 📌 לשמור ולשפר | → שורש ה-workspace, append יחיד | 2 |
| `COWORK_SETUP.md` | 🔀 למזג | האונבורדינג הושלם → נבלע ב-Global Instructions ובמודול הזה | 5 |
| `COMMAND_API.md` | 🔀 למזג | פקודות יומיומיות → slash commands; חוזי פלט → Global Instructions; הקובץ נשאר כ-reference | 5 |
| `marketing-strategy-framework.md` | 📌 לשמור | → `projects/ulease/` (knowledge עסקי) | 3 |
| `AI_SKILL_MAP.md` · `AI_PROGRESSION_PLAN.md` · `AI_LEARNING_RESOURCES.md` · `AI_7_SKILLS.md` · `AI_SKILLS_ACQUISITION.md` · `AI_TYPES.md` · `AI_CLAUDE_TOOL_SELECTOR.md` | 📌 לשמור | → `architecture/` (knowledge, on-demand) | 2 |
| `INVESTOR_RELATIONS.md` | 🔀 למזג | → `projects/ulease-seed/` | 3 |
| `README.md` | 📌 לשמור | נשאר בריפו (GitHub-facing; לא עובר ל-workspace) | — |
| `.claude/agents/os-auditor.md` | 📌 לשמור | נשאר בריפו (כלי Claude Code, לא Cowork) | — |

### 5.2 תיק ULease (`CASES/`)

| קבצים | פעולה | יעד ב-workspace | שלב |
|---|---|---|---|
| `ULEASE.md`, `ULEASE_SPEC.md`, `ULEASE_METHODOLOGY.md`, `ULEASE_AUDIT.md` | 🔀 למזג | → `projects/ulease/` (ליבת התיק) | 3 |
| `ULEASE_DECK.md/html/py`, `ULEASE_DASHBOARD.html/py` | 🔀 למזג | → `projects/ulease/` (פלטים + סקריפטים) | 3 |
| `ULEASE_FORECAST.py/csv`, `ULEASE_SCENARIOS.py/csv` | 🔀 למזג | → `projects/ulease/` (מודל פיננסי) | 3 |
| Playbooks: `IMPORTER`, `LEASING`, `DEMAND`, `OUTREACH_SCRIPTS`, `OUTBOUND_ENGINE` (+`n8n.json`/`py`), `PRICING_SLA`, `FINANCE_INSURANCE` | 🔀 למזג | → `projects/ulease/` (מו"מ ומכירות) | 3 |
| `ULEASE_HIRING.md`, `ULEASE_TECH_ONBOARDING.md`, `ULEASE_LAUNCH_CHECKLIST.md`, `ULEASE_AUTOMATION_MAP.md` | 🔀 למזג | → `projects/ulease/` (תפעול) | 3 |
| `ULEASE_FORECAST.csv` ופלטי HTML | 📌 לשמור | נוצרים מחדש מהסקריפטים — אין צורך להעביר ידנית | — |

**סיכום מספרי (הריפו הזה):** 1 לא-עובר (MEMORY) · 13 לשמירה · 29 למיזוג ל-Projects.

### 5.3 המלצת ביצוע — הריפו כ-workspace (אפשרות B)

לתוכנית המאסטר יש שתי דרכי ביצוע עבור הריפו הזה:

| | אפשרות A — לפי התוכנית | אפשרות B — הריפו הוא ה-workspace ⭐ מומלץ |
|---|---|---|
| **מהלך** | מעתיקים מהריפו ל-`ABRAHAM-WORKSPACE/` נפרד | משכפלים (clone) את הריפו מקומית ומחברים את Cowork ישירות אליו |
| **גיבוי** | תיקיית ארכיון ידנית | כל היסטוריית ה-git (21+ PRs) — נקודת שחזור לכל רגע |
| **סנכרון** | ידני (העתקות) | `git pull` / `git push` — מקור אמת אחד |
| **סיכון** | עותקים כפולים מתבדרים (הבעיה שהתוכנית באה לפתור) | אפס התבדרות; כל שינוי מתועד כ-commit |
| **מתי לבחור** | אם רוצים הפרדה מוחלטת בין ה-workspace לריפו | אם ממשיכים לעבוד גם עם Claude Code / GitHub (המצב הנוכחי) |

> **באפשרות B**, "המיגרציה" היא בעיקר ארגון מחדש של תיקיות בתוך הריפו (`projects/`, `architecture/`) + הגדרת Global Instructions — והתשתית הישנה מסומנת deprecated במקום להימחק.

---

## 6. נקודות אימות קריטיות (gates)

אל תעבור שלב לפני שעברת את ה-gate שלו:

| # | Gate | שלב | קריטריון מעבר |
|---|------|------|----------------|
| 1 | **Gate זהות** | 1 | Cowork מכיר את הזהות, השפה, הסטנדרטים (סשן ריק עונה נכון על "מי אני ומה הכללים שלי") |
| 2 | **Gate סקילז/פקודות** | 2 | לפחות סקיל אחד (בסביבה הרחבה) או פקודת `COMMAND_API` אחת (בריפו הזה) רצים בהצלחה |
| 3 | **Gate סטנדרט פלט** | 3 | בסביבה הרחבה: DOCX משפטי לפי הסטנדרט (David, RTL, 13pt). בריפו הזה: טיוטת תיק ULease בעברית/RTL שכל מספר בה מגובה במקור |
| 4 | **Gate קונקטור** | 4 | גישת קריאה/כתיבה ל-Drive עובדת |
| 5 | **Gate הרצה מקבילה** | 6 | שבועיים ללא פער מהותי |

---

## 7. טיוטת Global Instructions (שלב 1)

תוכן מוכן ל-`.global-instructions.md` עבור הריפו הזה — מיזוג של `CLAUDE.md` (רישום וטעינה), Boot Block (`OPERATING_SYSTEM.md` §4) וכרטיס הזהות (`MEMORY.md` §2):

```
# Global Instructions — Avraham Bar Yochai Chazan

## זהות
אברהם בר יוחאי חזן (avihazan112@gmail.com) — יזם, בעלים של Leasing.co.il / ULease:
פלטפורמת Marketplace תלת-צדדית (ספקים · ביקוש · מפיצים) למסחר רכבים חדשים בישראל.

## שפה וטון
עברית כברירת מחדל. מונחים טכניים באנגלית כשזה מדויק יותר. ישיר ותמציתי.

## לפני כל תשובה
1. קרא את DECISION_LOG.md — ההחלטה העדכנית גוברת על כל מסמך ישן.
2. שאלה על ULease (מוצר/תמחור/מו"מ) → קרא את projects/ulease/ הרלוונטי.
3. שאלה על גיוס/משקיעים → קרא את projects/ulease-seed/.

## כללי התנהגות (מה-Kernel)
- Context first — לעולם לא לענות גנרית כשיש זהות והקשר.
- אי-בהירות → שאלת הבהרה אחת ממוקדת, לא ניחוש.
- IP פנימי (Deal Score, Match API, אוטומציה משפטית) נשאר חסוי.
- כתיבה לזיכרון — רק באישור מפורש.

## סטנדרט פלט
- מסמכים עסקיים: עברית, RTL, טבלאות כשרלוונטי.
- כל מספר פיננסי חייב מקור (DECISION_LOG / תחזית ULease) — אין מספרים "מהאוויר".
- היררכיית הכרעה: Safety > חיסיון IP > החלטות מתועדות > העדפות > ברירת מחדל.
```

> **הערה:** בסביבה האישית הרחבה יש להוסיף לטיוטה את הסטנדרט המשפטי (David, RTL, 13pt) ואת תבנית התפקידים מ-`AGENT_PIPELINE.md` (חיצוני לריפו).

---

## 8. אזהרות וסיכונים שיש לתעד

- **תמונות ב-Drive:** הקונקטור מחלץ טקסט בלבד; ראיות סרוקות בתיקים לא ייקראו דרכו — השאר אותן מקומית ב-File System.
- **מחיקות הן בלתי הפיכות:** כל שלב מחיקה (4, 5, 7) מתועד ב-`DECISION_LOG.md` *לפני* הביצוע.
- **אל תמחק את הגיבוי:** נקודת השחזור נשמרת לארכיון לצמיתות. בריפו הזה — היסטוריית ה-git היא נקודת השחזור; הריפו לא נמחק ולא משוכתב.
- **עבודה משפטית:** כל כתב בי-דין נקרא מילה-במילה לפני הגשה — Cowork מנסח, אתה חותם.
- **פערי ספירה במאסטר:** סיכום המאסטר ("4 למחיקה · 5 לשמירה · 4 למיזוג") נשמר כלשונו מהמקור; הספירה המדויקת לריפו הזה היא ב-§5.2.

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | תוכנית מיגרציה ראשונית — עיקרון ההפשטה, מבנה יעד, טבלת הכרעה, 7 שלבים + gates, מיפוי הריפו, וטיוטת Global Instructions (D-020) | 2026-06-01 |

**Confidentiality.** קובץ זה הוא חלק מה-Claude Operating System האישי של Avraham Bar Yochai Chazan.

— *End of COWORK_MIGRATION.md v1.0.0 —*
