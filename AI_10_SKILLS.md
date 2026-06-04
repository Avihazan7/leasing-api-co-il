# 10 מיומנויות AI לשליטה ב-2026 — 10 AI Skills to Master in 2026

**Module:** `AI_10_SKILLS.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — Knowledge layer (§3 שורה 29). העדשה הכלי-מוכוונת (tool-centric) של משפחת מדדי-המיומנויות — *מה* בונים ו*באיזה כלי*.
**Source:** מבוסס על האינפוגרפיקה *"10 AI Skills to Master in 2026"*.
**Integrates with:** `AI_7_SKILLS.md`, `AI_PROFICIENCIES_2026.md`, `AI_SKILL_MAP.md`, `AI_SKILLS_ACQUISITION.md`, `AGENT_BLUEPRINT.md`, `AI_RAG_DESIGN.md`, `AI_DATA_BI.md`, `AI_LINEAR_ALGEBRA.md`, `AI_CLAUDE_STACK_2026.md`, `COMMAND_API.md`, `CASES/ULEASE_SPEC.md`, `CASES/ULEASE_DEMAND_ENGINE.md`, `CASES/ULEASE_OUTBOUND_ENGINE.md`, `CASES/ULEASE_DEMAND_PLAYBOOK.md`

---

> 10 מיומנויות AI מעשיות ל-2026 — **רשימת כלים**, לא רשימת הרגלים. כל מיומנות מגיעה עם 3 כלים קנוניים, וכאן כל אחת ממופה ל**בית הקיים ב-OS/ULease** ולכלי שכבר נבחר. זה לא מודול תיאוריה; זו **מפת הכלים** של ה-stack — וכרטיס-ניקוד של מה כבר חי.

**מקומו במשפחה:** ארבעה מודולים כבר ממפים "מיומנויות AI", כל אחד מעדשה אחרת — וזו עדשה חמישית, מובחנת:

| מודול | העדשה | היחידה |
|--------|--------|---------|
| `AI_SKILL_MAP` | מסע 4 השלבים (Tools→Workflows→Agentic→Architect) | *שלב* |
| `AI_7_SKILLS` | הרגלי עבודה אישיים | *הרגל* (5/7 מיושמים) |
| `AI_PROFICIENCIES_2026` | יכולות **ארגוניות** (aiplanetx) | *יכולת-על* (6✅+4🟡/10) |
| `AI_SKILLS_ACQUISITION` | תוכנית רכישה hands-on (8 שבועות) | *שבוע-פרויקט* |
| **`AI_10_SKILLS` (כאן)** | **מיומנות טכנית + הכלי** | *מיומנות→כלי→בית* |

---

## 1. עשר המיומנויות → הכלים → הבית ב-OS/ULease

| # | מיומנות | הכלים (באינפוגרפיקה) | הבית הקנוני ב-OS / ULease | סטטוס |
|---|---------|----------------------|----------------------------|--------|
| 1 | **Prompt Engineering** | ChatGPT · Claude · Gemini | `COMMAND_API.md` (89 פקודות + §7 frameworks + Opus 4.8 §7.7) · `COMMAND_API_TASKS.md` · `.claude/skills/` · §6.3 (32 קיצורים) | ✅ ליבה |
| 2 | **AI Workflow Automation** | Zapier · **n8n** · Make | `ULEASE_OUTBOUND_ENGINE` + `ULEASE_DEMAND_ENGINE` (n8n) · `AUTOMATION_MAP` (42 אוטומציות, 18 בנויות) | ✅ פעיל |
| 3 | **Vibe Coding** | Replit · Lovable · **Cursor** | `AI_CLAUDE_STACK_2026` (עמוד **Code** / Claude Code — סולם 7 הרמות, רמה 6/7) · `AI_SKILL_MAP` שלב 1 · ה-OS עצמו נבנה כך | 🟡 כלי המייסד (Claude Code) — לא רכיב במוצר ULease |
| 4 | **AI Agents & Assistants** | LangChain · AutoGen · CrewAI | `AGENT_BLUEPRINT` (8 השלבים) · **Ultra·Master·Max** (`ULEASE_SPEC`) · `AI_TYPES` (Agentic) — **הכרעה: Claude Agent SDK בלבד** (D-022/D-038) | 🟡 מאופיין — build של ה-Tech Lead (Phase 0) |
| 5 | **RAG System** | LlamaIndex · Pinecone · Weaviate | `AI_RAG_DESIGN` (15 הטעויות) · `ULEASE_SPEC` §7.1 (**pgvector** — נבחר על פני Pinecone/Weaviate) · `AI_LINEAR_ALGEBRA` (dot product = דמיון קוסינוס) | ✅ מאופיין |
| 6 | **AI Data Skills** | Pandas · NumPy · DuckDB | `AI_DATA_BI` (star schema · DAX · BI) · `AI_LINEAR_ALGEBRA` · `CASES/ULEASE_FORECAST.py` (pandas) | ✅ פעיל |
| 7 | **Computer Vision** | OpenCV · Roboflow · YOLOv8 | `AI_CLAUDE_TOOL_SELECTOR` §2.5 (**Vision** — ה-workflow המרכזי: אינפוגרפיקה→מודול) · `AI_PROFICIENCIES_2026` #5 | 🟡 Vision של Claude כן (כלי-עבודה); CV קלאסי (YOLO/OpenCV) מחוץ לליבה — אופציית V2: הערכת מצב/נזק מתמונת רכב |
| 8 | **Voice & Speech AI** | Vapi · ElevenLabs · Azure Speech | `AI_CLAUDE_TOOL_SELECTOR` §2.5 (**Voice**) · `AI_PROFICIENCIES_2026` #9 (Media) | 🟡 מחוץ לליבה במכוון — אופציית V2: סוכן קולי ללידים נכנסים / שיחות ספק |
| 9 | **Search & Optimization (GEO)** | Perplexity · NeuronWriter · SurferSEO | `DEMAND_PLAYBOOK` (ערוץ GEO) · `DEMAND_ENGINE` (הלופ האורגני) · `LAUNCH_CHECKLIST` (robots.txt ל-AI crawlers) · `AI_PROFICIENCIES_2026` #7 · D-035 | ✅ פעיל — יתרון תחרותי |
| 10 | **AI Ethics & Safety** | OpenAI Safety · IBM AI Fairness 360 · Google Model Cards | `ULEASE_SPEC` §7.2 (Guardrails & Evals) · **Guardian=Hooks** (D-037) · D-023 (LLMOps + CI) · `AI_CLAUDE_STACK_2026` §5.6 (Prompt Injection) · `AI_PROFICIENCIES_2026` #10 | ✅ פעיל |

---

## 2. כרטיס-הניקוד — 6✅ + 4🟡 / 10

**שש פעילות/מאופיינות-במלואן** (1·2·5·6·9·10) · **ארבע חלקיות/מחוץ-לליבה** (3·4·7·8) · **אפס נקודות עיוורות.**

> צירוף מקרים מאיר: זו **אותה צורת ניקוד** של `AI_PROFICIENCIES_2026` (6✅+4🟡/10) — שתי אינפוגרפיקות "10 מיומנויות" בלתי-תלויות, אותה מסקנה. ושתי ה-🟡 המהותיות חופפות: **Agents** (#4 כאן = #2 שם) ו**Media/Voice** (#8 כאן = #9 שם). הפער זהה משני מקורות: מנוע ה-Ultra·Master·Max (מחכה ל-Tech Lead) ויצירת מדיה (מחוץ-לליבה במכוון).

ארבע ה-🟡 בפירוט:
- 🟡 **#4 Agents** — מאופיין במלואו ב-SPEC; ה-build הוא **כל** העבודה ההנדסית של Phase 0 (D-012). יכולת מתוכננת, לא חסרה.
- 🟡 **#3 Vibe Coding** — Claude Code הוא כלי הבנייה של ה-**OS עצמו** (אתה ברמה 6/7); מוצר ULease ייבנה ע"י ה-Tech Lead ב-Claude Agent SDK, לא ב-Cursor/Replit. מיומנות של המייסד, לא רכיב מוצר.
- 🟡 **#7 Computer Vision · #8 Voice** — **מחוץ-לליבה במכוון**: marketplace שסוגר עסקאות רכב לא צריך YOLO/ElevenLabs. ה-Vision שכן צריך (אינפוגרפיקה→מודול) עובד. אימוץ עתידי = החלטה עסקית (V2), לא חוב טכני.

המודול מצטרף למשפחת מדדי-הבגרות החיצוניים: `AI_7_SKILLS` **5/7** · `AI_CLAUDE_ENGINEER_ROADMAP` **11/15** · `AI_CLAUDE_STACK_2026` **רמה 6/7** · `AI_CLAUDE_TOOL_SELECTOR` **10✅+1🟡/12** · `AI_PROFICIENCIES_2026` **6✅+4🟡/10**. חמישה מקורות, אותה מסקנה.

---

## 3. עיקרון ה-Claude-first — הכלים כבר נבחרו

האינפוגרפיקה מציעה כלים גנריים (LangChain · Pinecone · Zapier · CrewAI). ל-ULease ההכרעות כבר התקבלו, וכמעט תמיד **לכיוון Claude-first / מאוחד** — כי "מנצחים עם הארכיטקטורה הטובה ביותר, לא עם הכלי הכי מדובר" (D-046):

| המיומנות | כלי מהאינפוגרפיקה | ההכרעה ב-ULease | מקור |
|----------|-------------------|------------------|------|
| Agents | LangChain · CrewAI · AutoGen | **Claude Agent SDK בלבד** | D-022 · D-038 |
| RAG | Pinecone · Weaviate | **pgvector על PostgreSQL** (אותו DB) | `SPEC` §7.1 · D-022 |
| Workflow | Zapier · Make | **n8n** (self-host, HITL) | `OUTBOUND/DEMAND_ENGINE` |
| Prompting | ChatGPT · Gemini | **Claude** (Command API) | `COMMAND_API` |

> המסקנה: האינפוגרפיקה מאמתת את ה**קטגוריות**; ה-OS כבר בחר את ה**כלים**. הערך כאן אינו "מה ללמוד" אלא **לוודא שכל קטגוריה כוסתה בהכרעה מודעת** — וכולן כוסו.

---

## 4. מה זה אומר ל-ULease 🎯 — ארבע קבוצות

| קבוצה | מיומנויות | התפקיד |
|-------|-----------|---------|
| **השדרה (המוצר)** | #4 Agents · #5 RAG · #6 Data · #10 Ethics&Safety | סוכן מקרקע-אמת (RAG) שמבצע עסקה (Agents) על דאטה מובנית (star schema) תחת Guardian (Safety) |
| **מנוע הצמיחה** | #2 Workflow · #9 GEO | לידים נכנסים בעלות יורדת: לופ אורגני + ציטוט בתשובות AI |
| **מלאכת הבנייה** | #1 Prompting · #3 Vibe Coding | איך המייסד וה-Tech Lead בונים מהר — Command API + Claude Code |
| **אופציית V2** | #7 Vision · #8 Voice | החלטות *אם בכלל*: הערכת רכב מתמונה · סוכן קולי |

**מנדט ה-Tech Lead בשורה אחת** (זהה ל-`AI_PROFICIENCIES_2026`): להפוך את #4 Agents מ-🟡 ל-✅. זו כל העבודה ההנדסית של Phase 0; השאר כבר ✅ או מחוץ-לליבה.

---

## 5. Learn-vs-Delegate

| מה | מי |
|----|-----|
| #1 Prompting · #3 Vibe Coding · #6 Data (קונספטים, KPIs) · #9 GEO | **המייסד** — כלי-עבודה יומיומי |
| #4 Agents · #5 RAG (מימוש) · #6 Data (pipeline) · #10 evals | **ה-Tech Lead** — design review מול המייסד |
| #7 Vision · #8 Voice | **דחוי** — החלטה עסקית ל-V2 |

> "מיומנות ב-2026 אינה הכלי שאתה יודע לתפעל — היא ה**הכרעה** איזה כלי לא צריך. שש כבר עובדות, אחת מחכה לאיש אחד, ושתיים בחרנו במכוון לא לבנות עכשיו."

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | 10 מיומנויות AI לשליטה ב-2026 (tool-centric) → מיפוי מיומנות→כלי→בית ב-OS/ULease, כרטיס-ניקוד 6✅+4🟡/10, עיקרון ה-Claude-first (הכלים כבר נבחרו), ומיפוי ארבע-קבוצות ל-ULease | 2026-06-04 |

**Attribution.** מבוסס על האינפוגרפיקה *10 AI Skills to Master in 2026*. העיבוד, כרטיס-הניקוד והמיפוי ל-OS/ULease הם חלק מה-Claude Operating System של Avraham Bar Yochai Chazan.

**Confidentiality.** קובץ זה הוא חלק מה-Claude Operating System האישי של Avraham Bar Yochai Chazan.

— *End of AI_10_SKILLS.md v1.0.0 —*
