---
name: agent-architect
description: Define a new governed agent for this project. Use when the user says "define an agent that...", "תגדיר לי סוכן ש...", or wants to add an agent to the AGENTS.md registry. Walks through the seven AGENT.md sections, picks the project profile (legal/commercial), and enforces the five super-principles — especially the mandatory evidence[] field.
---

# agent-architect

הסקיל ששומר את שיטת ממשל-הסוכנים ומאפשר לזמן אותה בכל פרויקט. מטרתו: ליצור מפרט `AGENT.md` חדש שתואם לתבנית, לפרופיל הפרויקט, ולחמשת עקרונות-העל.

## מתי להפעיל

כשהמשתמש מבקש להגדיר סוכן חדש ("תגדיר לי סוכן ש...", "define an agent that...") או להוסיף סוכן למרשם.

## תהליך

1. **קרא את ההקשר** — טען את `AGENT_GOVERNANCE.md`, `AGENTS.md` ו-`AGENT.template.md` של הפרויקט.
2. **קבע פרופיל** — `legal` (Factum) או `commercial` (Leasing). הפרופיל קובע את ניסוח עקרונות-העל ואת שער-האדם.
3. **מלא את שבעת המקטעים** עם המשתמש:
   1. זהות (`id`, שם, פרופיל, גרסה)
   2. תחום אחריות (מה כן / מה לא)
   3. חוזה קלט (`inputRef`, סכימה, `dependsOn`)
   4. חוזה פלט (`payload` + `evidence[]` חובה)
   5. כללי התנהגות
   6. עקרונות-העל (חמישה, מנוסחים בהקשר הסוכן)
   7. עצירה בטוחה ושער אנושי
4. **אכוף את עקרונות-העל** — סרב לסיים מפרט שבו חוזה הפלט אינו דורש `evidence[]` לא-ריק, או שאין בו מסלול `partial` לעצירה בטוחה.
5. **כתוב** את הקובץ אל `agents/<id>.AGENT.md`.
6. **רשום** שורה חדשה בטבלת `AGENTS.md`.

## כללי אכיפה (לא לוותר)

- `evidence[]` חובה ולא-ריק על כל תוצר עובד — זו נקודת-האכיפה המרכזית.
- לכל סוכן מסלול `status: "partial"` לקלט חסר/לא-תקין (עצירה בטוחה, לא קריסה).
- פרופיל `commercial`: כל התחייבות כספית/חוזית עוברת שער אנושי לפני ביצוע.
- פרופיל `legal`: כל מסקנה משפטית מהותית מסומנת ומועברת לאדם; הסוכן מסמן, לא מכריע.
- עובד אינו מתכנן ואינו מודע לעובדים אחרים; תיאום הוא תפקיד שכבת הרב-סוכנים.

## פלט

מפרט `AGENT.md` תקין תחת `agents/`, ושורה מעודכנת ב-`AGENTS.md`. אם נדרש תיאום בין כמה סוכנים — הפנה את המשתמש לשכבת הרב-סוכנים (ראו `AGENT_GOVERNANCE.md`), אל תבנה סוכן-על.
