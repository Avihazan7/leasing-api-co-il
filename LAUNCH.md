# LAUNCH.md — ULease Go-Live 🚀

**Module:** `LAUNCH.md`
**Version:** 1.1.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Master ignition file. אישור של זה = ULease באוויר.
**Mission:** להפוך את Leasing.co.il לחברת ליסינג הראשונה בישראל שרצה מקצה-לקצה על Claude OS.

---

## 0. למה הקובץ הזה קיים

3 מודולים נכתבו (`COMMAND_API`, `WINDOWS_DEPLOYMENT`, `DEV_ENVIRONMENTS`).
3 קהלים שונים. סטאק אחד.

הקובץ הזה הוא **כפתור ההפעלה**: אישור מהמנכ"ל + 4 שבועות = ULease באוויר.
אם לא קוראים את זה — כל השאר נשאר על המדף.

---

## 1. The Stack — מבט-על

```
                   ULease / Leasing.co.il
                          │
            ┌─────────────┼─────────────┐
            │             │             │
        Business        Dev           Strategy
       (Office)      (6 tracks)       (IR/PM)
            │             │             │
            ▼             ▼             ▼
   WINDOWS_DEPLOYMENT  DEV_ENV    marketing-framework
            │             │             │
            └─────────────┼─────────────┘
                          │
                   COMMAND_API.md
                  (89 פקודות, חוזה משותף)
                          │
                       CLAUDE.md
                    (OS entry point)
```

**עיקרון:** מנכ"ל, רואה-חשבון, ומפתח בכיר — כולם מקלידים את אותה `/tldr`. רק
ה-context משתנה.

---

## 2. Day 0 — אש ירוקה

ביום שה-PR ממוזג ל-`main`:

| שעה | מי | מה |
|-----|-----|-----|
| 09:00 | מנכ"ל | שולח מייל all-hands: "מהיום אנחנו על Claude OS" |
| 10:00 | IT | מפעיל את `Deploy-ClaudeForOffice.ps1` לכל ה-endpoints |
| 10:30 | Tech Lead | רץ `setup-claude.sh` עם 2-3 מפתחי pilot |
| 12:00 | כולם | הפסקת צהריים. עוצרים. נושמים. |
| 13:00 | Power-users | מתחילים להזין Skills ראשונים לפי תפקיד |
| 16:00 | Tech Lead | סטטוס קצר — מה עבד, מה לא, מי תקוע |
| 17:00 | מנכ"ל | "סוף יום 1" — Slack post עם 3 wins |

**ברירת המחדל:** איש לא חוזר הביתה בלי לפחות פעולה אחת מוצלחת ב-Claude. אם זה
לא קרה — מישהו צריך לעזור לו מחר בבוקר.

---

## 3. Week 1 — Pilot Wave

| יום | פוקוס | תוצר נמדד |
|-----|--------|------------|
| ב' | Office: Word + Excel לצוות מכירות | 5 הצעות מחיר עם `/deal-quote` |
| ג' | Office: PowerPoint להנהלה | מצגת weekly עם `/board-deck` |
| ד' | Dev: VS Code + Claude Code לצוות backend | 1 PR שעבר `/code-review` |
| ה' | Skills: יצירה של 3 Skills ארגוניים | זמינים לכל הצוות |
| ו' | Retro: מה למדנו | רשימת 5 חיכוכים + 5 wins |

**Go/No-Go ל-Week 2:** לפחות 70% מהצוות התחבר ל-Claude ובצע פעולה אחת מוצלחת.

### 3.1 מסלול הדרכה — "Master Claude in a Week"

במקביל ל-pilot התפעולי, כל משתמש חדש (כולל סוכני סניפים — `BRANCH_KNOWLEDGE § 7`)
עובר מסלול 7-ימים מ-beginner ל-advanced. כל יום = deliverable נמדד, לא צפייה פסיבית.

| יום | פוקוס | תוצר נמדד | קשר ל-OS |
|-----|--------|------------|-----------|
| **1 · Foundations** | מה זה Claude, אנטומיית prompt טוב (role/context/instructions/examples/format) | 5 prompts חזקים בסגנונות שונים | `DEV_ENV נספח ד'` (setup) |
| **2 · Better Prompts** | Zero/Few-shot, CoT, system vs. user, הימנעות מעמימות | template לשימוש הנפוץ ביותר שלך | `COMMAND_API` (הפקודות = templates מוכנים) |
| **3 · Deeper Use Cases** | סיכום, חילוץ דאטה, ניתוח, long-context | 3 משימות אמיתיות הושלמו | `/tldr`, `/deal-quote`, `/fleet-report` |
| **4 · Advanced Control** | steering טון, constraining (format/length/rules), XML/JSON schemas, iteration | prompt מורכב שמייצר פלט מובנה מושלם | Karpathy doctrine (`AGENT_BLUEPRINT § 10`) |
| **5 · Build Workflows** | chaining, tools & APIs, אינטגרציות, מתי לאוטמט מול מתי prompt | workflow שחוסך זמן | `N8N_AUTOMATION` (5 workflows מוכנים) |
| **6 · Power Techniques** | meta-prompting, tree-of-thought, custom knowledge, long context, Artifacts | פתרון high-impact לבעיה מורכבת | `AGENT_BLUEPRINT § 9` (patterns) |
| **7 · Optimize & Own** | הערכה ושיפור, ספריית prompts אישית, אמינות, ה-playbook שלך | playbook אישי + אוסף משאבים | `BRANCHES/<סניף>.md` (ה-playbook של הסניף) |

**עיקרון:** *Practice daily. Build real things.* ההדרכה היא על משימות ULease אמיתיות —
לא תרגילי צעצוע. ה-deliverable של יום 7 (playbook) הופך לחלק מספר הידע של הסניף.

---

## 4. Month 1 — Adoption

יעדים מספריים שצריך לפגוע בהם תוך 30 יום:

| מטריקה | יעד | מי מודד |
|---------|-----|---------|
| % משתמשים פעילים שבועיים | ≥ 80% | IT (M365 telemetry) |
| Skills ארגוניים מוגדרים | ≥ 8 | Tech Lead |
| פעולות copy-paste בין דפדפן לקובץ | ירידה של 50% (סקר) | HR/COO |
| PRs שעוברים `/code-review` לפני merge | 100% | Tech Lead |
| אירועי security הקשורים ל-AI | 0 | DPO |

אם מטריקה לא נפגעת — escalation למנכ"ל בסוף שבוע 4.

---

## 5. Quarter 1 — Maturity

יעדים אסטרטגיים ל-90 יום:

- **כל מחלקה** מחזיקה לפחות 3 Skills ייעודיים שהיא בנתה לעצמה.
- **זמן הכנת דוח חודשי** ירד ב-50%+.
- **זמן הכנת מצגת משקיעים** ירד ב-60%+.
- **זמן ממוצע מ-issue ל-PR פתוח** ירד ב-30%+.
- **MCP server פנימי ל-ULease** נכתב ובשימוש (חשיפת fleet status, deal lookup,
  pricing — דרך Claude לכל הצוות). **קודם מ-"future" ל-Q1 milestone לפי הלקח
  מ-[`CASES/ROX_KEY.md § 5.2`](./CASES/ROX_KEY.md) — "נתונים כנכס אסטרטגי".**
- **NPS פנימי** על הכלי > +30.
- **NPS לקוחות חיצוניים** (חדש — לקח מ-[`CASES/ROX_KEY.md § 5.4`](./CASES/ROX_KEY.md))
  — נמדד בסוף כל אינטראקציה, יעד > +40.

> 💡 **Benchmark:** ROX Key בווייטנאם כבר מבצעים את המהלך הזה בענף ניהול הנכסים
> ($9.19B שוק, CAGR 6.92%). הסיפור שלהם הוא ה-proof point שלנו —
> פרטים מלאים ב-[`CASES/ROX_KEY.md`](./CASES/ROX_KEY.md).

---

## 6. RACI מרוכז

מי אחראי על מה ברמת הארגון:

| משימה | מנכ"ל | CTO/Lead | IT | DPO | מנהל מחלקה | משתמש |
|--------|:-----:|:--------:|:--:|:---:|:----------:|:------:|
| אישור Go-Live | **A** | C | I | C | I | I |
| התקנת תוסף Office | I | C | **R** | I | I | I |
| Onboarding מפתחים | I | **R** | C | I | I | I |
| יצירת Skills ארגוניים | I | **A** | I | C | **R** | C |
| Security review רבעוני | A | C | C | **R** | I | I |
| מדידת KPIs | A | **R** | C | I | C | I |
| Kill-switch (סעיף 8) | **A** | R | R | C | I | I |

`R` = Responsible · `A` = Accountable · `C` = Consulted · `I` = Informed

---

## 7. Go/No-Go Checklist — לפני שלוחצים על כפתור

המנכ"ל לא חותם על Day 0 בלי שכל אלה ירוקים:

```
□ Anthropic Team / Enterprise plan פעיל ובתוקף ל-12 חודשים
□ DPA חתום ובארכיון אצל DPO
□ Zero Data Retention מאומת מול Anthropic
□ M365 admin פתח את התוסף לכל ה-tenant
□ Firewall / Web filter פתחו את הדומיינים (ראה WINDOWS_DEPLOYMENT § 2.3)
□ .claudeignore קיים בריפו
□ API keys אישיים נוצרו ל-100% מהמפתחים
□ Onboarding script (.bin/setup-claude.sh) נבדק על endpoint נקי
□ 3 Skills ארגוניים בסיסיים מוכנים (/deal-quote, /fleet-report, /code-review)
□ Communication plan למייל all-hands מוכן ואושר
□ Kill-switch (סעיף 8) מתורגל ומובן לכל החתימים
□ Tech Lead זמין בכוננות 48 שעות אחרי Day 0
□ אין רכישות AI חיצוניות מקבילות מחוץ ל-Anthropic stack ללא אישור Tech Lead
   (לקח מ-CASES/ROX_KEY.md § 5.1 — "השקעות לא מקוטעות")
□ Claude Code Skills זמינים ומתועדים — `/plan`, `/agents`, `/compact`, `/review`,
   `/security-review`, `/todos`, `/output-style` (ראה COMMAND_API.md § קטגוריה 12)
```

14 ירוקים = אש ירוקה. אם אחד אדום — דוחים את Day 0 בשבוע.

---

## 8. Kill-Switch — מה עושים אם נדלקת אדומה

תרחישים שמצדיקים השעיה זמנית של Claude בארגון:

| תרחיש | פעולה | מי מאשר |
|--------|--------|---------|
| דליפת API key | revoke ל-key הספציפי תוך 15 דקות | Tech Lead |
| דליפת PII דרך prompt | השעיית user, חקירת DPO, דיווח רגולציה אם נדרש | DPO + מנכ"ל |
| השבתת Anthropic ארוכה (> 4 שעות) | מעבר זמני לעבודה ידנית בקבצים | Tech Lead |
| באג חמור ב-Skill ארגוני | un-publish ה-Skill, fix, re-publish | Tech Lead |
| ביקורת רגולטורית מפתיעה | freeze על שימוש בלקוחות חיים עד אישור DPO | DPO |

**עיקרון:** Kill-switch הוא **השעיה**, לא **ביטול**. אחרי טיפול — חוזרים.
מעולם לא חוזרים לעבוד "כמו פעם" — זו דרך אחורה.

---

## 9. Master Switch — איך מפעילים בפועל

ביום Go-Live, ה-Tech Lead מריץ את הרצף הזה:

```bash
# 1. מיזוג ה-PR ל-main
gh pr merge 3 --squash --delete-branch

# 2. tag לגרסה
git tag -a v1.0.0-os -m "Claude OS v1.0.0 — Go Live"
git push --tags

# 3. הפצת Office add-in מ-M365 Admin Center
#    (ידני — לוקח עד 12 שעות לכל ה-tenant)

# 4. הפצת onboarding script ל-IT
#    Intune → Scripts → Deploy-ClaudeForOffice.ps1 → All Devices

# 5. שליחת מייל all-hands (template ב-WINDOWS_DEPLOYMENT § 14)

# 6. פתיחת Slack channel #claude-os לתמיכה שוטפת
```

זהו. ULease באוויר.

---

## 10. אחרי שזה באוויר

הקובץ הזה לא נגמר ב-Day 0. הוא נקרא מחדש כל רבעון:

- **Q+1 (30 יום):** ביקורת מטריקות § 4. החלטה — להאיץ או לתקן.
- **Q+3 (90 יום):** ביקורת § 5. החלטה — להרחיב יכולות (Computer Use, MCP פנימי)
  או להעמיק קיים. **השוואה ל-benchmark** ב-[`CASES/ROX_KEY.md`](./CASES/ROX_KEY.md):
  האם הפער מצטמצם, יציב, או מתרחב?
- **Q+12 (שנה):** רטרוספקטיבה — מה ULease הייתה בלי, מה היא עם, ומה הצעד הבא.
  לפתוח cases חדשים תחת `CASES/` (Toyota Connected / Tesla Energy / Element Fleet)
  כדי לשמור על pipeline למידה מתחרים גלובליים.

הצעד הבא תמיד קיים. זו לא תוכנה — זו תרבות.

---

## גרסאות

| גרסה | תאריך | שינוי |
|------|--------|-------|
| 1.0.0 | 2026-05-28 | Initial ignition — Go-Live master file |
| 1.1.0 | 2026-06-03 | + § 3.1 מסלול הדרכה "Master Claude in a Week" — 7 ימים, deliverable יומי, ממופה למודולי ה-OS; משולב ב-onboarding סניפים |

---

**Tie-back ל-OS:** הקובץ הזה הוא ה-Master Switch. הוא לא מתאר את המערכת —
הוא **מפעיל** אותה. כל יתר המודולים (`COMMAND_API`, `WINDOWS_DEPLOYMENT`,
`DEV_ENVIRONMENTS`) הם הצינורות. זה הקובץ שפותח את הברז.

> **From here — we lift off. 🚀**
> **Leasing.co.il × Claude OS × ULease**
