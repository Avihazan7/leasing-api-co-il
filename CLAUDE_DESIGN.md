# Claude Design — 8 צעדים ⇄ שכבת ה-UI של ULease

**`claude.ai/design`: 8 הצעדים לעיצוב מקצה-לקצה, מוצלבים מול ה-storefront, ה-dashboard וה-BI של ULease.**

> Claude Design הוא ה-surface שמייצר wireframes, slide decks ו-prototypes. עבור ULease — שבו שכבת ה-UX היא "שכבה נפרדת" (`system-design-cheatsheet #12`) — זה ה-tool שסוגר את הפער בין ה-API (63→**65/65** טסטים, מחווט-RLS) ל**מה שהלקוח/דילר רואה**. המודול ממפה כל צעד למה שכבר קיים (`public/index.html` storefront + `public/dashboard.html` ops) ולמה שעוד doctrine.

---

## 1. שמונת הצעדים במבט-על

| # | צעד | המהות |
|---|-----|-------|
| 1 | **Open `claude.ai/design`** | URL ייעודי. Pro/Max; Team/Enterprise — toggle ב-Org settings → Capabilities → Anthropic Labs |
| 2 | **Pick your format** | Wireframe (אתרים) · Slide deck · Template (וידאו) · Freeform — ה-format מעצב את כל ה-prompt |
| 3 | **Get a `DESIGN.md`** | (א) drop assets ל-Cowork folder → *"save the full design system as DESIGN.md"* · (ב) steal מ-`getdesign.md` |
| 4 | **Prompt correctly** | בכל prompt: **Goal · layout · content · constraints** |
| 5 | **Video-to-slides** | ל-pitch deck: צור וידאו 30ש' קודם → *"convert the video into a slide pitch deck"* |
| 6 | **Iterate in two places** | מבני → chat (*"3 alternative layouts"*) · pixel → canvas (כפתור edit, נדלק ירוק) |
| 7 | **Always validate** | *"List WCAG 2.1 AA violations + fixes"* · desktop/tablet/mobile · 2 A/B variations |
| 8 | **Export** | PPTX · PDF · standalone HTML · bundle ל-Claude Code |

---

## 2. מ-8 הצעדים אל ה-UI של ULease

| צעד | המקבילה ב-ULease | סטטוס |
|-----|------------------|--------|
| 1 · Open design | surface חיצוני (claude.ai/design) — לא בריפו | ↗️ tool |
| 2 · Format | **Wireframe** ל-storefront/dashboard · **Slide deck** ל-`INVESTOR_RELATIONS` | 🟡 לא-מנוצל |
| 3 · `DESIGN.md` | חסר — אין design-system מתועד ל-Leasing.co.il. ה-seam: Cowork folder-first (`DEV_ENV נספח ד'`) | ⚠️ חוב |
| 4 · Prompt (Goal/layout/content/constraints) | זהה ל-**Working Rule #1 PLAN FIRST** + מבנה ה-prompt ב-`COMMAND_API` · `MASTER_CLAUDE_58` אשכול PROMPTING | ✅ דוקטרינה |
| 5 · Video-to-slides | pitch deck למשקיעים (`INVESTOR_RELATIONS`) — טכניקה לא-מיושמת | 🟡 הזדמנות |
| 6 · Iterate (chat/canvas) | תואם `AGENT_BLUEPRINT § 9` (איטרציה) · Working Rule #6 VERIFY | ✅ |
| 7 · Validate (WCAG/responsive) | `system-design-cheatsheet #12` (UX: responsiveness, נגישות) — כיום ללא בדיקת WCAG | ⚠️ חוב |
| 8 · Export (HTML) | **`public/index.html` (storefront) + `public/dashboard.html` (ops)** — מוגשים מ-`/ui` ב-`server.ts` עם CSP נפרד | ✅ קיים |

> **הקריאה:** ל-ULease כבר יש את **תוצר** הצעד ה-8 (HTML demo מוגש מ-`/ui`), אבל בלי הצעדים שלפניו: אין `DESIGN.md` (צעד 3) ואין validation שיטתי (צעד 7). ה-UI נבנה ad-hoc; Claude Design היה נותן לו design-system ו-WCAG.

---

## 3. הצעד שמכפיל ערך — #3 `DESIGN.md` = "Business Brain" ל-UI

בדיוק כמו ש-`CLAUDE.md` הוא ה-Business Brain להנדסה (`BUSINESS_PARTNER § 2`), **`DESIGN.md` הוא ה-Business Brain ל-UI**: צבעים, טיפוגרפיה, רכיבים, tone — מקור-אמת אחד שכל prompt עיצוב מפנה אליו. זה הופך עיצוב מ"כל פעם מאפס" ל**מערכת עקבית** — אותו עיקרון של ה-OS, בשכבת ה-UX.

- **drop-in ל-ULease:** תיקיית Cowork עם הלוגו/צבעים/פונטים של Leasing.co.il → *"save the full design system as DESIGN.md"* → reference בכל wireframe.
- **חיבור:** ה-CSP ב-`server.ts` כבר מתיר Tailwind CDN — ה-storefront מוכן לקבל design-system עקבי.

---

## 4. החוב הפתוח (כנה)

1. **`DESIGN.md`** — אין design-system מתועד; ה-UI ב-`public/` הוא demo ad-hoc. הצעד: לייצר `DESIGN.md` ל-Leasing.co.il (צעד 3).
2. **WCAG validation** — אין בדיקת נגישות שיטתית (צעד 7). הצעד: להריץ *"List WCAG 2.1 AA violations + fixes"* על ה-storefront לפני go-live (`LAUNCH`).
3. **Responsive matrix** — אין אימות desktop/tablet/mobile מתועד מול `system-design-cheatsheet #12`.

---

*תומלל מ-"How to Design Anything in Claude", ומופה לשכבת ה-UI של `leasing-api` (`public/`, `server.ts`) ול-OS בהמשך ל-`system-design-cheatsheet § 12` ו-`MASTER_CLAUDE_58.md`.*
