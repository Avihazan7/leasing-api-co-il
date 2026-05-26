# AGENTS — מרשם הסוכנים · Factum IL

> אינדקס מרכזי של כל הסוכנים בפרויקט. כל שורה מצביעה על מפרט `AGENT.md` מלא תחת `agents/`.
> פרופיל הפרויקט: **`legal`** — עיגון משפטי, ביסוס לכל טענה, אדם-בפיקוד על כל מסקנה מהותית.
>
> להבנת המערכת השלמה קרא תחילה את [`AGENT_GOVERNANCE.md`](./AGENT_GOVERNANCE.md).

## הסוכנים

| `id` | שם | תחום אחריות | מפרט | סטטוס |
| --- | --- | --- | --- | --- |
| `summarizer` | Summarizer | סיכום מסמך בסיכום מעוגן-מקור; כל נקודה מפנה לשורת מקור. | [`agents/summarizer.AGENT.md`](./agents/summarizer.AGENT.md) | ממומש ב-`stage-a/` |
| `timeline-builder` | Timeline-Builder | בניית ציר זמן כרונולוגי של אירועי תיק מתוך מסמכים מתוארכים. | [`agents/timeline-builder.AGENT.md`](./agents/timeline-builder.AGENT.md) | מתועד |
| `contract-review` | Contract-Review | סקירת סעיפי חוזה לאיתור סיכונים, החרגות וסעיפים חסרים. | [`agents/contract-review.AGENT.md`](./agents/contract-review.AGENT.md) | מתועד |

## שכבת הרב-סוכנים

ההוכחה הרצה של שכבת התיאום נמצאת תחת [`stage-a/`](./stage-a/) — מנהל אחד, עובד אחד (Summarizer), וזיכרון משותף append-only. חמשת מנגנוני הממשל נאכפים בקוד (`node stage-a/run-stage-a.js`). ה-Orchestrator טוען את מפרט הסוכן הרלוונטי בעת זימון ואוכף את חוזה הפלט.

## הצעד הבא

**Verification-Agent (תוכנית V14)** — בודק את ה-`evidence` של תוצרי סוכנים מול המקור ומרים טענות לא-מאומתות לשער אנושי. תבנית מלאה ב-[`AGENT.template.md`](./AGENT.template.md) (מקטע הדוגמה).

## הוספת סוכן חדש

1. הפעל את הסקיל `agent-architect` ("תגדיר לי סוכן ש...").
2. העתק את [`AGENT.template.md`](./AGENT.template.md) אל `agents/<name>.AGENT.md` ומלא את שבעת המקטעים בפרופיל `legal`.
3. ודא שחמשת עקרונות-העל מיושמים — במיוחד `evidence[]`.
4. הוסף שורה לטבלה למעלה.
