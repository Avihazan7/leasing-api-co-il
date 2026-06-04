# בלופרינט סוכן AI — How to Build an AI Agent

**Module:** `AGENT_BLUEPRINT.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — מודול ידע/בלופרינט (Knowledge layer).
**Source:** מבוסס על האינפוגרפיקה *"How to Build an AI Agent — A step-by-step blueprint to design, build and scale intelligent agents"* + הפוסט הנלווה (code231).
**Integrates with:** `OPERATING_SYSTEM.md` §4, `COMMAND_API.md` §8, `AI_CLAUDE_TOOL_SELECTOR.md`, `AI_SYSTEM_DESIGN.md`, `AI_RAG_DESIGN.md`, `AI_PROJECT_STRUCTURE.md`, `AI_CLAUDE_STACK_2026.md` §5.7, `CASES/ULEASE_SPEC.md` §7.1–§7.2 — ו-`leasing-api/CLAUDE.md` (צורך את §10 ככללי עבודה מחייבים).

---

> **בלופרינט-שדרה לבניית סוכן AI בשמונה שלבים.** המסר המרכזי: סוכן מוצלח הוא **מערכת**, לא מודל — בחירת ה-LLM היא חתיכה אחת מהפאזל. המודול הזה לא מלמד כל שלב מאפס; הוא **מאנדקס** — כל שלב מפנה לבית הקנוני שלו במשפחת ה-`AI_*` ובאיפיון ULease, ומסכם איפה ULease עומדת מולו. §10 הוא הבית הקנוני של **כללי העבודה** (דוקטרינת Karpathy) שאליו מפנה `leasing-api`.

---

## למה מודול-שדרה ולא עוד מודול ידע

עד היום משפחת ה-`AI_*` כיסתה את הרכיבים בנפרד: בחירת מודל (`SELECTOR`), כלים ותשתית (`SYSTEM_DESIGN`), זיכרון/RAG (`RAG_DESIGN`), מבנה ותזמור (`PROJECT_STRUCTURE`), evals (`ULEASE_SPEC` §7.2). מה שחסר היה **המבט מלמעלה** — הסדר שבו מרכיבים סוכן מקצה לקצה, ובית קנוני אחד לכללי העבודה. זה התפקיד כאן.

---

## שמונת השלבים — כל אחד ממופה לבית הקנוני ול-ULease

| # | השלב | מה מגדירים | 🎯 ב-ULease / OS | 📍 הבית הקנוני |
|---|------|------------|-------------------|------------------|
| 1 | **Purpose & Scope** | בעיה · משתמש · success criteria · אילוצים | מטרה לכל סוכן (Ultra·Master·Max); הצלחה = eval suite; אילוצים = Guardian | `CASES/ULEASE_SPEC.md`, `AI_PROCESS_INTELLIGENCE.md` (איפה להחיל + ROI) |
| 2 | **System Prompt** | Goals · Role/Persona · Instructions · Guardrails | ה-OS הזה: `CLAUDE.md` + Boot Block; guardrails = Guardian-as-Hooks (דטרמיניסטי) | `OPERATING_SYSTEM.md` §4, `COMMAND_API.md` §8 |
| 3 | **Choose LLM** | דיוק · חלון הקשר · מהירות · עלות — *התאמה, לא הגדול ביותר* | Haiku (ניקוד/ניתוב) · Sonnet (nurture/תוכן) · Opus (מורכב) + מנוף Effort (D-024) | `AI_CLAUDE_TOOL_SELECTOR.md` |
| 4 | **Tools & Integrations** | APIs · DBs · MCP · מערכות פנים · פונקציות | Max פועל דרך APIs (מימון, חוזה, חיוב); n8n; MCP=HOW | `AI_SYSTEM_DESIGN.md`, `AI_PROJECT_STRUCTURE.md` (`tools/`), `AI_CLAUDE_STACK_2026.md` §5.5 |
| 5 | **Memory** | שיחה · working · vector DB · structured · קבצים | RAG על pgvector (קורפוס: מלאי·מחירונים·רגולציה·היסטוריה); dot product = דמיון קוסינוס | `AI_RAG_DESIGN.md`, `CASES/ULEASE_SPEC.md` §7.1, `AI_LINEAR_ALGEBRA.md` |
| 6 | **Orchestration** | workflows · triggers · routing · agent-to-agent · error handling | Ultra→Master→Max; מנועי n8n (outbound/demand); Agent Teams כ-prototype | `AI_PROJECT_STRUCTURE.md`, `AI_SYSTEM_DESIGN.md` (תורים·Idempotency·DLQ), `AI_CLAUDE_STACK_2026.md` |
| 7 | **User Interface** | chat · web · API · Slack/Discord | אתר צרכני + Q&A Bot; קונסולת admin (הזנת מלאי, D-045); API לשותפים | `CASES/ULEASE_SPEC.md`, `AI_SYSTEM_DESIGN.md` (8 סגנונות API) |
| 8 | **Testing & Evals** | דיוק · אמינות · latency · UX · השפעה עסקית — *לעולם לא "גמור"* | eval חוסם-deploy (grounding 100% · golden 50 · red-team 0); CI חוסם-merge (D-023); שערי HITL (D-040); כלל 90 הימים | `CASES/ULEASE_SPEC.md` §7.2, `AI_RAG_DESIGN.md` |

> **המבנה הוא הסדר.** Purpose → Prompt → Model → Tools → Memory → Orchestration → Interface → Testing. רוב הצוותים מתחילים מ-3 (איזה LLM) ומדלגים על 1–2 — וזו בדיוק הסיבה ש"פרויקטי AI נופלים אחרי deployment" (`AI_CLAUDE_STACK_2026.md` §5.7, הצד התפעולי).

---

## §9 — האקו-סיסטם וה-Building Blocks במבט-על

טבלת ההשוואה מהמקור, עם עמודת "הזיקה אצלך". *(גרסאות המודל מופיעות באינפוגרפיקת המקור; הכוונון הקנוני שלך — `AI_CLAUDE_TOOL_SELECTOR.md`.)*

| קטגוריה | כלים (לפי המקור) | מתאים ל… | 🎯 הזיקה ל-ULease / OS |
|----------|--------------------|-----------|--------------------------|
| **Consumer AI Agents** | ChatGPT · Claude · Perplexity | עוזר כללי · מחקר · כתיבה | Claude = ה-stack (Chat/Cowork); ראו `AI_CLAUDE_TOOL_SELECTOR.md` |
| **Agentic Coding Tools** | Cursor · Windsurf · Claude Code | פיתוח, ריבוי-קבצים, CLI | **Claude Code = הריפו הזה** (skills · os-auditor · CI) |
| **No-Code Builders** | Lindy · Relay · **n8n** | אוטומציה עסקית, self-host | **n8n** = מנועי ה-outbound וה-demand (ציות ישראלי, self-host) |
| **Dev Frameworks** | LangGraph · CrewAI · LlamaIndex | מערכות production מורכבות | **ULease: Claude Agent SDK בלבד** (D-022) — framework נוסף = תלות ושכבת תרגום מיותרת (`AI_CLAUDE_STACK_2026.md` §5.6) |

**Building blocks at a glance:** Purpose (למה הסוכן קיים) · Prompt (הוראות) · Model (איזה LLM) · Tools (יכולות) · Memory (אחסון ואחזור) · Orchestration (תיאום) · Interface (כל ערוץ) · Testing (אימות ושיפור).

---

## §10 — כללי העבודה (דוקטרינת Karpathy)

> **המקור הקנוני.** `leasing-api/CLAUDE.md` (סעיף *Working Rules*) מפנה לכאן: *"מקור: `leasing-api-co-il/AGENT_BLUEPRINT.md § 10` — Karpathy doctrine"*. שמונת הכללים כאן הם אותם כללים — זה **הבית**; שם יושב ההעתק התפעולי שכל agent על קוד הריפו מחויב לו.

התובנה (Andrej Karpathy): *"LLMs become dramatically better when you force them into disciplined workflows"* — המודל לא משתפר; **המערכת סביבו** משתפרת. הדוקטרינה המלאה (חמשת כשלי הסוכנים, success-criteria-במקום-הוראות, תזמור מקביל, 7 כשלי הייצור) ב-`AI_CLAUDE_STACK_2026.md` §5.7. כללי העבודה הם הזיקוק התפעולי שלה:

1. **PLAN FIRST** — משימה לא-טריוויאלית מתחילה ב-plan, לא בקוד.
2. **ASK, DON'T ASSUME** — עמימות בדרישה? שאל. אל תנחש.
3. **SIMPLE** — הפתרון המינימלי שפותר את הבעיה. שום דבר ספקולטיבי.
4. **SURGICAL** — גע רק בקבצים שהמשימה דורשת. אל תשפץ מה שלא שבור.
5. **GOAL-DRIVEN** — הגדר success criteria (טסט שנכשל → עובר) לפני הביצוע; איטרט עד שעובר.
6. **VERIFY** — הרץ את הטסטים (`npm test`) ואת ה-build לפני commit. אין "אמור לעבוד".
7. **NO LAZINESS** — root cause, לא workaround. אם יש חוב — תעד אותו, אל תסתיר.
8. **SUBAGENTS** — exploration/research ב-subagent נפרד; שמור על context ראשי נקי.

> *"CLAUDE.md files behave like an operating system for the agent."* — זה בדיוק הריפו הזה. שמונת השלבים שמעל הם **מה** בונים; שמונת הכללים כאן הם **איך** בונים אותו.

---

## השורה התחתונה

סוכן הוא מערכת של שמונה שכבות — מטרה, פרומפט, מודל, כלים, זיכרון, תזמור, ממשק ובדיקות. ULease בנויה מכולן (כל שורה בטבלה מצביעה על המימוש), וה-OS הזה הוא היישום של דוקטרינת הבנייה עצמה. מי שמבין את זה — לא בוחר מודל; הוא בונה מערכת.

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | יצירת המודול — בלופרינט 8 השלבים (Purpose→Testing) כשכבת ניווט מעל משפחת `AI_*` + §9 טבלת ה-Ecosystem + §10 כללי העבודה (דוקטרינת Karpathy) כמקור קנוני שאליו מפנה `leasing-api`. מבוסס אינפוגרפיקת *"How to Build an AI Agent"* (D-056) | 2026-06-04 |

**Attribution.** מבנה 8 השלבים וטבלת האקו-סיסטם: האינפוגרפיקה *"How to Build an AI Agent"* (code231). דוקטרינת Karpathy (§10): פוסט התובנות של Andrej Karpathy. המיפוי ל-ULease ולמשפחת ה-`AI_*` — חלק מה-Claude OS של Avraham Bar Yochai Chazan.

**Confidentiality.** קובץ זה הוא חלק מה-Claude Operating System האישי של Avraham Bar Yochai Chazan.

— *End of AGENT_BLUEPRINT.md v1.0.0 —*
