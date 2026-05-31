# משאבי למידה — קוריקולום AI לפי המפה

**Module:** `AI_LEARNING_RESOURCES.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — מודול ידע/קוריקולום (Learning layer).
**Integrates with:** `AI_SKILL_MAP.md`, `AI_PROGRESSION_PLAN.md`, `CASES/ULEASE_SPEC.md`

> משלים את המפה (`AI_SKILL_MAP.md`) ואת התוכנית (`AI_PROGRESSION_PLAN.md`) ב**מה ללמוד בפועל** — קורסים ומשאבים לפי שלב, עם תיעדוף ל-ULease.

---

## 1. העיקרון

ללמוד **את מה שצריך, מתי שצריך** — לפי השלב במפה ולפי Learn-vs-Delegate (`AI_PROGRESSION_PLAN.md` §4). העדיפות שלך עכשיו: **שלב 3 (Agentic + RAG)** — בדיוק הטריטוריה של ULease.

---

## 2. 🎯 העוגן: IBM · Coursera — Agentic AI & RAG

**Master Agentic AI** — *"Learn to use RAG and agentic AI with expert training online from IBM."*

| למה זה הקורס הנכון **עכשיו** | |
|---|---|
| **מתאים בול לשלב 3** | RAG + עיצוב סוכנים — בדיוק המיומנויות של Agentic AI Systems במפה |
| **מתאים בול ל-ULease** | RAG → בסיס-ידע ל-Deal Score · סוכנים → מנוע Ultra·Master·Max |
| **רמת מוצר** | נותן לך להבין ולקבל החלטות מוצר — בדיוק מה ש**אתה** צריך ללמוד (לא להאציל) |

**מי ייקח:**
- 🧑‍💻 **אתה (אברהם)** — את ה**מושגים** (RAG, agent design) כדי לנהל ולחבר.
- 🤝 **ה-Tech Lead** — את ה**מימוש** לעומק.

> ℹ️ אמת את שם הקורס המדויק, האורך והמחיר ב-Coursera (קטלוג IBM מתעדכן). זה העוגן — לא תחליף לבנייה בפועל ב-ULease.

---

## 3. קוריקולום לפי שלב

| שלב | מה ללמוד | משאבים (לאמת זמינות עדכנית) |
|-----|-----------|------------------------------|
| **1 · Tools** | prompting מתקדם, הערכת פלט | תיעוד Anthropic/Claude · מדריכי prompt engineering (חינם) |
| **2 · Workflows** | אוטומציה, Webhooks, אינטגרציות | תיעוד **n8n / Make / Zapier** + tutorials (חינם) |
| **3 · Agentic** 🎯 | **RAG · עיצוב סוכנים · vector DB · guardrails** | **IBM Agentic AI & RAG (Coursera)** [עוגן] · **Claude Agent SDK** docs · intro ל-vector DB (pgvector/Pinecone) |
| **4 · Architect** | ארכיטקטורה, אבטחה, ממשל, עלויות | learning paths של ספק הענן · יסודות אבטחה/PCI · קריאה ב-AI governance |

> 🟢 חינם (docs) · 🔵 בתשלום (Coursera) — התחל מה-docs החינמיים, והשקע בקורס בתשלום לשלב 3 (העדיפות).

---

## 4. מסלול הלמידה המומלץ לאברהם

1. **עכשיו → השקה:** התחל את **IBM Agentic AI & RAG** (שלב 3) במקביל ל-MVP. כל מודול → יישום מיידי ב-ULease.
2. **במקביל:** `Claude Agent SDK` docs — להבין את Ultra·Master·Max ברמת מוצר.
3. **שלב 2 (לפי צורך):** n8n/Make — לחווט את האינטגרציות בעצמך (היעד שלך).
4. **2027 (שלב 4):** ארכיטקטורה, אבטחה וממשל — כשמרחיבים ל-scale.

> כלל הזהב: **לומדים תוך כדי בנייה.** כל מושג חדש → מיושם מיד ב-ULease, לא נשאר תיאוריה.

---

## 5. Learn vs Delegate (לכל משאב)

| משאב | אתה לומד | מאציל ל-Tech Lead |
|------|:--------:|:------------------:|
| IBM Agentic AI & RAG | ✅ מושגים, החלטות מוצר | ✅ מימוש לעומק |
| Claude Agent SDK | ✅ ארכיטקטורת סוכנים | ✅ קוד וייצור |
| n8n / Make | ✅ חיווט אינטגרציות | — (אתה מוביל) |
| Vector DB / RAG impl | רק מושגים | ✅ מימוש |
| Cloud / אבטחה / DevOps | רק כיווני-על | ✅ הכול |

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | קוריקולום ראשוני — עוגן IBM Agentic AI & RAG (Coursera) + משאבים לפי 4 שלבים + מסלול אישי | 2026-05-31 |

**Attribution.** העוגן מבוסס על מודעת *Master Agentic AI* (Coursera · IBM). העיבוד, המיפוי ל-ULease ול-Learn-vs-Delegate הם חלק מה-Claude OS של Avraham Bar Yochai Chazan.

— *End of AI_LEARNING_RESOURCES.md v1.0.0 —*
