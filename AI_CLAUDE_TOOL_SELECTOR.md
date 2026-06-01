# איזה Claude לבחור? — Which Claude Should You Use?

**Module:** `AI_CLAUDE_TOOL_SELECTOR.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — מודול ידע/רפרנס (Knowledge layer).
**Source:** מבוסס על האינפוגרפיקה *"Which Claude Should You Use?"*.
**Integrates with:** `COWORK_SETUP.md`, `COMMAND_API.md`, `AI_SKILL_MAP.md`, `CASES/ULEASE_SPEC.md`, `CASES/ULEASE_OUTBOUND_ENGINE.md`

> דרך פשוטה לבחור את הכלי הנכון לכל משימה — עץ החלטה אחד, 12 כלים, והמיפוי שלהם לעבודה היומיומית שלך ב-OS וב-ULease 🎯.

---

## 1. עץ ההחלטה — 8 שאלות לפי הסדר

עבור על השאלות מלמעלה למטה. "כן" → קיבלת את הכלי. "לא" → המשך לשאלה הבאה. כלום לא התאים → **Claude Chat**.

| # | קטגוריה | השאלה | אם כן → | מודל מומלץ |
|---|----------|--------|----------|-------------|
| 1 | **TASK TYPE** | עובד בתוך אפליקציה ספציפית עכשיו? | בדפדפן → **Claude in Chrome** · בקבצים מקומיים → **Claude Cowork** | Sonnet · Opus למסמכים ארוכים |
| 2 | **CODING** | צריך ש-Claude יכתוב או יריץ קוד? | סוכן אחד → **Claude Code** · כמה סוכנים במקביל → **Agent Teams** | Sonnet ליום-יום · Opus לארכיטקטורה / סוכן מוביל |
| 3 | **AUTOMATION** | חוזר על אותה משימה ורוצה טריגר במילה אחת? | **Claude Skills** (קובץ SKILL.md) | לפי צורכי המשימה |
| 4 | **SCHEDULING** | משימה שצריכה לרוץ אוטומטית בטיימר? | המחשב יכול להיות כבוי → **Routines** (ענן) · המחשב דולק → **Cowork Tasks** | Sonnet |
| 5 | **LIVE DATA** | צריך דאטה חי מהכלים האחרים שלך? | **Connectors MCP** (Gmail · Drive · Notion · Slack · GitHub…) | Sonnet |
| 6 | **DESIGN** | יוצר משהו ויזואלי מאפס? | **Claude Design** (UI · מצגות · עמודי web) | Sonnet |
| 7 | **PROJECTS** | חלק מפרויקט שנמשך על פני כמה sessions? | **Projects** (workspace קבוע עם זיכרון) | Sonnet |
| 8 | **DEEP THINKING** | הבעיה דורשת חשיבה איטית, זהירה, צעד-אחר-צעד? | **Adaptive Thinking** (Extended reasoning) | **Opus** |
| — | **ברירת מחדל** | שום דבר מהנ"ל | **Claude Chat** — נקודת ההתחלה לכל דבר מהיר | Sonnet · Haiku לתשובות מהירות |

---

## 2. כרטיסי הכלים — 12 הכלים בקצרה

### עבודה בתוך אפליקציה
| כלי | מה הוא עושה | מודל |
|-----|--------------|------|
| **Claude in Chrome** | יושב בסרגל הצד של הדפדפן. קורא כל עמוד ומשחזר משימות שהקלטת. | Sonnet |
| **Claude Cowork** | פותח, עורך ומסמן קבצים מקומיים ו-PDF — בלי copy-paste. | Sonnet · Opus למסמכים ארוכים |

### קוד
| כלי | מה הוא עושה | מודל |
|-----|--------------|------|
| **Claude Code** | חי בטרמינל. קורא את ה-codebase, כותב קבצים, מריץ טסטים ומתקן באגים. | Sonnet ליום-יום · Opus להחלטות ארכיטקטורה |
| **Agent Teams** | משרשר כמה Claude workers יחד: אחד חוקר, אחד כותב, אחד מבקר. | Sonnet ל-workers · Opus לסוכן המוביל |

### אוטומציה ותזמון
| כלי | מה הוא עושה | מודל |
|-----|--------------|------|
| **Claude Skills** | כותבים workflow פעם אחת כקובץ SKILL.md, מפעילים במילת מפתח מכל session. | לפי המשימה |
| **Routines** | מתזמן מבוסס-ענן. מריץ workflow בטיימר — בלי צורך במחשב דולק. | Sonnet |
| **Cowork Tasks** | משימות מקומיות אוטומטיות. רץ על המחשב שלך כל עוד הוא דולק. | Sonnet · Opus למסמכים מורכבים |

### דאטה, עיצוב ופרויקטים
| כלי | מה הוא עושה | מודל |
|-----|--------------|------|
| **Connectors MCP** | מחבר את Claude ל-Notion, Gmail, Slack, Google Drive, GitHub ועוד — קריאה ופעולה על דאטה חי. | Sonnet |
| **Claude Design** | בונה UI prototypes, מצגות ו-layouts מ-brief טקסטואלי פשוט. | Sonnet |
| **Projects** | workspace לכל פרויקט: קבצים, הוראות והיסטוריית שיחות נשמרים בין ביקורים. | Sonnet |

### חשיבה ושיחה
| כלי | מה הוא עושה | מודל |
|-----|--------------|------|
| **Adaptive Thinking** | מצב reasoning מורחב: Claude עובד על בעיות קשות ומראה כל שלב בחשיבה. | **Opus** |
| **Claude Chat** | שאלות מהירות, משימות חד-פעמיות, מחקר קז'ואלי. בלי setup. **נקודת ההתחלה הכי טובה לכל דבר מהיר.** | Sonnet · Haiku לפשוט ומהיר |

---

## 3. המיפוי שלך — איזה Claude לכל משימה ב-OS וב-ULease 🎯

| המשימה שלך | הכלי הנכון | איפה זה כבר חי אצלך |
|-------------|-------------|----------------------|
| עבודה על מודולי ה-OS, תיקים ו-playbooks | **Claude Cowork** + **Projects** | `COWORK_SETUP.md` — בדיוק בשביל זה |
| פיתוח הריפו: deck, דשבורד, תחזית (קוד) | **Claude Code** | `CASES/ULEASE_DECK.py` · `ULEASE_DASHBOARD.py` · `ULEASE_FORECAST.py` |
| מנוע **Ultra·Master·Max** | **Agent Teams** | אורקסטרציית Multi-agent — `CASES/ULEASE_SPEC.md` §7 |
| מנוע ה-Outbound (n8n + Claude) | **Routines** + **Connectors MCP** | רץ בענן בלי מחשב, מחובר למייל/CRM — `CASES/ULEASE_OUTBOUND_ENGINE.md` |
| 89 הפקודות (`/command`) | **Claude Skills** | `COMMAND_API.md` הוא ספריית ה-skills שלך |
| מצגת משקיעים, עמודי נחיתה, UI | **Claude Design** | `CASES/ULEASE_DECK.md` |
| מייל, יומן, דרייב (IR · גיוס · follow-up) | **Connectors MCP** | Gmail · Calendar · Drive מחוברים ל-OS |
| החלטות אסטרטגיות: תמחור, מו"מ, גיוס | **Adaptive Thinking (Opus)** | תורת המשחקים ו-Big Five — `CASES/ULEASE_METHODOLOGY.md` |
| שאלה מהירה, ניסוח הודעה, סיכום | **Claude Chat** | בלי overhead — פשוט לשאול |

---

## 4. כלל האצבע

1. **מהיר וחד-פעמי** → Chat.
2. **חוזר על עצמו** → Skill. **בטיימר** → Routine.
3. **קוד** → Code. **כמה ידיים במקביל** → Agent Teams.
4. **הקבצים שלך** → Cowork. **פרויקט מתמשך** → Projects.
5. **קשה באמת / אסטרטגי** → Opus + Adaptive Thinking.

> **בחירת מודל:** Sonnet כברירת מחדל · Haiku למהיר/פשוט/המוני · **Opus לקשה, לארוך ולאסטרטגי** — אותו עיקרון בדיוק שמיושם ב-`CASES/ULEASE_OUTBOUND_ENGINE.md` (Haiku לסינון וניקוד, Sonnet לפרסונליזציה).

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | עץ החלטה לבחירת כלי Claude — 12 כלים + מיפוי למשימות ה-OS ו-ULease | 2026-06-01 |

**Attribution.** מבוסס על האינפוגרפיקה *Which Claude Should You Use?*. העיבוד, התרגום והמיפוי ל-ULease הם חלק מה-Claude OS של Avraham Bar Yochai Chazan.

— *End of AI_CLAUDE_TOOL_SELECTOR.md v1.0.0 —*
