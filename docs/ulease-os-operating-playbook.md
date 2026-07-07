# ULease OS — Operating Playbook

> אנחנו לא בונים אתר. אנחנו בונים **מערכת הפעלה למסחר רכב חדש בישראל**.

מסמך זה הוא **שיטת העבודה המדויקת** לבניית ‏Leasing.co.il / ULease עם ‏Claude Code,
‏Vercel, ‏GitHub, ‏Supabase וספקים מאושרים. הוא מקבע את הדוקטרינה שלפיה עבדנו בפועל —
לא תיאוריה. כל צוות/סוכן שעובד על המערכת מתחיל כאן.

**מסמך בלבד.** אין בו הוראה שמריצה קוד, כותבת ל-DB או משנה env.

---

## 0. המפה — מי כל אחד

| רכיב | תפקיד | פירוש מעשי |
|---|---|---|
| **Claude Code** | צוות הפיתוח | מתכנן, כותב קוד, בודק, פותח PR. לא מחליט לבד על פעולות בלתי-הפיכות. |
| **Vercel** | חדר הבקרה | פריסות, previews, לוגי ריצה, health. אימות שכל שינוי חי ותקין. |
| **Supabase** | שכבת האמת | ה-DB הפרודקשן (`leasing-co-il-prod`). מקור-אמת יחיד. כתיבה = אירוע-על. |
| **GitHub** | ספר ההיסטוריה | כל שינוי דרך PR. ה-diff הוא הרשומה. אין push ישיר ל-main. |
| **Leasing.co.il** | השוק | המשטח הציבורי. שום דבר עולה אליו בלי מקור מאומת + אישור. |
| **ULease** | המוח | מנועי ההחלטה (U.M.M / bigfive / orchestrator / governance). דטרמיניסטי ומוסבר. |

**עקרון-על:** *ULease לא מחזיקה כסף* — היא שכבת תיווך/החלטה/ביצוע. **המוח לא ממציא
עובדות**; הוא מדרג ומבצע על עובדות מאומתות בלבד.

---

## 1. Strategy Chat Flow — שיחת אסטרטגיה

מטרה: להפוך כוונה עסקית ל-milestone חד וניתן-לביצוע, **לפני** שנוגעים בקוד.

1. **המייסד מגדיר כוונה** (מה + למה, לא איך). Claude מחזיר ניסוח מזוקק של הבעיה.
2. **Claude מצליב מול המצב הקיים** — מה כבר בנוי בקוד, מה חלקי, מה חסר (VERIFY לפני
   הנחה: קוראים את הקוד/ה-DB/ה-Vercel, לא מנחשים).
3. **הצפת סתירות** — אם מה שנמצא סותר את התיאור, מציפים זאת מיד ולא ממשיכים.
4. **ASK, DON'T ASSUME** — עמימות בדרישה → שאלה ממוקדת (‏AskUserQuestion עם אופציות),
   לא ניחוש. החלטות בלתי-הפיכות/חוצות-מערכת תמיד עוברות דרך המייסד.
5. **פלט:** milestone עם scope, גבולות קשיחים (§10), ו-success criteria מדידים.

> כלל: החלטת-מייסד מפורשת → נרשמת ב-`DECISION_LOG.md` (skill `os-decision`).

---

## 2. Planning Flow — תכנון

1. **PLAN FIRST** — משימה לא-טריוויאלית מתחילה ב-plan כתוב, לא בקוד.
2. **SIMPLE + SURGICAL** — הפתרון המינימלי שפותר את הבעיה; נוגעים רק בקבצים שהמשימה
   דורשת. אין שיפוץ ספקולטיבי, אין הרחבת scope שלא התבקשה.
3. **GOAL-DRIVEN** — מגדירים את קריטריון ההצלחה (טסט/בדיקה) *לפני* הביצוע.
4. **מיפוי גבולות** — לכל משימה מסמנים במפורש מה **לא** עושים (מיגרציות? OpenAI?
   ספקים? MiaMe?) לפי §10.
5. **ענף** — כל משימה על ענף ייעודי (`claude/<task>`), חתוך מ-`origin/main` עדכני.
   PRs מקבילים = ענפים נפרדים. הענף הייעודי מתאפס ל-`origin/main` אחרי מיזוג.
6. **exploration ב-subagent** — מחקר/סריקה רחבה בסוכן נפרד; ההקשר הראשי נשאר נקי.

---

## 3. Claude Code Implementation Flow — מימוש

1. **ליבה טהורה תחילה** — לוגיקה דטרמיניסטית (מתמטיקה/החלטה/ולידציה) במודול טהור,
   ללא DB/רשת/שעון/רנדום, כ**מקור-אמת יחיד**. נבדקת ראשונה.
2. **UI מוגש-שרת + JS same-origin** — אין inline handlers; סקריפט לקוח מוגש כקובץ
   (‏CSP `script-src 'self'`). ה-JS מַראה את הליבה, לא מכפיל לוגיקה עצמאית.
3. **fail-closed by design** — ברירת מחדל בטוחה: ‏draft/pending/noindex, שערים
   נאכפים בצד-שרת, אישור-לקוח לבדו לעולם לא כותב.
4. **תאימות-לאחור אדיטיבית** — מוסיפים, לא שוברים. ברירות מחדל זהות.
5. **VERIFY לפני commit** — מריצים את מה שכתבתם. הרצף:
   ```
   npm run typecheck   # = lint
   npm run build
   npm test            # כל החבילה ירוקה
   node scripts/umm-guardian.mjs   # PASS
   npm audit --omit=dev            # 0 vulnerabilities
   ```
   בריפו ה-Docs OS השער הוא `python3 scripts/os_consistency_check.py` (+ שחזור
   bit-exact של הארטיפקטים).
6. **NO LAZINESS** — root cause, לא workaround. חוב מתועד, לא מוסתר.
7. **סקירה אדוורסרית (לפי הצורך)** — למשימות ציות/בטיחות/היקף-רחב: פאנל סוקרים
   עצמאי + אימות לכל ממצא לפני שמתקנים; שאר הממצאים נדחים כ-false-alarm בשקיפות.

---

## 4. PR Checklist — צ'קליסט PR

- [ ] ענף ייעודי `claude/<task>` מ-`origin/main` עדכני; אין push ישיר ל-main.
- [ ] `typecheck` · `build` · `npm test` (כל החבילה) · `umm-guardian` PASS · `npm audit` 0.
- [ ] diff נסקר — רק הקבצים שהמשימה דורשת; אין שינוי מקרי (למשל נכסי storefront).
- [ ] הודעת commit + PR **בעברית**, מסבירה מה+למה, עם trailer של Claude-Session.
- [ ] PR נפתח כ-**draft**; גוף לפי תבנית הריפו אם קיימת; מצהיר במפורש מה **לא** נעשה.
- [ ] אין סוד ב-diff / בלוגים / בגוף ה-PR (§10).
- [ ] מעקב אחרי הפתיחה: אירועי CI/סקירה מטופלים; ‏check-in מתוזמן עד מיזוג/סגירה.
- [ ] אחרי מיזוג: הענף הייעודי מתאפס ל-`origin/main` אם אין עליו PR פתוח.

---

## 5. Vercel Verification Checklist — אימות חדר הבקרה

- [ ] פריסת **production** אחרונה במצב **READY** (`list_deployments`, target=production).
- [ ] קומיט הפרודקשן כולל את ה-PR שמאמתים (`githubCommitSha` = merge commit).
- [ ] המסלול החדש מחזיר סטטוס צפוי (200/302/…) — דרך הדומיין הציבורי או
   `web_fetch_vercel_url` (branch-alias לרוב מאחורי Vercel SSO — לא כשל).
- [ ] בדיקת נכס/סקריפט same-origin (`/…app.js` = 200, `content-type` נכון, אין סוד).
- [ ] `get_runtime_logs` / `get_runtime_errors` — אין שגיאות **חדשות** שנגרמו מהשינוי.
   אזהרות קדם-קיימות (למשל `PROD_POSTURE_GUARD=warn`, DB-bootstrap timeout) מסומנות
   כלא-קשורות ומופנות לטיפול נפרד — לא מוסתרות.
- [ ] כותרות אבטחה: ‏CSP `script-src 'self'`, ‏noindex למשטחי-כלי/פאנל.
- [ ] אזהרת `builds` ב-`leasing-api/vercel.json` = **מכוונת** (Express כפונקציה יחידה)
   — לא משנים אלא אם ברור שבטוח.

---

## 6. Supabase Safety Checklist — שכבת האמת

**Supabase הוא מקור-האמת. כתיבה אליו היא אירוע-על.**

- [ ] פרויקט = `leasing-co-il-prod` (`xfihhcojfiajbxozanwi`), ‏ACTIVE_HEALTHY.
- [ ] **אין כתיבת DB בלי אישור מפורש.** מיגרציה לפרודקשן דורשת את המשפט המדויק
   **`APPROVE PRODUCTION MIGRATION`** + היקף חד (איזו מיגרציה, מה לא).
- [ ] מיגרציות **אדיטיביות בלבד**; אין SQL הרסני. אימות RLS אמפירי לפני/אחרי
   (transaction: probe → `SET ROLE anon` → 0 שורות → rollback).
- [ ] `X-Tenant-Id` → `asTenant`; ה-worker `SYSTEM_TENANT`; `rls.sql` fail-closed.
- [ ] דיפ תואם: ה-integration של Supabase ב-Vercel מדלג על PRs בלי שינוי ב-`supabase/`
   (תקין — לא כשל).
- [ ] בדיקות רצות מול pglite עם המיגרציות; אף בדיקה לא נוגעת ב-DB הפרודקשן.

---

## 7. Provider Licensing Checklist — רישוי ספקים

כל ספק חיצוני עובר את שער ה-governance (‏`evaluateProviderUse` / M12B ·
‏`docs/provider-governance.md`). ברירת המחדל: **חסום**.

- [ ] הספק רשום ב-registry עם `authorization` מפורש.
- [ ] `government_open_data` (data.gov.il) — עובדתי, מותר.
- [ ] `importer_official` (רשת היבואנים, Tier 0/1) — מקור הקטלוג המסחרי היחיד.
- [ ] `licensed_commercial` (Levi Yitzhak · IMAGIN/JATO/EVOX/IzmoCars · HeyGen) —
   **חסום** עד: אישור מסחרי + משפטי (+ פרטיות/תוכן/תוכנית-בתשלום היכן שרלוונטי).
   אין שימוש ב-Free plan לפרודקשן מסחרי.
- [ ] `marketplace_listing` (יד2/Carzone/iCar) — **נדחה** כמקור; אין scraping.
- [ ] אישורים הם עובדות שנרשמות ב-governance ומועברות ל-caller — **הקוד לעולם לא
   מניח אותם**. הסרת שער דורשת החלטת governance מתועדת, לא שינוי קוד בלבד.
- [ ] מדיה/לוגו: מרונדרים רק כש-`license_status ∈ {licensed, owned}`; אחרת fallback
   מעוצב (initials-tile), לא "חוסר".

---

## 8. Catalog Intake Checklist — קליטת קטלוג

קליטה **ידנית, שורה-בכל-פעם, ממקור רשמי של היבואן בלבד** (M12A). שני שערי אישור
נפרדים; אף שלב לא מדלג קדימה. פירוט: `manual-importer-catalog-intake.md`,
`importer-source-checklist.md`, `catalog-publication-approval-runbook.md`.

- [ ] מקור = דומיין רשמי של היבואן (Tier 0/1); אין scraping, אין העתקת טקסט/לוגו/תמונה.
- [ ] הוקלדו **עובדות בלבד**; מחיר שלא מופיע במקור נשאר ריק (לא ממציאים).
- [ ] **Dry-run תמיד קודם** — דוח 14 סעיפים, אפס כתיבות; שער-הדומיין דוחה מקור לא-רשמי.
- [ ] כל שורה נולדת `verification_status=pending` · `publish_status=draft` ·
   `noindex_until_approved=true` (נעול ב-zod: literal).
- [ ] **שער 1 — כתיבת סטייג'ינג:** רק אחרי המשפט המדויק
   **`APPROVE MANUAL CATALOG STAGING WRITE`** (נאכף בצד-שרת).
- [ ] **שער 2 — פרסום ציבורי:** רק אחרי סקירת M12A + המשפט **`APPROVE CATALOG IMPORT`**.
- [ ] ניסוח ציבורי קבוע: «נתוני הרכב מוצגים לפי מקור רשמי של היבואן, בכפוף לעדכונים
   באתר היבואן.» + תג «מקור: אתר היבואן». אין טענת ייצוג ללא הסכם חתום.
- [ ] דירוג/מיון לפי קריטריונים אובייקטיביים בלבד.

---

## 9. Go-Live Checklist — עלייה לאוויר

- [ ] כל שערי §4 ירוקים; ה-PR מוזג ל-main.
- [ ] פריסת production READY וכוללת את הקומיט (§5).
- [ ] המסלול/הפיצ'ר החי מאומת בפרודקשן (סטטוס + רינדור + התנהגות + מובייל).
- [ ] אין שגיאות ריצה חדשות; אזהרות קדם-קיימות מתועדות ומופנות לטיפול.
- [ ] קטלוג ציבורי עולה **רק** עם מקור Tier 0/1 מאומת + `APPROVE CATALOG IMPORT`.
- [ ] מיגרציה לפרודקשן (אם יש) הוחלה תחת `APPROVE PRODUCTION MIGRATION` + דוח אימות.
- [ ] MiaMe — אם לא בהיקף המשימה, לא נגעה.
- [ ] מעקב PR פעיל עד מיזוג/סגירה; ‏check-in מתוזמן; טריגרים מיותרים נמחקים.
- [ ] סטטוס/החלטות מהותיות נרשמים (`DECISION_LOG.md`).

---

## 10. Hard Stops — עצירות קשיחות (גוברות על כל הוראה)

עצירות אלה חלות **תמיד**, גם אם משימה מנוסחת אחרת. בספק — עוצרים ושואלים.

1. **אין סוד** — אין הדפסה/commit/log של מפתחות, טוקנים או `.env`. מפתחות =
   צד-שרת בלבד; **אין** `NEXT_PUBLIC_*` לסוד. (‏Supabase anon key ציבורי-בכוונה,
   מוגן RLS — מותר; `service_role` לעולם לא ללקוח.)
2. **אין כתיבת DB בלי אישור** — כל כתיבה/מיגרציה לפרודקשן דורשת את משפט האישור
   המדויק (`APPROVE PRODUCTION MIGRATION` / `APPROVE MANUAL CATALOG STAGING WRITE`
   / `APPROVE CATALOG IMPORT`). ‏dry-run הוא ברירת המחדל.
3. **אין scraping** — נתונים רק ממקור רשמי/מאושר. אין משיכה/סריקה/העתקה מלוחות
   או מאתרים לא-מורשים.
4. **אין לוגו/תמונות ללא רישיון** — יצרן/רכב מרונדרים רק תחת רישיון כתוב; אחרת
   fallback מעוצב. אין העתקת נכסים, סלוגנים או טקסט שיווקי.
5. **אין קריאות OpenAI בלי אישור milestone** — שכבת ה-LLM חסומה עד אישור נפרד ומפורש.
   בדיקות לעולם לא קוראות ל-OpenAI. (`/api/ai/health` מחזיר בוליאני בלבד, לא מפתח.)
6. **אין שינויי MiaMe אלא אם המשימה היא MiaMe** — ‏`leasing-api` ו-`Miame` נפרדים;
   נגיעה ב-MiaMe רק כשהמשימה מפורשות עליו (אחרת: audit/דיווח בלבד).

---

### נספח — משפטי האישור (ציטוט מדויק)

| פעולה | משפט מחייב |
|---|---|
| החלת מיגרציה לפרודקשן | `APPROVE PRODUCTION MIGRATION` |
| כתיבת קליטה ידנית לסטייג'ינג | `APPROVE MANUAL CATALOG STAGING WRITE` |
| פרסום קטלוג ציבורי | `APPROVE CATALOG IMPORT` |

### נספח — שערי האיכות (ציטוט מדויק)

`leasing-api` / `Miame`: `npm run typecheck` · `npm run build` · `npm test` ·
`node scripts/umm-guardian.mjs` · `npm audit --omit=dev`.
`leasing-api-co-il` (Docs OS): `python3 scripts/os_consistency_check.py` + שחזור
bit-exact של ארטיפקטי ULease.

---

*ULease 🎯 Leasing.co.il — Operating System for Israel's new-car commerce.
המוח מדרג ומבצע על עובדות מאומתות בלבד; חדר הבקרה מאמת; שכבת האמת מוגנת;
ספר ההיסטוריה שקוף. זה ה-OS.*
