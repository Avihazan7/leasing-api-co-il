# בלופרינט סוכן AI — How to Build an AI Agent

**Module:** `AGENT_BLUEPRINT.md`
**Version:** 1.2.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — מודול ידע/בלופרינט (Knowledge layer).
**Source:** מבוסס על האינפוגרפיקה *"How to Build an AI Agent — A step-by-step blueprint to design, build and scale intelligent agents"* + הפוסט הנלווה (code231) + *"12 Must-Know Agentic AI Terms"* (AI Matt · Next Step Agents) — §11 + *"10 Best Practices For Building Reliable AI Agents in 2026"* (Alok Sharan) — §12.
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

## §11 — שנים-עשר מונחי ה-Agentic (מילון מהיר → הבית הקנוני)

> אם §9 הוא **אבני הבניין** של סוכן (8 השלבים) ו-§10 הם **כללי העבודה**, §11 הוא **אוצר המילים** — 12 המונחים שחוזרים בכל שיחה על סוכנים, ב-4 הקבוצות של המקור. אחות ל-`AI_CLAUDE_GLOSSARY.md` (מונחי **מוצר Claude**); כאן — מונחי **מערכות agentic** (vendor-neutral). כל מונח ממופה לבית הקנוני שלו ולגלגול שלו ב-ULease — אותו עיקרון של הגלוסרי: לא הגדרה לשמה, אלא **איפה זה כבר חי אצלך**.

### 🧱 יסודות (Foundations)
| # | מונח | מה זה | 📍 הבית הקנוני | 🎯 ב-ULease |
|---|------|--------|----------------|-------------|
| 1 | **MCP** | פרוטוקול חיבור אחד לכלים/דאטה ("USB-C של AI") | `AI_CLAUDE_STACK_2026.md` §5.5 (HOW) | GitHub MCP פעיל; סולק/ספקים/יומן בהמשך |
| 2 | **Memory** | זיכרון קצר-טווח (session) וארוך-טווח (vector) | שלב 5 (Memory) לעיל · `AI_RAG_DESIGN.md` · `MEMORY.md` | pgvector: מלאי · מחירונים · היסטוריית עסקאות |
| 3 | **Context Window** | תקרת ה"זיכרון העובד" — כמה נקרא ונשקל בבת אחת | `AI_CLAUDE_STACK_2026.md` §8 · §9.1 (כלכלת tokens) | `/compact` + sub-agent לשמירת הקשר רזה |

### 🔄 חשיבה וביצוע (Reasoning & Execution)
| # | מונח | מה זה | 📍 הבית הקנוני | 🎯 ב-ULease |
|---|------|--------|----------------|-------------|
| 4 | **Agent Loop** | Perceive → Plan → Act → Observe — מחזור הפעולה | `AI_CLAUDE_STACK_2026.md` §5.7 (success-criteria + loop) · שלב 6 (Orchestration) לעיל | Ultra: התאמה → הצעה → חוזה → מימון |
| 5 | **Tool Use** | קריאה ל-APIs / כלים / קוד | שלב 4 (Tools) לעיל · `AI_TYPES.md` #7 | Max: הצעה · חוזה · מימון · חיוב דרך APIs |
| 6 | **Sandboxing** | סביבה מבודדת להרצה בטוחה בלי לפגוע במארח | `AI_CLAUDE_STACK_2026.md` §5.5 (בידוד subagent) · `KUBERNETES_101.md` §9 | בידוד per-subagent + הרצת קוד/בדיקות מבודדת |

### 🛡️ בטיחות ואמינות (Safety & Reliability)
| # | מונח | מה זה | 📍 הבית הקנוני | 🎯 ב-ULease |
|---|------|--------|----------------|-------------|
| 7 | **Grounding** | עיגון כל טענה בעובדה מאומתת (נגד הזיות) | `AI_RAG_DESIGN.md` · `CASES/ULEASE_SPEC.md` §7.2 | grounding 100% לעובדות כספיות — כל מספר עם מקור |
| 8 | **Guardrails** | חוקים שחוסמים פעולה מזיקה/מחוץ-לתחום | `AI_CLAUDE_STACK_2026.md` §5.6 · `CASES/ULEASE_SPEC.md` §7.2 | Guardian-as-Hook מול המחירון (D-015), דטרמיניסטי |
| 9 | **Human-in-the-Loop** | אישור אדם לפני פעולה רגישה (Approval Gate) | `AI_PROCESS_INTELLIGENCE.md` · D-040 | `sendAndWait` + שער בגרות 3-שלבי (assist→אוטונומיה) |

### 🧩 תיאום וסקייל (Coordination & Scale)
| # | מונח | מה זה | 📍 הבית הקנוני | 🎯 ב-ULease |
|---|------|--------|----------------|-------------|
| 10 | **Orchestrator** | סוכן-על שמפרק מטרה ומאציל למומחים | שלב 6 (Orchestration) לעיל · `AI_MICROSERVICES.md` §6 (orchestration מול choreography) | **Ultra** |
| 11 | **Subagent** | סוכן ממוקד למשימה אחת, הקשר מבודד, ללא רקורסיה | `AI_CLAUDE_STACK_2026.md` §5.5 (WHO) | `os-auditor` (היום) · ה-**Masters** (ULease) |
| 12 | **Multi-Agent** | מערכת סוכנים שמשתפת פעולה לפתרון מטרה מורכבת | `CASES/ULEASE_SPEC.md` §7 · `AI_TYPES.md` #8 | **Ultra · Master · Max** — הארכיטקטורה כולה |

> **השורה התחתונה של §11: 12/12 כבר חיים ב-OS.** המונחים לא היו חסרים — הם היו **מפוזרים** על פני STACK · RAG · TYPES · SPEC · PROCESS. הטבלה הזו היא ה-**אינדקס** (אפס שכפול, נאמן לרף D-049/D-054): מי שמכיר את 12 המונחים האלה מדבר את שפת הסוכנים — וכל אחד מהם כבר בנוי כאן. שתי האחיות: `AI_CLAUDE_GLOSSARY.md` = "מה אומר מונח **מוצר Claude**", §11 כאן = "מה אומר מונח **מערכת agentic**".

---

## §12 — עשר פרקטיקות לסוכן אמין (Reliable-Agent Practices → הבית הקנוני)

> אם §9 הוא **אבני הבניין**, §10 **כללי העבודה** ו-§11 **אוצר המילים** — §12 הוא **צ'קליסט האמינות**: 10 הפרקטיקות שמפרידות בין סוכן-הדגמה לסוכן-production (Alok Sharan, 2026). אותו עיקרון של §11: לא דוקטרינה חדשה — **אינדקס** שסוגר פיזור. כל פרקטיקה כבר חיה ב-OS; הטבלה מוכיחה שדוקטרינת האמינות **שלמה**, ונותנת ל-Tech Lead צ'קליסט אחד לפני production.

| # | הפרקטיקה | התמצית | 📍 הבית הקנוני | 🎯 ב-ULease |
|---|-----------|---------|----------------|-------------|
| 1 | **Fail-Safe Design** | מטרות צרות · fallback · scale slowly | שלב 1 (Purpose/Scope) · §10 #3 SIMPLE · `AI_MICROSERVICES.md` (Circuit Breaker) | retry+fallback במנועי n8n (`OUTBOUND` §7, I4); סוכן צר לכל Master |
| 2 | **Context Configuration** | index · search · knowledge · retrieval | שלב 5 (Memory) · `AI_RAG_DESIGN.md` · `SPEC` §7.1 | pgvector: מלאי·מחירונים·רגולציה; 15 טעויות ה-Retrieval |
| 3 | **Tool-Based Capabilities** | כל פעולה = כלי מבוקר (schema · validate · nulls) | שלב 4 (Tools) · §11 #5 Tool Use · `AI_DATA_VALIDATION.md` | Max דרך APIs; ולידציית פלט (Type/Range/Format) |
| 4 | **Product-Spec Prompts** | פרומפט = דרישת מוצר (role·context·goal·format·constraints·steps) | שלב 2 (System Prompt) · `COMMAND_API.md` §7 (RTF·RACE·RISE·CO-STAR) | מסגרות הפרומפט; Skills מוגדרים צר |
| 5 | **Cost & Performance** | model routing · caching · tokens · batch | שלב 3 (Choose LLM) · `AI_CLAUDE_TOOL_SELECTOR.md` · Effort §7.7 (D-024) · `AUTOMATION_MAP` §12 | Haiku ניקוד/ניתוב · Sonnet כתיבה; כלל 90 הימים |
| 6 | **Versioning & Release Gates** | גרסה לכל prompt/tool/dataset/eval · gate release | **D-023** (CI חוסם-merge · eval חוסם-deploy) · `AI_PROCESS_INTELLIGENCE.md` §6 (generator=מקור-אמת) · `AI_PROJECT_STRUCTURE.md` (`prompts/registry.yaml`) | bit-exact CI; D-065 (prompt-to-prototype) |
| 7 | **Safety & Governance** | permissions · PII · audit · guardrails · escalate | §11 #8 Guardrails · Guardian-as-Hook (D-037/8) · `SPEC` §7.2 · `STACK` §5.6 (Prompt Injection) | Guardian דטרמיניסטי מול המחירון; ציות (תיקון 40, PII) |
| 8 | **Trustworthy Conversations** | הצג מגבלות · פעולות · escalation · שקיפות | §11 #9 HITL · `AI_PROCESS_INTELLIGENCE.md` (`sendAndWait`) · שלב 7 (Interface) · `SPEC` §7.2 ("לא יודע→אדם") | Q&A Bot מסנן ומסלים; grounding 100% לעובדות כספיות |
| 9 | **Real-World Evaluation** | dataset · edge cases · simulate tools · traces · fix gaps | שלב 8 (Testing) · `SPEC` §7.2 (golden 50 · red-team 0) · `AI_RAG_DESIGN.md` | eval suite חוסם-deploy; דגימת 10% (D-040) |
| 10 | **Continuous Improvement** | traces · feedback · retest · update memory · expand scope | שלב 8 · `AI_PROCESS_INTELLIGENCE.md` (מדידה · שער בגרות) · §10 #5 GOAL-DRIVEN (loop) | שער בגרות 3-שלבי (assist→אוטונומיה); Feedback Loop (`OUTBOUND` שכבה 08) |

> **השורה התחתונה של §12: 10/10 כבר מיושמות — מפוזרות על 8 השלבים · §10 · §11 · SPEC §7.2 · D-023 · D-040.** המקור (Sharan) מציג כל פרקטיקה כ-"flow" של sub-steps; הזיקוק שלנו ממפה אותה לבית שבו היא **כבר בנויה** (רף D-049/D-054/D-063: אינדקס, לא שכפול). זהו **צ'קליסט ה-go-live של ה-Tech Lead**: לפני שסוכן עולה ל-production, עוברים 10 השורות — כל אחת מצביעה על המנגנון הקיים שמספק אותה. שלוש האחיות סוגרות מעגל: §11 = *שפת* הסוכנים · §10 = *כללי* הבנייה · §12 = *פרקטיקות* האמינות.

---

## השורה התחתונה

סוכן הוא מערכת של שמונה שכבות — מטרה, פרומפט, מודל, כלים, זיכרון, תזמור, ממשק ובדיקות. ULease בנויה מכולן (כל שורה בטבלה מצביעה על המימוש), וה-OS הזה הוא היישום של דוקטרינת הבנייה עצמה. מי שמבין את זה — לא בוחר מודל; הוא בונה מערכת.

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | יצירת המודול — בלופרינט 8 השלבים (Purpose→Testing) כשכבת ניווט מעל משפחת `AI_*` + §9 טבלת ה-Ecosystem + §10 כללי העבודה (דוקטרינת Karpathy) כמקור קנוני שאליו מפנה `leasing-api`. מבוסס אינפוגרפיקת *"How to Build an AI Agent"* (D-056) | 2026-06-04 |
| 1.1.0 | §11 חדש (D-063): **12 מונחי ה-Agentic** ב-4 קבוצות (Foundations · Reasoning/Execution · Safety/Reliability · Coordination/Scale) כאינדקס מונח→בית-קנוני→ULease — אחות ל-`AI_CLAUDE_GLOSSARY` (מונחי מוצר Claude). הכרעת ספרנות: העשרה תחת הקפאת המודולים, לא מודול חדש (תקדים D-051/D-055/D-058). מבוסס *"12 Must-Know Agentic AI Terms"* (AI Matt) | 2026-06-07 |
| 1.2.0 | §12 חדש (D-068): **עשר פרקטיקות לסוכן אמין** (Reliable-Agent Practices) כאינדקס פרקטיקה→בית-קנוני→ULease — 10/10 כבר מיושמות אך מפוזרות (8 השלבים · §10 · §11 · SPEC §7.2 · D-023 · D-040) → צ'קליסט go-live ל-Tech Lead, אחות שלישית ל-§10/§11. הכרעת ספרנות: אינדקס, לא שכפול (תקדים D-063). מבוסס *"10 Best Practices For Building Reliable AI Agents in 2026"* (Alok Sharan) | 2026-06-08 |

**Attribution.** מבנה 8 השלבים וטבלת האקו-סיסטם: האינפוגרפיקה *"How to Build an AI Agent"* (code231). דוקטרינת Karpathy (§10): פוסט התובנות של Andrej Karpathy. 12 מונחי ה-Agentic (§11): *"12 Must-Know Agentic AI Terms"* (AI Matt · Next Step Agents). 10 פרקטיקות האמינות (§12): *"10 Best Practices For Building Reliable AI Agents in 2026"* (Alok Sharan). המיפוי ל-ULease ולמשפחת ה-`AI_*` — חלק מה-Claude OS של Avraham Bar Yochai Chazan.

**Confidentiality.** קובץ זה הוא חלק מה-Claude Operating System האישי של Avraham Bar Yochai Chazan.

— *End of AGENT_BLUEPRINT.md v1.2.0 —*
