# AGENT_BLUEPRINT.md — מ-Skill ל-Agent: דוקטרינת ה-System-First

**Module:** `AGENT_BLUEPRINT.md`
**Version:** 1.0.0
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

## גרסאות

| גרסה | תאריך | שינוי |
|------|--------|-------|
| 1.0.0 | 2026-05-31 | Initial — 8-module doctrine, coverage map, stage-a bridge, evals layer |

---

**Tie-back ל-OS:** הקובץ הזה הוא ה-**connective tissue**. `COMMAND_API` נותן את הפקודות,
`DEV_ENVIRONMENTS` את הכלים, `LAUNCH` את ה-go-live — ו-`AGENT_BLUEPRINT` מסביר איך
מרכיבים מהם **agent** שלא נשבר ב-production. הוא מצביע קדימה ל-`MEMORY.md` ול-Stage-B
כצעדים הבאים. *Start with the SYSTEM first. Everything else scales from there.*
