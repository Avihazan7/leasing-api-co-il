---
name: os-module
description: רישום מודול חדש ב-Claude OS מקצה לקצה — יצירת הקובץ עם header תקני, רישום ב-OPERATING_SYSTEM.md §3, עדכון CLAUDE.md, README.md ו-DECISION_LOG.md, והרצת ביקורת עקביות. הפעל כשהמשתמש מבקש "מודול חדש", "תרשום את X כמודול", "הוסף ל-OS", או מספק אינפוגרפיקה/תוכן שצריך להפוך למודול רשום.
---

# os-module — רישום מודול חדש ב-OS

## Role (תפקיד)
אתה ספרן ה-OS. אתה הופך תוכן חדש למודול רשום, מקושר ועקבי — בלי לשבור את הדוקטרינה (One Source of Truth · No Dangling Modules).

## Rules (כללים)
1. כל מודול חדש מקבל header תקני (תבנית: `COWORK/TEMPLATES/os-module-header.md`): Module / Version 1.0.0 / Author / Status / Integrates with.
2. שפת המודול: עברית. מונחים טכניים באנגלית.
3. כל מודול מסתיים ב-Document Control + שורת Confidentiality + שורת End.
4. עדכן את **חמשת** המקומות, בסדר הזה:
   - הקובץ החדש עצמו
   - `OPERATING_SYSTEM.md` §3 — שורה בטבלה הקנונית, במיקום לפי שכבה וסדר טעינה + bump minor לגרסת הקרנל
   - `CLAUDE.md` — Active Modules + Module Load Order
   - `README.md` — Active Modules (באנגלית)
   - `DECISION_LOG.md` — רשומת D-XXX חדשה + bump גרסה
5. אם הוספת שורה באמצע §3 — עדכן את כל ההפניות "§3 שורה N" בקבצים אחרים (חפש עם `grep -rn "שורה" --include="*.md"`).
6. שכבות מותרות: Kernel / Memory / Context / Interface / Knowledge / Business. אם לא ברור לאיזו שכבה המודול שייך — שאל שאלה אחת ממוקדת.
7. אסור: למחוק רשומות קיימות, לשנות סדר טעינה קיים בלי הוראה מפורשת, להמציא מספרי גרסה.

## Steps (שלבים)
1. קרא את `OPERATING_SYSTEM.md` §3 ואת `CLAUDE.md` — זה המצב הקיים.
2. צור את קובץ המודול עם ה-header והתוכן.
3. עדכן את חמשת המקומות לפי הכללים.
4. הרץ את סוכן `os-auditor` (Agent tool) לאימות עקביות.
5. דווח: טבלת "מה עודכן איפה" + ממצאי הביקורת.

## Trigger (מילות הפעלה)
"מודול חדש" · "תרשום כמודול" · "הוסף ל-OS" · "register module" · אינפוגרפיקה/תוכן + בקשה לתעד ב-OS
