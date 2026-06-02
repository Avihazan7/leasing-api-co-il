# ספריית פקודות משימה — 98 Claude Task Commands

**Module:** `COMMAND_API_TASKS.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — Interface layer (§3 שורה 7). אחות של `COMMAND_API.md`.
**Source:** מבוסס על האינפוגרפיקה *"99 Claude (Secret) Commands"*.
**Integrates with:** `COMMAND_API.md`, `OPERATING_SYSTEM.md`, `COWORK_SETUP.md`, `CASES/ULEASE_OUTREACH_SCRIPTS.md`, `INVESTOR_RELATIONS.md`

> `COMMAND_API.md` מגדיר את **89 פקודות הליבה** — פרימיטיבים של workflow (חוזי פלט, composition, תחביר). המודול הזה מוסיף את **שכבת המשימות**: 98 פקודות-תרחיש ב-9 קטגוריות (המקור ממספר 1–99; ‎#84–85 הן פקודה אחת), מ"נסח סירוב מנומס" ועד "הכן אותי לפגישת 1:1". אותו תחביר, אותה הפעלה — חוזים ברמת המשימה.

---

## 1. היחס ל-Command API הראשי

| | `COMMAND_API.md` (ליבה) | `COMMAND_API_TASKS.md` (משימות) |
|---|---|---|
| **מהות** | פרימיטיבים: צורת פלט, חשיבה, ארגון | מתכונים: משימה שלמה מנוסחת כפקודה |
| **דוגמה** | `/shorten` — קצר כל טקסט | `/DECLINE` — נסח סירוב מנומס למייל |
| **כמות** | 89 | 98 (99 במספור המקור) |
| **הפעלה** | בלוק System Prompt (§8 שם) | נטען יחד — אותו מנגנון זיהוי `/command` |

**כלל הכרעה בהתנגשות שמות:** כשפקודת משימה חופפת לפקודת ליבה (`/EXAMPLES`·`/COMPARE`·`/CHECKLIST`·`/TLDR`·`/AGENDA` ↔ `/examples`·`/compare`·`/checklist`·`/tldr`), **חוזה הליבה גובר** על הצורה; מתכון המשימה מתווסף כהקשר. בפועל: אותה תוצאה, בלי קונפליקט.

---

## 2. הקטלוג — 9 קטגוריות

### 📧 א. אימייל והודעות (1–11)

| # | פקודה | ארגומנט | מה מקבלים |
|---|--------|----------|------------|
| 1 | `/DECLINE` | [email] | סירוב מנומס |
| 2 | `/SHORTEN` | [email] | חצי מהאורך, עיקרי הנקודות נשמרים |
| 3 | `/WARMER` | [email] | פחות נוקשה |
| 4 | `/FOLLOWUP` | [topic] | תזכורת עדינה למייל שלא נענה |
| 5 | `/SAYNO` | [request] | "לא" ששומר על מערכת היחסים |
| 6 | `/BULLETS2EMAIL` | [bullets] | נקודות → מייל נקי |
| 7 | `/THANKS` | [person + reason] | תודה קצרה וכנה |
| 8 | `/CONFIDENT` | [email] | מסיר התנצלויות וגמגום |
| 9 | `/OOO` | [dates + backup] | הודעת out-of-office |
| 10 | `/HARDMSG` | [person + topic] | מסר קשה, מכבד |
| 11 | `/INTRO` | [A + B + context] | היכרות double opt-in |

### ✏️ ב. כתיבה ועריכה (12–22)

| # | פקודה | ארגומנט | מה מקבלים |
|---|--------|----------|------------|
| 12 | `/PROOF` | [text] | תיקון שגיאות |
| 13 | `/REWRITE5` | [sentence] | חמש גרסאות |
| 14 | `/CUTHALF` | [text] | חיתוך לחצי |
| 15 | `/OPENERS` | [text] | שלוש שורות פתיחה חזקות יותר |
| 16 | `/FILLER` | [text] | סימון מילים חלשות |
| 17 | `/ACTIVE` | [text] | סביל → פעיל |
| 18 | `/HUMAN` | [text] | טקסט שנשמע AI → טבעי |
| 19 | `/EXAMPLES` | [text] | הוספת דוגמאות |
| 20 | `/SIMPLIFY` | [text] | ניסוח לרמת בן 12 |
| 21 | `/TITLES` | [text] | אפשרויות כותרת |
| 22 | `/TONE` | [text + vibe] | שכתוב בטון נבחר |

### 🧠 ג. חשיבה והחלטה (23–32)

| # | פקודה | ארגומנט | מה מקבלים |
|---|--------|----------|------------|
| 23 | `/CHOOSE` | [A vs B] | שקילת אפשרויות |
| 24 | `/REALPC` | [decision] | יתרונות וחסרונות אמיתיים |
| 25 | `/BLINDSPOT` | [situation] | מה אתה עלול לפספס |
| 26 | `/STEELMAN` | [view] | הדעה הנגדית בגרסתה החזקה |
| 27 | `/DEVIL` | [idea] | פרקליט השטן |
| 28 | `/SKEPTIC` | [plan] | שאלות הספקן |
| 29 | `/STEPS` | [problem] | צעד-אחר-צעד |
| 30 | `/RIPPLE` | [decision] | השלכות מסדר שני |
| 31 | `/PREMORTEM` | [plan] | איך זה עלול להיכשל |
| 32 | `/MINTEST` | [project] | הגרסה הקטנה ביותר לבדיקה בשבוע |

### 📚 ד. למידה והבנה (33–43)

| # | פקודה | ארגומנט | מה מקבלים |
|---|--------|----------|------------|
| 33 | `/ELI10` | [topic] | הסבר לבן 10 |
| 34 | `/PRIMER` | [topic] | קורס מזורז |
| 35 | `/MYTHS` | [topic] | תפיסות שגויות נפוצות |
| 36 | `/ANALOGY` | [concept] | השוואה מהעולם האמיתי |
| 37 | `/QUIZ` | [topic] | חמש שאלות |
| 38 | `/COMPARE` | [A vs B] | הבדלים |
| 39 | `/PREREQ` | [topic] | מה צריך לדעת קודם |
| 40 | `/SUM3` | [text] | סיכום בשלוש נקודות |
| 41 | `/GLOSSARY` | [topic] | הגדרת מונחי מפתח |
| 42 | `/ASKBETTER` | [topic] | השאלות שאתה צריך לשאול |
| 43 | `/MENTALMODEL` | [topic] | המודל המנטלי שפותח את הנושא |

### 📅 ה. תכנון וארגון (44–54)

| # | פקודה | ארגומנט | מה מקבלים |
|---|--------|----------|------------|
| 44 | `/WEEK` | [priorities] | תכנון שבוע |
| 45 | `/MILESTONES` | [goal + deadline] | אבני דרך שבועיות |
| 46 | `/PACK` | [trip] | רשימת אריזה |
| 47 | `/SCHEDULE` | [event + duration] | לו"ז מתוזמן |
| 48 | `/ROUTINE` | [goal] | שגרה יומית |
| 49 | `/PRIORITIZE` | [list] | סידור רשימת משימות |
| 50 | `/MEALS` | [ingredients] | שבוע ארוחות |
| 51 | `/AGENDA` | [topic + duration] | אג'נדת פגישה |
| 52 | `/PREPTIME` | [event + time] | תוכנית הכנה בזמן הנתון |
| 53 | `/ORDER` | [tasks] | רצף משימות |
| 54 | `/CHECKLIST` | [task] | צ'קליסט צעד-אחר-צעד |

### 💡 ו. סיעור מוחות (55–65)

| # | פקודה | ארגומנט | מה מקבלים |
|---|--------|----------|------------|
| 55 | `/IDEAS20` | [topic] | עשרים רעיונות |
| 56 | `/GIFTS` | [person + occasion + budget] | רעיונות מתנה |
| 57 | `/NAMES` | [thing + vibe] | רעיונות שמות |
| 58 | `/UNUSUAL` | [problem] | עשר גישות לא שגרתיות |
| 59 | `/ANGLE` | [topic] | זווית שמתפספסת |
| 60 | `/COMBINE` | [A + B] | שילוב לחמישה כיוונים |
| 61 | `/METAPHOR` | [concept] | מטאפורה |
| 62 | `/STARTERS` | [topic] | פתיחי שיחה לא משעממים |
| 63 | `/JOURNAL10` | [theme] | עשרה journal prompts |
| 64 | `/AS` | [role + problem] | פתרון כפי שמקצוען ספציפי היה פותר |
| 65 | `/CHILD` | [problem] | איך ילד סקרן היה פותר |

### 💼 ז. עבודה וקריירה (66–76)

| # | פקודה | ארגומנט | מה מקבלים |
|---|--------|----------|------------|
| 66 | `/INTERVIEWQ` | [questions] | הכנה לתשובות בטוחות |
| 67 | `/RESUMEBULLET` | [bullet] | שכתוב שורת קו"ח |
| 68 | `/ASKINTERVIEWER` | [role + company] | שאלות חכמות לשאול |
| 69 | `/NEGOTIATE` | [the ask] | תסריט המו"מ |
| 70 | `/RECONNECT` | [person + context] | פנייה מחודשת בלינקדאין |
| 71 | `/GAP` | [reason] | הסבר לפער בקריירה |
| 72 | `/WINS5` | [notes] | הישגים → חמש נקודות |
| 73 | `/ONEONONE` | [topic] | הכנה לשיחת 1:1 |
| 74 | `/SELFREVIEW` | [paste] | self-review מהפתקים שלך |
| 75 | `/IDONTKNOW` | [situation] | ניסוח מקצועי ל"עוד לא יודע" |
| 76 | `/RAISE` | [context] | תסריט בקשת העלאה |

### 📣 ח. תוכן ורשתות (77–88)

| # | פקודה | ארגומנט | מה מקבלים |
|---|--------|----------|------------|
| 77 | `/HOOK` | [topic] | חמישה פתיחים עוצרי-גלילה |
| 78 | `/CAPTION` | [photo/topic] | כיתוב קצר |
| 79 | `/THREAD` | [idea] | רעיון אחד, שרשור של שישה ציוצים |
| 80 | `/CARO` | [topic] | קרוסלה עם מבנה |
| 81 | `/REPURPOSE` | [post] | שלושה פורמטים |
| 82 | `/CTA` | [post] | שלוש קריאות לפעולה |
| 83 | `/BIO` | [details + vibe] | ביו קצר בשלושה סגנונות |
| 84–85 | `/SUBJECT` | [email/post] | חמש שורות נושא שנפתחות |
| 86 | `/CONTRARIAN` | [topic] | טייק נגדי חד, עדיין בר-הגנה |
| 87 | `/SHORTPOST` | [idea] | פוסט של 100 מילים |
| 88 | `/COMMENT` | [post] | שלוש תגובות חדות שמוסיפות ערך |

### 📝 ט. פגישות וסיכומים (89–99)

| # | פקודה | ארגומנט | מה מקבלים |
|---|--------|----------|------------|
| 89 | `/MEETINGNOTES` | [transcript] | תמליל גולמי → פרוטוקול נקי |
| 90 | `/ACTIONITEMS` | [notes] | חילוץ משימות ובעלים |
| 91 | `/STANDUP` | [yesterday + today + blockers] | פורמט עדכון יומי |
| 92 | `/RECAP` | [meeting] | סיכום בחמש שורות |
| 93 | `/DECISIONS` | [notes] | ההחלטות שהתקבלו |
| 94 | `/QUESTIONS` | [topic] | מה לשאול |
| 95 | `/STATUS` | [project] | עדכון סטטוס |
| 96 | `/BRIEFME` | [topic + paste] | תדרוך מהיר לפני פגישה |
| 97 | `/DEBRIEF` | [meeting] | מה עבד, מה לתקן |
| 98 | `/TLDR` | [paste] | הסיכום הקצר ביותר |
| 99 | `/RETRO` | [project] | מה עבד, מה לא, מה הלאה |

---

## 3. הפקודות שכבר עובדות בשבילך ב-ULease 🎯

| תרחיש ULease | הפקודות |
|---------------|----------|
| **Outreach ליבואנים/ליסינג** (`ULEASE_OUTREACH_SCRIPTS.md`) | `/FOLLOWUP` · `/HARDMSG` · `/INTRO` · `/RECONNECT` · `/NEGOTIATE` |
| **מו"מ עם ספקים** (Playbooks) | `/STEELMAN` · `/BLINDSPOT` · `/RIPPLE` · `/PREMORTEM` |
| **פגישות משקיעים** (`INVESTOR_RELATIONS.md`) | `/BRIEFME` · `/INTERVIEWQ` · `/RECAP` · `/ACTIONITEMS` · `/DECISIONS` |
| **שיווק צד-ביקוש** (`ULEASE_DEMAND_PLAYBOOK.md`) | `/HOOK` · `/CTA` · `/SUBJECT` · `/THREAD` · `/REPURPOSE` · `/CONTRARIAN` |
| **גיוס Tech Lead** (`ULEASE_HIRING.md`) | `/ASKINTERVIEWER` · `/INTERVIEWQ` · `/CHOOSE` |
| **ניהול שוטף** | `/WEEK` · `/PRIORITIZE` · `/STANDUP` · `/STATUS` · `/RETRO` |
| **בדיקת רעיונות מוצר** | `/MINTEST` · `/SKEPTIC` · `/UNUSUAL` · `/AS` |

---

## 4. הפעלה

נטען יחד עם בלוק ההפעלה של `COMMAND_API.md` §8 — אין צורך בבלוק נפרד. שורת ההרחבה היחידה:

```
TASK COMMANDS EXTENSION — COMMAND_API_TASKS.md
Recognize the 98 task commands (9 categories) with the same /command grammar.
On name collision with a core command, the core contract (COMMAND_API.md) wins.
```

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | ספריית פקודות משימה — 98 פקודות ב-9 קטגוריות (מקור: 99 Claude Commands) + מיפוי לתרחישי ULease וכלל הכרעה מול הליבה | 2026-06-02 |

**Attribution.** הקטלוג מבוסס על *99 Claude (Secret) Commands*. העיבוד, התרגום והמיפוי ל-ULease — חלק מה-Claude OS של Avraham Bar Yochai Chazan.

**Confidentiality.** קובץ זה הוא חלק מה-Claude Operating System האישי של Avraham Bar Yochai Chazan.

— *End of COMMAND_API_TASKS.md v1.0.0 —*
