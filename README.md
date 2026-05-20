# leasing-api

מנוע דירוג עסקאות ליסינג עבור Leasing.co.il — פלטפורמה למסחר, שיווק ומכירת רכבים.

Deal Score Engine API: מקבל פרטי עסקת ליסינג ומחזיר ציון 0–100 עם פירוט.

## Stack

- Node.js 20+ / TypeScript
- Express 4
- Zod (ולידציה)
- Supabase (אחסון)
- Vitest + Supertest (בדיקות)
- פריסה: Vercel Serverless

## Setup

```bash
npm install
cp .env.example .env   # מלאו את הערכים
npm run dev            # פיתוח מקומי (vercel dev)
```

## Scripts

| Script | תיאור |
| --- | --- |
| `npm run build` | קומפילציה ל-`dist/` |
| `npm run typecheck` | בדיקת טיפוסים בלבד |
| `npm test` | הרצת בדיקות |
| `npm start` | הרצת השרת המקומפל |

## API

### `GET /health`
בדיקת חיות.

### `POST /v1/score`
מדרג עסקה אחת או אצווה. מוגן ב-HMAC (header `X-Signature: sha256=<hex>`).
ניתן לעקוף בפיתוח עם `HMAC_DISABLED=true`.

**Body — עסקה בודדת:**

```json
{
  "listPrice": 200000,
  "sellingPrice": 180000,
  "monthlyPayment": 2200,
  "downPayment": 10000,
  "termMonths": 36,
  "residualValue": 120000,
  "moneyFactor": 0.001,
  "incentives": 0,
  "fees": 1000,
  "reference": "quote-123"
}
```

**Body — אצווה:** `{ "deals": [ { ... }, { ... } ] }`

**תגובה:**

```json
{
  "count": 1,
  "results": [
    {
      "reference": "quote-123",
      "score": 77,
      "rating": "good",
      "breakdown": { "discount": 83.33, "financing": 70, "residual": 85.71, "cost": 70.66 },
      "metrics": { "discountPct": 10, "apr": 2.4, "residualPct": 60, "totalCost": 90200, "effectiveMonthlyCost": 2505.56 },
      "reasons": ["Strong discount off list price.", "Excellent residual value retention."]
    }
  ]
}
```

## מודל הציון

הציון משקלל ארבעה תתי-ציונים:

| מרכיב | משקל | מה נמדד |
| --- | --- | --- |
| discount | 25% | הנחה ממחיר המחירון |
| financing | 20% | עלות המימון (money factor → APR) |
| residual | 20% | שמירת ערך הרכב בתום החוזה |
| cost | 35% | יעילות העלות השנתית הכוללת מול מחיר הרכב |

## חתימת בקשות (HMAC)

```js
const crypto = require('node:crypto');
const body = JSON.stringify(payload);
const sig = crypto.createHmac('sha256', process.env.HMAC_SECRET).update(body).digest('hex');
// header: X-Signature: sha256=<sig>
```
