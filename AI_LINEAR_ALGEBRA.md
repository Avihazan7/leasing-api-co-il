# יסודות אלגברה לינארית — Linear Algebra Foundations (Cheat Sheet)

**Module:** `AI_LINEAR_ALGEBRA.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — מודול ידע/יסודות (Knowledge layer). הבסיס המתמטי של ML, נטען on-demand.
**Source:** מבוסס על האינפוגרפיקה *"Linear Algebra Cheat Sheet"* (mltut).
**Integrates with:** `AI_LEARNING_RESOURCES.md`, `AI_SKILL_MAP.md`, `AI_RAG_DESIGN.md`, `AI_DATA_BI.md`, `CASES/ULEASE_SPEC.md`

---

> אלגברה לינארית היא **השפה שבה כתוב כל מודל ML** — embedding הוא וקטור, שכבת רשת היא כפל מטריצות, וחיפוש RAG הוא מכפלה סקלרית. זה לא מודול שאברהם *מיישם* (זה תחום ה-Tech Lead) — זה מודול **אוריינות**: הקומה התחתונה של קוריקולום ה-AI (`AI_SKILL_MAP`), שמאפשרת להוביל design review בלי לכתוב קוד. 12 המושגים מהדף — וכל אחד, לאן הוא מתחבר ב-ULease.

---

## 1. שנים-עשר המושגים → ולמה הם חשובים

| # | מושג | תמצית / נוסחה | למה זה חשוב ל-ML/AI |
|---|------|----------------|---------------------|
| 1 | **סקלר · וקטור · מטריצה** | סקלר = מספר בודד · וקטור = n×1 (גודל+כיוון) · מטריצה = m×n (מערך 2D) | אבני הבניין: feature בודד = סקלר · embedding = וקטור · batch/שכבה = מטריצה |
| 2 | **חיבור / חיסור** | element-wise, מימדים זהים (A+B) | צבירת gradients · residual connections |
| 3 | **כפל מטריצות** | (AB)ᵢⱼ = Σₖ aᵢₖ·bₖⱼ · עמודות A = שורות B · **לא** קומוטטיבי | ⭐ הפעולה המרכזית: כל שכבת רשת = כפל מטריצה + אי-לינאריות |
| 4 | **טרנספוז** | שורות ↔ עמודות · (Aᵀ)ᵀ = A | יישור מימדים לכפל · מטריצות גרם/קווריאנס |
| 5 | **דטרמיננטה** | 2×2: ad − bc · מודד נפח/הפיכות · det = 0 → סינגולרית | האם מערכת פתירה · יציבות נומרית |
| 6 | **מטריצה הופכית** | A·A⁻¹ = I · קיימת רק אם det ≠ 0 | פתרון Ax = b · least-squares (regression) |
| 7 | **מטריצת יחידה** | אלכסון 1, אפס מסביב · AI = IA = A | אלמנט נייטרלי · אתחול · regularization (A + λI) |
| 8 | **מכפלה סקלרית (dot)** | x·y = Σ xᵢyᵢ → סקלר · **מודדת דמיון** | ⭐ ליבת חיפוש RAG: דמיון query ↔ document |
| 9 | **נורמה (L2)** | ‖x‖₂ = √(Σ xᵢ²) ≥ 0 | אורך וקטור · normalization · weight decay · cosine = dot/(‖x‖·‖y‖) |
| 10 | **ערכים/וקטורים עצמיים** | Av = λv (v לא מחליף כיוון, רק נמתח פי λ) | PCA / SVD → הקטנת מימד · דחיסת embeddings |
| 11 | **דרגה (rank)** | מספר שורות/עמודות בלתי-תלויות · rank ≤ min(m, n) | תוכן-מידע · low-rank = הבסיס ל-LoRA fine-tuning |
| 12 | **מערכת לינארית** | Ax = b · פתרון יחיד אם A ריבועית בדרגה מלאה | regression · optimization · פתרון משקלים |

⭐ = הנגיעות הישירות ביותר ב-ULease (ראו §2).

---

## 2. הגשר ל-ULease 🎯 — מ-dot product ל-RAG

המושגים מהדף שיושבים **בלב מוצר חי** של ULease הם #8 (מכפלה סקלרית) ו-#9 (נורמה):

- **חיפוש RAG = דמיון קוסינוס = מכפלה סקלרית מנורמלת.** ב-`CASES/ULEASE_SPEC.md` §7.1 הקורפוס (מלאי · מחירונים · רגולציה · playbooks · היסטוריית עסקאות) מאוחסן כ-embeddings ב-**pgvector**. כששואלים את ה-Q&A Bot, או כש-Deal Score מחפש עסקאות דומות — השאילתה הופכת לווקטור, והמערכת מחזירה את ה-top-k הקרובים. "קרוב" = cosine similarity = `x·y / (‖x‖·‖y‖)` — בדיוק #8 חלקי #9.
- **זה מסגר ישירות את `AI_RAG_DESIGN.md`** (D-025): chunking · top-k · Precision@k — כולם פעולות על וקטורים במרחב רב-ממדי. מי שמבין ש-embedding הוא וקטור ושדמיון הוא dot product, מבין *למה* normalization, בחירת מימד ו-k משנים את איכות ה-retrieval — ויכול לשאול את שאלות הביקורת שבצ'קליסט.
- **eigenvalues / PCA (#10)** נכנס כשה-embeddings גדלים: הקטנת מימד לאשכולות (פרסונות Big Five, סגמנטי עסקאות) בלי לאבד אות.
- **rank / low-rank (#11)** הוא הבסיס המתמטי של **LoRA** — שיטת ה-fine-tuning הזולה. ULease דחתה fine-tuning ל-~1,000 עסקאות (D-022); כשהשאלה תחזור, low-rank הוא המנגנון.

> השאר (כפל מטריצות, דטרמיננטה, הופכית) הם המתמטיקה **שמתחת** ל-Claude עצמו ולכל מודל — חשובים להבנה, לא לתפעול יומי של ULease.

---

## 3. מה זה אומר לך (המייסד)

- **אוריינות design review, לא יישום.** אברהם לא מחשב SVD — הוא מזהה אותו בשיחה. כשה-Tech Lead אומר "נטמיע את המלאי ונעשה cosine top-k", זה לא ז'רגון: זה #8+#9, והצ'קליסט ב-`AI_RAG_DESIGN.md` כבר נותן את שאלות הביקורת. עיקרון תאום ל-`AI_DATA_BI.md` ("ה-BI מנתח, ה-API מחשב"): כאן — **ה-Tech Lead מיישם, המייסד סוקר**.
- **הקומה התחתונה של הקוריקולום.** `AI_SKILL_MAP.md` בנוי Tools → Workflows → Agentic → Architect; כל קורס ML מניח אלגברה לינארית מתחת לשלב 1. המודול הופך את ההנחה למפורשת ב-`AI_LEARNING_RESOURCES.md` — בלי "להעמיד פנים" שצריך לשלוט בה כדי להוביל את ULease.
- **למה מודול נפרד ולא העשרה?** אין ב-OS בית קיים למתמטיקת-יסוד: `AI_DATA_BI.md` הוא סטטיסטיקה/BI/DAX (ענף יישומי אחר), ו-`AI_RAG_DESIGN.md` *משתמש* בווקטורים אך לא מלמד אותם. זהו מודול היסוד המתמטי הראשון ב-OS.

---

## 4. כלים (מהדף)

NumPy (Python) · MATLAB/Octave · Jupyter Notebook · Excel (חישובים בסיסיים). ב-ULease המימוש מופשט מאחורי pgvector + ה-embedding API — אף אחד לא כותב כפל מטריצות ביד; הערך הוא לדעת מה קורה מתחת.

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | 12 מושגי יסוד באלגברה לינארית + עמודת "למה זה חשוב ל-ML" + הגשר ל-ULease (dot product → RAG/pgvector) ומיקום בקוריקולום | 2026-06-03 |

**Attribution.** מבוסס על האינפוגרפיקה *Linear Algebra Cheat Sheet* (mltut). העיבוד, עמודת ה-ML והמיפוי ל-OS/ULease הם חלק מה-Claude Operating System של Avraham Bar Yochai Chazan.

**Confidentiality.** קובץ זה הוא חלק מה-Claude Operating System האישי של Avraham Bar Yochai Chazan.

— *End of AI_LINEAR_ALGEBRA.md v1.0.0 —*
