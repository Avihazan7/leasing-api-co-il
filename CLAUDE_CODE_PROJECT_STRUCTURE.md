# Claude Code Project Structure — האנטומיה ⇄ ה-OS של ULease

**מבנה פרויקט Claude Code סטנדרטי (Robbert van Vlijmen), מוצלב מול מבנה ה-OS בפועל של הריפו הזה.**

> הריפו הזה **הוא** פרויקט Claude Code — אבל בגרסה בוגרת: במקום `.claude/` רזה הוא הפך לשכבת-OS של מסמכים (`CLAUDE.md` כ-entry point + 14 מודולים). המודול הזה לוקח את 8 אבני-הבניין מהאינפוגרפיקה, מסביר כל אחת, ומראה **מה כבר קיים, מה ממופה למודול אחר, ומה חסר** (חוב מתועד).

---

## 1. 8 אבני-הבניין — מבט-על

| רכיב | תפקיד (מהאינפוגרפיקה) | gitignored? |
|------|----------------------|-------------|
| `CLAUDE.md` | קובץ הוראות ראשי שנטען בתחילת session: project overview, tech stack, build/test, conventions | לא |
| `CLAUDE.local.md` | overrides אישיים | ✅ כן |
| `.mcp.json` | תצורות אינטגרציית MCP (GitHub/JIRA/Slack/DBs), משותף בגיט | לא |
| `.claude/settings.json` | permissions, tools, model selection, hooks | לא |
| `.claude/settings.local.json` | overrides מקומיים | ✅ כן |
| `rules/` | קבצי הוראות מודולריים לפי נושא, נטענים אוטומטית לפי frontmatter | לא |
| `commands/` | slash commands ידניים (`/project:<filename>`), תומך `!`backtick shell | לא |
| `skills/` | workflows מופעלי-context (`SKILL.md` + support files), נטענים רק בעת צורך | לא |
| `agents/` | subagents עם context מבודד, persona+tools+model | לא |
| `hooks/` | סקריפטי automation מבוססי-אירוע (לפני/אחרי tool use), חוסמים פעולות מסוכנות | לא |

---

## 2. האנטומיה ⇄ ULease — מה כבר קיים

| רכיב סטנדרטי | המקבילה ב-ULease | סטטוס |
|--------------|------------------|--------|
| `CLAUDE.md` | `CLAUDE.md` — OS Entry Point (Active Modules + Load Order + Working Rules + Activation) | ✅ קיים, בוגר |
| `rules/` (code-style, testing, api-conventions) | **Working Rules** ב-`CLAUDE.md` (8 כללי Karpathy) + `system-design-cheatsheet` + `BACKEND_ROADMAP` | ✅ ממופה (inline, לא תיקייה) |
| `commands/` | `COMMAND_API.md` — **100 slash commands** ב-12 קטגוריות (native ⚙️ + behavioral 💬) + composition operators | ✅ קיים, מעבר לסטנדרט |
| `skills/` (`SKILL.md` per skill) | `AGENT_BLUEPRINT § 11` (Skill=Learn/SOP) + הבהרת המינוח `§ 11.2` | ✅ ממופה (doctrine) |
| `agents/` (code-reviewer, security-auditor) | `stage-a/` — Agent Runtime (Plan & Execute); `/code-review`, `/security-review` skills | ✅ קיים |
| `.mcp.json` | `DEV_ENVIRONMENTS § 10` (MCP servers) + `N8N § 8` (MCP דו-כיווני) | 🟡 doctrine, אין קובץ root |
| `.claude/settings.json` (permissions/hooks) | `AGENT_BLUEPRINT § 6` (governance) · `DEV_ENV § 9.4` (allow/deny) | 🟡 doctrine, אין קובץ |
| `hooks/` (validate-bash.sh) | `AGENT_BLUEPRINT § 6` (governance-in-code) — מתואר, לא ממומש כסקריפט | ⚠️ חוב מתועד |

---

## 3. ההבחנה הקריטית — 4 הפרימיטיבים לא חופפים

האינפוגרפיקה מבדילה בין `rules/`, `commands/`, `skills/`, `agents/`. זו בדיוק ההפרדה ש-`AGENT_BLUEPRINT § 11.2` אוכף בריפו:

| פרימיטיב | מתי נטען | האנלוגיה |
|----------|----------|----------|
| `rules/` | אוטומטית כשקובץ רלוונטי נפתח | "always-on" guardrails |
| `commands/` | ידנית, כשמקלידים `/name` | כפתור שאתה לוחץ |
| `skills/` | אוטומטית לפי context (חוסך context window) | SOP שנשלף בעת צורך — **Learn** (`§ 11`) |
| `agents/` | ב-subagent עם context מבודד | עובד נפרד עם persona משלו |
| `.mcp.json` | חיבור תמידי | **Connect** — AI-native APIs (`§ 11`) |

> **הכלל:** `skills/`=ידע תהליכי (Learn), `.mcp.json`=חיבור למערכות (Connect). לערבב ביניהם זה ה-anti-pattern ש-`AGENT_BLUEPRINT § 11.3` (Use-Both) מזהיר מפניו. ראה גם Working Rule #8 (SUBAGENTS) — בדיוק ה-`agents/` עם context מבודד.

---

## 4. חוב פתוח — מה שכדאי להוסיף בפועל

הריפו עשיר ב-doctrine אך דל ב-**קבצים שניתנים-להרצה**. הצעדים הקונקרטיים (P-Tooling):

1. **`hooks/`** — לממש את governance-in-code (`§ 6`) כסקריפט אמיתי: hook שמריץ `npm test`/`typecheck` לפני commit (תואם Working Rule #6 VERIFY). יש skill מובנה `session-start-hook` בדיוק לכך.
2. **`.claude/settings.json`** — לקבע permissions ו-allow-list (skill `fewer-permission-prompts`) במקום doctrine בלבד.
3. **`.mcp.json` ב-root** — לעגן את ה-MCP servers מ-`DEV_ENV § 10` כקובצי-תצורה ממשיים.

> זה לא פער מקרי: הריפו בנה את שכבת ה-**ידע** (14 מודולים) לפני שכבת ה-**אכיפה** (hooks/settings). השלמת שכבת האכיפה היא הצעד הטבעי הבא.

---

*תומלל מ-"Claude Code Project Structure" (Robbert van Vlijmen), ומופה למבנה ה-OS בפועל של `leasing-api-co-il` בהמשך ל-`AGENT_BLUEPRINT.md` ו-`COMMAND_API.md`.*
