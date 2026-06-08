# מילון Claude — 30 מונחים שחייבים להכיר

**Module:** `AI_CLAUDE_GLOSSARY.md`
**Version:** 1.1.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — Knowledge layer (§3 שורה 17). המודול השלישי במשפחת ה-Claude (Selector · Stack · Glossary).
**Source:** מבוסס על האינפוגרפיקה *"30 Must Know Terms in Claude"* + עדכון *"Claude Glossary"* (3 מונחי 2026, קבוצה ו').
**Integrates with:** `AI_CLAUDE_TOOL_SELECTOR.md`, `AI_CLAUDE_STACK_2026.md`, `COMMAND_API.md`, `COWORK_SETUP.md`, `MEMORY.md`, `PROJECTS_SETUP.md`

> משפחת ה-Claude ב-OS: ה-**Selector** עונה "באיזה כלי להשתמש", ה-**Stack** עונה "איך בונים עם זה", וה-**Glossary** הזה עונה "מה כל מילה אומרת". 30 המונחים — והעמודה החשובה ביותר: **איפה כל מונח כבר חי בריפו הזה**.

---

## 1. המילון — 30 מונחים בחמש קבוצות

### 🧰 א. מוצרים וכלים

| # | מונח | הגדרה | ✅ איפה אצלך |
|---|------|--------|---------------|
| 1 | **Models** | Opus לחשיבה עמוקה · Sonnet לעבודה יומית · Haiku לתשובות מהירות | `AI_CLAUDE_TOOL_SELECTOR.md` §מודלים + מנוע ה-Outbound (Haiku/Sonnet) |
| 2 | **Chat** | ממשק הצ'אט הבסיסי ב-claude.ai | השיחות היומיות שלך |
| 3 | **Projects** | workspace מאורגן לעבודה והקשר | `PROJECTS_SETUP.md` — 3 פרויקטים חיים |
| 4 | **Claude Code** | למפתחים שבונים עם Claude | הריפו הזה — נבנה כולו ב-Claude Code |
| 5 | **Claude Design** | בניית אתרים וויזואלים בלי קוד | מועמד לעיצוב דפי ULease |
| 6 | **Claude in Excel** | עבודה עם Claude בתוך גיליונות | ניתוח תחזיות (`ULEASE_FORECAST.csv`) |
| 7 | **Claude in Chrome** | סוכן גלישה שמבין את הדף | מחקר שוק/מתחרים |
| 16 | **Dispatch** | אפליקציית הטלפון ששולחת משימות ל-Claude בדסקטופ | מועמד לשגרת העבודה הניידת |
| 15 | **Computer Use** | Claude מקליק ומקליד על המחשב שלך | אוטומציות עתידיות |

### 📄 ב. קבצים ופורמטים

| # | מונח | הגדרה | ✅ איפה אצלך |
|---|------|--------|---------------|
| 8 | **Artifacts** | מסמכים, קוד ואפליקציות בחלונית צד | הדשבורד והמצגת נולדו כך |
| 9 | **Markdown** | הפורמט המועדף על Claude | כל ה-OS כתוב בו |
| 10 | **CLAUDE.md** | קובץ הזיכרון ש-Claude Code קורא באתחול | `CLAUDE.md` — נקודת הכניסה של ה-OS |
| 12 | **SKILL.md** | הטריגר וההוראות בתוך Skill | `.claude/skills/*/SKILL.md` — 4 קבצים |
| 29 | **Outputs** | כל מה ש-Claude יוצר — טקסט, טבלאות, קוד, אפליקציות | `COWORK/OUTPUTS/` |

### 🔌 ג. הרחבה וחיבורים

| # | מונח | הגדרה | ✅ איפה אצלך |
|---|------|--------|---------------|
| 11 | **Skills** | פרומפטים ו-workflows שמורים שמפעילים עם `/` | `.claude/skills/` — os-module · os-decision · ulease-refresh · investor-update |
| 13 | **Plugins** | חבילות של Skills + Connectors לעבודה ספציפית | שלב הבא אחרי ה-skills |
| 14 | **Connectors** | חיבורים בין Claude לאפליקציות שלך | יומן Google (תזכורות D-020), n8n |

### ⚡ ד. יכולות

| # | מונח | הגדרה | ✅ איפה אצלך |
|---|------|--------|---------------|
| 17 | **Adaptive Thinking** | Claude חושב עמוק יותר לפני שהוא עונה | מופעל בניתוחים מורכבים (ביקורת, תחזית) |
| 18 | **Research** | מחקר רשת עמוק שהופך לדוחות מלאים | מחקר שוק הרכב, רגולציה |
| 19 | **Web Search** | תוצאות חיות מהאינטרנט | אימות מחירונים ומתחרים |
| 20 | **AskUserQuestion** | Claude שואל אותך שאלות עם טפסים לחיצים | שאלות ההבהרה ב-skills |
| 21 | **Scheduled Tasks** | הרצת Claude בלוח זמנים קבוע | מועמד: עדכון משקיעים חודשי אוטומטי |
| 28 | **Vibecoding** | בנייה של כל דבר ע"י תיאור מה שרוצים | כך נבנו הדשבורד וה-deck |

### 🧠 ה. הקשר וזיכרון

| # | מונח | הגדרה | ✅ איפה אצלך |
|---|------|--------|---------------|
| 22 | **Global Instructions** | Claude קורא את זה לפני כל משימה מתוזמנת | Boot Block (`OPERATING_SYSTEM.md` §4) |
| 23 | **Custom Instructions** | חוקים והעדפות ברמת פרויקט | הוראות ה-drop-in ב-`PROJECTS_SETUP.md` |
| 24 | **Memory** | Claude זוכר פרטים שימושיים בין צ'אטים ופרויקטים | `MEMORY.md` + כרטיס הזהות |
| 25 | **Projects (workspace)** | workspace אחד לכל משימה כדי לשמור על פוקוס | "תוצר אחד לכל פרויקט" (`PROJECTS_SETUP.md`) |
| 26 | **Prompt** | הטקסט והקבצים שאתה שולח ל-Claude | `COMMAND_API.md` §7 — מסגרות פרומפט |
| 27 | **Styles** | פריסטים שמורים של טון ופורמט | `COWORK/ABOUT-ME/anti-ai-style.md` |
| 30 | **Power User Mindset** | שילוב הכלים הנכונים להכפלת התפוקה פי 10 | **ה-OS הזה כולו** |

### 🆕 ו. עדכוני 2026 (מעבר ל-30 הבסיסיים)

מהאינפוגרפיה *Claude Glossary* — שלושה מונחים שנכנסו אחרי המקור המקורי:

| # | מונח | הגדרה | ✅ איפה אצלך |
|---|------|--------|---------------|
| 31 | **Compaction** | Claude מסכם אוטומטית הודעות ישנות כדי לשמור צ'אטים ארוכים רצים | ניהול הקשר ב-sessions ארוכים (כמו אלו שבונים את ה-OS) |
| 32 | **Claude in PowerPoint** | Claude בונה ועורך שקפים ישירות ב-PowerPoint | מועמד ל-pitch deck — משלים את `CASES/ULEASE_DECK` (Marp) |
| 33 | **Claude Marketplace** | hub לגילוי והתקנת Connectors · Plugins · Skills | מקור ההתקנה של חבילות ה-Skills (`CASES/ULEASE_AUTOMATION_MAP.md` §11–§11.2) |

---

## 2. המבחן: כמה מה-30 כבר מיושמים אצלך?

| סטטוס | מונחים | ספירה |
|--------|---------|:------:|
| ✅ **חי בריפו** | Models · Chat · Projects · Claude Code · Artifacts · Markdown · CLAUDE.md · Skills · SKILL.md · Outputs · Connectors · Adaptive Thinking · AskUserQuestion · Vibecoding · Global Instructions · Custom Instructions · Memory · Projects-workspace · Prompt · Styles · Power User Mindset | **21/30** |
| 🔜 **מועמד הבא** | Scheduled Tasks (עדכון משקיעים אוטומטי) · Claude in Excel (תחזיות) · Dispatch · Plugins | 4 |
| ⏳ **בהמשך** | Claude Design · Claude in Chrome · Computer Use · Research · Web Search | 5 |
| 🆕 **תוספת 2026** | Compaction · Claude in PowerPoint · Claude Marketplace (קבוצה ו') | +3 |

> **70% מהמילון כבר בשימוש.** זו ההוכחה שה-OS הוא לא תיעוד — הוא יישום.

---

## 3. שלוש האחיות — מתי פותחים איזה מודול

| שאלה | מודול |
|-------|--------|
| "באיזה כלי Claude להשתמש למשימה X?" | `AI_CLAUDE_TOOL_SELECTOR.md` |
| "איך בונים את זה בפועל (Cowork/Projects/Skills/Code)?" | `AI_CLAUDE_STACK_2026.md` |
| "מה המונח הזה אומר ואיפה הוא אצלי?" | **המודול הזה** |

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | מילון 30 מונחי Claude בחמש קבוצות + מיפוי "איפה אצלך" (21/30 מיושמים) + שלוש האחיות | 2026-06-02 |
| 1.1.0 | קבוצה ו' חדשה (D-067): +3 מונחי 2026 מאינפוגרפיית *Claude Glossary* — Compaction · Claude in PowerPoint · Claude Marketplace (33 מונחים) | 2026-06-08 |

**Attribution.** המילון מבוסס על *30 Must Know Terms in Claude*. העיבוד והמיפוי ל-OS — חלק מה-Claude OS של Avraham Bar Yochai Chazan.

**Confidentiality.** קובץ זה הוא חלק מה-Claude Operating System האישי של Avraham Bar Yochai Chazan.

— *End of AI_CLAUDE_GLOSSARY.md v1.1.0 —*
