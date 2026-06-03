# AGENT_BLUEPRINT.md — מ-Skill ל-Agent: דוקטרינת ה-System-First

**Module:** `AGENT_BLUEPRINT.md`
**Version:** 1.2.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Doctrine. הגשר בין ה-Docs OS ל-Agent Runtime.
**Integrates with:** `CLAUDE.md`, `COMMAND_API.md`, `DEV_ENVIRONMENTS.md`, `LAUNCH.md`, `stage-a/`
**Thesis:** *Design the SYSTEM first. The model is only one layer.*

---

## 0. למה הקובץ הזה קיים

בנינו שני חצאים — ועד עכשיו הם לא הכירו זה את זה:

```
   ┌─────────────────────────┐         ┌─────────────────────────┐
   │      DOCS OS            │         │     AGENT RUNTIME       │
   │  (איך בני אדם משתמשים)  │   ❓    │   (איך agents רצים)     │
   ├─────────────────────────┤  ────►  ├─────────────────────────┤
   │ COMMAND_API · WINDOWS   │ הגשר    │ stage-a/                │
   │ DEV_ENV · LAUNCH        │ החסר    │ manager · worker        │
   │ CASES                   │         │ shared-memory · gov     │
   └─────────────────────────┘         └─────────────────────────┘
```

**הפער:** ל-`LAUNCH.md` יש Skills (`/deal-quote`, `/fleet-report`, `/board-deck`) —
אבל Skill הוא **prompt**, לא **agent**. agent צריך mission, memory, tools, orchestration,
ו-evals. הקובץ הזה הוא הדוקטרינה שהופכת Skill ל-agent production-grade, ומחבר את
התיאוריה ל-`stage-a/` שכבר רץ בקוד.

**עיקרון מנחה (מהפוסט שהצית את המודול):**
> רוב הצוותים כותבים prompt, בוחרים מודל, מוסיפים כלים, וקוראים לזה "agent".
> זה מרשים ב-demo ונשבר ב-production. agent אמיתי נבנה מ-**ארכיטקטורה**, לא מ-hype.

---

## 1. The 8-Module Blueprint

כל agent ב-ULease נבנה מ-8 המודולים האלה, **בסדר הזה**. דילוג על מודול = חוב טכני.

| # | Module | השאלה שהוא עונה |
|---|--------|------------------|
| 1 | **Purpose & Scope** | איזו משימה ה-agent מחזיק כל שבוע? איזו החלטה נשארת אצל אדם? |
| 2 | **System Prompt** | מה ה-goals, rules, guardrails, refusal & escalation? |
| 3 | **Choose LLM** | איזה מודל ל-job הזה? (opus/sonnet/haiku — cost vs. capability) |
| 4 | **Tools & Integrations** | מה ה-agent יכול לעשות בפועל? (MCP, API, DB, functions) |
| 5 | **Memory Systems** | מה הוא זוכר בין ריצות? (episodic / working / vector / SQL) |
| 6 | **Orchestration** | triggers, routing, retries, queues, error handling, human gates |
| 7 | **User Interface** | איפה המשתמש פוגש אותו? (Slack / web / API / Office task pane) |
| 8 | **Testing & Evals** | איך יודעים שהוא אמין? (completion, latency, cost, failure, correction) |

---

## 2. Coverage Map — מה יש, מה חסר (כנה)

| # | Module | מצב | היכן / מה חסר |
|---|--------|------|----------------|
| 1 | Purpose & Scope | 🟡 חלקי | RACI ב-`LAUNCH.md § 6`. חסר: one-sentence mission + success metric לכל Skill |
| 2 | System Prompt | ✅ מלא | `COMMAND_API.md § 7` — drop-in system prompt |
| 3 | Choose LLM | ✅ מלא | `DEV_ENVIRONMENTS.md` — `/model` ⚙️, decision matrix |
| 4 | Tools & Integrations | ✅ מלא | `DEV_ENVIRONMENTS.md § 10` — MCP servers, internal MCP roadmap |
| 5 | Memory Systems | 🟡 חלקי | `stage-a/shared-memory.js` (append-only). **חסר:** 4 ה-tiers + `MEMORY.md` |
| 6 | Orchestration | ✅ POC | `stage-a/manager.js` + `worker-summarizer.js` (plan→route→execute) |
| 7 | User Interface | ✅ מלא | 6 tracks (`DEV_ENV`) + Office task pane (`WINDOWS_DEPLOYMENT`) |
| 8 | Testing & Evals | ❌ **פער** | **אין כלום.** ראה § 5 — זו עבודת ה-priority הבאה |

**שורה תחתונה:** 5 מודולים ✅, 2 חלקיים 🟡, 1 פער ❌. ה-system כמעט שלם —
הליבה החסרה היא **Evals** (אמינות) ו-**Memory tiers** (זיכרון אמיתי).

---

## 3. הגשר ל-stage-a — מה כבר רץ בקוד

`stage-a/` הוא לא mock. הוא מממש 3 מודולים מ-§ 1, עם **governance שנאכף בקוד**:

| רכיב ב-stage-a | Module | מה הוא אוכף |
|-----------------|--------|--------------|
| `manager.js` | 6 · Orchestration | מטרה → תוכנית; **תקרת צעדים** עוצרת לולאות בורחות; מנתב, לא מבצע |
| `worker-summarizer.js` | 6 · Orchestration | מבצע לפי חוזה AGENT.md; **safe-stop** על קלט חסר |
| `shared-memory.js` | 5 · Memory | append-only single-source-of-truth; **`evidence[]` חובה** על תוצר; audit מלא |

ה-governance של `stage-a` (תקרת צעדים · evidence חובה · append-only · safe-stop)
הוא **בדיוק** מודול 8 חלקי באינפוגרפיקה השנייה (Safety & Governance) — אבל מיושם,
לא מתועד. ה-`AGENT_BLUEPRINT` מאמץ אותו כסטנדרט: **כל agent ב-ULease יורש את
4 מנגנוני הממשל האלה.**

---

## 4. Build Order — מ-Skill ל-Agent (דוגמה: `/deal-quote`)

איך הופכים את ה-Skill הקיים ל-agent מלא, מודול-אחר-מודול:

```
1. Purpose     → "ה-agent מחזיק יצירת הצעות מחיר. תמחור סופי > ₪X = אישור אנושי."
2. Prompt      → goals + refusal (לא מצטט מחיר בלי מקור) + escalation
3. LLM         → sonnet (מהיר, זול) ל-draft; opus רק לקצוות מורכבים
4. Tools       → MCP: pricing-quote + deal-lookup (DEV_ENV § 10.5, read-only)
5. Memory      → working: העסקה הנוכחית · episodic: היסטוריית הלקוח · vector: policy docs
6. Orchestr.   → stage-a manager מפרק; worker מתמחר; human gate מעל ₪X
7. UI          → Office task pane (WINDOWS § 7) + Slack notify
8. Evals       → completion rate, מקרי "מחיר בלי evidence" = 0, human-correction < 10%
```

אותו תהליך חל על `/fleet-report`, `/board-deck`, `/competitor-scan`. **Skill = שלב 2 בלבד.
agent = כל ה-8.**

---

## 5. הפער האמיתי — Evals Doctrine (מודול 8)

זו השכבה שחסרה לנו לגמרי, וזו השכבה שממנה מגיעה האמינות. **כל agent ב-ULease
נמדד ב-5 המטריקות האלה, שבועית:**

| מטריקה | הגדרה | יעד | פעולה אם נכשל |
|---------|--------|-----|----------------|
| **Task completion rate** | % משימות שהושלמו בלי התערבות | > 85% | חדד prompt / tools |
| **Latency** | זמן ממוצע למשימה | < SLA לפי סוג | optimize / החלף מודל |
| **Cost per run** | $ למשימה מושלמת | < תקרה לפי ROI | sonnet במקום opus |
| **Tool failure rate** | % קריאות tool שנכשלו | < 5% | תקן integration / retry logic |
| **Human correction rate** | % תוצרים שאדם תיקן | < 10% | re-train prompt / הוסף guardrail |

**הטקס השבועי:** Tech Lead עובר על failed runs, מעדכן prompt/tools/permissions/workflow.
זה לא אופציונלי — זה ה-loop שמייצר production-grade. ראה גם `LAUNCH.md § 4` (KPIs).

> **כלל ברזל:** agent בלי evals הוא demo. אל תשחרר agent ל-production בלי 5 המטריקות
> מוגדרות ו-baseline נמדד.

---

## 6. Safety & Governance — איחוד השכבה

מאוחד מ-3 מקורות שכבר קיימים + סטנדרט `stage-a`:

| שכבת ממשל | מקור | אכיפה |
|------------|------|--------|
| Permission controls | `DEV_ENVIRONMENTS § 9.4` (Claude Code allow/deny) | config |
| Secrets & PII | `WINDOWS § 13` (`/scrub-pii`) + `DEV_ENV § 13` | pre-flight |
| Step ceiling | `stage-a/manager.js` | **קוד** |
| Evidence mandatory | `stage-a/shared-memory.js` | **קוד** |
| Append-only audit | `stage-a/shared-memory.js` | **קוד** |
| Human escalation gates | `AGENT_BLUEPRINT § 4` build order | doctrine |
| Kill-switch | `LAUNCH.md § 8` | playbook |

**העיקרון:** ככל שהממשל נאכף ב-**קוד** ולא ב-prompt — הוא חזק יותר. `stage-a`
מראה את הדרך; כל agent חדש מקודד את ה-guardrails שלו, לא רק מבקש אותם.

---

## 7. Roadmap — השלבים הבאים

| שלב | תוכן | תלוי ב- |
|-----|------|----------|
| **MEMORY.md** | דוקטרינת 4 ה-tiers (episodic/working/vector/SQL) — סוגר dangling ref + מודול 5 | — |
| **Stage-B** | מנהל + N עובדים מקבילים; routing דינמי | stage-a |
| **Stage-C** | MCP פנימי חי (`mcp-ulease`) כ-tool layer ל-agents | `DEV_ENV § 10.5` |
| **Evals harness** | מדידה אוטומטית של 5 המטריקות (§ 5) ב-CI | Stage-B |
| **OPERATING_SYSTEM.md** | מסמך-על — סוגר dangling ref אחרון ב-load order | כל המודולים |

**שלוש הפניות מתות** ב-`CLAUDE.md` load order (`OPERATING_SYSTEM.md`, `MEMORY.md`,
`INVESTOR_RELATIONS.md`) — מתועדות כאן כ-roadmap מוצהר, לא כחור שקט.

---

## 8. Self-Assessment — לפני שמשחררים agent

```
□ מודול 1: mission במשפט אחד + success metric כתובים
□ מודול 2: system prompt כולל refusal + escalation
□ מודול 3: מודל נבחר לפי cost/capability, לא ברירת-מחדל
□ מודול 4: tools עם approval gate לפני פעולות יקרות/בלתי-הפיכות
□ מודול 5: working memory ו-long-term memory מופרדים
□ מודול 6: step ceiling + safe-stop + audit (יורש מ-stage-a)
□ מודול 7: ה-UI בתוך ה-workflow הקיים של המשתמש
□ מודול 8: 5 מטריקות evals מוגדרות + baseline נמדד
```

8 ✅ = agent ל-production. פחות מ-8 = demo. אל תבלבל בין השניים.

---

## 9. Orchestration Patterns — בחירת ה-topology

מודול 6 (`§ 1`) אומר *לבנות* orchestration. זה לא מספיק. צריך גם **לבחור צורה**.
9 ה-patterns המוכרים ב-2026 (מקור: Anthropic + רכש קהילה), עם מיפוי ישיר ל-ULease.

### 9.1 הקטלוג

| # | Pattern | מה זה | אצלנו |
|---|---------|--------|--------|
| 1 | **Prompt Chaining** | step→step→step, כל קריאה מקבלת פלט מהקודמת | `/deal-quote` (gather→price→validate→format) |
| 2 | **Parallelization** | N קריאות במקביל, אגרגטור מאחד | `/competitor-scan` (N מתחרים) |
| 3 | **Orchestrator-Worker** | Central LLM מפרק דינמית ושולח ל-workers, Synthesizer מאחד | `/board-deck` (research + writing + visuals) |
| 4 | **Evaluator-Optimizer** | Generator→Evaluator→Generator עד אישור (חד-פעמי לרוב) | `/proofread`, `/improve` |
| 5 | **Router** | Classifier מפנה ל-pipeline ייעודי | Customer support triage, MAD (Multi-Agent Debate) |
| 6 | **Autonomous Workflow** | LLM פועל עם environment, feedback loop | Computer Use — QA חי, מערכות legacy בלי API |
| 7 | **Reflexion** | Responder→Tools→Revisor, **n-times** עד שמספיק טוב | `/code-review ultra`, `/security-review` |
| 8 | **ReWOO** | Planner מגדיר את **כל** המשימות *לפני* הרצה; חוסך LLM calls | `/research`, `/fact-check` ארוכים |
| 9 | **Plan and Execute** | Planner→Tasks→Single Task Agents→**Replan** דינמי | **`stage-a/` = זה.** Stage-B = + Replan loop |

### 9.2 ULease Skills Map — נכון ל-v1.1.0

| Skill | Pattern | למה דווקא זה |
|--------|---------|---------------|
| `/deal-quote` | Chaining (1) | שלבים קבועים, סדר חשוב |
| `/board-deck` | Orchestrator-Worker (3) | סוכנים שונים (R+W+V), הרכבה דינמית |
| `/competitor-scan` | Parallelization (2) | אותו flow על N מטרות |
| `/fleet-report` | Chaining (1) + Tools | ETL ליניארי + DB read |
| `/code-review` (ultra) | **Reflexion (7)** | loop של ביקורת-תיקון, לא חד-פעמי |
| `/security-review` | Reflexion (7) | אותה סיבה — n-iterations עם tools |
| `/proofread`, `/improve` | Evaluator-Optimizer (4) | תיקון חד-פעמי, בלי tools |
| `/research`, `/fact-check` | ReWOO (8) | תכנון כולל לפני exec, חוסך עלות |
| `/deal-quote-batch` (עתידי) | Plan and Execute (9) | מורכב, צריך Replan דינמי |
| Customer FAQ Bot | Router (5) | classify → pipeline ייעודי |
| Fleet emergency response (עתידי) | Autonomous (6) | sensor input, real-time decisions |

### 9.3 stage-a — הזיהוי

`stage-a/manager.js` + `worker-summarizer.js` = **Plan and Execute (pattern #9)** —
לא "manager+worker גנרי", אלא pattern מוכר עם use cases מוצהרים: **"Business Process
Automation · Data Pipeline Orchestration"**. אלה בדיוק שתי הקטגוריות שמתארות את
ULease. זו לא תאוריה — זו אקסטרנליזציה של החלטה ארכיטקטונית שכבר נכונה.

### 9.4 Stage-B — הגדרה חדה (עדכון § 7)

Roadmap אמר "מנהל + N עובדים מקבילים". ההגדרה החדה:

> **Stage-B = Plan and Execute + Replan loop**

המנהל לא רק מפזר ל-N עובדים — הוא **בודק אם התוכנית עדיין תקפה** אחרי כל step,
ומוציא Replan כשהקרקע השתנתה. זה ההבדל בין pattern #9 (היעד שלנו) ל-pattern #8
(ReWOO, שאין לו replan).

### 9.5 כלל בחירה

```
משימה ליניארית קבועה?      → Chaining (1)
משימה זהה על N מטרות?      → Parallelization (2)
משימה תלוית-סיווג?         → Router (5)
משימה דורשת agents שונים?  → Orchestrator-Worker (3)
משימה דורשת iteration?     → Evaluator (4) חד-פעמי / Reflexion (7) n-פעמי
משימה דורשת תכנון מוקדם?   → ReWOO (8) קבוע / Plan&Execute (9) דינמי
משימה תלוית-environment?   → Autonomous (6)
משימה פשוטה?              → Skill בלבד — לא agent. חזור ל-COMMAND_API.
```

**הכלל הראשון:** אם Skill מספיק, אל תבנה agent. agent מצדיק את עצמו רק כשמודול 6
(orchestration) באמת נדרש.

---

## 10. Coding Workflow Doctrine — Karpathy's CLAUDE.md

§ 1–§ 9 עונים על *"איך בונים agent"*. הסעיף הזה עונה על *"איך agent עובד על קוד"* —
מבוסס על ה-CLAUDE.md של Andrej Karpathy. התובנה המרכזית שלו היא **בדיוק** התזה של
הקובץ הזה:

> *LLMs לא משתפרים כשמנסחים להם prompt טוב יותר. הם משתפרים כשכופים עליהם
> workflow ממושמע. CLAUDE.md הוא לא prompt — הוא operating system של ה-agent.*

זה מה שהריפו הזה **הוא**. Karpathy נותן את השכבה שחסרה: הכללים שה-agent עצמו
מציית להם כשהוא נוגע בקוד.

### 10.1 ששת עקרונות ה-Workflow

| # | עיקרון | הכלל האופרטיבי | למה זה קיים |
|---|--------|------------------|--------------|
| 1 | **Plan Mode First** | plan mode לכל משימה לא-טריוויאלית; spec לפני קוד; צמצום עמימות לפני כתיבה | מודלים **מניחים** במקום לשאול |
| 2 | **Verify Relentlessly** | בדוק הנחות, הרץ טסטים, סקור diffs; אל תאשר בעיוורון — הישאר ב-loop | מודלים מסתירים בלבול |
| 3 | **Keep It Simple** | העדף 100 שורות על 1,000; נקה dead code; שאל "יש דרך פשוטה יותר?" | מודלים עושים overengineering |
| 4 | **Surgical Edits Only** | שנה רק מה שנדרש; אל תיגע בקוד לא קשור; אל "תשפר" מה שלא שבור | מודלים משכתבים קוד לא קשור |
| 5 | **Goal-Driven Execution** | תן success criteria, כתוב טסטים, תן ל-agent לאיטרט עד שהיעד מושג | מודלים מייעלים ל-completion, לא ל-correctness |
| 6 | **Parallelize with Subagents** | research/exploration/analysis ל-subagents; משימה אחת לכל subagent; מיזוג עם שיקול דעת | context אחד מתמלא — subagents שומרים אותו נקי |

**3 עקרונות ליבה מעל הכול:** Simplicity First (קוד מינימלי שפותר את הבעיה, כלום
ספקולטיבי) · No Laziness (root causes, לא תיקונים זמניים) · Minimal Impact (גע רק
במה שנדרש, אפס side effects).

### 10.2 מיפוי ל-Blueprint — הדוקטרינות מתלכדות

| עיקרון Karpathy | איפה זה כבר אצלנו | מה זה מוסיף |
|------------------|--------------------|--------------|
| Plan Mode First (1) | § 9 patterns #8 (ReWOO) · #9 (Plan & Execute) | אותו עיקרון ברמת **משימת קוד בודדת**, לא רק topology |
| Verify Relentlessly (2) | § 5 Evals (fleet-scale, שבועי) | Karpathy = אותו loop ברמת **ה-run הבודד**, בזמן אמת |
| Keep It Simple (3) | § 9.5 "אם Skill מספיק, אל תבנה agent" | אותו כלל ברמת הקוד: אם פונקציה מספיקה, אל תבנה מערכת |
| Surgical Edits (4) | `stage-a` governance — step ceiling, safe-stop | Minimal Impact כ-**doctrine**, לא רק כאכיפה בקוד |
| Goal-Driven Execution (5) | § 9 patterns #4 (Evaluator) · #7 (Reflexion) | *"אל תגיד מה לעשות — תן success criteria ותן לו לאיטרט"* = ההגדרה התמציתית של שני ה-patterns |
| Parallelize Subagents (6) | § 9 patterns #2 (Parallelization) · #3 (Orchestrator-Worker) · Stage-B | "צוות הנדסה של agents" = בדיוק Stage-B (מנהל + N עובדים) |

**המסקנה:** Karpathy לא מוסיף מודול תשיעי ל-blueprint. הוא נותן את ה-**רזולוציה
הנמוכה** — איך כל worker בודד מתנהג בתוך ה-orchestration שכבר הגדרנו. § 9 בוחר
את ה-topology; § 10 קובע איך כל node בתוכה כותב קוד.

### 10.3 The Shift — מ-Prompting ל-Systems

> *"From: 'write this function' → To: 'here's the goal, constraints, tests, and
> verification system — now iterate until correct.'"*

| לפני | אחרי | אצלנו |
|------|------|--------|
| כותבים prompt | בונים workflow | `COMMAND_API` → `AGENT_BLUEPRINT` |
| מבקשים פונקציה | נותנים success criteria | מודול 1 (mission + metric) + מודול 8 (evals) |
| agent אחד עוזר | צוות agents מתוזמר | Stage-B (§ 9.4) |
| בודקים את הפלט | בונים verification system | § 5 — 5 המטריקות |

זה גם הטיעון העסקי של הקובץ: *"The highest leverage engineers won't be the best
coders — they'll be the people who build the best systems around AI agents."*
ה-Docs OS הזה הוא בדיוק ה-system הזה עבור ULease.

### 10.4 Working Rules — הבלוק האופרטיבי

הכללים האלה נטענים ב-`CLAUDE.md` של **שני הריפואים** (`leasing-api-co-il` +
`leasing-api`) ומחייבים כל agent שעובד על הקוד:

```
1. PLAN FIRST    — משימה לא-טריוויאלית מתחילה ב-plan, לא בקוד.
2. ASK, DON'T ASSUME — עמימות בדרישה? שאל. אל תנחש.
3. SIMPLE        — הפתרון המינימלי שפותר את הבעיה. שום דבר ספקולטיבי.
4. SURGICAL      — גע רק בקבצים שהמשימה דורשת. אל תשפץ מה שלא שבור.
5. GOAL-DRIVEN   — הגדר success criteria (טסט/בדיקה) לפני הביצוע; איטרט עד שעובר.
6. VERIFY        — הרץ את מה שכתבת. diff נסקר לפני commit. אין "אמור לעבוד".
7. NO LAZINESS   — root cause, לא workaround. אם יש חוב — תעד אותו, אל תסתיר.
8. SUBAGENTS     — exploration/research ב-subagent נפרד; שמור על context ראשי נקי.
```

### 10.5 Mindset — ארבע אזהרות

| מושג | המשמעות ל-ULease |
|------|-------------------|
| **Tenacity** | agents לא מתעייפים — איטרציה חסרת-רחמים היא מכפיל כוח. בנה את ה-loop, לא את התשובה |
| **Leverage** | Imperative → Declarative. הגדר *מה* נכון, לא *איך* לעשות |
| **Atrophy** | כתיבה וקריאה של קוד הם שרירים — ה-Tech Lead חייב להמשיך לקרוא diffs בעצמו (ראה § 5, הטקס השבועי) |
| **Slopacolypse** | 2026 = שיטפון של AI slop. ה-signal הוא **שיפוט אנושי** — בדיוק ה-human gates של § 4 ו-§ 6 |

---

## גרסאות

| גרסה | תאריך | שינוי |
|------|--------|-------|
| 1.0.0 | 2026-05-31 | Initial — 8-module doctrine, coverage map, stage-a bridge, evals layer |
| 1.1.0 | 2026-05-31 | + § 9 Orchestration Patterns — 9 patterns, ULease Skills map, stage-a קלסיפיקציה (Plan & Execute), Stage-B חדד (= P&E + Replan) |
| 1.2.0 | 2026-06-03 | + § 10 Coding Workflow Doctrine — עקרונות ה-CLAUDE.md של Karpathy: 6 עקרונות workflow, מיפוי ל-§ 1/§ 5/§ 9, Working Rules block לשני הריפואים, mindset |

---

**Tie-back ל-OS:** הקובץ הזה הוא ה-**connective tissue**. `COMMAND_API` נותן את הפקודות,
`DEV_ENVIRONMENTS` את הכלים, `LAUNCH` את ה-go-live — ו-`AGENT_BLUEPRINT` מסביר איך
מרכיבים מהם **agent** שלא נשבר ב-production. § 9 בוחר את ה-topology, § 10 קובע איך
כל agent בתוכה כותב קוד. הוא מצביע קדימה ל-`MEMORY.md` ול-Stage-B כצעדים הבאים.
*Start with the SYSTEM first. Everything else scales from there.*
