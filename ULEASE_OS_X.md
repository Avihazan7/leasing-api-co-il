# ULease OS X — 2026

> **The Autonomous Mobility Economy Engine**
> מערכת ההפעלה לכלכלת המוביליטי הישראלית. לא פלטפורמת ליסינג, לא CRM, לא אתר לידים —
> שכבת **ההחלטה, התיווך, המשא-ומתן, החוזה והביצוע** בין כל שחקני השוק.
>
> מודול מתודולוגיה (לא קוד). מקור: חזון המייסד (Hi-Tech-Top). גרסה 1.0.0.

---

## § 0 · העיקרון המכונן — ULease לא מחזיקה כסף

זהו חוק-העל של הארכיטקטורה, וכל שכבה תחתיו חייבת לכבד אותו:

> **ULease אינה צד פיננסי. היא לא מחזיקה כסף, לא מלווה, לא מבטחת ולא מוכרת רכב.**

ULease היא **שכבת התיווך וההחלטה** בין:
**יבואנים · דילרים · חברות ליסינג · בנקים · חברות ביטוח · לקוחות קצה** —
במודל **B2B2C & B2B**, על פני שלושה מסלולים: **רכישה / מימון / ליסינג**.

מה ש-ULease כן עושה מקצה-לקצה: **התאמה · משא-ומתן · יצירת הצעות · חוזים · קבלת החלטות · ביצוע (orchestration)**.
הכסף זורם ישירות בין הספק ללקוח/לבנק; ULease גובה **take-rate** על התיווך — ולכן נשארת ניטרלית, רזה, וניתנת להרחבה למאות ספקים.

**משמעות הנדסית:** ה-ledger הקיים (`ledger_entries`, `settlements`) הוא **רישום עמלות ותיווך** — לא חשבון נאמנות. אין wallet, אין החזקת כספי לקוח. זה גם מקטין דרמטית את חשיפת הרגולציה.

---

## § 1 · תזת 2026 — הצוואר אינו ה-Agents

המגמה של 2026 ברורה: ארגונים מגלים שהבעיה **אינה לבנות סוכנים**, אלא:

```
Data  ·  Governance  ·  Orchestration  ·  AI Identities
```

רוב הפיילוטים נתקעים מהיעדר **שכבת שליטה מרכזית (Control Plane)**. סוכנים אוטונומיים
שרצים בלי נתוני-יסוד איכותיים רק **מגבירים כאוס**. מי שמצליח — בונה
**Data + Orchestration + Governance _לפני_ שכבת הסוכנים**.

לכן ULease OS X הופך את הסדר: הסוכנים הם השכבה **האחרונה**, על תשתית של נתונים, התנהגות, תורת-משחקים וממשל.

---

## § 2 · UDM — ULease Unified Decision Methodology

חמש שכבות יסוד, עם **ממשל (Governance)** כעמוד-שדרה רוחבי, ו-**Web Intelligence** כדלק:

```
        ┌──────────────  GOVERNANCE  (Identity · Audit · Kill-Switch)  ──────────────┐
        │                                                                            │
   DATA  →  BEHAVIOR  →  COGNITIVE  →  GAME THEORY  →  EXECUTION
 (Entity   (Big Five)  (Instrumental  (Multi-Player    (Agents)
  Graph)                Enrichment)    Optimization)
        │                                                                            │
        └──────────────  WEB / MARKET INTELLIGENCE  (feeds every layer)  ────────────┘
```

---

### שכבה 1 · Universal Entity Graph — *כל דבר הוא ישות*

```
Customer · Vehicle · Supplier · Bank · Insurance · Offer · Contract · Invoice · Renewal
```

כל אירוע יוצר **Edge** חדש:

```
Customer --requested--> Vehicle --quotedBy--> Supplier
        --financedBy--> Bank --insuredBy--> Insurance --signed--> Contract
```

הגרף הוא מקור-האמת היחיד: לא טבלאות מנותקות אלא **רשת יחסים** שממנה נגזרות החלטות, המלצות ו-network effects.

---

### שכבה 2 · Big Five Decision Engine — *מנוע החלטות, לא CRM*

```ts
interface BigFiveProfile {
  openness: number; conscientiousness: number; extraversion: number;
  agreeableness: number; neuroticism: number;
}
```

| תכונה (גבוהה) | מה הלקוח מעדיף | השלכה עסקית |
|---|---|---|
| **Conscientiousness** | אמון, יציבות, חוזים ארוכים, מותגים חזקים | להציע ליסינג ארוך + מותג מוביל |
| **Neuroticism** | סיכון נמוך, תשובות מיידיות, אחריות, אמון גבוה | אחריות מורחבת + מענה אנושי מהיר |
| **Extraversion** | רכבי פרימיום, החלטה מהירה, מותגי סטטוס | דחיפת דגמי דגל + Deal מהיר |
| **Openness** | חשמלי, דגמים חדשניים, מנויים | EV / מודלים גמישים / subscription |
| **Agreeableness** | פשטות, חבילות, יחסים ארוכי-טווח | bundle אחד + ליווי מתמשך |

הפרופיל מזין גם את **חווית המשתמש** (Calm Tech): צפיפות מידע, אנימציות ומצב-קוגניטיבי מותאמים אישית.

---

### שכבה 3 · Instrumental Enrichment Layer — *שיפור איכות ההחלטה*

בהשראת **ההעשרה האינסטרומנטלית (פוירשטיין)**: המערכת לא רק מתאימה עסקה — היא משפרת את **איכות קבלת ההחלטה**. היא שואלת:

```
האם הלקוח קיבל מספיק מידע? → האם הוא מבין את הסיכונים? →
האם יש עומס קוגניטיבי? → האם חסר מידע? → האם ההחלטה אופטימלית?
```

**Cognitive Friction Engine:**

```
cognitiveLoad = informationComplexity + numberOfOffers
              + decisionUncertainty + timePressure
```

כש-`cognitiveLoad` גבוה → המערכת **מפשטת** (פחות הצעות, מידע מובנה, מצב Calm) במקום להעמיס.

---

### שכבה 4 · Game Theory Engine — *הליבה*

שחקנים: **Customer · Supplier · Bank · Insurance · ULease**.

**Utility Function:**
```
U = economicBenefit + trust + speed + futureValue − risk
```

**Nash — לא מחפשים מחיר, מחפשים יציבות מערכת:**
```
maximize( customerUtility, supplierUtility, ecosystemUtility )
```

**Cooperative Game — עסקה מתבצעת רק כשכולם מרוויחים:**
```
if (supplierProfit > 0 && customerSavings > 0 && ecosystemGrowth > 0)
    executeDeal = true
```

זה מה שהופך את ULease מ"זירת מחירים" ל**מנוע אופטימיזציה של אקו-סיסטם** — ה-take-rate שלה תלוי בבריאות כל הצדדים, לא בסחיטת אחד מהם.

---

### שכבה 5 · Web / Market Intelligence — *הדלק*

סריקות שוק רציפות:
```
Vehicle Prices · Inventory · Demand · Interest Rates · Competition · Supplier Signals · Consumer Trends
```

**Market Temperature Engine:**
```
marketTemperature = inventoryPressure*0.30 + searchDemand*0.25
                  + interestRates*0.15 + competitorActivity*0.15 + seasonality*0.15
```

---

### עמוד-השדרה · Governance Layer — *החלק הקריטי ביותר*

כל סוכן הוא **זהות (Identity)**; כל פעולה **נרשמת (Audit)**; יש **Kill-Switch**.

```ts
interface AgentIdentity {
  id: string; role: string; permissions: string[];
  allowedActions: string[]; riskLevel: number; owner: string;
}
interface AuditEvent { who; what; why; confidence; cost; impact; timestamp }
```

רגולטורים בעולם כבר בודקים Data Governance, הרשאות, Kill-Switch, ספקי צד-ג' ויכולת-הסבר של החלטות AI. שכבה זו היא תנאי-סף, לא תוספת.

---

## § 3 · Autonomous Decision Score (ADS) + פרוטוקול ביצוע

```
ADS = dealIQ*0.25 + trustScore*0.20 + marketTemperature*0.15
    + closeProbability*0.20 + supplierPressure*0.10 + ltvScore*0.10
```

```
ADS > 90 → EXECUTE_NOW
ADS > 75 → SEND_OFFER
ADS > 60 → NEGOTIATE
ADS > 40 → WAIT
ADS < 40 → REJECT
```

ה-ADS הוא הגשר בין ההחלטה לביצוע — וכל מעבר-סף נרשם ב-Audit עם confidence ו-impact.

---

## § 4 · מיפוי לקוד הקיים — קיים ✅ / חלקי 🟡 / חסר ❌

עיגון כן: מה כבר בנוי ב-`leasing-api`, מול מה שעדיין חזון.

| שכבת UDM | מצב | עיגון / פער |
|---|---|---|
| **Entity Graph** | 🟡 | יש `vehicle_read_model`, `settlements`, `ledger_entries`, outbox-events — אך לא גרף-ישויות מאוחד (חסרים customer/supplier/bank/insurance/contract כישויות-קשר) |
| **Big Five** | ❌ | קיים seam `decisionEngine` בלבד; אין פרופיל התנהגותי ולא טבלת `agent_memory` |
| **Instrumental / Cognitive** | 🟡 | יש Calm-Tech + העשרת קטלוג בצד-לקוח; אין Cognitive Friction Engine מדיד |
| **Game Theory** | ❌ | חסר — היום ניקוד חד-צדדי (Deal Score), לא אופטימיזציית רב-שחקן |
| **Web / Market Intelligence** | 🟡 | מנוע סנכרון מחירון משרד התחבורה (`sync/`) פעיל; אין מדד Market Temperature ולא איסוף ביקושים/ריביות |
| **ADS / Decision Protocol** | 🟡 | יש `dealScore` דטרמיניסטי + `/v1/kpi`; ADS המלא (6 מרכיבים) טרם הולחם |
| **Governance** | 🟡 | RLS + HMAC + `audit_log` קיימים; חסר רישום Agent-Identity ו-Kill-Switch |
| **Execution / Agents** | ❌ | אין עדיין AI Agent runtime; ה-Outbox+Sink הם ה-seam לבנות עליו |

**מסקנה:** התשתית האירועית והממשל הבסיסי **קיימים וחזקים**. מה שחסר הוא שכבות ה-Behavior / Game-Theory / Agents — וזה הסדר הנכון לבנות בו (Data+Governance תחילה, סוכנים בסוף).

---

## § 5 · ה-Moat — לא AI

ה-AI הוא commodity. החפיר התחרותי האמיתי של ULease 🎯 Leasing.co.il יהיה:

```
Data  +  Behavior  +  Game Theory  +  Governance  +  Network Effects
```

ככל שיותר ספקים (מאות תוך 12 חודשים) ויותר גולשים (SEO + קידום אורגני + נוכחות בכל מנועי ה-AI) —
כך הגרף, הפרופילים והאופטימיזציה משתפרים, וה-Moat מעמיק. **Network effects, לא מודל.**

---

## § 6 · סדר היישום המומלץ

1. **Entity Graph + Data Brain** — להשלים ישויות-קשר + `agent_memory`, `events`, `kpi_snapshots` (additive, אותו דפוס RLS).
2. **Governance** — `AgentIdentity` + `AuditEvent` + Kill-Switch (על ה-`audit_log` הקיים).
3. **ADS** — להלחים את 6 המרכיבים על `dealScore` + `kpi` הקיימים, עם פרוטוקול הסף.
4. **Game Theory** — utility רב-שחקן + תנאי ה-cooperative-deal.
5. **Agents** — אחרונים, על ה-Outbox/Sink, כל אחד עם Identity וגבולות הרשאה.

> בע"ה — ULease 🎯 Leasing.co.il: מערכת ההפעלה לכלכלת המוביליטי.
