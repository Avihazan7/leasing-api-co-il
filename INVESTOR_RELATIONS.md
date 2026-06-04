# INVESTOR_RELATIONS.md — קשרי משקיעים

**Module:** `INVESTOR_RELATIONS.md` · **Version:** 1.0.0
**Status:** סוגר את ה-dangling ref השלישי ב-load order (ראה `AGENT_BLUEPRINT § 7`).
**Thesis:** *הסיפור למשקיע נשען על הקוד, לא על שקפים.*

---

## 0. תכלית

מודול זה מרכז את ה-narrative וה-evidence ל-investor updates של ULease / Leasing.co.il.
העיקרון: כל טענה ניתנת-להוכחה ממופה ל-artifact אמיתי בריפו (`leasing-api`) או למודול OS.

## 1. One-liner

ULease הופכת מסחר ברכב חדש לפלטפורמה event-driven: **Deal Score Engine** שקוף +
**מלאי מבוסס-אירועים** עם הגנת overselling, מעל שכבת AI-agents מתוזמרת.

## 2. Evidence Map — טענה ⇄ artifact

| טענה למשקיע | ההוכחה בקוד/OS |
|-------------|----------------|
| "מנוע ניקוד דטרמיניסטי ושקוף" | `leasing-api/src/scoring/dealScore.ts` + `decisionEngine.ts` (seam ל-ML) |
| "מלאי אמין, ללא מכירה כפולה" | `inventory/repository.ts` (`UPDATE … WHERE status='AVAILABLE'`) + טסטי concurrency |
| "ארכיטקטורת אירועים production-grade" | Transactional Outbox + relay (`SKIP LOCKED`) + CQRS read model |
| "מוכנות BI/דשבורדים" | `src/db/bi_views.sql` (star schema) + `power-bi-essential-concepts.md` |
| "שכבת אוטומציה עסקית" | `N8N_AUTOMATION.md` (Outbox → n8n workflows) |
| "מפת דרכים מבוססת-CTO" | `CTO_REVIEW.md` (scorecard + Platform v2.0 P0–P7) |

## 3. Metrics to report (כשיהיו)

מחזור עסקאות · conversion rate (מ-`bi.vw_kpi_summary`) · עמלות מצטברות (`fact_settlements`) ·
זמן עד-go-live לסוכנות חדשה (ראה `LAUNCH.md` / `BRANCH_KNOWLEDGE.md`).

## 4. Roadmap

מודול זה הוא anchor; ה-deck המלא ומחזור ההכנסות יתווספו כשהמדדים יתייצבו
(תלות: Evals harness + נתוני פרודקשן ראשונים — ראה `AGENT_BLUEPRINT § 7`).
