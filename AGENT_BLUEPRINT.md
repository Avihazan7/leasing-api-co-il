# AGENT_BLUEPRINT.md — מ-Skill ל-Agent: דוקטרינת ה-System-First

**Module:** `AGENT_BLUEPRINT.md`
**Version:** 1.5.0
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

### 6.1 חיזוק חיצוני — Gartner על אבטחת AI

Gartner (webinar, יוני 2026) מפרק 5 תפיסות שגויות — וכל אחת מאשרת החלטה שכבר
קיבלנו. זה החומר להציג ל-DPO ולמשקיעים כשנשאלים "על סמך מה הממשל שלכם":

| ❌ התפיסה השגויה | ✅ המציאות (Gartner) | אצלנו |
|-------------------|------------------------|--------|
| כל AI מנוהל אותו דבר ברמת סיכון | ל-Traditional/GenAI/Agentic יש שיקולי אבטחה נפרדים + חופפים | בדיוק ההפרדה שלנו: Skill ≠ n8n Workflow ≠ stage-a Agent (`N8N § 11`) |
| צריך ממשל סייבר חדש לגמרי ל-AI | מתאימים בקרות קיימות; גישות חדשות יתפתחו | ה-DPO מרחיב מסגרת קיימת — לא בונה מאפס (`WINDOWS § 13`) |
| סיכוני AI דורשים פרקטיקות חדשות | AI בעיקר **מגביר** סיכונים קיימים; מטפלים בכלים קיימים | HMAC, kill-switch, audit — אותם כלים, היקף רחב יותר |
| Agents בטוחים לשימוש אוטונומי | **לא** פורסים agents בלי פיקוח ו-safeguards | human gates (§ 4) + step ceiling + safe-stop — אכוף בקוד |
| ערך מובטח — AI סייבר משפר יעילות | נדרשת גישה מובנית אך זריזה להערכת יכולות | Evals (§ 5) לפני כל הרחבה. אין פריסה בלי baseline |

**שורה תחתונה:** הדוקטרינה שלנו עומדת בביקורת Gartner סעיף-סעיף. זה לא מקרה —
זה מה שקורה כשבונים system-first.

---

## 7. Roadmap — השלבים הבאים

| שלב | תוכן | תלוי ב- |
|-----|------|----------|
| **MEMORY.md** | דוקטרינת 4 ה-tiers (episodic/working/vector/SQL) — סוגר dangling ref + מודול 5 | — |
| **Stage-B** | מנהל + N עובדים מקבילים; routing דינמי | stage-a |
| **Stage-C** | MCP פנימי חי (`mcp-ulease`) כ-tool layer ל-agents | `DEV_ENV § 10.5` |
| **Evals harness** | מדידה אוטומטית של 5 המטריקות (§ 5) ב-CI | Stage-B |
| **A2A protocol** | פרוטוקול תקשורת מנהל⇄עובדים (מקור: Gulli ch.15, ראה § 9.6) | Stage-B |
| **Exception & Recovery** | recovery doctrine — לא רק safe-stop (Gulli ch.12, § 9.6) | stage-a |
| **Resource-Aware routing** | בחירת מודל דינמית לפי משימה (Gulli ch.16) — היום סטטי במודול 3 | Evals harness |
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

### 9.6 הקנון — *Agentic Design Patterns* (Antonio Gulli, 424 עמ')

הספר הוא ה-reference המלא של התחום — 21 פרקים + נספחים. מיפוי מול מה שיש לנו:

| חלק בספר | פרקים | מכוסה אצלנו | פער |
|-----------|--------|--------------|------|
| **Part 1 · Patterns** | Chaining, Routing, Parallelization, Reflection, Tool Use, Planning, Multi-Agent | ✅ § 9.1 — כל 7 הפרקים ממופים ל-patterns 1–9 שלנו | — |
| **Part 2 · תשתית** | Memory Management, Learning, **MCP**, Goal Setting | 🟡 מודול 5 (חלקי) · MCP ב-`DEV_ENV § 10` · מודול 1 | **Memory tiers** — מאשרר את `MEMORY.md` כ-priority |
| **Part 3 · עמידות** | Exception Handling & Recovery, **Human-in-the-Loop**, RAG | 🟡 human gates (§ 4) · vector memory (מודול 5) | **Exception/Recovery doctrine** — אין לנו. נכנס ל-roadmap |
| **Part 4 · מתקדם** | **A2A (Inter-Agent)**, Resource-Aware Optimization, Reasoning, **Guardrails**, **Evaluation & Monitoring**, Prioritization | ✅ Guardrails (§ 6) · Evals (§ 5) · cost (מודול 3) | **A2A protocol** — רלוונטי ל-Stage-B (תקשורת מנהל⇄עובדים) |

**3 תוספות ל-roadmap (§ 7) מהספר:**

1. **Exception Handling & Recovery** — מה agent עושה כשהוא נכשל באמצע (לא רק safe-stop — recovery).
2. **A2A (Agent-to-Agent)** — פרוטוקול התקשורת בין מנהל לעובדים ב-Stage-B. הספר נותן את הסטנדרט.
3. **Resource-Aware Optimization** — בחירת מודל דינמית לפי משימה (היום זה סטטי במודול 3).

**אימות עצמי:** מתוך 21 פרקי הספר — 16 כבר ממופים למודול או pattern קיים אצלנו.
ה-blueprint לא המציא כלום; הוא תמצת נכון.

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

## 11. MCP vs. Agent Skills — Connect ⇄ Learn

מודול 4 (`§ 1`) קורא ל-tools "MCP, API, DB, functions" — ולאורך הקובץ אנחנו קוראים
ל-`/deal-quote` ולחבריו "Skills". אלה **שתי שכבות שונות**, וקל לבלבל ביניהן. ההבחנה
הזו (מקור: אינפוגרפיקה *MCP vs. Agent Skills*, ByteByteGo) היא הציר שמסדר את כל מודול 4.

> **השאלה הלא-נכונה:** "MCP או Skills?" — הן לא מתחרות.
> **השאלה הנכונה:** *איך ה-agent יתחבר למערכות?* (MCP) · *איך ה-agent ילמד workflows?* (Skills)

**שני מודלים מנטליים:**
- 👉 **MCP = AI-native APIs** — מערכת העצבים. מלמד agent **איך לתקשר עם מערכות**.
- 👉 **Skills = AI-native SOPs** — ספר הנהלים. מלמד agent **איך לבצע משימה** באופן עקבי.

### 11.1 חמשת הממדים — ומיפוי ל-ULease

| # | ממד | 🟢 MCP | 🔵 Agent Skills | העוגן אצלנו |
|---|------|---------|------------------|--------------|
| 1 | **Integration** | client ⇄ server; N agents × M backends; חיבור תמידי | `SKILL.md` (name + description) **always loaded** → הוראות מלאות on-trigger | MCP: `DEV_ENV § 10` · `N8N § 8` / Skills: `COMMAND_API` |
| 2 | **Architecture** | תהליך נפרד, runtime משלו (JSON-RPC) | תיקייה: `SKILL.md` + `scripts/` + `references/` + `assets/` | `mcp-ulease` (Stage-C) / הגדרת Skill ב-`COMMAND_API` |
| 3 | **Invocation** | params → schema validation → tool A → tool B (chained) | agent מריץ `bash`/`python`/`curl` מתוך `SKILL.md` → output | tool schemas / `§ 9.1` Chaining |
| 4 | **Runtime** | MCP server בתוך container | רץ ב-env של ה-agent (bash · python · curl/node) | `docker-compose` (n8n/api) / סביבת Claude Code |
| 5 | **Where it fits** | DB · Queue · OAuth · SaaS (Slack · GitHub · Postgres · Stripe) — high-frequency, low-latency | know-how · conventions · CLI recipes · templates — lightweight, **no infra** | backends של `leasing-api` / מודולי הידע של ה-OS |

### 11.2 הבהרת מינוח — "Skill" בריפו הזה

`§ 0` אמר *"Skill הוא prompt, לא agent"*. זה היה מדויק לרזולוציה הישנה. ב-Anthropic
**Agent Skill** הוא יותר מ-prompt: תיקייה עם `SKILL.md` + scripts + references + assets —
SOP ארוז. ההבחנה המעודכנת:

| השכבה | מה זה | אצלנו |
|--------|--------|--------|
| **slash command** | טריגר/קיצור | תחביר `/command` ב-`COMMAND_API` |
| **Agent Skill** | ה-SOP הארוז (`SKILL.md` + scripts/references/assets) | התוכן וההוראות מאחורי הפקודה |
| **MCP tool** | חיבור למערכת חיצונית | `DEV_ENV § 10` · `N8N § 8` |
| **Agent** | מרכיב את כולם דרך מודול 6 | `stage-a/` |

### 11.3 הדוקטרינה — Use Both

MCP ו-Skills **משלימים**, לא מתחרים. ה-agent הכי חזק משתמש בשניהם:

```
Agent = Skill (איך מבצעים את המשימה — SOP) ⊕ MCP (איך מגיעים למערכות — tools) ⊕ Orchestration (§6)
```

זה בדיוק build order של `§ 4`: **מודול 4 = MCP** (חיבור ל-pricing-quote/deal-lookup),
ואילו ה-Skill עצמו (`/deal-quote`) הוא ה-**SOP** שאומר *מתי* ובאיזה סדר לקרוא להם. הסר
אחד מהם וה-agent שבור: MCP בלי Skill = ידיים בלי ספר-נהלים; Skill בלי MCP = נהלים
בלי ידיים.

> **כלל ברזל:** לפני שמוסיפים MCP server חדש, שאל *"זו בעיית חיבור או בעיית workflow?"*.
> בעיית חיבור (DB/SaaS/queue) → MCP. בעיית ידע-תהליכי (איך מפיקים דוח, באיזה פורמט,
> לפי איזה policy) → Skill. הוספת MCP לבעיית-workflow היא over-engineering; הוספת Skill
> לבעיית-חיבור היא reinvention. ראה כלל הבחירה המלא ב-`N8N § 11`.

### 11.4 חיבור ל-§ 9.6 (הקנון)

הספר *Agentic Design Patterns* (Gulli) מקדיש פרק נפרד ל-**MCP** ב-Part 2 (תשתית) —
שם, ולא ב-Part 1 (Patterns). זה מאשר את ההבחנה: MCP הוא **שכבת תשתית/חיבור**, בעוד
ה-patterns (chaining, routing…) הם שכבת ה-**workflow/Skill**. אותה הפרדה, מקור אחר.

---

## 12. אימות חיצוני — "How to Actually Build an AI Agent" (7-step framework)

עוד אינפוגרפיקה מהשדה (*"From goal setting, choosing models to testing"*), באותו תפקיד
כמו Gartner (§ 6.1), Gulli (§ 9.6) ו-Karpathy (§ 10): מקור חיצוני שמאמת את התזה. שורת
המחץ שלה היא **בדיוק** הדוקטרינה של הקובץ:

> *"The best AI agents aren't the smartest — they're the best engineered."*

7 הצעדים שלה הם וריאציה דקה יותר על 8 המודולים שלנו (§ 1). המיפוי מאשר שלא המצאנו —
תמצתנו נכון; ושלושה פריטים בה **מחדדים** החלטות שאצלנו היו מרומזות.

### 12.1 מיפוי 7 הצעדים ⇄ 8 המודולים

| # | הצעד באינפוגרפיקה | המודול אצלנו (§ 1) | מצב |
|---|---------------------|----------------------|------|
| 1 | **Start with a Goal** (outcome, metrics, constraints) | 1 · Purpose & Scope + 8 · Evals (metrics) | ✅ § 4 build order + § 5 |
| 2 | **Pick the Right Model** (LRM/LLM/SLM) | 3 · Choose LLM | 🟡 קיים, אבל בינארי opus/sonnet/haiku — ראה § 12.2(a) |
| 3 | **Choose the Right Framework** (n8n/Smol ↔ LangChain/CrewAI/LlamaIndex/ADK/OpenAI SDK) | — *(אין מודול)* | ⚠️ החלטה מרומזת — ראה § 12.2(b) |
| 4 | **Connect Tools** (REST/GraphQL/MCP, function calling, vector DB) | 4 · Tools & Integrations | ✅ `DEV_ENV § 10` · ההבחנה MCP⇄Skill ב-§ 11 |
| 5 | **Manage Memory** (short / episodic / long-term) | 5 · Memory Systems | 🟡 `stage-a` append-only — ראה § 12.2(c) |
| 6 | **Test & Evaluate** (accuracy, latency, cost, edge cases, red-team) | 8 · Testing & Evals | ✅ § 5 — 5 המטריקות |
| 7 | **Deploy, Monitor & Improve** (guardrails, rate limits, iterate) | 6 · Orchestration + 8 · Evals + governance | ✅ § 6 + § 5 הטקס השבועי + `LAUNCH.md` |

**6 מתוך 7 צעדים כבר מכוסים.** הצעד היחיד בלי בית אצלנו הוא **#3 (Framework)** — וזו לא
השמטה, זו החלטה שלא תיעדנו (§ 12.2b).

### 12.2 מה האינפוגרפיקה מחדדת — שלושה deltas אמיתיים

**(a) טקסונומיית המודלים LRM / LLM / SLM** — מודול 3 שלנו מדבר opus/sonnet/haiku. האינפוגרפיקה
נותנת את ה-**קטגוריה** מעל ה-מותג:

| קטגוריה | מתי | אצלנו |
|---------|-----|--------|
| **LRM** (Large Reasoning) | reasoning מורכב, planning, multi-step | Opus + extended thinking — `/board-deck`, manager planning |
| **LLM** (General) | משימות כלליות, יחס token סביר | Sonnet — רוב ה-Skills, worker execution |
| **SLM** (Small) | latency נמוך, routing, classification, edge | Haiku — triage, `/fleet-report` ETL, classifiers |

זה **מחזק את פריט ה-roadmap "Resource-Aware routing"** (§ 7): המעבר מ-מודל סטטי לבחירה
דינמית הוא מעבר מ-"בחר מותג" ל-"בחר קטגוריה לפי דרישת המשימה".

**(b) בחירת Framework — ההחלטה שלא תיעדנו.** האינפוגרפיקה מפרידה *Simple Workflows*
(n8n, Smol) מ-*Production-Grade* (LangChain, CrewAI, LlamaIndex, Google ADK, OpenAI Agent SDK).
אצלנו ההחלטה כבר נפלה אבל מעולם לא נכתבה כ-decision:

> **ULease = build, not buy.** `stage-a/` הוא runtime מותאם על ה-Anthropic stack
> (Claude Agent SDK), לא framework חיצוני. n8n משמש כ-Glue Layer בלבד (`N8N § 11`),
> לא כ-agent runtime. LangChain/CrewAI **לא** אומצו — בכוונה: שליטה מלאה ב-governance
> שנאכף בקוד (§ 6) שווה יותר מ-time-to-market של framework.

זו לא המלצה להחליף — זו הפיכת החלטה מרומזת למפורשת, כפי שהדוקטרינה דורשת (Working
Rule: *NO LAZINESS — תעד חוב/החלטה, אל תסתיר*).

**(c) שלוש שכבות זיכרון ⇄ ארבע ה-tiers שלנו.** האינפוגרפיקה: short-term (context window) /
episodic (session) / long-term (vector DB). ה-roadmap שלנו (§ 7, `MEMORY.md`) מדבר על 4
tiers. הפיוס:

| אינפוגרפיקה | ה-tier שלנו | מימוש |
|--------------|--------------|--------|
| Short-term (context) | working | context window הנוכחי של ה-run |
| Episodic (session) | episodic | `stage-a/shared-memory.js` (append-only) |
| Long-term (persistent) | vector + SQL | RAG (vector) + state עסקי (SQL/Supabase) |

האינפוגרפיקה מאחדת vector+SQL ל-"long-term" אחד; אנחנו מפצלים כי ב-ULease יש הבחנה
תפעולית (policy docs ב-vector ≠ ledger ב-SQL). **המודל שלנו עשיר יותר, לא סותר.**

### 12.3 חמשת עקרונות ההצלחה ⇄ הדוקטרינה

| Key Principle (אינפוגרפיקה) | איפה זה אצלנו |
|------------------------------|----------------|
| Start simple, iterate fast | § 9.5 *"אם Skill מספיק, אל תבנה agent"* + Karpathy *Keep It Simple* (§ 10.1) |
| Balance quality / latency / cost | § 5 (3 מתוך 5 המטריקות) + טקסונומיית המודלים (§ 12.2a) |
| Security, privacy & safety non-negotiable | § 6 governance-in-code + § 6.1 Gartner |
| Modular design scales | 8-module blueprint (§ 1) + § 9 patterns |
| Measure everything, improve continuously | § 5 Evals + הטקס השבועי (§ 10.5 *Atrophy*) |

5/5 העקרונות כבר מקודדים בדוקטרינה. אין כאן עיקרון חדש — יש אישור.

### 12.4 שורה תחתונה

האינפוגרפיקה לא משנה את ה-blueprint — היא מאמתת אותו (6/7 צעדים מכוסים, 5/5 עקרונות
מקודדים) ותורמת **שלושה חידודים**: טקסונומיית LRM/LLM/SLM (מחזקת Resource-Aware ב-§ 7),
תיעוד מפורש של החלטת build-not-buy (§ 12.2b), ופיוס מודל הזיכרון 3⇄4 tiers. כמו Gartner
ו-Gulli — *system-first עומד בביקורת חיצונית, סעיף-סעיף.*

---

## גרסאות

| גרסה | תאריך | שינוי |
|------|--------|-------|
| 1.0.0 | 2026-05-31 | Initial — 8-module doctrine, coverage map, stage-a bridge, evals layer |
| 1.1.0 | 2026-05-31 | + § 9 Orchestration Patterns — 9 patterns, ULease Skills map, stage-a קלסיפיקציה (Plan & Execute), Stage-B חדד (= P&E + Replan) |
| 1.2.0 | 2026-06-03 | + § 10 Coding Workflow Doctrine — עקרונות ה-CLAUDE.md של Karpathy: 6 עקרונות workflow, מיפוי ל-§ 1/§ 5/§ 9, Working Rules block לשני הריפואים, mindset |
| 1.3.0 | 2026-06-03 | + § 6.1 חיזוק Gartner (5 misconceptions ⇄ הדוקטרינה) · + § 9.6 מיפוי הקנון *Agentic Design Patterns* (Gulli) · 3 פריטי roadmap חדשים (A2A · Exception&Recovery · Resource-Aware) |
| 1.4.0 | 2026-06-05 | + § 11 MCP vs. Agent Skills — Connect⇄Learn: 5 ממדים ממופים ל-ULease, הבהרת מינוח (slash command / Agent Skill / MCP tool / Agent), דוקטרינת Use-Both, וחיבור ל-§ 9.6 |
| 1.5.0 | 2026-06-07 | + § 12 אימות חיצוני — "How to Actually Build an AI Agent" (7-step framework): מיפוי 7 הצעדים ⇄ 8 המודולים, 3 חידודים (טקסונומיית LRM/LLM/SLM · תיעוד build-not-buy · פיוס זיכרון 3⇄4 tiers), 5 עקרונות ההצלחה ⇄ הדוקטרינה |

---

**Tie-back ל-OS:** הקובץ הזה הוא ה-**connective tissue**. `COMMAND_API` נותן את הפקודות,
`DEV_ENVIRONMENTS` את הכלים, `LAUNCH` את ה-go-live — ו-`AGENT_BLUEPRINT` מסביר איך
מרכיבים מהם **agent** שלא נשבר ב-production. § 9 בוחר את ה-topology, § 10 קובע איך
כל agent בתוכה כותב קוד, § 11 מפריד בין ה-**חיבור** (MCP) ל-**ידע התהליכי** (Skill),
ו-§ 12 מאמת את הדוקטרינה מול ה-7-step framework החיצוני. הוא מצביע קדימה ל-`MEMORY.md`
ול-Stage-B כצעדים הבאים.
*Start with the SYSTEM first. Everything else scales from there.*
