# MEMORY.md — דוקטרינת הזיכרון + לולאת הלקחים

**Module:** `MEMORY.md` · **Version:** 1.0.0
**Status:** סוגר את ה-dangling ref השני ב-load order ואת מודול 5 ב-`AGENT_BLUEPRINT` (Memory Systems).
**Thesis:** *agent בלי זיכרון מתוכנן הוא chatbot. זיכרון הוא ארכיטקטורה, לא history.*

---

## 1. ארבעת ה-Tiers

מקור: `AGENT_BLUEPRINT § 7` (Memory Systems). כל agent ב-ULease בוחר אילו tiers הוא צריך —
דילוג מודע מותר, דילוג שקט אסור.

| Tier | מה הוא מחזיק | מימוש ב-ULease |
|------|-------------|----------------|
| **Working** | הקשר המשימה הנוכחית | חלון ההקשר + `CLAUDE.md` load order |
| **Episodic** | מה קרה בריצות קודמות, לקחים | § 3 כאן + `leasing-api/MEMORY.md` |
| **Vector** | ידע סמנטי לאחזור (RAG) | Pinecone/Weaviate (ראה `AI_ENGINEER_STACK.md`) |
| **SQL / Structured** | מצב עסקי סמכותי | Postgres של `leasing-api` (`settlements`, `ledger_entries`, `vehicle_read_model`) |

## 2. לולאת השיפור-העצמי (Card 1 §6)

> *"After ANY correction from the user: update lessons. Write rules that prevent the same mistake."*

זהו החוזה: **כל תיקון מהמשתמש → שורת לקח חדשה.** הלולאה:

```
טעות/תיקון → לקח (§3) → כלל-פעולה → קריאה לפני עבודה חוזרת → פחות הישנות
```

לקח בלי כלל-פעולה ניתן-לבדיקה = רעש. שמור קצר ואופרטיבי.

## 3. Lessons (OS-level)

פורמט: `- [YYYY-MM-DD] <תחום> — <מה התגלה> → <כלל>`
<!-- חדש בראש -->

- [2026-06-04] manifest — `CLAUDE.md › Active Modules` היה לא-מסונכרן (פנה לקבצים חסרים,
  השמיט קיימים) → אחרי כל הוספת/מחיקת מודול, עדכן גם Active Modules וגם Load Order באותו commit.
- [2026-06-04] dead links — load order הפנה ל-`OPERATING_SYSTEM`/`MEMORY`/`INVESTOR_RELATIONS`
  שלא היו קיימים → מודול שמוזכר ב-load order חייב להתקיים בדיסק, או להיות מסומן במפורש כ-roadmap.

## 4. גבולות (Working Rules ⇄ Memory)

`MEMORY.md` אוגר **לקחים וחוב**, לא סודות ולא PII. מצב עסקי חי חי ב-SQL tier (Postgres),
לא כאן. ידע סניפי חי ב-`BRANCH_KNOWLEDGE.md` / `BRANCHES/` עם RLS doctrine.
