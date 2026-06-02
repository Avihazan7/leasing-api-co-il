# CLAUDE COMMAND API — Master Reference & Router

**Module:** `COMMAND_API.md`
**Version:** 1.1.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Drop-in. Add to OS context to activate.
**Integrates with:** כל המודולים הרשומים ב-`OPERATING_SYSTEM.md` §3 (קרנל, זיכרון, הקשר, Knowledge ו-Business).

---

## הקדמה — מה זה ולמה

**עובדה חשובה לפני שמתחילים:** ב-claude.ai/anthropic אין `/commands` מובנים. הסלאש קומנדים שמסתובבים ברשת (כולל הגרסה של 89 פקודות) הם framework של יוצרי תוכן — לא תכונה של המוצר.

**אבל הם יכולים לעבוד.** הקובץ הזה הופך אותם ל-API התנהגותי אמיתי: ברגע שהוא טעון בהקשר של Claude (דרך userPreferences, system prompt, או טעינה דרך OS שלך), Claude מזהה תחביר `/command` ופועל לפי החוזה המוגדר כאן.

**מטרת המסמך:**
1. להגדיר חוזה מדויק ל-89 הפקודות (מה הקלט, מה הפלט, מה ההתנהגות)
2. להגדיר composition — איך פקודות מתחברות יחד
3. לספק system prompt drop-in שמטמיע את הכל
4. להשתלב עם ה-OS הקיים בלי קונפליקטים

---

## תוכן עניינים

1. [ארכיטקטורה ועקרונות](#1-ארכיטקטורה-ועקרונות)
2. [תחביר פקודות (Grammar)](#2-תחביר-פקודות-grammar)
3. [טבלת ייחוס מהירה — כל 89 הפקודות](#3-טבלת-ייחוס-מהירה)
4. [קטלוג פקודות מפורט (11 קטגוריות)](#4-קטלוג-פקודות-מפורט)
5. [Composition — שילוב פקודות](#5-composition--שילוב-פקודות)
6. [Power Shortcuts](#6-power-shortcuts)
7. [Prompting Frameworks — מסגרות לכתיבת פרומפטים](#7-prompting-frameworks--מסגרות-לכתיבת-פרומפטים)
8. [System Prompt — Drop-in](#8-system-prompt--drop-in)
9. [אינטגרציה עם ה-Claude OS שלך](#9-אינטגרציה-עם-ה-claude-os-שלך)
10. [הרחבה ויצירת פקודות אישיות](#10-הרחבה-ויצירת-פקודות-אישיות)
11. [גרסאות וחיפוי לאחור](#11-גרסאות-וחיפוי-לאחור)
12. [נספח: כללי הכרעה ו-edge cases](#12-נספח)

---

## 1. ארכיטקטורה ועקרונות

### 1.1 מודל מנטלי

הפקודות **לא** משנות את Claude — הן מצמצמות את מרחב ההתנהגויות שלו לקטגוריה ספציפית. כל פקודה היא **התחייבות לפלט מסוג מסוים**.

```
Default Claude  →  conversational, helpful, length-adaptive
                ↓  (פקודה מצמצמת)
/tldr           →  ≤ 3 שורות, נקודות עיקריות בלבד, אין preamble
```

זו הסיבה שזה עובד בלי תמיכת מוצר: הפקודה היא הוראה מבנית, לא קריאת API.

### 1.2 חמישה עקרונות יסוד

| עיקרון | משמעות |
|--------|--------|
| **One Command, One Job** | כל פקודה עושה דבר אחד. אם רוצים שניים — מחברים שניים. |
| **Deterministic Output Shape** | פלט של `/bullet` תמיד bullets. אם בקשה מתנגשת עם פקודה, הפקודה מנצחת. |
| **Implicit Args** | `/focus AI` = `AI` הוא הארגומנט. אין צורך ב-syntax מורכב. |
| **Stateless by default** | כל פקודה עומדת בפני עצמה. State משותף רק ב-`/context` ו-`/focus`. |
| **Fail Loud, Not Silent** | פקודה לא ברורה → Claude שואל הבהרה במקום לנחש. |

### 1.3 שכבות

```
┌──────────────────────────────────────────────────────┐
│  USER LAYER     (you typing /command args)           │
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│  PARSER         (recognizes /command + args)         │
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│  COMMAND CATALOG  (this file — 89 contracts)         │
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│  CLAUDE OS      (CLAUDE.md + skills + memory)        │
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│  EXECUTION      (Claude generates the output)        │
└──────────────────────────────────────────────────────┘
```

---

## 2. תחביר פקודות (Grammar)

### 2.1 צורות הקלט המקובלות

```
/command                          ← פקודה ללא ארגומנטים
/command arg                      ← פקודה עם ארגומנט
/command "arg with spaces"        ← ארגומנט עם רווחים
/command arg1 /command2 arg2      ← שתי פקודות ברצף (sequential)
/command1 | /command2             ← pipeline (פלט של 1 → קלט של 2)
/command1 + /command2             ← composition (שתי ההתנהגויות יחד)
/command --flag                   ← דגל מודיפיקטור
```

### 2.2 כללי שדרוג

| מצב | התנהגות |
|-----|----------|
| פקודה לא מוכרת | "פקודה לא זוהתה. רצית X או Y?" |
| ארגומנט חסר (נדרש) | שאלת המשך אחת בלבד, ממוקדת |
| התנגשות בין פקודות | אחרונה מנצחת (`/shorten /expand` → `/expand`) |
| פקודה בתוך טקסט רגיל | Claude מתעלם — לא כל "/" הוא פקודה |
| פקודה לא בתחילת השורה | אופציונלי: מטופלת רק אם זה הניסוח היחיד בהודעה |

### 2.3 escape

כדי לכתוב `/word` כטקסט רגיל (לא כפקודה): `\/word` או "`/word`" בתוך גרשיים.

---

## 3. טבלת ייחוס מהירה

| # | פקודה | קטגוריה | מה זה עושה |
|---|-------|---------|------------|
| 1 | `/new` | Start | מסמן התחלת thread חדש לוגית בתוך השיחה |
| 2 | `/project` | Start | מצהיר project context — Claude מנהל אותו לרוחב פניות |
| 3 | `/upload` | Start | מסמן שהמשתמש העלה קובץ — קרא אותו לפני המשך |
| 4 | `/paste` | Start | המידע הבא הוא paste — התייחס אליו כקלט גולמי |
| 5 | `/template` | Start | השתמש בתבנית — שם התבנית כארגומנט |
| 6 | `/import` | Start | ייבא תוכן מקובץ — נתיב כארגומנט |
| 7 | `/scan` | Start | סרוק מסמך — OCR או extract מובנה |
| 8 | `/voice` | Start | קלט הוא תמליל קולי — סלח על שגיאות תמלול |
| 9 | `/focus` | Focus | קבע מטרה ראשית לשיחה — Claude לא יסטה |
| 10 | `/context` | Focus | הוסף רקע לפני הבקשה הבאה |
| 11 | `/details` | Focus | ספק יותר פרטים בתשובה |
| 12 | `/examples` | Focus | תן דוגמאות מוחשיות, לא רק הסברים |
| 13 | `/clarify` | Focus | שאל את כל שאלות ההבהרה הנדרשות |
| 14 | `/define` | Focus | הגדר מונחים מרכזיים לפני המשך |
| 15 | `/assumptions` | Focus | חשוף את ההנחות שאתה עושה |
| 16 | `/priorities` | Focus | קבע סדר עדיפויות |
| 17 | `/constraints` | Focus | רשום אילוצים |
| 18 | `/analyze` | Think | פירוק לרכיבים — בלי מסקנה מהירה |
| 19 | `/compare` | Think | השווה שתי אפשרויות ומעלה |
| 20 | `/pros-cons` | Think | יתרונות וחסרונות במבנה מקביל |
| 21 | `/evaluate` | Think | הערכה לפי קריטריונים מוצהרים |
| 22 | `/recommend` | Think | המלצה ברורה + נימוקים |
| 23 | `/brainstorm` | Think | רעיונות — כמות לפני איכות |
| 24 | `/solve` | Think | פתור — תהליך ופתרון מובהק |
| 25 | `/challenge` | Think | תקוף את ההנחה — סנגור השטן |
| 26 | `/write` | Write | כתוב תוכן חדש — נושא כארגומנט |
| 27 | `/edit` | Write | ערוך לבהירות, שמור על משמעות |
| 28 | `/rewrite` | Write | כתוב מחדש בגישה חדשה |
| 29 | `/shorten` | Write | קצר — שמור על מה שחשוב |
| 30 | `/expand` | Write | הרחב — הוסף עומק ופירוט |
| 31 | `/improve` | Write | שפר כתיבה — סגנון, רהיטות, חוזק |
| 32 | `/summarize` | Write | סכם — כל המידע, מבנה מקוצר |
| 33 | `/paraphrase` | Write | נסח מחדש — שמור משמעות, שנה ניסוח |
| 34 | `/proofread` | Write | הגהה — דקדוק, איות, פיסוק |
| 35 | `/outline` | Organize | צור מבנה היררכי |
| 36 | `/structure` | Organize | סדר תוכן קיים למבנה ברור |
| 37 | `/bullet` | Organize | פלט bullets בלבד |
| 38 | `/numbered` | Organize | פלט רשימה ממוספרת |
| 39 | `/table` | Organize | פלט טבלה — עמודות מסבירות עצמן |
| 40 | `/summary` | Organize | פסקת סיכום — לא רשימה |
| 41 | `/key-points` | Organize | חלץ נקודות מפתח בלבד |
| 42 | `/mindmap` | Organize | mindmap בטקסט/Mermaid |
| 43 | `/flowchart` | Organize | flowchart בטקסט/Mermaid |
| 44 | `/code` | Code | כתוב קוד — שפה בארגומנט או נסיק |
| 45 | `/debug` | Code | מצא ותקן באג |
| 46 | `/explain` | Code | הסבר קוד — שורה אחר שורה אם צריך |
| 47 | `/optimize` | Code | שפר ביצועים — זמן/זיכרון/קריאות |
| 48 | `/refactor` | Code | שנה מבנה בלי לשנות התנהגות |
| 49 | `/test` | Code | כתוב tests — unit/integration לפי הקשר |
| 50 | `/convert` | Code | המר פורמט/שפה |
| 51 | `/documentation` | Code | כתוב docs לקוד |
| 52 | `/review` | Code | סקירת קוד — נקודות לשיפור, לא תיקון מיידי |
| 53 | `/analyze-data` | Data | נתח נתונים — סטטיסטיקה תיאורית + תובנות |
| 54 | `/visualize` | Data | צור גרף — סוג מתאים לנתונים |
| 55 | `/insights` | Data | חלץ תובנות — לא רק תיאור, גם משמעות |
| 56 | `/forecast` | Data | תחזית — מודל פשוט + הנחות מפורשות |
| 57 | `/report` | Data | דוח מקיף — תקציר, ניתוח, מסקנות |
| 58 | `/stats` | Data | סטטיסטיקות — מספרים, לא פרשנות |
| 59 | `/clean` | Data | נקה נתונים — duplicates, NaN, outliers |
| 60 | `/workflow` | Automate | תכנן workflow — שלבים, תפקידים, גיבויים |
| 61 | `/automate` | Automate | הצע אוטומציה — כלים + script |
| 62 | `/api` | Automate | אינטגרציה עם API — קוד דוגמה |
| 63 | `/integrate` | Automate | חבר שני כלים/מערכות |
| 64 | `/schedule` | Automate | תזכורת/timing — בלי לעקוב פעיל |
| 65 | `/trigger` | Automate | הגדר טריגר — תנאי + פעולה |
| 66 | `/tasklist` | Automate | צור רשימת משימות בת-ביצוע |
| 67 | `/checklist` | Automate | צ'קליסט עם תיבות סימון |
| 68 | `/preferences` | Personalize | קבע/שנה העדפות — נכנס ל-userPreferences |
| 69 | `/memory` | Personalize | נהל זיכרון — view/add/remove |
| 70 | `/tone` | Personalize | שנה טון — ארגומנט: formal/casual/expert/coach |
| 71 | `/style` | Personalize | שנה סגנון כתיבה — בארגומנט |
| 72 | `/length` | Personalize | קבע אורך תשובה — short/medium/long/X words |
| 73 | `/format` | Personalize | שנה פורמט תשובה — bullets/prose/table |
| 74 | `/reset` | Personalize | אפס מצב שיחה — שמור הקשר, נקה הוראות זמניות |
| 75 | `/clear` | Personalize | נקה הקשר — התחל נקי |
| 76 | `/search` | Learn | חיפוש web — Claude משתמש בכלי |
| 77 | `/research` | Learn | מחקר עמוק — מקורות מרובים, סינתזה |
| 78 | `/learn` | Learn | הסבר נושא — pedagogical mode |
| 79 | `/tldr` | Learn | סיכום של ≤ 3 שורות |
| 80 | `/sources` | Learn | מצא וצטט מקורות |
| 81 | `/fact-check` | Learn | בדוק עובדה — confidence + מקור |
| 82 | `/explore` | Learn | חקור נושא רחב — נושאי משנה ושאלות |
| 83 | `/share` | Collab | הכן תוכן לשיתוף — פורמט נקי |
| 84 | `/export` | Collab | ייצא — Markdown/PDF/HTML לפי הקשר |
| 85 | `/download` | Collab | הכן קובץ להורדה |
| 86 | `/copy` | Collab | פורמט שמתאים ל-clipboard |
| 87 | `/email` | Collab | טיוטת מייל — נושא + גוף + חתימה |
| 88 | `/publish` | Collab | הכן לפרסום — title, lead, body, meta |
| 89 | `/feedback` | Collab | בקש משוב — שאלות מובנות |

---

## 4. קטלוג פקודות מפורט

### קטגוריה 1: Start & Create

הפקודות בקטגוריה זו **פותחות** משימה או הקשר. הן רובן stateful — קובעות משהו שמשפיע על ההמשך.

#### `/new`
**Trigger:** `/new` או `/new <topic>`
**Behavior:** Claude מתייחס להמשך כ-thread חדש לוגית. ניקוי הקשר רך — זוכר מי המשתמש (שמירה על userMemories) אבל "שוכח" את ה-thread הקודם בשיחה.
**Use case:** עוברים מנושא משפטי לנושא תכנותי באותה שיחה.
**Output:** הודעה קצרה: "Thread חדש. במה נתחיל?"
**Example:**
```
You: /new Leasing pitch deck
Claude: Thread חדש על Leasing pitch deck. כמה שקפים? קהל יעד?
```

#### `/project`
**Trigger:** `/project <name>` או `/project <name> <description>`
**Behavior:** רושם project context שיישמר לכל אורך השיחה. כל פלט מתייחס אליו כברירת מחדל.
**Persistent:** עד `/new` או `/clear`.
**Example:**
```
You: /project Kapsula חירום משפחה
Claude: Project pinned. כל בקשה מכאן תתייחס לתיק קפסולה אלא אם תציין אחרת.
```

#### `/upload` `/paste` `/import` `/scan`
ארבע פקודות לסימון מקור הקלט:
- `/upload` — קובץ שהועלה למערכת (Claude יקרא ממנו)
- `/paste` — הדבקה מ-clipboard (טקסט גולמי, ייתכן עם בעיות פורמט)
- `/import <path>` — קריאה מנתיב מקובץ
- `/scan` — מסמך לסריקה (OCR אם דרוש, אחרת extract)

**Behavior משותף:** Claude מאשר קליטה לפני שמתחיל לעבוד. "קלטתי את X. מה לעשות איתו?"

#### `/template`
**Trigger:** `/template <name>` או `/template <name> with <vars>`
**Behavior:** ממלא תבנית שמורה. אם השם לא מזוהה — Claude מציע את הרשימה הזמינה.
**Pre-defined templates (Avraham OS):**
- `legal-document` — מסמך משפטי בפורמט David RTL
- `investor-email` — מייל למשקיע
- `case-summary` — סיכום תיק משפטי
- `pitch-deck-slide` — שקף בודד למצגת
- `decision-log-entry` — רשומה ל-DECISION_LOG.md

#### `/voice`
**Trigger:** `/voice` ואז תמליל
**Behavior:** Claude סלחני לשגיאות תמלול נפוצות (homophones, פיסוק חסר). יבקש הבהרה רק אם זה משנה משמעות מהותית.

---

### קטגוריה 2: Focus & Context

פקודות שעוטפות את הבקשה בהקשר נוסף. **רובן מודיפיקטורים** — מצורפות לבקשה אמיתית, לא עומדות לבדן.

#### `/focus`
**Trigger:** `/focus <objective>`
**Behavior:** קובע מטרה ראשית. Claude מסרב לסטות גם אם המשתמש שואל משהו צדדי — מציין שזה צדדי ומציע "להחזיר ל-focus".
**Persistent:** עד `/focus <new>` או `/clear`.
**Example:**
```
You: /focus סגירת סבב seed תוך 90 יום
[Later]
You: בוא נדבר על השיווק
Claude: זה מתרחק מ-focus (סגירת seed). רוצה: (a) להחזיר ל-focus, (b) להחליף focus, (c) discussion קצרצר בלי לאבד focus?
```

#### `/context`
**Trigger:** `/context <background>` ואז הבקשה
**Behavior:** הרקע הוא מידע נדרש לפני שהבקשה תעובד. Claude מתייחס אליו כעובדה.

#### `/details` ↔ `/shorten` ↔ `/expand`
שלוש פקודות שמשנות רמת פירוט (חלק מטופלות גם בקטגוריה 4):
- `/details` — Claude יוסיף עומק בתשובות הבאות (טמפורלית, לא לכל השיחה)
- `/shorten` — נגדי
- `/expand` — equivalent ל-`/details` עם דגש על "תוסיף מה שחסר"

#### `/clarify`
**Trigger:** `/clarify` או `/clarify <subject>`
**Behavior:** Claude שואל **את כל** שאלות ההבהרה הנדרשות לפני שיתחיל לעבוד. בדרך כלל 2–5 שאלות, ממוקדות. **חוסך איטרציות.**
**Example:**
```
You: /clarify הכן לי מצגת
Claude: 1. קהל היעד? 2. מספר שקפים? 3. שפה? 4. עברית או אנגלית? 5. יש מצגות קודמות לשמור בעקבותיהן?
```

#### `/examples`
**Trigger:** משולב ברוב הבקשות (`/examples write X`, `/examples explain Y`)
**Behavior:** Claude נשען על מקרים מוחשיים — תמיד 2–3 דוגמאות, לא תאוריה לבד.

#### `/define` `/assumptions` `/priorities` `/constraints`
מקבץ של ארבעה — כל אחד **מציג** משהו לפני שמתחילים:
- `/define <terms>` — Claude מגדיר מונחים שיופיעו לפני העבודה
- `/assumptions` — Claude מציג מה הוא מניח לפני שיתחיל; המשתמש יכול לתקן
- `/priorities` — שואל איך לסדר עדיפויות אם יש קונפליקט
- `/constraints` — מבקש לרשום אילוצים (זמן, תקציב, regulatory)

---

### קטגוריה 3: Think & Solve

ה**פקודות החזקות ביותר** למקרים של החלטה. רובן מצדדות **בהפרדה בין ניתוח ובין המלצה** — קודם חושבים, אז ממליצים.

#### `/analyze`
**Trigger:** `/analyze <subject>`
**Behavior:** Claude מפרק את הנושא לרכיבים. **לא** ממליץ. תפקיד הפקודה — להציג את שדה הבעיה.
**Output shape:** 4–7 רכיבים, כל אחד עם 2–4 משפטי הסבר.

#### `/compare`
**Trigger:** `/compare X vs Y` או `/compare A, B, C`
**Behavior:** טבלת השוואה לפי קריטריונים נגזרים מההקשר. הקריטריונים יוצגו מפורשות.
**Output shape:** טבלה + 2–3 שורות סיכום (בלי המלצה — לזה יש `/recommend`).

#### `/pros-cons`
**Trigger:** `/pros-cons <option>` או על שתי אפשרויות בנפרד
**Behavior:** שני טורים מקבילים, מינימום 3 פריטים בכל צד. אם צד אחד דליל — Claude מציין: "מאמץ לאזן אבל יתרונות/חסרונות אמיתיים כאן הם א-סימטריים."

#### `/evaluate`
**Trigger:** `/evaluate <thing> using <criteria>` — אם criteria לא ניתנו, Claude יציע 4–6.
**Behavior:** ציון לכל קריטריון (1–5 או 1–10) + שורת רציונל. ציון סופי משוקלל אם דרוש.

#### `/recommend`
**Trigger:** `/recommend X` (אחרי `/analyze` או `/compare`, או עצמאית)
**Behavior:** המלצה אחת ברורה. נימוקים. אזכור הסיכון העיקרי. אופציה אחת חלופית.
**Anti-pattern:** "תלוי" — אסור. אם תלוי, Claude מבקש את המידע החסר.

#### `/brainstorm`
**Trigger:** `/brainstorm <topic>` או `/brainstorm <topic> --count 15`
**Behavior:** רעיונות מרובים. ברירת מחדל: 10. **בלי לסנן ולבקר** ברגע הראשון — זה תפקיד `/evaluate` לאחר מכן.
**Output shape:** רשימה ממוספרת קצרה. כל רעיון בשורה אחת.

#### `/solve`
**Trigger:** `/solve <problem>`
**Behavior:** פתרון מובהק — לא ניתוח. Claude עוקב אחרי תהליך: הבנה → אסטרטגיה → ביצוע → אימות.
**Output shape:** 4 חלקים בכותרות.

#### `/challenge`
**Trigger:** `/challenge <thesis>` או `/challenge <my last answer>`
**Behavior:** Claude נכנס לתפקיד סנגור השטן. תוקף את ההנחה הכי חזקה. **לא** מתנצל ולא מסייג. אחרי שגומר, מציין: "זו עמדת מנגד — לא בהכרח מה שאני חושב."

---

### קטגוריה 4: Write & Edit

#### `/write`
**Trigger:** `/write <type> <topic>` או רק `/write <topic>` (סוג נסיק מהקשר)
**Behavior:** יצירה מאפס. מבקש הבהרת אורך/קהל אם לא ברור.

#### `/edit`
**Trigger:** `/edit` + טקסט קיים
**Behavior:** עריכה **שמרנית** — קולו של הכותב נשמר. שינויים מוצגים בסוף ברשימה ("שיניתי: 1. ..., 2. ...").

#### `/rewrite`
**Trigger:** `/rewrite` + טקסט + הנחיה אופציונלית
**Behavior:** כתיבה מחדש **תוקפנית** — קולו של הטקסט עשוי להשתנות. אופציה: `/rewrite formal`, `/rewrite punchy`, `/rewrite simpler`.

#### `/shorten`
**Trigger:** `/shorten` + טקסט, או `/shorten by 50%`
**Behavior:** מקצר תוך שמירה על תוכן עיקרי. אם המשתמש לא ציין יעד — חותך ~40%.

#### `/expand`
**Trigger:** `/expand` + טקסט
**Behavior:** מוסיף עומק — לא רק יותר מילים. דוגמאות, ניואנס, רקע.

#### `/improve` `/summarize` `/paraphrase` `/proofread`
- `/improve` — שיפור כללי: בהירות + חוזק + רהיטות
- `/summarize` — כל המידע, פחות מילים
- `/paraphrase` — אותה משמעות, ניסוח שונה (שימושי להימנעות מהעתקה)
- `/proofread` — רק שגיאות: דקדוק, איות, פיסוק. **לא** משפר סגנון.

---

### קטגוריה 5: Organize & Structure

פקודות **פלט-מבני**. כל אחת מתחייבת לצורת פלט.

| פקודה | Output Contract |
|-------|-----------------|
| `/outline` | היררכיה ממוספרת/אותיות, 2–3 רמות עומק |
| `/structure` | משחזר תוכן קיים למבנה הגיוני |
| `/bullet` | bullets בלבד, ללא prose עוטף |
| `/numbered` | רשימה ממוספרת, סדר משמעותי |
| `/table` | טבלה — עמודות חייבות להיות מסבירות עצמן |
| `/summary` | פסקה אחת (לא רשימה!) |
| `/key-points` | 3–7 נקודות, **קצרות** |
| `/mindmap` | Mermaid mindmap או indent-based |
| `/flowchart` | Mermaid flowchart |

**כלל ההכרעה בקטגוריה הזו:** אם המשתמש מבקש "הכן לי X" ומשלב פקודה מבנית, הפקודה המבנית **קובעת את הצורה**, לא ברירת המחדל של Claude.

---

### קטגוריה 6: Code & Tech

#### `/code`
**Trigger:** `/code <language> <task>` או `/code <task>` (Claude יחליט שפה)
**Behavior:**
- אם המשימה > 50 שורות → קובץ בנפרד
- תמיד מתועד מינימלית
- error handling כלול
- אם יש Claude OS skill רלוונטי (Python, TS, React) — נטען לפני הכתיבה

#### `/debug`
**Trigger:** `/debug` + הקוד הבעייתי + (אופציונלי) פלט השגיאה
**Behavior:** Claude מאתר את הבעיה, מסביר למה היא קורית, מציע תיקון. **לא** מציע פתרון לפני שמסביר את הסיבה — מונע "fixed it" בלי הבנה.

#### `/explain`
**Trigger:** `/explain <code>` או `/explain <concept>`
**Behavior:** הסבר ברמת המשתמש. אם Claude לא יודע את רמת המשתמש — שואל אחת ("מתחיל / מנוסה?").

#### `/optimize`
**Trigger:** `/optimize <code> for <speed|memory|readability>`
**Behavior:** מציג Before/After + מדד שיפור (theoretical או measured).

#### `/refactor`
**Trigger:** `/refactor` + קוד
**Behavior:** **שינוי מבנה בלבד**, ללא שינוי התנהגות. tests חייבים להמשיך לעבור.

#### `/test`
**Trigger:** `/test <code>` — בוחר רמה: unit / integration / e2e לפי ההקשר
**Behavior:** כיסוי happy path + 2–3 edge cases לפחות.

#### `/convert`
**Trigger:** `/convert <input> to <target>` — שפה לשפה, פורמט לפורמט (JSON↔YAML, CSV↔Markdown table וכו')

#### `/documentation`
**Trigger:** `/documentation <code>`
**Behavior:** כותב README-style: מטרה, התקנה, שימוש, API, דוגמאות.

#### `/review`
**Trigger:** `/review <code>`
**Behavior:** code review — מצביע על בעיות **לא** מתקן ישירות. רמות חומרה: 🔴 חובה, 🟡 מומלץ, 🟢 רעיון.

---

### קטגוריה 7: Data & Analysis

#### `/analyze-data`
**Trigger:** `/analyze-data` + נתונים (CSV/Excel/JSON)
**Behavior:** סטטיסטיקה תיאורית + 3–5 תובנות לא טריוויאליות. **לא** רק "ממוצע 42, חציון 39".

#### `/visualize`
**Trigger:** `/visualize <data>` — Claude בוחר סוג גרף לפי הנתונים (אלא אם צוין)
**Behavior:** מייצר את הגרף בפועל אם זמין כלי, או נותן קוד matplotlib/recharts מוכן.

#### `/insights`
**Trigger:** `/insights <data>`
**Behavior:** **רק** התובנות החזקות. בלי תיאור נתונים. כל תובנה: מה + למה + מה לעשות.

#### `/forecast`
**Trigger:** `/forecast <metric> <horizon>` (למשל 12 חודשים)
**Behavior:** תחזית עם הנחות מפורשות. **תמיד** מציג טווח אי-וודאות.

#### `/report`
**Trigger:** `/report <topic>`
**Behavior:** דוח מקיף בחלקים: Executive Summary → Findings → Analysis → Conclusions → Recommendations.

#### `/stats`
**Trigger:** `/stats <data>`
**Behavior:** מספרים בלבד — mean/median/mode/std/quartiles/correlations. **בלי פרשנות** (לזה יש `/insights`).

#### `/clean`
**Trigger:** `/clean <data>`
**Behavior:** מציג מה זוהה (duplicates, NaN, outliers, type mismatches), מציע פעולה, מבצע לאחר אישור.

---

### קטגוריה 8: Automate & Integrate

#### `/workflow`
**Trigger:** `/workflow <process>`
**Behavior:** תכנון תהליך — שלבים, owner של כל שלב, גיבויים, KPIs.

#### `/automate`
**Trigger:** `/automate <task>`
**Behavior:** מציע פתרון בכלים זמינים (Zapier/Make/Python/n8n) + script אם רלוונטי + עלות מוערכת.

#### `/api`
**Trigger:** `/api <integration>` (לדוגמה: `/api Gmail send email`)
**Behavior:** קוד דוגמה מלא + authentication setup + טיפול בשגיאות.

#### `/integrate`
**Trigger:** `/integrate <A> with <B>`
**Behavior:** ארכיטקטורת חיבור — endpoints, schemas, error handling, אבטחה.

#### `/schedule`
**Trigger:** `/schedule <reminder> at <time>`
**Behavior:** מתעד את התזכורת בשיחה. **שקיפות:** Claude לא מנהל timers אקטיביים — זו הוראה ליומן שלך.

#### `/trigger`
**Trigger:** `/trigger when <condition> do <action>`
**Behavior:** מציע מבנה event-driven — webhook/cron/event listener בהתאם.

#### `/tasklist` `/checklist`
- `/tasklist` — רשימת משימות מבצעית (סדר, dependency)
- `/checklist` — צ'קליסט עם תיבות סימון (סדר לא קריטי, לרוב)

---

### קטגוריה 9: Personalize & Control

הקטגוריה היחידה שמשנה את ההתנהגות של Claude **לכל ההמשך**.

#### `/preferences`
**Trigger:** `/preferences view` או `/preferences set <key> <value>`
**Behavior:** view/set על העדפות. שינוי דורש אישור: "להוסיף ל-userPreferences? (yes/no)".

#### `/memory`
**Trigger:** `/memory view | add | remove | replace`
**Behavior:** ממומש דרך כלי `memory_user_edits` — Claude לעולם **לא** מבטיח לזכור בלי להפעיל את הכלי.

#### `/tone`
**Trigger:** `/tone <type>`
**Options:** `formal | casual | expert | coach | direct | warm`
**Persistence:** עד `/tone reset`.

#### `/style`
**Trigger:** `/style <description>`
**Behavior:** שינוי סגנון כתיבה — "כמו Hemingway", "כמו דוח Goldman Sachs", "כמו פוסט לינקדאין".

#### `/length`
**Trigger:** `/length short | medium | long | <N words>`
**Behavior:** ברירת מחדל לתשובות עד `/length reset`.

#### `/format`
**Trigger:** `/format bullets | prose | table | code | markdown`
**Behavior:** ברירת מחדל לתשובות עד `/format reset`.

#### `/reset`
**Trigger:** `/reset`
**Behavior:** מאפס הוראות זמניות (`/tone`, `/length`, `/format`) **אבל שומר** `/focus` ו-`/project`.

#### `/clear`
**Trigger:** `/clear`
**Behavior:** מנקה הכל — `/focus`, `/project`, `/tone`, `/length`, `/format`. **לא** מוחק זיכרון ארוך-טווח.

---

### קטגוריה 10: Learn & Research

#### `/search`
**Trigger:** `/search <query>`
**Behavior:** Claude משתמש בכלי web search אם זמין. **אם לא** — מבקש מהמשתמש להפעיל ב-settings.

#### `/research`
**Trigger:** `/research <topic>`
**Behavior:** מחקר עמוק — מקורות מרובים (≥ 3), סינתזה, נקודות הסכמה וחילוקי דעות. אם Claude OS מוגדר עם Research Mode — נטען אוטומטית.

#### `/learn`
**Trigger:** `/learn <topic>` או `/learn <topic> --level beginner`
**Behavior:** Pedagogical mode — מבני, הדרגתי, דוגמאות, שאלות לבדיקת הבנה בסוף.

#### `/tldr`
**Trigger:** `/tldr` + טקסט/נושא
**Behavior:** **קשיח: ≤ 3 שורות.** בלי לפרק כללים — Claude יקצר עוד אם חרג.

#### `/sources`
**Trigger:** `/sources <claim>` או `/sources` אחרי תשובה
**Behavior:** מקורות עם URLs ותאריך גישה. אם אין — Claude אומר "אין לי מקור מאומת — זה ידע פנימי" ולא ממציא.

#### `/fact-check`
**Trigger:** `/fact-check <claim>`
**Behavior:** מצב התראה — Claude מסביר את ה-confidence שלו ומציע מקורות לאימות חיצוני.

#### `/explore`
**Trigger:** `/explore <broad topic>`
**Behavior:** מיפוי נושא — תת-נושאים, שאלות מעניינות, נקודות כניסה. **לא** דוח — מטרה: לזהות איפה לחפור.

---

### קטגוריה 11: Collaborate & Share

#### `/share`
**Trigger:** `/share <content>` או `/share` אחרי תשובה
**Behavior:** מנקה את התוכן מ-context שלא רלוונטי לקורא חיצוני. מסיר התייחסויות פנימיות.

#### `/export`
**Trigger:** `/export <format>` — markdown / pdf / html / docx
**Behavior:** מייצר קובץ במקום פלט inline. עם file output tool אם זמין.

#### `/download`
**Trigger:** `/download`
**Behavior:** alias ל-`/export` עם הדגשה שהמטרה היא קובץ.

#### `/copy`
**Trigger:** `/copy <content>`
**Behavior:** פלט נקי שמתאים להעתקה — בלי emojis, בלי backticks חיצוניים, plain text מסודר.

#### `/email`
**Trigger:** `/email to <recipient> about <subject>`
**Behavior:** מבנה מלא: Subject + Greeting + Body + Sign-off. שלוש גרסאות אם המצב אסטרטגי (משתמש ב-message_compose tool אם זמין).

#### `/publish`
**Trigger:** `/publish <topic> for <platform>` — LinkedIn / Twitter / Medium / Blog
**Behavior:** פורמט מותאם לפלטפורמה: כותרת + lead + body + meta tags + CTA.

#### `/feedback`
**Trigger:** `/feedback on <topic>`
**Behavior:** בקשת משוב מובנה — 3–5 שאלות ספציפיות, לא "מה דעתך".

---

## 5. Composition — שילוב פקודות

המקום שבו השיטה הופכת חזקה במיוחד.

### 5.1 שלושה אופרטורים

| אופרטור | משמעות | דוגמה |
|---------|---------|--------|
| **רצף (space)** | פקודה אחר פקודה — שתי פעולות נפרדות | `/analyze /recommend` |
| **Pipeline (`|`)** | פלט של 1 הופך לקלט של 2 | `/research X \| /tldr` |
| **Composition (`+`)** | שתי ההתנהגויות משתלבות בפלט אחד | `/bullet + /short` |

### 5.2 דוגמאות מעשיות (ULTRA — שאתה תשתמש בהן)

```
/focus סבב Seed Leasing.co.il
/research israeli leasing market size | /key-points | /export markdown
/clarify /draft pitch deck slide 1
/compare Anthropic Sonnet vs GPT-5 | /table | /recommend
/analyze לקוח קפסולה תיק | /assumptions | /pros-cons /strategy
/email to משה מסיקה about partnership update | /tone warm
/code Python Excel automation | /test | /documentation
/brainstorm 20 supplier pitches | /evaluate by feasibility | /recommend top 3
/learn vector embeddings --level expert | /examples | /code TypeScript
/visualize seed round burn | /report | /export pdf
```

### 5.3 שמירת combos אישיים

ב-`OPERATING_SYSTEM.md` שלך, מומלץ להגדיר macros:

```yaml
macros:
  /pitch-prep:
    expansion: /research $1 | /key-points | /format slide
  /case-brief:
    expansion: /analyze $1 | /assumptions | /priorities | /recommend
  /investor-update:
    expansion: /summarize $1 | /tone formal | /email
  /sos:
    expansion: /clarify /assumptions /priorities /constraints
```

ואז `/pitch-prep "Israeli leasing market"` מתורגם אוטומטית.

---

## 6. Power Shortcuts

מה-Bonus בתמונה המקורית. אלה **לא** פקודות — אלה **עקרונות שימוש**.

### 6.1 השישה

| # | עיקרון | יישום |
|---|---------|--------|
| 1 | **Use `/` for quick access** | תחביר אחיד — תמיד יודעים מה מצפים מ-Claude |
| 2 | **Combine commands for better results** | רוב הפלטים החזקים הם compositions, לא single commands |
| 3 | **Add context early** | כל פקודה שמגדירה context (`/focus`, `/project`, `/context`) — לפני, לא אחרי |
| 4 | **Be specific and clear** | `/write` חלש. `/write LinkedIn post 200 words about X for B2B audience` חזק |
| 5 | **Iterate and refine** | פלט ראשון = טיוטה. `/edit /improve /shorten` עליו עד שזה נכון |
| 6 | **Save and reuse what works** | macros (סעיף 5.3) + תבניות (`/template`) — לא להמציא מחדש פעמיים |

### 6.2 אנטי-דפוסי שכדאי להימנע

- ❌ פקודות מסוכרות (`/analyze /compare /evaluate /recommend` ברצף בלי context) — Claude מאבד את חוט המחשבה
- ❌ פקודה שמתנגשת עם רכיב OS קיים (`/tone formal` כשיש כבר ב-userPreferences "תמיד formal" — Claude מתבלבל)
- ❌ פקודה אחרי בקשה ארוכה ("…תכין לי X, /shorten") — שים את הפקודה ראשונה
- ❌ macro מרובד מדי — מעבר ל-3 רמות נכשל לרוב

---

## 7. Prompting Frameworks — מסגרות לכתיבת פרומפטים

אם קטגוריות 1–11 מעצבות את ה**פלט** של Claude, המסגרות כאן מעצבות את ה**קלט** שלך. פקודה מצוינת על פרומפט רשלני עדיין נותנת פלט בינוני — `garbage in` לא מתבטל ב-`/format`.

**מקור ושקיפות:** הסעיף זוקק מהאינפוגרפיקה *"How To Write Better AI Prompts"*. שמרנו את המהות השמישה (techniques, strategies, frameworks, key terms), תיקנו ראשי-תיבות משובשים למסגרות המקובלות בפועל, ודילגנו על ה-hype של אקוסיסטם ChatGPT (Custom GPTs, DALL-E, CTA שיווקי) — באותה דיסציפלינת-מקור של ההקדמה.

**הגשר לפקודות:** כל טכניקה ממופה לפקודה שכבר קיימת ב-API. המסגרות הן ה"איך לחשוב"; הפקודות הן ה"איך לבצע".

### 7.1 ארבע טכניקות ליבה (Core Techniques)

| טכניקה | מה זה | מתי | פקודת OS מקבילה |
|---------|--------|------|------------------|
| **Zero-shot / Few-shot** | הוראה ישירה מול הוראה + 2–3 דוגמאות לכיול | few-shot כשהפורמט או הטון קריטיים | `/examples` |
| **Role-Playing** | הקצאת פרסונה ("אתה אנליסט בכיר", "כמו CFO") | כשצריך עומק-תחום או register ספציפי | `/tone` · `/style` |
| **Context Injection** | הזרקת רקע/דאטה לפני הבקשה | תמיד כשיש מידע רלוונטי שלא בהקשר | `/context` · `/focus` · `/project` |
| **Output Formatting** | קביעת צורת הפלט מראש (טבלה, bullets, JSON) | כשהפלט נכנס למסמך או מערכת אחרת | `/format` · `/table` · `/bullet` · `/outline` |

### 7.2 ארבע אסטרטגיות מתקדמות (Advanced Strategies)

| אסטרטגיה | מה זה | מתי | פקודת OS מקבילה |
|----------|--------|------|------------------|
| **Chain-of-Thought (CoT)** | "חשוב צעד-אחר-צעד לפני התשובה" | בעיות רב-שלביות, חישוב, היגיון | `/analyze` · `/solve` |
| **Self-Critique** | בקש מ-Claude לבקר ולשפר את עצמו | טיוטה שנייה כמעט תמיד טובה מהראשונה | `/challenge` · `/review` · `/improve` |
| **ReAct (Reason + Act)** | היגיון משולב בפעולה או כלי | מחקר, code review, workflows עם כלים | `/research` · `/workflow` + pipelines |
| **Meta-Prompting** | בקש מ-Claude לשכתב את הפרומפט עצמו | כשהתוצאה חלשה — תקן את הקלט, לא רק את הפלט | `/improve` · `/rewrite` (על הפרומפט) |

> *Tooling:* את ReAct ואת ה-chaining בקנה מידה מתפעלים אוטומטית כלים ייעודיים — DSPy, LangChain, PromptLayer — אך אותו היגיון מתבטא ידנית ב-composition (סעיף 5).

### 7.3 מסגרות פרומפט — מתי כל אחת

מהפשוט למורכב. בחר את הקטנה ביותר שמכסה את המשימה:

| מסגרת | רכיבים | הכי טובה ל… |
|--------|---------|--------------|
| **RTF** | Role · Task · Format | בקשה מהירה יומיומית — שלושת המינימום |
| **RACE** | Role · Action · Context · Expectation | משימה עם רקע ותוצאה מוגדרת |
| **CO-STAR** | Context · Objective · Style · Tone · Audience · Response | תוכן שיווקי/תקשורת — שליטה מלאה בטון וקהל |
| **RISE** | Role · Input · Steps · Expectation | משימה אנליטית רב-שלבית (ראו 7.4) |
| **CLEAR** | Concise · Logical · Explicit · Adaptive · Reflective | עקרונות *לחידוד* פרומפט קיים, לא לבנייתו מאפס |

> **מיפוי לפקודות:** Role → `/tone`+`/style` · Context → `/context` · Format/Response → `/format` · Steps → `/outline` + composition. מסגרת שלמה = stack של פקודות (ראו 7.6).

### 7.4 RISE — פירוק מסגרת לדוגמה (Leasing.co.il)

המסגרת שהאינפוגרפיקה פירקה, על דאטה אמיתית שלך:

```
Role:        אתה אנליסט נתונים בכיר בתחום הליסינג.
Input:       דוח עסקאות Q3 — נפח, ריבית ממוצעת, סוג רכב, ספק.
Steps:       1) זהה 3 מגמות.  2) השווה ל-Q2.  3) הצע 3 הזדמנויות צמיחה.
Expectation: טבלה + bullet לכל הזדמנות, עד 200 מילה, בעברית.
```

כאותה משימה ב-API:
```
/context דוח עסקאות Q3 [מצורף]
/analyze-data | /insights | /table + /length 200
```

### 7.5 מונחי מפתח (Key Terms)

| מונח | פירוש קצר | רלוונטי ל… |
|------|-----------|-------------|
| **Context Engineering** | בניית זיכרון/הקשר/דאטה כך שה-LLM "מבוסס" ולא מנחש | `MEMORY.md` · `/context` · `/project` |
| **Prompt Chaining** | שרשור פרומפטים — פלט אחד מזין את הבא | אופרטור ה-pipeline (סעיף 5) |
| **Temperature** | 0 = עקבי ולוגי · 1 = יצירתי ופתוח | הגדרת מודל, לא פקודה — שיקול לפי משימה |
| **RAG** | חיבור המודל לדאטה חיצוני לדיוק עובדתי | `/search` · `/research` · `/sources` |
| **Self-Consistency** | מספר תשובות → השוואה → הטובה ביותר | מעלה אמינות; שלב עם `/evaluate` |

### 7.6 מסגרת → Stack פקודות

הדרך להפוך מסגרת תיאורטית להרצה: תרגם כל רכיב לפקודה והרכב ב-`+` או `|`. CO-STAR מלאה למייל למשקיע:

```
/project investor update Q3
/context [מספרי הרבעון]
/email to משקיע מוסדי (non-technical) about Q3 update | /tone formal + /length 180
```

- **C**ontext → `/context` · `/project`
- **O**bjective → גוף הבקשה (`/email … about …`)
- **S**tyle + **T**one → `/style` · `/tone`
- **A**udience → תיאור מפורש בתוך הבקשה (אין פקודה ייעודית)
- **R**esponse → `/format` · `/length`

**הכלל:** אל תשנן ראשי-תיבות — שנן ש**פרומפט חזק = פרסונה + הקשר + משימה + צורת-פלט**, וזה בדיוק מה שה-stack מבטא.

---

## 8. System Prompt — Drop-in

זה הבלוק שדורש העתקה ל-`userPreferences` או ל-`CLAUDE.md` ראשי. **זה מה שגורם לכל המסמך הזה לעבוד.**

```
COMMAND API ENABLED — v1.0

When the user begins a message with /command syntax, parse and execute
according to COMMAND_API.md (loaded in OS context).

Parser rules:
1. /command at line start = command invocation
2. /command in mid-sentence with quotes = literal text, not invocation
3. Arguments follow the command, separated by spaces
4. Quoted args ("with spaces") are treated as single tokens
5. Unknown command → ask 1 clarifying question with closest 2 suggestions
6. Conflicting commands → last one wins, note this to user

Composition operators:
- Space = sequential (run cmd1 then cmd2 on its output)
- "|" = pipeline (cmd2's input is cmd1's output)
- "+" = blend (combine behaviors in single output)

Behavioral overrides:
- Command behavior CONTRACT (output shape) overrides default Claude tone
- /focus and /project persist across turns until /clear
- /tone, /length, /format persist until /reset
- /clarify forces clarifying questions BEFORE work begins
- /recommend forbids "it depends" — Claude must commit or ask for the missing fact

Integration with existing OS:
- Commands DO NOT override safety rules
- Commands DO NOT override IP-protection rules (e.g., Deal Score Engine secrecy)
- Commands respect skill triggers — if /code triggers a Python skill, the skill loads first
- Memory commands (/memory) ALWAYS call memory_user_edits tool — never just acknowledge

When uncertain whether something is a command, default to LITERAL interpretation
and offer: "Is this a /command, or literal text?"
```

---

## 9. אינטגרציה עם ה-Claude OS שלך

### 9.1 מיקום הקובץ
> מבנה מתומצת. מקור-האמת המלא לרישום ולסדר הטעינה הוא `OPERATING_SYSTEM.md` §3.
```
Claude OS Root/
├── CLAUDE.md                  ← נקודת כניסה ראשית
├── OPERATING_SYSTEM.md        ← קרנל (חוקים, §3 רישום + §3.1 תשתית תפעולית)
├── MEMORY.md                  ← זיכרון נמשך
├── DECISION_LOG.md            ← יומן החלטות
├── COWORK_SETUP.md            ← הקשר / אונבורדינג Cowork
├── PROJECTS_SETUP.md          ← הקשר / Claude Projects
├── COMMAND_API.md             ← ← זה. המסמך הזה.
├── marketing-strategy-framework.md   ← Business: אסטרטגיית שיווק
├── AI_SKILL_MAP.md · AI_PROGRESSION_PLAN.md · AI_LEARNING_RESOURCES.md · AI_7_SKILLS.md · AI_SKILLS_ACQUISITION.md · AI_TYPES.md · AI_CLAUDE_TOOL_SELECTOR.md · AI_CLAUDE_STACK_2026.md   ← Knowledge
├── INVESTOR_RELATIONS.md
├── COWORK/                    ← סביבת Cowork בפועל (ABOUT-ME · TEMPLATES · OUTPUTS)
├── .claude/                   ← Claude Code (4 skills + סוכן os-auditor)
└── CASES/
    └── ULEASE*.md             ← תיק ULease 🎯
```

### 9.2 רישום ב-CLAUDE.md

הסדר הקנוני המלא מוגדר ב-`OPERATING_SYSTEM.md` §3 ומשתקף ב-`CLAUDE.md`. תמצית:

```markdown
## Active Modules
- COMMAND_API.md v1.1.0 — 89 slash commands, composition, prompting frameworks, system prompt loaded
- (כל שאר המודולים — ראו §3)

## Module Load Order (canonical, §3)
1. OPERATING_SYSTEM.md
2. MEMORY.md
3. DECISION_LOG.md
4. COWORK_SETUP.md
5. PROJECTS_SETUP.md
6. COMMAND_API.md           ← לפני הקטגוריות העסקיות
7. marketing-strategy-framework.md
8. AI_* (Knowledge, on-demand)
9. INVESTOR_RELATIONS.md
10. CASES/*.md
```

### 9.3 כללי הכרעה במצב התנגשות

| התנגשות | כלל |
|---------|------|
| פקודה ↔ userPreferences | פקודה זמנית מנצחת. preference חוזרת אחרי `/reset`. |
| פקודה ↔ skill trigger | Skill נטען ראשון, ואז הפקודה מיושמת על הפלט. |
| פקודה ↔ child safety | Safety תמיד מנצח. הפקודה מסורבת בנימוס. |
| `/focus` ↔ בקשה זמנית | Focus מנצח אבל Claude מציע "side quest" ב-1–2 משפטים. |
| `/memory` ↔ זיכרון קיים | Claude מבקש אישור לפני שמשנה memory edits קיימים. |

### 9.4 logging אופציונלי

ב-`DECISION_LOG.md`, מומלץ לשמור log של commands משמעותיים:

```markdown
## 2026-05-19
- /focus סבב Seed → 90 יום timeline
- /project Leasing pivot to multi-tier suppliers
- /tone formal לכל הפניות למשקיעים
```

---

## 10. הרחבה ויצירת פקודות אישיות

אתה כבר בנית 18,000+ שורות OS — תרצה להוסיף פקודות משלך.

### 10.1 תבנית להוספת פקודה

```markdown
#### `/yourcommand`
**Trigger:** `/yourcommand <args>`
**Category:** (יוצר חדשה אם צריך)
**Behavior:** [מה Claude עושה במדויק]
**Output Contract:** [צורת הפלט המובטחת]
**Persistence:** session | persistent | one-shot
**Compatible with:** [אילו פקודות אחרות מתשלבות איתה]
**Anti-patterns:** [מה לא לעשות]
**Example:**
```

### 10.2 המלצות לפקודות אישיות עבורך (Avraham OS)

מבוסס על מבנה השימושים שלך, הפקודות הבאות יוסיפו ערך מיידי:

| פקודה | תפקיד | מבוסס על |
|-------|--------|-----------|
| `/case <case_name>` | טוען הקשר מלא של תיק מ-CASES/ | מבנה התיקים שלך |
| `/legal <document_type>` | מפעיל legal-automation skill עם פורמט David RTL | סטנדרט המסמכים המשפטיים |
| `/leasing <topic>` | מקפיץ הקשר Leasing.co.il + skill | הפלטפורמה |
| `/council <decision>` | מפעיל council-of-sages skill | קיים אצלך |
| `/keeper status` | סיכום context-keeper של השיחה | קיים אצלך |
| `/deal-score <vehicle>` | מציג Deal Score (mock או אמיתי) | Deal Score Engine |
| `/investor <name>` | טוען investor profile + history | INVESTOR_RELATIONS.md |
| `/decision` | מתעד החלטה ל-DECISION_LOG.md | קיים אצלך |

הוסף אותם ל-`COMMAND_API.md` שלך תחת קטגוריה 12: "Avraham Personal".

---

## 11. גרסאות וחיפוי לאחור

### 11.1 Versioning

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | Initial 89 commands + composition + system prompt | 2026-05-19 |
| 1.1.0 | Prompting Frameworks (§7) — core techniques, advanced strategies, framework→command mapping, key terms | 2026-05-31 |

### 11.2 Backward Compatibility

- שדרוגי minor (1.x) — לא ישברו פקודות קיימות; רק יוסיפו ויחדדו
- שדרוגי major (2.0) — יחייבו עדכון system prompt; הודעת deprecation 30 יום מראש

### 11.3 Roadmap

| גרסה | תוכן | יעד |
|-------|--------|-----|
| 1.2 | פקודות Avraham Personal (סעיף 10.2) | יוני 2026 |
| 1.3 | Macros library מורחבת + פקודות multi-step | יולי 2026 |
| 1.4 | אינטגרציה רשמית עם council-of-sages ו-context-keeper | אוגוסט 2026 |
| 2.0 | Agentic commands (`/agent <task>` שמפעיל skill chain אוטומטית) | Q4 2026 |

---

## 12. נספח

### 12.1 כללי הכרעה ב-edge cases

**מה אם המשתמש כתב `/focus` כדבר אחרון בהודעה?**
→ Claude מתייחס לזה כאופציה לפתוח שיחה חדשה: "תרצה לקבוע focus? על מה?"

**מה אם פקודה ארוכה מתישה ההקשר?**
→ Claude משלים מה שהוא יכול ומסמן: "השלמתי 3 מ-5 הפקודות; להמשיך?"

**מה אם המשתמש כותב פקודה בעברית: /נתח?**
→ Claude מקבל ומתייחס לזה כ-`/analyze`. רשימת aliases עברית:
- `/נתח` = `/analyze`
- `/סכם` = `/summarize`
- `/השווה` = `/compare`
- `/המלץ` = `/recommend`
- `/חקור` = `/research`

**מה אם פקודה דורשת כלי שאינו זמין (e.g., `/search` בלי web access)?**
→ Claude מסביר במשפט אחד מה חסר ומה לעשות, לא ממציא תוצאות.

### 12.2 Quick Card להדפסה

```
START: /new /project /upload /template /import
FOCUS: /focus /context /clarify /constraints
THINK: /analyze /compare /pros-cons /recommend /challenge
WRITE: /write /edit /shorten /improve /summarize
ORG:   /outline /bullet /numbered /table /key-points
CODE:  /code /debug /optimize /refactor /test /review
DATA:  /analyze-data /visualize /insights /report /stats
AUTO:  /workflow /automate /api /integrate /checklist
PREF:  /tone /style /length /format /reset /clear
LEARN: /search /research /tldr /sources /fact-check
SHARE: /share /export /email /publish /feedback

COMPOSE: cmd1 cmd2 (sequence) | (pipeline) + (blend)
SPECIFIC > GENERAL.  ITERATE.  SAVE WHAT WORKS.
```

### 12.3 קונטרקטים ל-LLM gateway (אופציונלי)

אם תרצה לבנות parser רשמי כתת-מערכת (לא רק תלוי בקריאת Claude), הנה ה-schema:

```typescript
interface ParsedCommand {
  command: string;          // 'analyze' (no slash)
  args: string[];
  flags: Record<string, string | boolean>;
  composition: 'sequence' | 'pipeline' | 'blend' | null;
  next?: ParsedCommand;
}

interface CommandContract {
  name: string;
  category: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11;
  trigger_regex: RegExp;
  args_required: string[];
  args_optional: string[];
  output_shape: 'prose' | 'bullets' | 'numbered' | 'table' | 'code' | 'mixed';
  persistence: 'one_shot' | 'session' | 'persistent';
  composable_with: string[];
  conflicts_with: string[];
  pre_hooks: string[];      // skill loads required
  post_hooks: string[];     // logging, memory updates
}
```

---

## Document Control

| Section | Owner | Last reviewed |
|---------|--------|---------------|
| Architecture & Grammar | OS Architect (you) | 2026-05-19 |
| Command Catalog | this file | 2026-05-19 |
| System Prompt | this file + userPreferences | 2026-05-19 |
| Integration | CLAUDE.md (root) | 2026-05-19 |
| Prompting Frameworks | this file | 2026-05-31 |

**Confidentiality.** This file is part of the personal Claude Operating System of Avraham Bar Yochai Chazan. Commands referencing internal IP (Deal Score, Match API, legal automation) inherit the confidentiality of those sub-systems.

— *End of COMMAND_API.md v1.1 —*
