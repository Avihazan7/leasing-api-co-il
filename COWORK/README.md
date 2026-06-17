# COWORK — סביבת העבודה של Claude Cowork

> זו התיקייה שמחברים ל-**Claude Cowork** (אפליקציית Desktop). היא מיישמת בפועל את המבנה מ-`COWORK_SETUP.md` ואת כלל ה-cheat sheet "How to use Claude in 2026": **ABOUT-ME · TEMPLATES · OUTPUTS**.

## המבנה

```
COWORK/
├── ABOUT-ME/              ← מי אני (3 קבצים, יחד < 6,000 tokens)
│   ├── about-me.md            מי אני, איך אני עובד, הסטנדרטים שלי
│   ├── my-company.md          ULease 🎯: מספרים, קהלים, למה אומרים לא
│   └── anti-ai-style.md       מילים וביטויים שאסור ל-Claude לכתוב
├── TEMPLATES/             ← תבניות לתוצרים חוזרים
│   ├── investor-email.md      מייל עדכון משקיע
│   ├── weekly-status.md       סטטוס שבועי
│   ├── decision-entry.md      רשומת החלטה ל-DECISION_LOG
│   └── os-module-header.md    header תקני למודול OS חדש
├── OUTPUTS/               ← כל תוצר ש-Claude מפיק נשמר כאן (עם תאריך)
└── README.md              ← הקובץ הזה
```

## Global Instructions — העתק ל: Settings → Cowork → Global instructions

```
לפני כל תשובה: קרא את COWORK/ABOUT-ME/about-me.md, my-company.md ו-anti-ai-style.md.
אם השאלה נוגעת לתיק ספציפי — קרא גם את הקובץ הרלוונטי ב-CASES/.
כל תוצר חדש שמור ב-COWORK/OUTPUTS/ עם תאריך בשם הקובץ (YYYY-MM-DD-שם.md).
אל תתחיל משימה לפני שקראת. אם משהו לא ברור — שאל לפני שאתה מנחש.
```

## הפרומפט האחד לכל משימה

```
קרא את התיקייה שלי. שאל אותי שאלות לפני שאתה מתחיל.
אם משהו לא ברור — אל תנחש.
```

## כללי עבודה

1. **ABOUT-ME קצר** — שלושת הקבצים יחד מתחת ל-6,000 tokens. קצר ומתוחזק > ארוך ומיושן.
2. **כל תוצר ל-OUTPUTS** — עם תאריך: `YYYY-MM-DD-<שם>.md`. לא משאירים תוצרים בצ'אט.
3. **תבנית לפני יצירה** — יש תבנית מתאימה? משתמשים בה. אין? יוצרים אחת ושומרים ב-TEMPLATES.
4. **שיחה חדשה כל ~20 הודעות** — הודעות ישנות עולות tokens בכל turn.
5. **Sonnet לעבודה קצרה · Opus למשימות קשות** (אסטרטגיה, מסמכים ארוכים, החלטות).
