# תבנית: Header למודול OS חדש

> משמש את ה-skill `os-module`. כל מודול חדש ב-OS מתחיל מכאן.

---

```markdown
# [שם המודול בעברית] — [שם באנגלית]

**Module:** `FILENAME.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — [שכבה: Kernel / Memory / Context / Interface / Knowledge / Business].
**Integrates with:** [מודולים קשורים, מופרדים בפסיקים]

---

> [שורת תקציר: מה המודול עושה ולמה הוא קיים.]

[תוכן המודול]

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | [תיאור השינוי הראשוני] | YYYY-MM-DD |

**Confidentiality.** קובץ זה הוא חלק מה-Claude Operating System האישי של Avraham Bar Yochai Chazan.

— *End of FILENAME.md v1.0.0 —*
```

## אחרי יצירת הקובץ — רישום בחמשת המקומות
1. הקובץ עצמו (התבנית למעלה) ✓
2. `OPERATING_SYSTEM.md` §3 — שורה בטבלה + bump גרסת קרנל
3. `CLAUDE.md` — Active Modules + Module Load Order
4. `README.md` — Active Modules (באנגלית)
5. `DECISION_LOG.md` — רשומת D-XXX + bump גרסה

(או פשוט: הפעל את ה-skill `os-module` שעושה את כל זה.)
