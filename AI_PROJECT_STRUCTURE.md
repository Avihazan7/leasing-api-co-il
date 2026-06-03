# מבנה פרויקט AI — ארבע תיקיות, אפס בלגן

**Module:** `AI_PROJECT_STRUCTURE.md`
**Version:** 1.1.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — Knowledge layer (§3 שורה 19). תקן הנדסי לריפו הפלטפורמה של ULease.
**Source:** מבוסס על *"The 4-folder structure I use for every AI project"* (Brij Kishore Pandey) + אינפוגרפיקת *"Enterprise GenAI Project Folder Structure"*.
**Integrates with:** `CASES/ULEASE_SPEC.md`, `CASES/ULEASE_TECH_ONBOARDING.md`, `AI_RAG_DESIGN.md`, `AI_SYSTEM_DESIGN.md`, `AI_CLAUDE_STACK_2026.md`, `CASES/ULEASE_HIRING.md`

> רוב פרויקטי ה-AI לא נכשלים בגלל המודל — הם נכשלים כי אף אחד לא תכנן את המערכת **סביב** המודל. ארבע תיקיות — `prompts/` · `data/` · `agents/` · `evals/` — הופכות מערכת AI מ"אוסף סקריפטים" ל**מוצר ניתן לתחזוקה** (§1), ומבנה ה-Enterprise (§3) הוא היעד שאליו הריפו גדל כשהפלטפורמה מבשילה. זה התקן שריפו הפלטפורמה של ULease יקום עליו ביום הראשון של ה-Tech Lead — וגדל איתו עד V2.

---

## 1. המבנה

```
ai-project/
├── prompts/    ← כל פרומפט כקובץ אמיתי
│   ├── system/      הוראות מערכת
│   ├── tasks/       פרומפטים למשימות ספציפיות
│   └── tools/       הסברי כלים
├── data/       ← הקלטים שה-AI קורא
│   ├── raw/         דאטה גולמית
│   └── processed/   דאטה מעובדת
├── agents/     ← קונפיגורציות סוכנים, skills, כלים
│   ├── skills/
│   └── tools/
└── evals/      ← ההוכחה שה-AI באמת עובד
    ├── tests/       מקרי בדיקה ותשובות צפויות
    ├── traces/      תיעוד ריצות וכשלים
    └── scorecards/  דיוק, עלויות, ביצועים לאורך זמן
```

**כללי המפתח:** תיקייה אחת = מטרה אחת · קובץ אחד = אחריות אחת · הכל ב-version control · עובד חדש מבין את הפרויקט תוך דקות.

---

## 2. למה כל תיקייה קריטית

| תיקייה | העיקרון | למה זה משנה |
|---------|----------|---------------|
| **prompts/** | פרומפטים הם קוד — לא מחרוזות חבויות בתוך notebooks | הפרומפטים הם מהנכסים היקרים במערכת; כשהם נשברים צריך לעקוב, לסקור ולשפר אותם כמו קוד |
| **data/** | הפרדת raw/processed + דאטה של בדיקות ו-RAG | כשתוצאה נכשלת, חייבים לדעת מה השתנה: המודל, הפרומפט או הדאטה |
| **agents/** | סוכן = רכיב תוכנה אמיתי, לא סקריפט | לסוכנים מודרניים יש לוגיקה, workflows והגדרות משלהם — חייבים להיות ניתנים לסקירה |
| **evals/** | בלי הערכה יש רק דמו; עם הערכה יש מוצר | מדידת ביצועים, עלויות וכשלים לאורך זמן — הביטחון לפני deploy |

---

## 3. מבנה ה-Enterprise — היעד כשהפלטפורמה גדלה

ארבע התיקיות הן נקודת הפתיחה. כשהמערכת הופכת לפלטפורמה רב-סוכנית עם API חיצוני — כמו ULease — המבנה גדל לתקן ה-Enterprise:

```
enterprise-agent-platform/
├── README.md            ← סקירת הפרויקט, הוראות הקמה, תקציר ארכיטקטורה, onboarding
├── CLAUDE.md            ← הקשר לעוזר ה-AI: קונבנציות, חוקי ארכיטקטורה, הנחיות פיתוח
├── .env.example         ← תבנית משתני הסביבה הנדרשים — בלי לחשוף סודות
│
├── agents/              ← כל הסוכנים: תזמור + worker agents מתמחים
│   ├── orchestrator/        מתכנן מרכזי: פירוק משימות, ניתוב, תיאום בין סוכנים
│   │   ├── agent.py
│   │   └── policies.yaml
│   └── specialists/         סוכני domain ממוקדים
│       ├── retrieval_agent/
│       ├── code_agent/
│       └── compliance_agent/
│
├── tools/               ← רישום ומימוש כלים: APIs חיצוניים, מסדי נתונים, MCP servers
│   ├── registry.py
│   ├── definitions/
│   └── mcp_servers/
│
├── orchestration/       ← workflows, גרפי ביצוע, לוגיקת ניתוב ו-state משותף
│   ├── graph.py
│   ├── state.py
│   └── router.py
│
├── prompts/             ← ניהול מרכזי של פרומפטים, תבניות וקונפיגורציות
│   ├── library/
│   └── registry.yaml
│
├── api/                 ← שכבת service: חשיפת יכולות הסוכנים ב-REST/streaming מאובטח
│   ├── routes/
│   ├── schemas/
│   ├── auth/
│   └── middleware/
│
├── governance/          ← בטיחות, ציות, auditing ומנגנוני guardrails
│   ├── policies/
│   ├── guardrails/
│   └── audit/
│
├── evals/               ← מסגרת הערכה: ביצועים, בטיחות, דיוק, רגרסיות
│   ├── datasets/
│   ├── suites/
│   └── reports/
│
├── tests/               ← בדיקות unit ו-integration לאמינות רכיבי הפלטפורמה
│   ├── unit/
│   └── integration/
│
└── docs/                ← תיעוד ארכיטקטורה, החלטות עיצוב, הפניות טכניות
    └── architecture/
```

> **ההבדל המהותי:** אפליקציית GenAI אינה LLM עטוף בצ'אטבוט — היא **אקוסיסטם** של סוכנים, כלים, workflows, governance והערכה שעובדים יחד. מי שינצח עם AI הם לא בעלי המודלים הגדולים ביותר, אלא בעלי **הארכיטקטורה** הטובה ביותר. (זה בדיוק נרטיב הפיץ' של ULease: אנחנו לא בונים מודל — אנחנו בונים ארכיטקטורה.)

### 3.1 עשר השכבות ומה כל אחת פותרת

| שכבה | תפקיד | בלעדיה |
|-------|--------|---------|
| **Orchestrator** | פירוק משימות, ניתוב ותיאום ביצוע | כל סוכן ממציא את ה-workflow של עצמו |
| **Specialist Agents** | retrieval, קוד, ציות, אנליזה — עבודה ממוקדת-domain | סוכן-על אחד שעושה הכל בינוני |
| **Tools Layer** | חיבור APIs, מסדי נתונים, MCP servers ומערכות חיצוניות | כל סוכן מחזיק עותק פרטי של אותו חיבור |
| **Orchestration Layer** | ניהול workflows, ניתוב ו-state משותף | ה-flow חבוי בתוך קוד הסוכנים — בלתי ניתן לדיבוג |
| **Prompt Library** | ריכוז פרומפטים ותבניות לשימוש חוזר | פרומפטים מפוזרים כמחרוזות בקוד |
| **Governance Layer** | אבטחה, ציות, guardrails ו-auditing | אין שום דבר שעוצר סוכן לפני נזק |
| **Evaluation Framework** | מדידה רציפה: דיוק, בטיחות, ביצועים, רגרסיות | יש דמו, אין מוצר |
| **API Layer** | חשיפת יכולות למוצרים, צוותים ושותפים | המערכת כלואה בתוך עצמה |
| **Testing Infrastructure** | אימות אמינות לפני production | כל deploy הוא הימור |
| **Documentation** | מהנדס חדש מבין את המערכת מהר | הידע חי רק בראש של מי שבנה |

### 3.2 מפת הצמיחה — מ-4 תיקיות ל-Enterprise

שום דבר לא נזרק במעבר. כל תיקיית MVP גדלה לתוך מקבילתה:

| MVP (יום 1) | Enterprise (Phase 1+) | מה קורה במעבר |
|--------------|----------------------|----------------|
| `prompts/` | `prompts/library/` + `registry.yaml` | כל פרומפט מקבל רישום: גילוי, גרסה, בעלים |
| `agents/` | `agents/orchestrator/` + `agents/specialists/` | ההפרדה תזמור↔התמחות הופכת להפרדת תיקיות |
| `agents/tools/` | `tools/` עצמאית (registry · definitions · mcp_servers) | הכלים מפסיקים להיות "של סוכן" — הם שכבה משותפת |
| `data/` | `data/` + צינור ה-RAG | raw/processed מזין את הקורפוס (pgvector) |
| `evals/` | `evals/` + `governance/` + `tests/` | ההערכה (מדידה) נפרדת מהאכיפה (guardrails) ומבדיקות הקוד |
| — | `orchestration/` | ה-workflow יוצא מקוד הסוכנים לשכבה משלו: graph · state · router |
| — | `api/` | הפלטפורמה נחשפת החוצה — ספקים, מפיצים, שותפים |
| — | `docs/` + `README.md` + `CLAUDE.md` + `.env.example` | onboarding: מהנדס חדש (או Claude) מבין את המערכת תוך דקות |

**שער המעבר (נגד over-engineering):** מתחילים ב-4 תיקיות. תיקיית Enterprise נפתחת רק כשהתוכן שלה קיים — לא לפני:

1. סוכן production **שני** עולה לאוויר (Ultra + Master ראשון) → נפתחות `agents/orchestrator|specialists/` ו-`orchestration/`
2. ה-API נפתח לצרכן **חיצוני** (ספק/מפיץ) → נפתחת `api/`
3. ה-**Guardian** עולה לאוויר → נפתחת `governance/`

(אותו עיקרון כמו מפת הרכיבים MVP/V1/V2 ב-`AI_SYSTEM_DESIGN.md` §4.5 — הארכיטקטורה ידועה מראש, הביצוע מדורג.)

---

## 4. המיפוי לריפו הפלטפורמה של ULease 🎯

זו ההנחיה ל-Tech Lead (יום 1 — `CASES/ULEASE_TECH_ONBOARDING.md`): ריפו `ulease-platform` נפתח עם השלד הזה, וכל רכיב מהאיפיון כבר יודע לאן הוא שייך:

| תיקייה | מה נכנס בה ב-ULease | מקור באיפיון |
|---------|----------------------|---------------|
| **prompts/system/** | פרומפטי הליבה של Ultra · Master · Max · Guardian | `ULEASE_SPEC.md` §7 |
| **prompts/tasks/** | ניקוד לידים (Haiku) · פרסונליזציה (Sonnet) · ניסוח הצעות | `ULEASE_OUTBOUND_ENGINE.md` |
| **prompts/tools/** | הסברי כלים לסוכני Max (e-sign, חיוב, הגשת מימון) | `ULEASE_SPEC.md` §7 |
| **data/raw/** | מלאי ספקים (API/CSV), מחירונים, נתוני משרד התחבורה | `ULEASE_SPEC.md` §9 |
| **data/processed/** | קורפוס ה-RAG אחרי chunking + embedding (pgvector) | `ULEASE_SPEC.md` §7.1 |
| **agents/skills/** | התמחויות ה-Masters: Match, Pricing, Negotiation, Compliance | `ULEASE_SPEC.md` §7 |
| **agents/tools/** | הגדרות MCP, חיבורי API (סולק, e-sign, מימון) | `ULEASE_SPEC.md` §9 |
| **evals/tests/** | ה-Golden Set — 50 תרחישים עם תשובות ידועות | `ULEASE_SPEC.md` §7.2 (D-023) |
| **evals/traces/** | AgentRun + AuditLog — כל ריצת סוכן מתועדת | `ULEASE_SPEC.md` §8 |
| **evals/scorecards/** | grounding ≥100% כספי · הזיות <1% · latency · עלות לשאילתה | `ULEASE_SPEC.md` §7.2 |

> **הנקודה:** האיפיון כבר הגדיר את *כל* התוכן של ארבע התיקיות. ה-Tech Lead לא מתחיל מדף ריק — הוא מתחיל ממבנה + תוכן ממופה.

### 4.1 מיפוי ה-Enterprise — האיפיון כבר ממלא את כל עשר התיקיות

ULease *היא* enterprise-agent-platform בהגדרה — Ultra·Master·Max הם בדיוק orchestrator + specialists. כשהריפו עובר את שער המעבר (§3.2), זה המיפוי:

| תיקיית Enterprise | מה נכנס בה ב-ULease | מקור |
|--------------------|----------------------|------|
| `agents/orchestrator/` | **Ultra** — פירוק עסקה, ניתוב, תיאום Masters (`policies.yaml` = חוקי הסלמה ו-HITL) | `ULEASE_SPEC.md` §7 |
| `agents/specialists/` | **Masters**: Match · Pricing · Negotiation · Compliance + סוכני **Max** (ביצוע) | `ULEASE_SPEC.md` §7 |
| `tools/registry.py` + `definitions/` | רישום הכלים: בדיקת מלאי, חישוב PMT, Deal Score | `ULEASE_SPEC.md` §9 |
| `tools/mcp_servers/` | חיבורי MCP: סולק, e-sign, הגשת מימון, נתוני משרד התחבורה | `ULEASE_SPEC.md` §9 |
| `orchestration/` (graph · state · router) | זרימת העסקה: ליד → התאמה → מו"מ → חתימה → מסירה + Event/AgentRun | `ULEASE_SPEC.md` §6 · §8 |
| `prompts/library/` + `registry.yaml` | פרומפטי Ultra · Masters · Max · Guardian — רשומים, מגורסים, ניתנים לגילוי | `ULEASE_SPEC.md` §7 |
| `api/` (routes · schemas · auth · middleware) | ה-API של הפלטפורמה: Gateway, JWT ספקים, webhooks מלאי, RLS | `AI_SYSTEM_DESIGN.md` |
| `governance/` (policies · guardrails · audit) | **Guardian כ-Hooks דטרמיניסטיים** (D-037) + Guardrails & Evals + AuditLog | `ULEASE_SPEC.md` §7.2 |
| `evals/` (datasets · suites · reports) | Golden Set (50 תרחישים) · eval suite חוסם-deploy · scorecards | `ULEASE_SPEC.md` §7.2 (D-023) |
| `tests/` (unit · integration) | בדיקות הקוד — נפרדות מ-evals של הסוכנים; CI על כל PR | D-023 |
| `docs/architecture/` | האיפיון, החלטות עיצוב (ADRs), הפניות טכניות | `ULEASE_SPEC.md` |
| `README.md` · `CLAUDE.md` · `.env.example` | onboarding ל-Tech Lead · הקשר ל-Claude Code · מפתחות (סולק, e-sign, מימון) | `ULEASE_TECH_ONBOARDING.md` |

> **הנקודה:** האיפיון של ULease מגדיר תוכן לכל אחת מעשר התיקיות — כולל אלה שנפתחות רק ב-V1/V2. ה-Tech Lead מקבל את מסלול הצמיחה של הריפו מראש, מיום 1 ועד V2, בלי לזרוק כלום בדרך.

---

## 5. וגם הריפו הזה (Claude OS) כבר בנוי כך

| עיקרון | המימוש ב-OS |
|---------|--------------|
| prompts/ — פרומפטים כקבצים | `COMMAND_API.md` (89 חוזים) · `COMMAND_API_TASKS.md` (98 מתכונים) · `.claude/skills/` |
| data/ — קלטים ניתנים לשחזור | `CASES/*.csv` + הגנרטורים (`ULEASE_FORECAST.py` …) |
| agents/ — סוכנים כרכיבים | `.claude/agents/os-auditor.md` |
| evals/ — הוכחה שזה עובד | `scripts/os_consistency_check.py` + CI על כל PR (D-023) |
| ורכיבי ה-Enterprise (§3) | `CLAUDE.md` (פשוטו כמשמעו) · governance = os-auditor + CI · docs = המודולים עצמם · tools = חיבורי MCP (Calendar · Gmail · Drive · GitHub) |

> מי שפותח את הריפו מבין אותו מיד = מערכת. מי שלא מוצא כלום = חוב טכני. הריפו הזה עבר את המבחן.

---

## 6. צ'קליסט קבלה ל-Tech Lead

- [ ] ריפו `ulease-platform` נפתח עם ארבע התיקיות מיום 1
- [ ] `README.md` + `CLAUDE.md` + `.env.example` קיימים מיום 1 — ה-onboarding של המהנדס הבא (או של Claude)
- [ ] אף פרומפט לא חי בתוך קוד — הכל קבצים ב-`prompts/`
- [ ] כל מקור דאטה (ספק/מחירון) נכנס דרך `data/raw/` → pipeline → `data/processed/`
- [ ] ה-Golden Set (50 תרחישים, §7.2) יושב ב-`evals/tests/` לפני שהסוכן הראשון עולה
- [ ] כל ריצת סוכן כותבת trace — בלי יוצאים מהכלל
- [ ] scorecard עלות-לשאילתה מחובר ל-unit economics (CPL ₪103)
- [ ] המעבר ל-Enterprise נעשה לפי שער המעבר (§3.2) — לא נפתחות תיקיות ריקות מראש
- [ ] `governance/` נפתחת יחד עם ה-Guardian — לא אחריו

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | תקן 4 התיקיות (prompts·data·agents·evals) + מיפוי מלא לרכיבי האיפיון של ULease + צ'קליסט קבלה ל-Tech Lead | 2026-06-02 |
| 1.1.0 | מבנה ה-Enterprise (D-046): עץ 10 התיקיות + עשר השכבות (§3), מפת הצמיחה MVP→Enterprise עם שער מעבר נגד over-engineering (§3.2), מיפוי Enterprise מלא ל-ULease — Ultra=orchestrator · Masters=specialists · Guardian=governance (§4.1), והרחבת צ'קליסט ה-Tech Lead | 2026-06-03 |

**Attribution.** המבנה מבוסס על *The 4-folder structure I use for every AI project* (Brij Kishore Pandey) ועל אינפוגרפיקת *Enterprise GenAI Project Folder Structure*. העיבוד והמיפוי ל-ULease — חלק מה-Claude OS של Avraham Bar Yochai Chazan.

**Confidentiality.** קובץ זה הוא חלק מה-Claude Operating System האישי של Avraham Bar Yochai Chazan.

— *End of AI_PROJECT_STRUCTURE.md v1.1.0 —*
