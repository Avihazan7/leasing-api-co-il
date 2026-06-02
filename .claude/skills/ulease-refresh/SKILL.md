---
name: ulease-refresh
description: רענון כל ארטיפקטי ULease אחרי שינוי במודל הפיננסי — הרצת ULEASE_FORECAST.py → ULEASE_DASHBOARD.py → ULEASE_DECK.py → ULEASE_SCENARIOS.py, ואימות שהמספרים בקבצי ה-md (ULEASE.md, INVESTOR_RELATIONS.md, ULEASE_DECK.md) תואמים ל-CSV. הפעל אחרי כל שינוי תמחור/תחזית/הנחות, או כשמבקשים "רענן את הדשבורד/התחזית/המצגת".
---

# ulease-refresh — רענון ארטיפקטים פיננסיים

## Role (תפקיד)
אתה מהנדס ה-build של תיק ULease 🎯. שינוי במודל = רענון כל שרשרת הארטיפקטים + אימות עקביות bit-exact.

## Rules (כללים)
1. מקור האמת למספרים: `CASES/ULEASE_FORECAST.py` (הנחות מכוילות) → `CASES/ULEASE_FORECAST.csv` (התוצאה). כל השאר נגזרות.
2. סדר הרצה מחייב:
   ```
   python3 CASES/ULEASE_FORECAST.py
   python3 CASES/ULEASE_DASHBOARD.py
   python3 CASES/ULEASE_DECK.py
   python3 CASES/ULEASE_SCENARIOS.py
   ```
3. אחרי הרצה — `git diff --stat`: כל שינוי בארטיפקט חייב להיות מוסבר ע"י שינוי במקור. ארטיפקט שהשתנה "לבד" = באג.
4. המספרים המוצהרים ב-`CASES/ULEASE.md` (§1, §9), `INVESTOR_RELATIONS.md` (§4) ו-`CASES/ULEASE_DECK.md` חייבים להתאים ל-CSV. אי-התאמה = לדווח ולתקן.
5. שינוי הנחות במודל בלי הכרעת מייסד מתועדת (D-XXX ב-`DECISION_LOG.md`) — אסור. עצור והפעל קודם את `os-decision`.

## Steps (שלבים)
1. ודא שיש רשומת החלטה שמכסה את השינוי (אם רלוונטי).
2. כייל את ההנחות ב-`ULEASE_FORECAST.py` (קבועים בראש הקובץ, עם הערת D-XXX).
3. הרץ את 4 הסקריפטים בסדר.
4. `git diff --stat` — ודא שהשינויים צפויים.
5. השווה KPIs מוצהרים (הכנסה 26/27, נטו, עסקאות, מנויים, GMV) בקבצי ה-md מול ה-CSV; תקן סטיות.
6. דווח: טבלת לפני/אחרי לכל KPI שהשתנה + רשימת הקבצים שעודכנו.

## Trigger (מילות הפעלה)
"רענן" · "עדכן את הדשבורד" · "עדכן את התחזית" · "שיניתי את התמחור" · "refresh artifacts" · אחרי merge שנוגע ל-FORECAST.py
