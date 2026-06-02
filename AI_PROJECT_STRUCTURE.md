# מבנה פרויקט AI — ארבע תיקיות, אפס בלגן

**Module:** `AI_PROJECT_STRUCTURE.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — Knowledge layer (§3 שורה 19). תקן הנדסי לריפו הפלטפורמה של ULease.
**Source:** מבוסס על *"The 4-folder structure I use for every AI project"* (Brij Kishore Pandey).
**Integrates with:** `CASES/ULEASE_SPEC.md`, `CASES/ULEASE_TECH_ONBOARDING.md`, `AI_RAG_DESIGN.md`, `AI_CLAUDE_STACK_2026.md`, `CASES/ULEASE_HIRING.md`

> רוב פרויקטי ה-AI מתבלגנים מהר. ארבע תיקיות — `prompts/` · `data/` · `agents/` · `evals/` — הופכות מערכת AI מ"אוסף סקריפטים" ל**מוצר ניתן לתחזוקה**. זה התקן שריפו הפלטפורמה של ULease יקום עליו ביום הראשון של ה-Tech Lead.

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

## 3. המיפוי לריפו הפלטפורמה של ULease 🎯

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

---

## 4. וגם הריפו הזה (Claude OS) כבר בנוי כך

| עיקרון | המימוש ב-OS |
|---------|--------------|
| prompts/ — פרומפטים כקבצים | `COMMAND_API.md` (89 חוזים) · `COMMAND_API_TASKS.md` (98 מתכונים) · `.claude/skills/` |
| data/ — קלטים ניתנים לשחזור | `CASES/*.csv` + הגנרטורים (`ULEASE_FORECAST.py` …) |
| agents/ — סוכנים כרכיבים | `.claude/agents/os-auditor.md` |
| evals/ — הוכחה שזה עובד | `scripts/os_consistency_check.py` + CI על כל PR (D-023) |

> מי שפותח את הריפו מבין אותו מיד = מערכת. מי שלא מוצא כלום = חוב טכני. הריפו הזה עבר את המבחן.

---

## 5. צ'קליסט קבלה ל-Tech Lead

- [ ] ריפו `ulease-platform` נפתח עם ארבע התיקיות מיום 1
- [ ] אף פרומפט לא חי בתוך קוד — הכל קבצים ב-`prompts/`
- [ ] כל מקור דאטה (ספק/מחירון) נכנס דרך `data/raw/` → pipeline → `data/processed/`
- [ ] ה-Golden Set (50 תרחישים, §7.2) יושב ב-`evals/tests/` לפני שהסוכן הראשון עולה
- [ ] כל ריצת סוכן כותבת trace — בלי יוצאים מהכלל
- [ ] scorecard עלות-לשאילתה מחובר ל-unit economics (CPL ₪103)

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | תקן 4 התיקיות (prompts·data·agents·evals) + מיפוי מלא לרכיבי האיפיון של ULease + צ'קליסט קבלה ל-Tech Lead | 2026-06-02 |

**Attribution.** המבנה מבוסס על *The 4-folder structure I use for every AI project* (Brij Kishore Pandey). העיבוד והמיפוי ל-ULease — חלק מה-Claude OS של Avraham Bar Yochai Chazan.

**Confidentiality.** קובץ זה הוא חלק מה-Claude Operating System האישי של Avraham Bar Yochai Chazan.

— *End of AI_PROJECT_STRUCTURE.md v1.0.0 —*
