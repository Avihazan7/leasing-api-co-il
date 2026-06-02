# יסודות System Design — ארכיטקטורת הפלטפורמה

**Module:** `AI_SYSTEM_DESIGN.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — Knowledge layer (§3 שורה 23). מודול ההנדסה השני (אחרי `AI_PROJECT_STRUCTURE.md`) — שפת הארכיטקטורה מול ה-Tech Lead.
**Source:** מבוסס על *"Reverse Proxy vs API Gateway vs Load Balancer"* (Level Up Coding) · *"Queues 101"* (Raul Junco) · *"How JWT Works"* (Amigoscode) · *"6 API Architecture Styles"* (James Code Lab).
**Integrates with:** `CASES/ULEASE_SPEC.md` (§3 · §8 · §9 · §10), `AI_PROJECT_STRUCTURE.md`, `AI_RAG_DESIGN.md`, `AI_DATA_BI.md`, `CASES/ULEASE_HIRING.md`, `CASES/ULEASE_PRICING_SLA.md`

> ארבעה מושגי-יסוד של ארכיטקטורת backend — שער כניסה, סגנונות API, תורים ואימות — מתורגמים לרכיבי הפלטפורמה של ULease. המטרה: שאברהם יוכל לנהל design review מול ה-Tech Lead **בלי לכתוב שורת קוד**, ולזהות החלטה גרועה לפני שהיא נבנית.

---

## 1. שער הכניסה — Reverse Proxy · API Gateway · Load Balancer

| רכיב | מה הוא עושה | 🎯 ב-ULease |
|------|--------------|--------------|
| **Reverse Proxy** (NGINX/Envoy) | מקבל את כל התעבורה הנכנסת, מסתיר את השרתים הפנימיים | חזית האתר — Leasing.co.il |
| **API Gateway** (AWS/Kong) | נקודת כניסה אחת ל-APIs: ניתוב, **אימות והרשאה**, אגרגציה של כמה שירותים | שער ה-ingestion לספקים + ה-API של הפורטלים (לקוח/ספק/מפיץ) |
| **Load Balancer** (ALB/HAProxy) | מפזר עומס בין שרתים + בודק בריאות | מאחורי ה-SLA: uptime 99.5% (`ULEASE_PRICING_SLA.md` §4) ו-99.9% (NFR §10) |

**הסדר בפועל:** לקוח → Load Balancer → API Gateway (אימות) → השירותים. ב-MVP על ספק ענן מנוהל — שלושתם שירות מדף, לא משהו שבונים.

---

## 2. שישה סגנונות API — ומה ULease באמת צריכה

| סגנון | מה זה | ההכרעה ל-ULease |
|--------|--------|-------------------|
| **REST** | משאבים על HTTP, JSON, stateless | ✅ **MVP** — ingestion ספקים, הפורטלים, ה-API הציבורי. פשוט, סטנדרטי, קל לדבג |
| **Webhooks / WebSockets** | חיבור קבוע, דחיפה בזמן אמת | ✅ **V1** — עדכוני **מכרז מחיר-שני** בזמן אמת (מי מוביל) + סטטוס חדר-עסקה |
| **GraphQL** | הלקוח שולף בדיוק את השדות שהוא צריך | ⏳ לא עכשיו — מורכבות שרת/caching מיותרת ב-MVP; לשקול ב-V2 לפורטל המפיצים (דאטה עשירה) |
| **gRPC** | RPC בינארי מהיר עם סכמה | ⏳ V2 — תקשורת פנימית בין שירותי הסוכנים אם ה-scale ידרוש |
| **SOAP** | XML ארגוני כבד | רק אם יבואן ותיק מחייב (אינטגרציה ל-ERP ישן) — לא מתכננים |
| **MQTT** | pub/sub קל ל-IoT | ❌ לא רלוונטי |

> **הכלל:** אין סגנון "הכי טוב" — יש הכי-נכון-לאילוץ. ל-MVP: REST לכל דבר + webhook אחד למכרז. כל חריגה מזה צריכה הצדקה בכתב מה-Tech Lead.

---

## 3. תורים (Queues) — הלב של ארכיטקטורת ה-Events ⭐

ה-SPEC כבר קבע (§3): *"כל אירוע (ליד, בקשת עסקה, מכרז) הוא event שעובר ב-Core ומתוזמר ע"י שכבת ה-Multi-agent"*. **תורים הם המימוש של המשפט הזה.**

```
Producers                    Broker/Queue                  Consumers
(ingestion · אתר · מכרז)  →  [ Event Queue ]  →  הסוכנים (Ultra → Master → Max)
                                   ↓ נכשל אחרי retries
                              [ DLQ — תור אירועים מתים ]
```

| מושג | מה זה | למה ULease חיה או מתה על זה |
|------|--------|------------------------------|
| **ACK** | אישור שהאירוע עובד בהצלחה | ליד שלא קיבל ACK = ליד שאבד = ₪150 שלא נגבו |
| **Idempotency** | עיבוד כפול לא יוצר תוצאה כפולה | 🔴 **קריטי**: retry על אירוע תשלום לא יחייב את הלקוח פעמיים; הצעה לא תישלח פעמיים לאותו ספק |
| **DLQ** | תור לאירועים שנכשלו סופית | עסקה שנתקעה לא נעלמת — היא מחכה לטיפול אנושי (Ops console) |
| **Visibility timeout** | אירוע "נעול" בזמן עיבוד | שני סוכנים לא יתפסו את אותו ליד במקביל |
| **Correlation ID** | מזהה שעובר בכל השרשרת | בדיוק ה-`AgentRun.eventId` מה-SPEC §8 — traceability מקצה לקצה |

**מדדי הבריאות לניטור** (מתחבר להתראות מ-`AI_DATA_BI.md` §6.ד): עומק תור (backlog) · גיל ההודעה הוותיקה (lag) · קצב עיבוד · שיעור שגיאות · גודל ה-DLQ.

**הדפוסים ש-ULease צריכה:** Work Queue (חלוקת לידים לסוכנים) · Pub/Sub (אירוע עסקה → גם חיוב, גם דשבורד, גם התראה) · Delayed Queue (follow-up אחרי 3 ימים) · Priority Queue (ליד חם לפני עדכון מלאי).

---

## 4. JWT — איך ספק מוכיח מי הוא בלי session

**JWT** = טוקן חתום שמוכיח זהות בלי שהשרת שומר state. ה-API סומך על הטוקן כי הוא חתום בסוד משותף — אפס פניות ל-DB באימות.

**הזרימה ב-ULease:**
1. ספק מתחבר (אימות + KYC) → השרת מחזיר JWT עם ה-claims: `supplierId` · `role: supplier` · `exp`
2. כל קריאת API (עדכון מלאי, משיכת לידים) נושאת `Authorization: Bearer <jwt>`
3. ה-API Gateway מאמת את החתימה ומחלץ את ה-claims — **בלי DB lookup**
4. ה-claims הם ה-**RLS של ה-API**: `supplierId` בטוקן ⇒ רואה רק את הדאטה שלו

> **החיבור המשולש:** JWT (אימות ברמת ה-API) + RLS (סינון ברמת הדאטה, `AI_DATA_BI.md` §6.ב) + Guardian (אכיפת מדיניות, SPEC §7) = שלוש שכבות ההגנה על סודיות הספקים. כלל: הטוקן ב-httpOnly cookie, לא ב-localStorage.

---

## 5. צ'קליסט Design Review מול ה-Tech Lead

- [ ] **שער כניסה:** מי עושה אימות — ה-Gateway או כל שירות לחוד? (תשובה נכונה: Gateway)
- [ ] **API:** הכל REST ב-MVP? כל חריגה — למה? (#2)
- [ ] **Events:** איך ממומש תור האירועים? מה קורה לאירוע שנכשל (DLQ)? (#3)
- [ ] **Idempotency:** מה קורה אם אותו אירוע תשלום מעובד פעמיים? (#3 — תשובה לא טובה = עצור הכל)
- [ ] **Traceability:** האם כל אירוע נושא Correlation ID שמגיע עד ה-AuditLog? (SPEC §8)
- [ ] **אימות:** JWT? איפה הטוקן נשמר בצד לקוח? כמה זמן הוא חי? (#4)
- [ ] **ניטור:** אילו מדדי-תור מחוברים להתראות? (#3 + `AI_DATA_BI.md` §6.ד)

---

## 6. החיבור ל-OS

| איפה | מה |
|------|-----|
| `CASES/ULEASE_SPEC.md` §3 + §8 | ארכיטקטורת ה-events והישויות Event/AgentRun — המודול הזה הוא המימוש ההנדסי שלהן |
| `AI_PROJECT_STRUCTURE.md` | המבנה (prompts·data·agents·evals) — המודול הזה ממלא את שכבת ה-infra שמתחתיו |
| `AI_RAG_DESIGN.md` + `AI_DATA_BI.md` | שלושת מודולי ההנדסה: RAG (ידע) · BI (דאטה) · System Design (תשתית) |
| `CASES/ULEASE_HIRING.md` §ו | שאלות הראיון הטכניות — הצ'קליסט ב-§5 הוא ההמשך שלהן אחרי הגיוס |
| Learn-vs-Delegate | **אתה:** המושגים + הצ'קליסט · **Tech Lead:** הבחירות והמימוש |

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | ארבעה יסודות backend (שער כניסה · סגנונות API · תורים · JWT) ממופים לארכיטקטורת ULease + צ'קליסט design review | 2026-06-02 |

**Attribution.** המקורות: *Reverse Proxy vs API Gateway vs Load Balancer* (Level Up Coding) · *Queues 101* (Raul Junco) · *How JWT Works* (Amigoscode) · *6 API Architecture Styles* (James Code Lab). העיבוד והמיפוי ל-ULease — חלק מה-Claude OS של Avraham Bar Yochai Chazan.

**Confidentiality.** קובץ זה הוא חלק מה-Claude Operating System האישי של Avraham Bar Yochai Chazan.

— *End of AI_SYSTEM_DESIGN.md v1.0.0 —*
