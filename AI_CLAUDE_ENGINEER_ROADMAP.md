# Claude AI Engineer Roadmap — 15 שלבים, ואיפה אתה עליהם

**Module:** `AI_CLAUDE_ENGINEER_ROADMAP.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — Knowledge layer (§3 שורה 21). סוגר את משפחת הלמידה (Skill Map → Progression → Resources → Acquisition → **Roadmap**).
**Source:** מבוסס על האינפוגרפיקה *"Claude AI Engineer Roadmap (with Free Course & Certificate)"*.
**Integrates with:** `AI_SKILL_MAP.md`, `AI_LEARNING_RESOURCES.md`, `AI_SKILLS_ACQUISITION.md`, `AI_CLAUDE_GLOSSARY.md`, `AI_CLAUDE_STACK_2026.md`, `AI_ROLES_2026.md`, `CASES/ULEASE_TECH_ONBOARDING.md`

> מסלול 15 השלבים להפוך ל-**Claude AI Engineer** — עם טוויסט: כשממפים אותו מול הריפו הזה מגלים ש**11 מתוך 15 השלבים כבר בנויים כאן**. אתה לא בתחילת המסלול; אתה בשלב 11. מה שנשאר (12–14) הוא בדיוק הגדרת התפקיד של ה-Tech Lead, ושלב 15 הוא ULease עצמה.

---

## 1. חמישה-עשר השלבים — מול מה שכבר בנוי

| שלב | נושא | ✅ ההוכחה בריפו | סטטוס |
|:----:|------|-----------------|:------:|
| 1 | **AI Basics** | `AI_TYPES.md` — 3 סוגי AI, 9 יכולות, ממופים ל-ULease | ✅ |
| 2 | **Claude Interface & Features** | `AI_CLAUDE_GLOSSARY.md` (30 מונחים) + `AI_CLAUDE_TOOL_SELECTOR.md` (12 כלים) | ✅ |
| 3 | **Prompt Engineering Basics** | `COMMAND_API.md` §7 — מסגרות פרומפט (RAG · CoT · few-shot) | ✅ |
| 4 | **Advanced Prompting Techniques** | 89 פקודות ליבה + composition (`COMMAND_API.md`) + 98 פקודות משימה (`COMMAND_API_TASKS.md`) | ✅ |
| 5 | **Content Creation** | `marketing-strategy-framework.md` · `ULEASE_OUTREACH_SCRIPTS.md` · מצגת הפיץ' | ✅ |
| 6 | **Research & Summarization** | `ULEASE_AUDIT.md` — 4 סוכני מחקר מקבילים, 41 ממצאים | ✅ |
| 7 | **Coding with Claude** | הריפו הזה (Claude Code) + 4 גנרטורים (`FORECAST.py` · `DASHBOARD.py` · `DECK.py` · `SCENARIOS.py`) | ✅ |
| 8 | **Workflow Automation** | `ULEASE_OUTBOUND_ENGINE.md` (n8n, 8 שכבות) + `ULEASE_AUTOMATION_MAP.md` (40 אוטומציות) | ✅ |
| 9 | **Data Handling & Analysis** | מודל פיננסי משוחזר-בית-בבית: CSV ↔ Python ↔ דשבורד אינטראקטיבי | ✅ |
| 10 | **AI Productivity Systems** | **ה-Claude OS עצמו** — kernel, memory, skills, decision log, CI | ✅ |
| 11 | **Real-world Use Cases** | **ULease 🎯** — תיק עסקי שלם: איפיון, playbooks, תחזית, מחירון | ✅ |
| 12 | **API & Integration** | `ULEASE_SPEC.md` §9 — מאופיין, ממתין למימוש | 🔜 Tech Lead |
| 13 | **AI Tools Ecosystem** | `AI_CLAUDE_STACK_2026.md` + n8n; pgvector ו-MCP בהמשך | 🟡 חלקי |
| 14 | **Deployment & Scaling** | `ULEASE_SPEC.md` §10 (NFR) + §7.2 (Evals) — מאופיין | 🔜 Tech Lead |
| 15 | **Build Projects** | **השקת ULease MVP** — הפרויקט עצמו | 🎯 בתהליך |

**הציון: 11 ✅ · 1 🟡 · 2 🔜 · 1 🎯** — הרודמאפ הוא לא תוכנית לימודים בשבילך; הוא **תעודת שליטה רטרואקטיבית**.

---

## 2. מיפוי למפת המיומנויות (4 השלבים)

| שלבי הרודמאפ | שלב במפה (`AI_SKILL_MAP.md`) | מי מחזיק |
|---------------|-------------------------------|-----------|
| 1–6 (יסודות, פרומפטים, תוכן, מחקר) | שלב 1 — Tools 🧰 | ✅ אתה |
| 7–10 (קוד, אוטומציה, דאטה, מערכות) | שלב 2 — Workflows 🔁 | ✅ אתה |
| 11–13 (use cases, API, אקוסיסטם) | שלב 3 — Agentic 🤖 | אתה (מוצר) + Tech Lead (מימוש) |
| 14–15 (deployment, scale, פרויקט) | שלב 4 — Architect 🏛️ | Tech Lead מבצע · אתה מנהל |

---

## 3. הפער (שלבים 12–14) = הגדרת ה-Tech Lead

בדיוק שלושת השלבים שחסרים הם התפקיד שמגויס (`AI_ROLES_2026.md` §2):

| שלב חסר | התפקיד מ-2026 שמכסה אותו |
|----------|---------------------------|
| 12 · API & Integration | **AI Integration Engineer** (#13) |
| 13 · AI Tools Ecosystem | **AI Agent Engineer** (#14) + **AI Knowledge Engineer** (#2) |
| 14 · Deployment & Scaling | **MLOps/LLMOps Engineer** (#7) |

> **לשיחת הגיוס:** "המסלול שלנו מכוסה עד שלב 11. אתה נכנס בדיוק בשלבים 12–14 — עם איפיון מוכן, ולא מדף ריק."

---

## 4. הקורס החינמי והתעודה — איך להשתמש

| למי | למה |
|-----|------|
| **אתה (אברהם)** | ולידציה + תעודה רשמית: הופך 11 שלבים של עבודה קיימת לאישור פורמלי. שווה את הזמן רק עבור שלבים 12–14 ברמת מושגים |
| **מועמדי Tech Lead** | פילטר סינון: מועמד שסיים את הקורס (או מציג שווה-ערך) מדבר את השפה מיום 1 — להוסיף ל-`ULEASE_HIRING.md` כיתרון |
| **Onboarding** | חומר יום-0 ל-Tech Lead לצד `ULEASE_TECH_ONBOARDING.md` — במקום להסביר מה זה Claude, שולחים את הרודמאפ |

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | 15 שלבי הרודמאפ ממופים מול ה-OS (11/15 בנויים) + מיפוי למפת המיומנויות, לפער ה-Tech Lead ולשימושי הקורס/תעודה | 2026-06-02 |

**Attribution.** מבנה הרודמאפ מבוסס על *Claude AI Engineer Roadmap (with Free Course & Certificate)*. העיבוד והמיפוי ל-OS ול-ULease — חלק מה-Claude OS של Avraham Bar Yochai Chazan.

**Confidentiality.** קובץ זה הוא חלק מה-Claude Operating System האישי של Avraham Bar Yochai Chazan.

— *End of AI_CLAUDE_ENGINEER_ROADMAP.md v1.0.0 —*
