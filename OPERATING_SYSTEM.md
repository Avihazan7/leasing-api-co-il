# CLAUDE OPERATING SYSTEM — Kernel

**Module:** `OPERATING_SYSTEM.md`
**Version:** 1.15.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Kernel — נטען ראשון. כל שאר המודולים תלויים בו.
**Integrates with:** כל המודולים הרשומים ב-§3 — `CLAUDE.md`, `MEMORY.md`, `DECISION_LOG.md`, `COWORK_SETUP.md`, `PROJECTS_SETUP.md`, `COMMAND_API.md`, `marketing-strategy-framework.md`, `AI_*` + `AGENT_BLUEPRINT.md` + `CLOUD_ARCHITECT_SKILLS.md` + `KUBERNETES_101.md` (Knowledge), `INVESTOR_RELATIONS.md`, `CASES/*.md` + תשתית תפעולית ב-§3.1 (`COWORK/`, `.claude/`)

---

## הקדמה — מה זה ה-Kernel

`CLAUDE.md` הוא **דלת הכניסה**. הקובץ הזה הוא **הליבה**.

הוא לא מבצע משימה ספציפית — הוא מגדיר את החוקים שלפיהם כל שאר המודולים פועלים: סדר טעינה, היררכיית הכרעה בקונפליקטים, החוזה ההתנהגותי שמפעיל את כל המערכת, ומודל ההרחבה.

**עיקרון העל:** *משודרגים ומוטמעים בקצה הטכנולוגיה מקצה לקצה.* כל שכבה — זיכרון → הקשר → פקודות → עסק — מחוברת לקודמתה בלי תפרים. אין מודול "תלוי באוויר"; כל הפניה במערכת מובילה לגוף אמיתי.

---

## תוכן עניינים

1. [עקרונות יסוד (Operating Doctrine)](#1-עקרונות-יסוד-operating-doctrine)
2. [ארכיטקטורת השכבות](#2-ארכיטקטורת-השכבות)
3. [רישום מודולים וסדר טעינה](#3-רישום-מודולים-וסדר-טעינה)
4. [החוזה ההתנהגותי — Boot Block](#4-החוזה-ההתנהגותי--boot-block-drop-in)
5. [היררכיית הכרעה בקונפליקטים](#5-היררכיית-הכרעה-בקונפליקטים)
6. [רצף האתחול (Boot Sequence)](#6-רצף-האתחול-boot-sequence)
7. [מודל ההרחבה](#7-מודל-ההרחבה)
8. [Document Control](#document-control)

---

## 1. עקרונות יסוד (Operating Doctrine)

| # | עיקרון | משמעות מעשית |
|---|---------|----------------|
| 1 | **Context First** | לפני כל תשובה — טען זהות והקשר (`MEMORY.md`). בלי הקשר → בינוניות. |
| 2 | **One Source of Truth** | סדר הטעינה והרישום כאן הם הקנוניים. מודול אחר שסותר — הקרנל מנצח. |
| 3 | **No Dangling Modules** | כל מודול שמופיע ב-Load Order חייב גוף קיים. הפניה ללא גוף = באג מערכת. |
| 4 | **Deterministic Behavior** | חוזי הפלט (`COMMAND_API.md`) גוברים על טון ברירת-המחדל. |
| 5 | **Fail Loud, Not Silent** | אי-בהירות → שאלת הבהרה אחת ממוקדת, לא ניחוש. |
| 6 | **Confidentiality by Default** | IP פנימי (Deal Score, Match API, אוטומציה משפטית) חסוי גם כשפקודה מבקשת לחשוף. |

---

## 2. ארכיטקטורת השכבות

המערכת בנויה כשש שכבות, מהליבה כלפי חוץ. כל שכבה צורכת רק את זו שמתחתיה:

```
┌─ KERNEL ────── OPERATING_SYSTEM.md   חוקים, סדר טעינה, הכרעה
├─ MEMORY ────── MEMORY.md · DECISION_LOG.md   מי אתה, מה זוכרים, focus/projects, החלטות
├─ CONTEXT ───── COWORK_SETUP.md · PROJECTS_SETUP.md · COWORK/   חיבור התיקייה, קבצי md, Global Instructions, פרויקטים
├─ INTERFACE ─── COMMAND_API.md · COMMAND_API_TASKS.md · .claude/ (skills · agents)   89 פקודות ליבה + 98 פקודות משימה + 4 Claude Code skills + os-auditor
├─ KNOWLEDGE ─── AI_SKILL_MAP · AI_PROGRESSION_PLAN · AI_LEARNING_RESOURCES · AI_7_SKILLS · AI_SKILLS_ACQUISITION · AI_TYPES · AI_CLAUDE_TOOL_SELECTOR · AI_CLAUDE_STACK_2026 · AI_CLAUDE_GLOSSARY · AI_RAG_DESIGN · AI_PROJECT_STRUCTURE · AI_ROLES_2026 · AI_CLAUDE_ENGINEER_ROADMAP · AI_DATA_BI · AI_SYSTEM_DESIGN · AI_PROCESS_INTELLIGENCE · AI_PROFICIENCIES_2026 · AI_LINEAR_ALGEBRA · AGENT_BLUEPRINT · CLOUD_ARCHITECT_SKILLS · KUBERNETES_101 · AI_MICROSERVICES   ידע אישי/לימודי (on-demand)
└─ BUSINESS ──── marketing-strategy-framework.md · INVESTOR_RELATIONS.md · CASES/*.md   הקשר עסקי נקודתי
```

**הזרימה מקצה לקצה:** המשתמש מקליד פקודה → ה-INTERFACE מזהה אותה → היא נפתרת מול ה-CONTEXT וה-MEMORY → בכפוף לחוקי ה-KERNEL → ומיושמת על מודול ה-BUSINESS הרלוונטי.

---

## 3. רישום מודולים וסדר טעינה

זוהי הטבלה הקנונית. `CLAUDE.md` משקף אותה, אך **כאן** היא מקור האמת.

| סדר | מודול | שכבה | סטטוס | תפקיד |
|-----|--------|------|--------|--------|
| 1 | `OPERATING_SYSTEM.md` | Kernel | ✅ פעיל | חוקים, סדר, הכרעה |
| 2 | `MEMORY.md` | Memory | ✅ פעיל | זהות, העדפות, focus/projects |
| 3 | `DECISION_LOG.md` | Memory | ✅ פעיל | יומן החלטות append-only — רציונל וסטטוס |
| 4 | `COWORK_SETUP.md` | Context | ✅ פעיל | חיבור תיקייה, קבצי md, אונבורדינג |
| 5 | `PROJECTS_SETUP.md` | Context | ✅ פעיל | Claude Projects — 3 פרויקטים, תוצר אחד לכל אחד, הוראות drop-in |
| 6 | `COMMAND_API.md` | Interface | ✅ פעיל | 89 פקודות, composition, prompting frameworks, system prompt |
| 7 | `COMMAND_API_TASKS.md` | Interface | ✅ פעיל | 98 פקודות משימה ב-9 קטגוריות (99 Claude Commands) + 30 פרומפטי גיליונות (§4) + מיפוי לתרחישי ULease |
| 8 | `marketing-strategy-framework.md` | Business | ✅ פעיל | מסגרת 10-שלבית לאסטרטגיית שיווק |
| 9 | `AI_SKILL_MAP.md` | Knowledge | ✅ פעיל | מפת מיומנויות AI — 4 שלבים ומיקום ULease |
| 10 | `AI_PROGRESSION_PLAN.md` | Knowledge | ✅ פעיל | תוכנית התקדמות אישית — Learn-vs-Delegate, 90 יום |
| 11 | `AI_LEARNING_RESOURCES.md` | Knowledge | ✅ פעיל | קוריקולום AI — משאבים לכל שלב |
| 12 | `AI_7_SKILLS.md` | Knowledge | ✅ פעיל | 7 מיומנויות לשליטה ב-AI (2026) + מיפוי ל-OS |
| 13 | `AI_SKILLS_ACQUISITION.md` | Knowledge | ✅ פעיל | תוכנית רכישת מיומנויות hands-on (8 שבועות) |
| 14 | `AI_TYPES.md` | Knowledge | ✅ פעיל | טקסונומיית סוגי AI (Traditional·Generative·Agentic, 3×9) + מיפוי ל-ULease |
| 15 | `AI_CLAUDE_TOOL_SELECTOR.md` | Knowledge | ✅ פעיל | עץ החלטה לבחירת כלי Claude — 15 כלים + מיפוי ל-ULease |
| 16 | `AI_CLAUDE_STACK_2026.md` | Knowledge | ✅ פעיל | 4 עמודי ה-stack של 2026 (Cowork · Projects · Skills · Code) + מיפוי ה-build התפעולי |
| 17 | `AI_CLAUDE_GLOSSARY.md` | Knowledge | ✅ פעיל | מילון 30 מונחי Claude + מיפוי "איפה אצלך" (21/30 מיושמים) |
| 18 | `AI_RAG_DESIGN.md` | Knowledge | ✅ פעיל | תכנון RAG — 15 טעויות Retrieval + פתרונות, ממופה ל-ULease (משלים את SPEC §7.1) |
| 19 | `AI_PROJECT_STRUCTURE.md` | Knowledge | ✅ פעיל | תקן 4 התיקיות (prompts·data·agents·evals) לריפו הפלטפורמה + צ'קליסט Tech Lead |
| 20 | `AI_ROLES_2026.md` | Knowledge | ✅ פעיל | 21 תפקידי AI (2026) ממופים: מייסד · Tech Lead (5 בכובע אחד) · Guardian |
| 21 | `AI_CLAUDE_ENGINEER_ROADMAP.md` | Knowledge | ✅ פעיל | רודמאפ 15 השלבים ל-Claude AI Engineer — 11/15 כבר בנויים ב-OS; הפער = Tech Lead |
| 22 | `AI_DATA_BI.md` | Knowledge | ✅ פעיל | יסודות BI ומידול נתונים (Power BI) — star schema, ETL, DAX — ממופה ל-M9 |
| 23 | `AI_SYSTEM_DESIGN.md` | Knowledge | ✅ פעיל | יסודות System Design — Gateway, סגנונות API, תורים, JWT — ממופה לארכיטקטורת הפלטפורמה |
| 24 | `AI_PROCESS_INTELLIGENCE.md` | Knowledge | ✅ פעיל | מודיעין תהליכים ובקרת הטמעה — איפה להחיל Gen AI (GenIQ), HITL ושער בגרות, מדידת ROI |
| 25 | `AI_PROFICIENCIES_2026.md` | Knowledge | ✅ פעיל | 10 מיומנויות AI חיוניות ל-2026 + כרטיס-ניקוד (6✅+4🟡/10) ומיפוי תלת-שכבתי ל-ULease (שדרה · צמיחה · תשתית) |
| 26 | `AI_LINEAR_ALGEBRA.md` | Knowledge | ✅ פעיל | יסודות אלגברה לינארית (12 מושגים) + עמודת "למה זה חשוב ל-ML" — הגשר ל-ULease: dot product → RAG/pgvector; מודול היסוד המתמטי הראשון |
| 27 | `AGENT_BLUEPRINT.md` | Knowledge | ✅ פעיל | בלופרינט 8 השלבים לבניית סוכן AI (Purpose→Testing) כשכבת ניווט מעל `AI_*` + טבלת Ecosystem + §10 כללי העבודה (דוקטרינת Karpathy) — המקור הקנוני שאליו מפנה `leasing-api` |
| 28 | `CLOUD_ARCHITECT_SKILLS.md` | Knowledge | ✅ פעיל | 5 שכבות כישורי ארכיטקט ענן (Foundation→Enterprise) עם מדרגת Beginner/Intermediate/Advanced + רובריקת ראיון ל-Tech Lead ותמונת בגרות ULease — הציר התשתיתי המשלים ל-`AI_SKILL_MAP` |
| 29 | `KUBERNETES_101.md` | Knowledge | ✅ פעיל | יסודות Kubernetes (K8s) — 10 אבני-הבניין (Pod · Control Plane · Deployment · Service · HPA…) + §11 הכרעת design-review MVP/V1/V2 ושער אנטי-over-engineering; ה-deep-dive מתחת לשכבה 4 של `CLOUD_ARCHITECT_SKILLS` |
| 30 | `AI_MICROSERVICES.md` | Knowledge | ✅ פעיל | איך שירות מתחבר לאחר (REST · gRPC · Message Broker · Service Discovery · LB), sync מול async + ההכרעה **Modular-Monolith-first** ל-ULease (microservices = V2) + צ'קליסט design review |
| 31 | `INVESTOR_RELATIONS.md` | Business | ✅ פעיל | חברה, cap table, גיוס 150K, תחזית ומעקב משקיעים |
| 32 | `CASES/ULEASE*.md` | Business | ✅ פעיל | תיק ULease 🎯 — מודל עסקי, תחזית, איפיון, מתודולוגיה, גיוס, playbooks, מנועי אקווזיציה (היצע + ביקוש), ביקורת ומחירון/SLA |

> **הערה על שכבות:** מודולי `AI_*` הם שכבת **Knowledge** — ידע אישי/לימודי שיושב לוגית בין ה-INTERFACE ל-BUSINESS. הם פעילים אך נטענים on-demand, לא בכל turn.
> כשמודול עובר מ-🔜 ל-✅ — מעדכנים את הסטטוס כאן ואת ה-Active Modules ב-`CLAUDE.md` ו-`README.md`.

### 3.1 תשתית תפעולית (Working Sets)

קבצים שאינם נטענים כמודולים בצ'אט, אלא ע"י הכלי הרלוונטי. רשומים כאן כדי לקיים את "No Dangling Modules" גם עליהם:

| Working set | שכבה | נטען ע"י | תפקיד |
|-------------|------|-----------|--------|
| `COWORK/` (ABOUT-ME · TEMPLATES · OUTPUTS) | Context | אפליקציית Claude Cowork | סביבת העבודה בפועל — קבצי זהות, תבניות ותוצרים |
| `.claude/skills/` (os-module · os-decision · ulease-refresh · investor-update) | Interface | Claude Code (auto-trigger) | 4 משימות חוזרות שהפכו ל-skills |
| `.claude/agents/os-auditor.md` | Interface | Claude Code (sub-agent) | סוכן ביקורת עקביות קריאה-בלבד |
| `.github/workflows/` + `scripts/` | Interface | GitHub Actions (כל PR) | CI — בדיקות עקביות מכניות + שחזור ארטיפקטים bit-exact (D-023) |

---

## 4. החוזה ההתנהגותי — Boot Block (drop-in)

זה הבלוק שמפעיל את כל ה-OS. העתק אותו ל-`userPreferences` / system prompt / Cowork Global Instructions:

```
CLAUDE OS ENABLED — Kernel v1.15

On every turn, before responding:
1. Load identity & context from MEMORY.md (and the Cowork "about-me" file if connected).
2. Honor active session state: /focus, /project, /tone, /length, /format.
3. Recognize /command syntax per COMMAND_API.md and apply its output contracts.

Module load order (canonical, from OPERATING_SYSTEM.md §3):
  OPERATING_SYSTEM → MEMORY → DECISION_LOG → COWORK_SETUP → PROJECTS_SETUP → COMMAND_API → marketing-strategy-framework → KNOWLEDGE (AI_*) → BUSINESS modules
  (working sets, §3.1: COWORK/ loaded by the Cowork app · .claude/ loaded by Claude Code)

Conflict hierarchy (highest wins, from §5):
  Safety > IP-protection > Kernel rules > Memory/userPreferences > Session commands > Defaults

Doctrine:
- Context first — never answer "generically" when identity is available.
- Output-shape contracts override default tone.
- Unknown/ambiguous input → one focused clarifying question, never a silent guess.
- Internal IP (Deal Score, Match API, legal automation) stays confidential.
```

---

## 5. היררכיית הכרעה בקונפליקטים

כששני כללים מתנגשים — הגבוה ברשימה מנצח. **תמיד.**

| דרגה | רובד | דוגמה לקונפליקט | מי מנצח |
|------|------|------------------|----------|
| 1 | **Safety** | פקודה מבקשת תוכן מזיק | Safety — מסורב בנימוס |
| 2 | **IP-protection** | `/explain` על מנגנון Deal Score | חיסיון — הסבר כללי בלבד |
| 3 | **Kernel rules** | מודול מצהיר סדר טעינה אחר | הקרנל (§3) |
| 4 | **Memory / userPreferences** | העדפת "תמיד פורמלי" | מתקיימת אלא אם פקודת session דורסת זמנית |
| 5 | **Session commands** | `/tone casual` מול העדפה פורמלית | הפקודה הזמנית — עד `/reset` |
| 6 | **Defaults** | אין כלל אחר רלוונטי | התנהגות ברירת-המחדל של Claude |

---

## 6. רצף האתחול (Boot Sequence)

מה קורה בתחילת שיחה חדשה כש-OS מחובר:

1. **Kernel up** — נטענים החוקים מהקובץ הזה.
2. **Mount memory** — נקראת הזהות מ-`MEMORY.md` / קובץ ה-`about-me` ב-Cowork.
3. **Attach context** — אם Cowork מחובר לתיקייה, נטענים קבצי ה-`md` הרלוונטיים.
4. **Arm interface** — מנוע הפקודות (`COMMAND_API.md`) דרוך לזיהוי `/command`.
5. **Ready** — Claude עונה מתוך "הוא כבר מכיר אותי", לא מאפס.

> ה-Global Instruction "תמיד תקרא את עליי לפני שאתה עונה" (ראו `COWORK_SETUP.md` §3) הוא בדיוק מה שמפעיל את שלבים 2–3 אוטומטית.

---

## 7. מודל ההרחבה

הוספת מודול חדש ל-OS — checklist:

- [ ] צור את הקובץ עם Header סטנדרטי (Module / Version / Author / Status / Integrates with).
- [ ] הוסף אותו לטבלת הרישום (§3) עם השכבה והסטטוס.
- [ ] שבץ אותו ב-`Module Load Order` ב-`CLAUDE.md`.
- [ ] רשום אותו תחת `Active Modules` ב-`CLAUDE.md` וב-`README.md`.
- [ ] אם הוא משנה התנהגות גלובלית — עדכן את ה-Boot Block (§4).
- [ ] תעד את התוספת ב-`DECISION_LOG.md` (כשקיים).

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | קרנל ראשוני — עקרונות, ארכיטקטורת שכבות, רישום מודולים, Boot Block, היררכיית הכרעה | 2026-05-30 |
| 1.0.1 | רישום `AI_CLAUDE_TOOL_SELECTOR` (כיום שורה 15, D-018) + הוספת `CASES/ULEASE_AUDIT.md` לתיק ULease (D-019) | 2026-06-01 |
| 1.1.0 | Claude Stack 2026 (D-021): רישום `PROJECTS_SETUP.md` (שורה 5) + `AI_CLAUDE_STACK_2026.md` (כיום שורה 16), סעיף §3.1 תשתית תפעולית (`COWORK/`, `.claude/`), ועדכון Boot Block | 2026-06-02 |
| 1.2.0 | רישום תשתית CI ב-§3.1 (D-023): `.github/workflows/os-consistency.yml` + `scripts/os_consistency_check.py` — בדיקות עקביות אוטומטיות על כל PR | 2026-06-02 |
| 1.3.0 | רישום `AI_RAG_DESIGN` (כיום שורה 18, D-025) — מודול Knowledge לתכנון RAG, משלים את שכבת ה-RAG ב-SPEC §7.1; Boot Block כולל את marketing-strategy-framework בסדר הטעינה | 2026-06-02 |
| 1.4.0 | גל ידע #2 (D-026): רישום `COMMAND_API_TASKS` (שורה 7, Interface) + `AI_CLAUDE_GLOSSARY` (שורה 17) + `AI_PROJECT_STRUCTURE` (שורה 19) + `AI_ROLES_2026` (שורה 20). הסטת שורות: marketing 7→8 · AI_* 8→9 עד 16→18 · IR 17→21 · CASES 18→22 | 2026-06-02 |
| 1.5.0 | רישום `AI_CLAUDE_ENGINEER_ROADMAP` (שורה 21, D-027) — רודמאפ 15 השלבים, סוגר את משפחת הלמידה. הסטת שורות: IR 21→22 · CASES 22→23 | 2026-06-02 |
| 1.6.0 | רישום `AI_DATA_BI` (שורה 22, D-032) — מודול הדאטה הראשון: יסודות BI ל-M9. הסטת שורות: IR 22→23 · CASES 23→24 | 2026-06-02 |
| 1.7.0 | רישום `AI_SYSTEM_DESIGN` (שורה 23, D-036) — יסודות backend לארכיטקטורת הפלטפורמה. הסטת שורות: IR 23→24 · CASES 24→25 | 2026-06-02 |
| 1.8.0 | רישום `AI_PROCESS_INTELLIGENCE` (שורה 24, D-039) — מודיעין תהליכים (GenIQ) + Human-in-the-Loop (n8n). הסטת שורות: IR 24→25 · CASES 25→26 | 2026-06-02 |
| 1.9.0 | יישור הקרנל אחרי גל D-040..D-047: `CASES/ULEASE_DEMAND_ENGINE` נרשם תחת גלוב שורה 26 (D-042) והכפיל `AI_ACQUISITION_FLYWHEEL` הוסר (D-047); עדכון תיאורי שורה 7 (+30 פרומפטי גיליונות, D-043) ושורה 26 (מנועי אקווזיציה) | 2026-06-03 |
| 1.10.0 | רישום `AI_PROFICIENCIES_2026` (שורה 25, D-050) — 10 מיומנויות AI חיוניות ל-2026 (כרטיס-ניקוד 6✅+4🟡/10). הסטת שורות: IR 25→26 · CASES 26→27 | 2026-06-03 |
| 1.11.0 | רישום `AI_LINEAR_ALGEBRA` (שורה 26, D-052) — מודול היסוד המתמטי הראשון: 12 מושגי אלגברה לינארית, הגשר dot product → RAG/pgvector. הסטת שורות: IR 26→27 · CASES 27→28 | 2026-06-03 |
| 1.12.0 | רישום `AGENT_BLUEPRINT` (שורה 27, D-056) — בלופרינט 8 השלבים לבניית סוכן AI + §10 כללי העבודה (המקור הקנוני ל-`leasing-api`, סוגר הפניה שבורה חוצת-ריפו). הסטת שורות: IR 27→28 · CASES 28→29 | 2026-06-04 |
| 1.13.0 | רישום `CLOUD_ARCHITECT_SKILLS` (שורה 28, D-057) — 5 שכבות כישורי ארכיטקט ענן (Foundation→Enterprise) + רובריקת ראיון ל-Tech Lead ותמונת בגרות ULease; הציר התשתיתי המשלים ל-`AI_SKILL_MAP`. הסטת שורות: IR 28→29 · CASES 29→30 | 2026-06-04 |
| 1.14.0 | רישום `KUBERNETES_101` (שורה 29, D-061) — יסודות Kubernetes: 10 אבני-הבניין + §11 הכרעת design-review MVP/V1/V2 ושער אנטי-over-engineering; ה-deep-dive מתחת לשכבה 4 של `CLOUD_ARCHITECT_SKILLS`. הסטת שורות: IR 29→30 · CASES 30→31 | 2026-06-04 |
| 1.15.0 | רישום `AI_MICROSERVICES` (שורה 30, D-062) — איך שירות מתחבר לאחר (REST · gRPC · Message Broker · Service Discovery · LB), sync מול async + ההכרעה **Modular-Monolith-first** ל-ULease (microservices = V2). הסטת שורות: IR 30→31 · CASES 31→32 | 2026-06-04 |

**Confidentiality.** קובץ זה הוא הליבה של ה-Claude Operating System האישי של Avraham Bar Yochai Chazan.

— *End of OPERATING_SYSTEM.md v1.15.0 —*
