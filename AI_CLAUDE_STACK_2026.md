# Claude Stack 2026 — How to use Claude in 2026

**Module:** `AI_CLAUDE_STACK_2026.md`
**Version:** 1.3.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — Knowledge layer (§3 שורה 16) + מפרט ה-build התפעולי של 4 העמודים.
**Source:** מבוסס על ה-cheat sheet *"How to use Claude in 2026"* + סדרת *"The 7 Levels of Claude Code"* (learn.nextwork.org) + *"Understanding Agent Skills"* (Skills·MCP·Subagents·Hooks·Plugins).
**Integrates with:** `AI_CLAUDE_TOOL_SELECTOR.md`, `AI_CLAUDE_GLOSSARY.md` (מודול אחות — המילון), `COWORK_SETUP.md`, `PROJECTS_SETUP.md`, `COMMAND_API.md`, `OPERATING_SYSTEM.md` §3.1, `COWORK/README.md`, `.claude/skills/`, `CASES/ULEASE.md`

---

> ה-cheat sheet מגדיר 4 עמודים — **Cowork · Projects · Skills · Code** — וכלל זהב אחד לבחירה ביניהם.
> המודול הזה עושה שני דברים: **(1)** מזקק את ארבעת העמודים, **(2)** מתעד **מה נבנה בפועל בריפו** כדי שכל עמוד יעבוד מקצה לקצה.
> זה ההבדל בין "לדעת על הכלים" לבין "להיות בנוי בהם".

---

## תוכן עניינים

1. [כלל הזהב — איזה כלי למה](#1-כלל-הזהב--איזה-כלי-למה)
2. [עמוד 1: Claude Cowork](#2-עמוד-1--claude-cowork)
3. [עמוד 2: Claude Projects](#3-עמוד-2--claude-projects)
4. [עמוד 3: Claude Skills](#4-עמוד-3--claude-skills)
5. [עמוד 4: Claude Code](#5-עמוד-4--claude-code)
6. [ה-build בריפו — מה קיים איפה](#6-ה-build-בריפו--מה-קיים-איפה)
7. [הזרימה המשולבת — דוגמה מקצה לקצה](#7-הזרימה-המשולבת--דוגמה-מקצה-לקצה)
8. [כללי תחזוקה](#8-כללי-תחזוקה)

---

## 1. כלל הזהב — איזה כלי למה

| אם… | אז זה… | אצלך זה חי ב… |
|------|---------|----------------|
| אתה עושה את אותה עבודה כל שבוע | **Project** | `PROJECTS_SETUP.md` — 3 פרויקטים מוגדרים |
| נתת את אותן הוראות יותר מ-3 פעמים | **Skill** | `.claude/skills/` — 4 skills |
| Claude צריך לגעת בקבצים האמיתיים שלך | **Cowork** | `COWORK/` + המדריך `COWORK_SETUP.md` |
| אתה מפתח משהו | **Code** | הריפו הזה + `CLAUDE.md` + `os-auditor` |

> משלים את עץ ההחלטה המלא (15 כלים) ב-`AI_CLAUDE_TOOL_SELECTOR.md`. הכלל כאן עונה על 80% מהמקרים בשאלה אחת.

---

## 2. עמוד 1 — Claude Cowork

**מה זה:** Cowork חי באפליקציית ה-Desktop. הוא קורא את הקבצים שלך, פועל עליהם ושומר תוצרים — בלי copy-paste. *"It acts on your files. It is not just a chatbot."*

**Setup נכון (פעם אחת):**
1. תיקיית-אם אחת ובתוכה שלוש תיקיות: **ABOUT-ME · OUTPUTS · TEMPLATES**.
2. ב-ABOUT-ME שלושה קבצים קטנים:
   - `about-me.md` — מי אתה, איך אתה עובד, הסטנדרטים שלך
   - `my-company.md` — היעדים, הקהל, ולמה אתה אומר לא
   - `anti-ai-style.md` — כל מילה וביטוי ש-Claude לעולם לא ישתמש בהם
3. שלושת הקבצים יחד — **מתחת ל-6,000 tokens**.
4. Settings → Cowork → **Global Instructions**: "קרא כל קובץ ב-ABOUT-ME לפני כל משימה". מגדירים פעם אחת — רץ בכל session.

**הפרומפט האחד לכל דבר:**
```
קרא את התיקייה שלי. שאל אותי שאלות לפני שאתה מתחיל.
אם משהו לא ברור — אל תנחש.
```

**כללי שימוש:** שיחה חדשה כל ~20 הודעות (הודעות ישנות עולות tokens בכל turn) · Sonnet לעבודה קצרה · Opus למשימות קשות · קבצי ABOUT-ME קטנים — קבצים גדולים שורפים את התקציב לפני שהעבודה מתחילה.

**✅ הסטטוס אצלך:** בנוי. `COWORK/` בריפו — 3 קבצי ABOUT-ME מאוכלסים מ-`MEMORY.md` ומתיק ULease, 4 תבניות, תיקיית OUTPUTS, ו-Global Instructions מוכנות להעתקה ב-`COWORK/README.md`.

---

## 3. עמוד 2 — Claude Projects

**מה זה:** Projects נותנים ל-Claude workspace קבוע ב-claude.ai. כל שיחה בתוך Project מתחילה כשהקבצים, ההוראות והדוגמאות כבר טעונים. *"Every chat starts loaded. No briefing from zero."*

**הכללים:**
| כלל | פירוט |
|------|--------|
| פרויקט = תוצר אחד | לא נושא כללי. טון/פורמט שונה = פרויקט נפרד |
| מעלים 3 דברים בלבד | דוגמת הפלט הטובה ביותר · מסמכי הרקע · תבנית/בריף קיימים |
| 5 קבצים חדים > 50 אקראיים | לא שופכים את כל ה-Drive |
| Instructions מלאות | מה מיוצר · למי · איך נקרא · מה אסור |
| בדיקה לפני שימוש | שיחה חדשה → תרחיש מומצא → קוראים → מתקנים |

**✅ הסטטוס אצלך:** בנוי. `PROJECTS_SETUP.md` מגדיר 3 פרויקטים — "ULease 🎯 השקה", "גיוס ₪150K", "Claude OS" — כל אחד עם בלוק Instructions להעתקה, רשימת 3 קבצים ובדיקת קבלה.

---

## 4. עמוד 3 — Claude Skills

**מה זה:** workflow שכותבים פעם אחת כקובץ SKILL.md, ו-Claude טוען אותו אוטומטית כשהוא רלוונטי — במילת טריגר או לפי הקשר.

**3 החלקים של כל Skill (ולא יותר):**
| חלק | מה הוא מגדיר |
|------|---------------|
| **Role** | התפקיד של Claude למשימה הזו |
| **Rules** | מה לעשות, ממה להימנע, איך לפרמט |
| **Trigger** | המילה/ביטוי שגורמים ל-Skill להיטען |

**בניית Skill ראשון ב-30 דקות:**
1. בחר את המשימה שאתה מסביר מחדש הכי הרבה.
2. פתח Cowork והקלד: "בנה לי skill למשימה הזו".
3. ענה על השאלות שלו. ספציפי — תשובות עמומות = skill עמום.
4. העלה את קובץ ה-Skill. בדוק עם 5 ניסוחים שונים של אותה בקשה.
5. Claude פספס משהו? תקן את הקובץ. ככל שהקובץ טוב יותר — אתה מקליד פחות, לתמיד.

**הכלל שמציל הכל:** משימה אחת ל-Skill. Skill שמנסה לעשות הכל לא עושה כלום טוב. **צר מנצח רחב, בכל פעם.**

**Skill מול Project:** Skill = מתכון ל"איך" של משימה חוזרת · Project = workspace ל"מה" שצריך זיכרון. משתמשים בשניהם יחד.

**✅ הסטטוס אצלך:** בנוי. 4 skills ב-`.claude/skills/` — נבחרו לפי הכלל "הוסבר יותר מ-3 פעמים":
| Skill | המשימה החוזרת | Trigger |
|-------|----------------|---------|
| `os-module` | רישום מודול חדש ב-5 מקומות בלי לשבור עקביות | "מודול חדש" / "הוסף ל-OS" |
| `os-decision` | רישום החלטת מייסד ביומן append-only | "תרשום החלטה" / "החלטתי" |
| `ulease-refresh` | רענון תחזית → דשבורד → deck אחרי שינוי מודל | "רענן" / "שיניתי תמחור" |
| `investor-update` | עדכון משקיעים מהמספרים העדכניים | "עדכון משקיעים" / "סטטוס גיוס" |

> 89 הפקודות ב-`COMMAND_API.md` הן שכבת ה-interface ה"רכה" (תחביר `/command` בצ'אט); ה-skills כאן הם השכבה ה"קשיחה" שרצה בפועל ב-Claude Code.

---

## 5. עמוד 4 — Claude Code

**מה זה:** Claude בטרמינל — *for developers and builders*. קורא את כל ה-codebase, עורך קבצים, מריץ בדיקות ופקודות, ומשלח עבודה. המחשב שלך עושה את העבודה.

**Setup נכון (פעם אחת):** `/init` בתיקיית הפרויקט → Claude כותב `CLAUDE.md` — הזיכרון שלו לפרויקט. החוקים, הכלים והפקודות נכנסים לשם. נקרא בתחילת כל session. **מתחת ל-200 שורות.**

**הדרך הנכונה לתת פרומפט ל-Code:**
- **תאר את הבעיה, לא את הפתרון.** התיקון שאתה מדמיין לא רלוונטי.
- הלולאה: **Find → Fix → Test → Refactor.**
- פרק בקשות גדולות לצעדים קטנים שניתן לאמת — כל תוצאה בונה ביטחון ומשלחת מהר יותר.

**חיסכון tokens:**
| פקודה | מתי | מה היא עושה |
|--------|------|--------------|
| `/compact` | באמצע חלון ההקשר | Claude מסכם ומתאפס — וממשיך |
| `/clear` | בין משימות | מצב נקי, חוסך ~40% tokens |
| sub-agent | משימות כבדות | סוכן טרי עושה את העבודה ומחזיר סיכום נקי — ההקשר נשאר רזה |

**סולם 7 הרמות של Claude Code** — *"רוב האנשים עוצרים ברמה 3. הטובים מגיעים עד 7"*:

| רמה | יכולת | ✅ איפה אצלך |
|:----:|--------|---------------|
| 1 | **Prompt** — פרומפטים אפקטיביים | `COMMAND_API.md` §7 — מסגרות פרומפט |
| 2 | **Context** — קבצי הקשר קבועים | `CLAUDE.md` — נקודת הכניסה של כל ה-OS |
| 3 | **Tools** — הכלים המובנים (קבצים, טרמינל, חיפוש) | כל הריפו נבנה איתם |
| 4 | **MCP** — חיבור לשרתים חיצוניים | 🟡 GitHub MCP פעיל ב-sessions; שרתים ייעודיים (יומן, n8n) — בהמשך |
| 5 | **Skills** — workflows קבועים ב-SKILL.md | `.claude/skills/` — 4 skills |
| 6 | **Subagents** — האצלה לסוכני-משנה | `os-auditor` — רץ על כל שינוי OS |
| 7 | **Agent Teams** — צי sessions במקביל (ניסיוני) | 🔜 נפתח עם ה-Tech Lead — ראו בלוק למטה |

> **הציון שלך: רמה 6 מתוך 7.** רוב המשתמשים עוצרים ב-3 — ה-OS הזה כבר שתי רמות מעבר, ורמה 7 היא מסלול ה-prototype של ULease.

**רמה 7 בפירוט — Agent Teams (ניסיוני, opt-in):** צי של Claude sessions שמתקשרים זה עם זה ורצים על העבודה במקביל:

| רכיב | תפקיד |
|------|--------|
| **Team lead** | session מוביל — מפרק את העבודה, מחלק ומסנכרן |
| **Teammates** | sessions עמיתים — כל אחד תופס (claim) משימה מהרשימה |
| **Shared tasks** | רשימת משימות משותפת ומסונכרנת בין כולם |

שתי משמעויות:
1. **ל-OS** — זו ההסמכה של מה שכבר קורה כאן: ביקורת 4 הסוכנים (D-019) וה-`os-auditor` כ-sub-agent. ההבדל: ב-Agent Teams הסוכנים מתקשרים זה עם זה, לא רק מחזירים דוח.
2. **ל-ULease 🎯** — מסלול ה-prototype של **Ultra·Master·Max** (`ULEASE_SPEC.md` §7): Team lead = Ultra (מתזמר) · Teammates = Masters (מומחים) · Shared tasks = מודל Event/AgentRun (§8). ה-Tech Lead יכול להוכיח את הארכיטקטורה עם Agent Teams **לפני** שבונים תשתית ייעודית.

> ⚠️ ניסיוני ודורש הפעלה מפורשת — כלי prototype ולמידה, לא תשתית production.

**✅ הסטטוס אצלך:** בנוי. הריפו הזה הוא ה-codebase: `CLAUDE.md` (נקודת הכניסה, רזה), סוכן `os-auditor` (sub-agent לביקורת עקביות), 4 skills, וצינור ארטיפקטים ב-Python (`CASES/ULEASE_FORECAST.py` → דשבורד → deck).

---

## 5.5 ה-Agent Extension Stack — שש השכבות שמרכיבות סוכן production

רוב האנשים מבלבלים בין Skills ל-MCP. הם לא מתחרים — הם **שכבות שנערמות**, וכל אחת עונה על שאלה אחרת:

| שכבה | השאלה שהיא עונה עליה | מהות | ✅ אצלך בריפו |
|-------|------------------------|-------|----------------|
| **Skills** | WHAT — מה לדעת | מודולי ידע שנטענים on-demand (Progressive Disclosure: קודם metadata, תוכן מלא רק כשצריך) | `.claude/skills/` — 4 skills |
| **MCP** | HOW — איך להתחבר | פרוטוקול חיבור אוניברסלי לעולם החיצון ("USB-C של AI", ‎10,000+ שרתים) | GitHub MCP פעיל; יומן/Gmail בהמשך |
| **Subagents** | WHO — מי מבצע | סוכני-משנה בהקשר מבודד: מודל משלהם, הרשאות משלהן, מחזירים סיכום | `os-auditor` |
| **Hooks** | WHEN — מתי לאוטומט | סקריפטים **דטרמיניסטיים** מחוץ ללולאת ה-LLM: pre-tool, post-tool, on-edit | ה-CI שלנו (בדיקות עקביות על כל PR) הוא בדיוק זה |
| **CLAUDE.md** | WHERE — איפה מעוגן | הקשר always-on שנטען בכל session | `CLAUDE.md` — נקודת הכניסה של ה-OS |
| **Plugins** | SHIP — איך אורזים | אריזת הכל (Skills+Hooks+Subagents+MCP) ליחידה אחת ניתנת להתקנה | חבילת 31 ה-Skills (`ULEASE_AUTOMATION_MAP.md` §11) היא דוגמה |

**הכוח האמיתי הוא בשרשור:** `CLAUDE.md` טוען הקשר → Skill נותן מומחיות → MCP מתחבר למערכות → Subagent מבצע בבידוד → Hook מאוטמט את המסירה → Plugin אורז הכל לצוות.

> **ל-ULease:** זו בדיוק הארכיטקטורה שה-Tech Lead ירכיב ב-Agent Teams (רמה 7): Ultra = הסוכן הראשי עם CLAUDE.md, ה-Masters = Subagents עם Skills תחומיים, החיבור לספקים/סולק = MCP, וה-Guardian רץ כ-Hooks דטרמיניסטיים (לא נתון לשיקול ה-LLM — בדיוק כמו שציות צריך להיות).

**Skills קהילתיים ששווה להתקין** (מ-"Make Claude 10x Smarter"): `/brainstorming` · `/skill-creator` · `/writing-plans` + `/executing-plans` · `/frontend-design` (נגד AI-slop) · Brave Search / `/firecrawl` (דאטה חי מהרשת — רלוונטי למחקר מתחרים ומחירונים).

---

## 6. ה-build בריפו — מה קיים איפה

| עמוד | תשתית בריפו | איך מפעילים |
|------|---------------|--------------|
| **Cowork** | `COWORK/ABOUT-ME/` (3 קבצים) · `COWORK/TEMPLATES/` (4) · `COWORK/OUTPUTS/` | חבר את תיקיית הריפו ל-Cowork → העתק Global Instructions מ-`COWORK/README.md` |
| **Projects** | `PROJECTS_SETUP.md` — 3 בלוקים מוכנים | claude.ai → New Project → הדבק בלוק → העלה 3 קבצים → בדיקת קבלה |
| **Skills** | `.claude/skills/` — os-module · os-decision · ulease-refresh · investor-update | Claude Code מזהה אוטומטית לפי טריגר; אין מה להפעיל ידנית |
| **Code** | `CLAUDE.md` · `.claude/agents/os-auditor.md` · סקריפטי `CASES/*.py` | `claude` בטרמינל בתיקיית הריפו |

הרישום הקנוני של כל התשתית: `OPERATING_SYSTEM.md` §3 (מודולים) + §3.1 (working sets).

---

## 7. הזרימה המשולבת — דוגמה מקצה לקצה

תרחיש אמיתי — **שינוי תמחור** (כמו D-015):

```
1. Projects   דיון בהחלטה בפרויקט "ULease 🎯 השקה" — ההקשר כבר טעון
2. Code       skill os-decision   → ההחלטה נרשמת D-0XX ב-DECISION_LOG.md
3. Code       skill ulease-refresh → FORECAST.py מכויל → CSV → דשבורד → deck
4. Code       agent os-auditor    → ביקורת עקביות על כל ההפניות והגרסאות
5. Cowork     skill investor-update → טיוטת עדכון משקיעים מהמספרים החדשים → COWORK/OUTPUTS/
6. Projects   העדכון נשלח מפרויקט "גיוס ₪150K" — בטון ובכללים שכבר מוגדרים שם
```

**זה "מקצה לקצה":** החלטה → תיעוד → מודל → ארטיפקטים → ביקורת → תקשורת. כל שלב מוזן מהקודם, אפס תדרוך ידני באמצע.

---

## 8. כללי תחזוקה

| כלל | למה |
|------|------|
| ABOUT-ME מתחת ל-6,000 tokens | קבצים גדולים שורפים את התקציב לפני שהעבודה מתחילה |
| CLAUDE.md מתחת ל-200 שורות | נקרא בכל session — חייב להישאר רזה |
| שיחה חדשה כל ~20 הודעות (Cowork/Chat) | הודעות ישנות עולות tokens בכל turn |
| `/compact` באמצע · `/clear` בין משימות (Code) | חוסך ~40% tokens |
| Skill חדש רק אחרי 3 חזרות | לא בונים תשתית לדבר חד-פעמי |
| משימה אחת ל-Skill · תוצר אחד ל-Project | צר ומדויק מנצח רחב ועמום |
| קבצי הקשר מתעדכנים כשהמציאות משתנה | הקשר מיושן גרוע מאין הקשר |

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | זיקוק ה-cheat sheet "How to use Claude in 2026" + תיעוד ה-build התפעולי המלא (COWORK/ · PROJECTS_SETUP.md · `.claude/skills/`) | 2026-06-02 |
| 1.1.0 | נוסף ל-§5 בלוק **Agent Teams** (ניסיוני): Team lead · Teammates · Shared tasks + מסלול prototype ל-Ultra·Master·Max (D-029) | 2026-06-02 |
| 1.2.0 | נוסף ל-§5 **סולם 7 הרמות של Claude Code** (Prompt→Context→Tools→MCP→Skills→Subagents→Agent Teams) + הציון: רמה 6/7 (D-030) | 2026-06-02 |
| 1.3.0 | §5.5 חדש (D-037): **ה-Agent Extension Stack** — שש השכבות (Skills=WHAT · MCP=HOW · Subagents=WHO · Hooks=WHEN · CLAUDE.md=WHERE · Plugins=SHIP) + המיפוי ל-Ultra·Master·Max ו-Guardian-as-Hooks + Skills קהילתיים מומלצים | 2026-06-02 |

**Attribution.** מבוסס על ה-cheat sheet *"How to use Claude in 2026"*; סולם 7 הרמות ובלוק Agent Teams (§5): סדרת *The 7 Levels of Claude Code* (learn.nextwork.org); ה-Extension Stack (§5.5): *Understanding Agent Skills* + *Make Claude 10x Smarter*. העיבוד, התרגום, ובעיקר ה-build התפעולי — חלק מה-Claude OS של Avraham Bar Yochai Chazan.

— *End of AI_CLAUDE_STACK_2026.md v1.3.0 —*
