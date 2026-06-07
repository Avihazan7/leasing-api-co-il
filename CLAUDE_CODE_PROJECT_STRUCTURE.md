# Claude Code Project Structure — האנטומיה ⇄ ה-OS של ULease

**מבנה פרויקט Claude Code סטנדרטי (Robbert van Vlijmen) + האנטומיה המפורטת (Jamie AI Empire), מוצלבים מול מבנה ה-OS בפועל של הריפו הזה.**

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

## 5. האנטומיה המפורטת (Jamie AI Empire) — מ-doctrine ל-drop-in

האינפוגרפיקה השנייה מפרקת את `.claude/` לרמת-הקובץ. כאן ה-§4 הופך מ"חוב" ל**קבצים קונקרטיים** המכוונים ל-ULease — בדיוק מה שצריך כדי לסגור את ה-P-Tooling.

### 5.1 ששת סוגי ההרחבה — ומה כל אחד אצלנו

| הרחבה | מתי | המקבילה ב-ULease |
|-------|-----|------------------|
| **Skill** | auto-activate לפי התאמת-משימה | `AGENT_BLUEPRINT § 11` (Learn/SOP) · `/code-review`, `/security-review` |
| **Hook** | lifecycle event scripts | ⚠️ חוב — ראו 5.2 (drop-in מוכן) |
| **MCP** | חיבורי כלים חיצוניים | `DEV_ENV § 10` · `N8N § 8` — ראו 5.3 |
| **Subagent** | עבודה מקבילה מבודדת | Working Rule #8 · `stage-a/` |
| **Agent Team** | תיאום רב-סוכנים | `AGENT_BLUEPRINT § 9.4` (Stage-B) |
| **Plugin** | חבילה ניתנת-להפצה | 🟡 עתידי — אריזת ה-OS כ-plugin פנימי |

### 5.2 Hook Events ⇄ Working Rules

| Event | תפקיד | חיבור ל-OS |
|-------|------|------------|
| **PreToolUse** | חסימה לפני הרצה | governance (`AGENT_BLUEPRINT § 6`) — חסימת פקודות מסוכנות |
| **PostToolUse** | auto-fix/lint/test אחרי כתיבה | **Working Rule #6 VERIFY** — `npm test`/`typecheck` |
| **SessionStart** | טעינת context בעלייה | טעינת `CLAUDE.md` + Load Order |
| **SessionStop / PreCompact** | שמירת session · זיהוי secrets | `MEMORY.md` · governance |
| **Notification** | התראות (Slack) | `N8N_AUTOMATION` (alerting) · `BRANCH_KNOWLEDGE` (ערוץ Slack) |

### 5.3 שני הקבצים שסוגרים את §4 — drop-in ל-ULease

`.claude/settings.json` — permissions + hook שמריץ את ה-VERIFY של Working Rule #6:

```jsonc
{
  "permissions": {
    "allow": ["Bash(npm test)", "Bash(npm run typecheck)", "Bash(npm run build)"],
    "deny": ["Bash(rm -rf*)", "Bash(git push --force*)"]
  },
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{ "type": "command", "command": "npm run typecheck" }]
    }]
  }
}
```

`.mcp.json` — מעגן את שרתי ה-MCP מ-`DEV_ENV § 10` כקובץ ממשי (GitHub + Supabase/Postgres של ULease):

```jsonc
{
  "mcpServers": {
    "github":   { "command": "npx", "args": ["-y", "@anthropic/mcp-github"],
                  "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" } },
    "postgres": { "command": "npx", "args": ["-y", "@anthropic/mcp-postgres"],
                  "env": { "DATABASE_URL": "${DATABASE_URL}" } }
  }
}
```

> שני אלה + `hooks/` (סקריפט שמריץ `npm test` ב-PreToolUse של commit) הם **בדיוק** שלושת הפריטים ב-§4. ה-`DATABASE_URL` כבר חי ב-`leasing-api` (`config.ts`), וה-MCP של postgres ייתן ל-Claude שאילתות קריאה ישירות מול הסכמה — תחת RLS, אם מגדירים `app.current_tenant`.

### 5.4 Context Management — ספי-עבודה

האינפוגרפיקה נותנת ספים תפעוליים שמשלימים את Working Rule #8 (SUBAGENTS = שמירת context נקי):

| ניצול חלון | פעולה |
|-----------|-------|
| 0–60% | עבודה חופשית |
| 50–70% | ניטור |
| 70–90% | `/compact` |
| 80%+ | `/clear` (חובה) |

---

## 6. ה-takeaway

> ULease חזק ב-**ידע** (מכלול המודולים) וב-**agents** (`stage-a`), אך שכבת ה-**אכיפה הניתנת-להרצה** (`.claude/settings.json` · `.mcp.json` · `hooks/`) עדיין doctrine. §5.3 נותן את ה-drop-in המדויק. זה הצעד הבא ב-P-Tooling — מ"כתוב מה לעשות" ל"הכלי אוכף את זה".

---

*תומלל מ-"Claude Code Project Structure" (Robbert van Vlijmen) ו-"Claude Code Project Architecture" (Jamie AI Empire), ומופה למבנה ה-OS בפועל של `leasing-api-co-il` בהמשך ל-`AGENT_BLUEPRINT.md` ו-`COMMAND_API.md`.*
