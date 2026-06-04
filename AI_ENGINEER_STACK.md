# AI_ENGINEER_STACK.md — 12 Tools ⇄ ULease

**Module:** `AI_ENGINEER_STACK.md` · **Version:** 1.0.0
**מקור:** הכרטיס *12 Tools You Need to Become an AI Engineer* (Rushikesh Meharwade).
**Thesis:** *כלי הוא בחירה ארכיטקטונית. מפה כל כלי ל-tier ולצורך אמיתי — לא לאסוף hype.*

---

## 0. למה המודול קיים

הכרטיס מונה 12 כלים. מודול זה ממפה כל אחד ל-**מקומו בארכיטקטורת ULease** (או מסמן
"לא בשימוש / roadmap"), כך שבחירת כלי תהיה החלטה מתועדת ולא ברירת-מחדל.

## 1. הטבלה — 12 Tools ⇄ Tier

| # | Tool | קטגוריה | מצב ב-ULease |
|---|------|---------|--------------|
| 1 | **OpenAI** | LLM | ↔️ חלופי; ברירת המחדל היא Claude |
| 2 | **Claude** | LLM | ✅ ליבת ה-OS — long context, reasoning, coding (כל ה-agents) |
| 3 | **LangChain** | orchestration | ⚠️ נשקל; כיום ה-orchestration ב-`stage-a/` + `AGENT_BLUEPRINT § 9` |
| 4 | **LlamaIndex** | RAG / connectors | 🔭 roadmap — חיבור docs/DB ל-Vector tier (`MEMORY.md`) |
| 5 | **CrewAI** | multi-agent | ⚠️ השוואה ל-`stage-a` (manager+workers); ראה Stage-B |
| 6 | **vLLM** | inference | ❌ לא נדרש (משתמשים ב-API מנוהל) |
| 7 | **Ollama** | local models | 🔭 dev/privacy — הרצה מקומית בזמן פיתוח |
| 8 | **Pinecone** | vector DB | 🔭 Vector tier (`MEMORY.md`) — managed |
| 9 | **Weaviate** | vector DB | 🔭 חלופה ל-Pinecone (hybrid search) |
| 10 | **Weights & Biases** | experiment tracking | 🔭 ל-Evals harness (`AGENT_BLUEPRINT § 7`) |
| 11 | **FastAPI** | API serving | ↔️ מקביל ל-Express; `leasing-api` כבר על Express/Node |
| 12 | **Docker** | packaging | ✅ בשימוש — `Dockerfile` + `docker-compose.yml` ב-`leasing-api` |

מקרא: ✅ בשימוש · ⚠️ נשקל/מושווה · 🔭 roadmap · ↔️ חלופי · ❌ לא נדרש.

## 2. עקרון הבחירה

לכל החלטת tool: (1) איזה tier הוא משרת (Working/Episodic/Vector/SQL — ראה `MEMORY.md`)?
(2) מה ה-build-vs-buy? (3) מה ה-exit cost? בחירה מתועדת כאן + לקח ב-`MEMORY.md` אם השתנתה.

## 3. ה-stack בפועל היום

Claude (LLM) · Express/Node + Postgres (`leasing-api`) · Docker (packaging) ·
n8n (אוטומציה, `N8N_AUTOMATION.md`) · Power BI (BI). השאר — roadmap מתועד.
