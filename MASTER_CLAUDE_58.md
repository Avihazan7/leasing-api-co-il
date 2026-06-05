# 58 Ways to Master Claude — הצ'קליסט ⇄ ה-OS של ULease

**8 אשכולות לשליטה ב-Claude (@coder_surya), מוצלבים מול המודולים שכבר מיישמים אותם בריפו.**

> רוב הרשימות מהסוג הזה הן כלליות. כאן כל אחד מ-8 האשכולות מוצלב מול **המודול ב-OS שכבר מיישם אותו** — כך שהצ'קליסט הופך ל-self-audit של בגרות ה-OS של ULease, לא לפוסטר. הכותרת ⇄ המודול; הפריטים ⇄ הראיה.

---

## 1. שמונת האשכולות ⇄ המודול האחראי

| אשכול | בקצרה (מהאינפוגרפיקה) | המודול שמיישם ב-ULease | סטטוס |
|-------|----------------------|------------------------|--------|
| ⚙️ **SETUP** | profile, connect tools day one, system instructions, memory, default style | `DEV_ENVIRONMENTS.md` (נספח ד' Setup סטנדרטי) · `CLAUDE.md` Activation | ✅ |
| 🧩 **MODELS** | pick the right model, balance quality/speed/cost, reasoning models | `DEV_ENVIRONMENTS` (model selection) · `AGENT_BLUEPRINT § 9` Router | ✅ |
| 💬 **PROMPTING** | clear/specific, goal in first line, context, constraints, examples, steps | `COMMAND_API.md` · Working Rules #1-3 (PLAN/ASK/SIMPLE) | ✅ |
| 🙋 **ASK USER TOOL** | ask for missing info early, goals, examples, clarify, confirm assumptions | **Working Rule #2 ASK, DON'T ASSUME** · `AskUserQuestion` | ✅ |
| 🔌 **CONNECTORS** | Google Drive, Slack, Notion, GitHub, spreadsheets, multiple sources | `DEV_ENVIRONMENTS § 10` (MCP) · `N8N_AUTOMATION § 8` (MCP דו-כיווני) | ✅ |
| 📁 **PROJECTS** | create projects, upload docs, instructions, centralized knowledge, reusable | **ה-OS עצמו** — `CLAUDE.md` + 14 מודולים = project knowledge מרכזי | ✅ |
| 🎨 **ARTIFACTS** | drafts, spreadsheets, charts, prototype, slides, iterate | `power-bi-essential-concepts` (דשבורדים) · `public/` demo UI · `docs/specs/` | ✅ |
| 🚀 **PRO LEVEL** | chain prompts, reusable libraries, multi-step, automate, optimize, AI systems | `AGENT_BLUEPRINT § 9` (orchestration) · `stage-a/` · `N8N` (automate) | ✅ |

---

## 2. ה-Mapping המעמיק — איפה כל אשכול "חי" בקוד/דוקטרינה

- **SETUP ⇄ `DEV_ENVIRONMENTS` נספח ד'** — Cowork folder-first, ABOUT-ME, Global Instructions; ה-`CLAUDE.md` Activation block הוא ה-"system instructions you love".
- **PROMPTING ⇄ `COMMAND_API`** — *"break complex tasks into steps"* ו-*"request structured output"* = composition operators + 100 ה-slash commands.
- **ASK USER TOOL ⇄ Working Rule #2** — האינפוגרפיקה מקדישה אשכול שלם ל-*"ask for missing info early / reduce guesswork before execution"*. זה **בדיוק** כלל העבודה המחייב #2 (ASK, DON'T ASSUME) ב-`CLAUDE.md` — ומומש בפועל ב-session הזה (שאלת-הבהרה לפני כתיבת המודולים).
- **CONNECTORS ⇄ MCP** — *"Connect GitHub repositories / combine multiple data sources"* = שכבת ה-MCP (`AGENT_BLUEPRINT § 11`: Connect).
- **PROJECTS ⇄ ה-OS** — *"keep knowledge centralized / build reusable project systems"* = בדיוק מה ש-`CLAUDE.md` (Module Load Order) ו-14 המודולים עושים. הריפו הזה הוא Claude Project בוגר.
- **PRO LEVEL ⇄ `stage-a` + `AGENT_BLUEPRINT § 9`** — *"chain prompts / run multi-step workflows / combine tools for compound leverage"* = 9 ה-orchestration topologies; `stage-a` הוא Plan & Execute (`§ 9.3`).

---

## 3. החיבור ל-LAUNCH § 3.1 — "Master Claude in a Week"

האינפוגרפיקה היא **רשימת יכולות**; `LAUNCH § 3.1` היא **לוח-זמנים** שמתרגם אותן ל-7 ימים עם deliverable יומי. המיפוי:

| יום (LAUNCH § 3.1) | אשכול תואם (58 Ways) |
|--------------------|----------------------|
| Setup + Global Instructions | SETUP |
| Prompting + Commands | PROMPTING · ASK USER TOOL |
| Connectors + MCP | CONNECTORS |
| Projects + Knowledge | PROJECTS |
| Artifacts + Dashboards | ARTIFACTS |
| Orchestration + Automation | PRO LEVEL |
| Models + Optimization | MODELS |

> **הקריאה:** ה-58 Ways מאשרר ש-7 הימים של `LAUNCH § 3.1` מכסים את כל 8 האשכולות. אין אשכול "יתום" — מה שמאשר שמסלול ההדרכה שלם.

---

## 4. Self-Audit — בגרות ה-OS מול 8 האשכולות

| אשכול | בשל ב-ULease? | פער |
|-------|--------------|-----|
| SETUP · PROMPTING · ASK · PROJECTS · ARTIFACTS · PRO LEVEL | ✅ מלא (מודול ייעודי + ראיה) | — |
| CONNECTORS | 🟡 doctrine | אין `.mcp.json` ב-root (ראה `CLAUDE_CODE_PROJECT_STRUCTURE § 4`) |
| MODELS | 🟡 doctrine | Router pattern מתואר, טרם חי ב-`stage-a` (ראה `AI_SDLC_ORCHESTRATION § 5`) |

> שני הפערים זהים לאלה שזוהו במודולים האחרים — מה שמאשר שהם **חוב אמיתי ועקבי**, לא רעש: חיווט MCP בפועל ו-LLM routing חי. שניהם P-Tooling/Stage-B.

---

*תומלל מ-"58 Ways to Master Claude" (@coder_surya), ומופה למודולי ה-OS של `leasing-api-co-il` בהמשך ל-`LAUNCH.md § 3.1` ו-`DEV_ENVIRONMENTS.md`.*
