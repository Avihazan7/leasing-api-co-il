# Production Readiness Follow-up — 2026-07-07

היגיינת Vercel ומצב מוכנות לשלושת פרויקטי Leasing.co.il / ULease OS.
צוות Vercel: **Hi-tech Top** (`team_ryT0nQh6t2SlGaEoxCG2R1BY`).

> **שורה תחתונה:** שלושת ה-**production** deployments במצב **READY**. בעיית ה-build
> של `leasing-api-co-il` **כבר תוקנה ומוזגה** (PR #70) ופרודקשן ירוק מאז; כל ה-ERROR
> שנצפו הם על **ענפים מתפצלים/ישנים** שאין בהם `vercel.json`, לא על main. אין כתיבת
> DB, אין מיגרציות, אין חשיפת סוד — המסמך הזה תיעוד + הקשחה מינימלית בלבד.

## 1. סטטוס Vercel לפי פרויקט

| פרויקט | Project ID | Production | הערה |
|---|---|---|---|
| `leasing-api` | `prj_YZvTLeBa9QmtjFthh6V1KzaXiCT4` | ✅ READY | Express כפונקציית Node יחידה דרך `builds` (ראה §2). PR #294 מוזג ל-main. |
| `miame` | *(פרויקט Next.js)* | ✅ READY | Next.js אמיתי (`next build`). PR #94 מוזג. לא נגענו — audit בלבד. |
| `leasing-api-co-il` | `prj_oW7yEnr0MM1SmRznUm3RR4vwxjDc` | ✅ READY | ריפו docs/OS. תיקון ה-build נחת ב-PR #70; production ירוק. |
| `ulease-mos` | `prj_BNAdif9lHWdgIxCkxCThsXIxfVIb` | — | פרויקט נוסף בצוות; מחוץ להיקף המשימה. |

### 1.1 leasing-api-co-il — אבחון מדויק של ה-ERROR previews

מקור כשל ה-build ההיסטורי: זהו ריפו **docs/OS** (עשרות `.md`, `CASES/`, `COWORK/`)
ללא `package.json` וללא framework — ולכן Vercel נכשל ב-`No Next.js version detected`.

**התיקון כבר קיים ב-main** (commit `154bc9d`/PR #70 — *"Fix always-failing Vercel
deploy on docs repo (static landing + vercel.json)"*):

- `vercel.json` בשורש: `framework: null` · `buildCommand: null` · `installCommand: null`
  · `outputDirectory: "public"` — עוצר את זיהוי ה-framework ומגיש סטטית.
- `public/index.html` — עמוד נחיתה שמצהיר שזה ריפו התיעוד ומפנה ל-`leasing.co.il`.
  **אינו** מגיש את מסמכי ה-OS הפנימיים (רק `public/` נפרס).

מדוע עדיין נראים ERROR ב-previews: כל ה-ERROR האחרונים הם על **ענפים שאינם main** —
בעיקר `claude/marketing-strategy-framework-Is1dZ` (ענף בעל היסטוריה מקבילה ישנה
שאין בו את `vercel.json`) וענפי feature מלפני PR #70. Vercel מנסה לבנות אותם
בברירת-מחדל ונכשל באותו זיהוי framework. **production (main) לא מושפע — הוא READY.**

**פעולת dashboard/git מומלצת (מחוץ להיקף שינוי-repo, טעונה החלטת מייסד):**
- מחיקת הענף הישן `claude/marketing-strategy-framework-Is1dZ` (היסטוריה מקבילה שלא
  נועדה למיזוג), **או**
- ב-Vercel → Project → Settings → Git: הגבלת Preview Deployments (למשל רק ל-PR
  branches / רק לענפי `claude/*` פעילים), כדי שענפים מתפצלים לא ייצרו ERROR רועש.
- לוודא ש-Root Directory של הפרויקט = `./` (שורש) ו-Framework Preset = *Other*,
  כדי שה-`vercel.json` בשורש יחול. (אם ה-Root Directory מצביע לתת-תיקייה — ה-
  `vercel.json` בשורש מתעלמים ממנו, וזו דריפט ברמת ה-dashboard בלבד.)

**הקשחה שנכללת ב-PR הזה:** הוספת `<meta name="robots" content="noindex,nofollow">`
ל-`public/index.html` — רכזת פנימית לא צריכה להתאנדקס.

## 2. leasing-api — אזהרת `builds` (סקירה, בלי שינוי)

`leasing-api/vercel.json` משתמש במפתח ה-legacy `builds`:

```json
"builds": [{ "src": "api/index.ts", "use": "@vercel/node", "config": { "includeFiles": "public/**" } }],
"routes": [{ "src": "/(.*)", "dest": "api/index.ts" }]
```

האזהרה *"Due to `builds` existing in your configuration file, the Build and
Development Settings defined in your Project Settings will not apply"* היא
**התנהגות מתועדת ומכוונת** של Vercel: כשמוגדר `builds`, הגדרות ה-Build/Dev ב-
dashboard מתעלמות במכוון. זהו בדיוק ה-setup הרצוי כאן — Express יחיד שכל התעבורה
מנותבת אליו (`api/index.ts`) + 7 crons. הפרויקט **READY** ללא שגיאות ריצה ב-6 השעות
האחרונות. **המלצה: לא לשנות** — שינוי ל-`functions`/framework-detection היה מחזיר
שליטה ל-dashboard אך מסכן את הניתוב הקיים ללא תועלת. (אם בעתיד רוצים לנהל build
מה-dashboard — זו הגירה מכוונת בנפרד, לא במסגרת המשימה הזו.)

## 3. סטטוס GitHub PRs

| ריפו | PR אחרון ב-main | מצב |
|---|---|---|
| `leasing-api` | #294 `docs(presenters): HeyGen AI vehicle presenter blueprint` | merged |
| `leasing-api` | #293 `feat(catalog): manual importer catalog staging workflow` | merged |
| `leasing-api` | #292 `fix(catalog): harden 2026 reads + nano-crystal UI` | merged |
| `miame` | #94 `feat(go-live): final launch polish, trust layer, deal buzz` | merged |
| `leasing-api-co-il` | #77 `docs(os): vehicle-centric architecture doctrine (D-070)` | merged |
| `leasing-api-co-il` | #70 `fix: static landing + vercel.json (docs repo build fix)` | merged |

## 4. Supabase

- פרויקט `leasing-co-il-prod` — **ACTIVE_HEALTHY**; RLS מופעל על הטבלאות הציבוריות.
- **לא בוצעה כל כתיבה ל-DB, אין מיגרציות, אין ייבוא קטלוג** במסגרת המשימה הזו.
- ה-integration של Supabase ב-Vercel מדלג על PRs ללא שינוי בתיקיית `supabase/`
  (התנהגות תקינה) — נצפה גם ב-PRs האחרונים של `leasing-api`.

## 5. OpenAI / בטיחות env + מפתחות

בדיקת קוד (read-only) לשימוש בצד-שרת בלבד:

- **`leasing-api`**: `OPENAI_API_KEY` מופיע **אך ורק** ב-`src/server.ts` בתוך
  readiness-guard צד-שרת שמחזיר בוליאני בלבד — `{ configured: Boolean(process.env.OPENAI_API_KEY) }`.
  המפתח **לעולם לא מודפס** ואין לו חשיפת `NEXT_PUBLIC_*`. ✅
- **`miame`**: אין מפתח OpenAI. חשיפת הלקוח היחידה היא `NEXT_PUBLIC_SUPABASE_ANON_KEY`
  — anon key ציבורי-בכוונה המוגן ב-RLS (התכן הנכון); אין חשיפת `service_role`. ✅
- לא נוצרו/הודפסו מפתחות. פרויקט OpenAI `Leasing.co.il ULease OS` לא נגענו בו.

## 6. סיכון ידוע

**`leasing-api-co-il` preview root mismatch** — previews על ענפים מתפצלים (בעיקר
`claude/marketing-strategy-framework-Is1dZ`) מייצרים ERROR כי אין בהם `vercel.json`.
**אין השפעה על production** (main ירוק). התיקון: מחיקת/סגירת הענף המתפצל או הגבלת
Preview Deployments ב-dashboard (§1.1). זהו רעש היגייני, לא כשל ייצור.

## 7. המלצה — בעלות קנונית ומקור-אמת לפרודקשן

| שכבה | פרויקט Vercel קנוני | תפקיד |
|---|---|---|
| **אפליקציה + קטלוג (production source of truth)** | `leasing-api` | ה-Express/SSR החי של Leasing.co.il — הקטלוג, ה-API, ה-crons, האדמין. זהו מקור-האמת לפרודקשן. |
| **אתר MiaMe** | `miame` | אפליקציית ה-Next.js הנפרדת של MiaMe.co.il. |
| **תיעוד/מתודולוגיה (Docs OS)** | `leasing-api-co-il` | לא משטח מוצר — deploy סטטי מינימלי בלבד (עמוד נחיתה). מומלץ: preview deploys מוגבלים; לשקול ניתוק/ארכוב אם אין צורך אפילו ב-landing. |
| **פרויקט נוסף** | `ulease-mos` | לאמת מול המייסד אם עדיין נדרש; אם לא — מועמד לניקוי כדי לצמצם בלבול deploy. |

**כלל אצבע:** production של Leasing.co.il = `leasing-api` בלבד. `leasing-api-co-il`
הוא ריפו ידע פנימי — ה-deploy שלו נועד רק שלא "ייכשל תמיד", לא לשרת מוצר.

## 8. אימות שרץ (item D)

`leasing-api-co-il` הוא ריפו docs ללא `package.json` — אין בו סקריפטי
`typecheck`/`lint`/`test`/`build`. שער האיכות שלו הוא ה-CI `os-consistency`
(`scripts/os_consistency_check.py` + שחזור bit-exact של 4 ארטיפקטים). השינויים כאן
(`noindex` ל-`public/index.html` + מסמך זה) אינם מודולי OS ואינם ארטיפקטים
מחוללים — ה-consistency check אמור לעבור ללא שינוי.

| פרויקט | typecheck | lint | test | build |
|---|---|---|---|---|
| `leasing-api-co-il` | n/a | n/a | n/a | n/a — ראה `os_consistency_check.py` |
| `leasing-api` | ✅ (ידוע ירוק ב-main; לא נגענו) | ✅ | ✅ 1188/1188 | ✅ |
| `miame` | ✅ (ידוע ירוק; לא נגענו) | — | — | ✅ |
