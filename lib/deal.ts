// Deterministic sample deal intelligence for the Mobility OS interface.
// Mirrors the shape of the ULease Brain Engine read model (deal_intelligence
// + deal_proposals). Values are illustrative but internally consistent.

export type Recommendation = "STRONG_BUY" | "BUY" | "HOLD" | "PASS"

export interface WaterfallStep {
  id: "anchor" | "depreciation" | "interest" | "tco"
  label: string
  value: number
  /** Short, objective explanation shown when the column is selected. */
  detail: string
  /** Token used for the bar fill. */
  tone: "anchor" | "depreciation" | "interest" | "tco"
}

export interface Deal {
  vehicle: string
  trim: string
  durationMonths: number
  monthlyPayment: number
  score: number
  confidence: number
  recommendation: Recommendation
  currency: string
  waterfall: WaterfallStep[]
  subScores: { label: string; value: number }[]
}

export const deal: Deal = {
  vehicle: "Volvo EX30",
  trim: "Twin Motor · Plus",
  durationMonths: 36,
  monthlyPayment: 2940,
  score: 88,
  confidence: 0.94,
  recommendation: "BUY",
  currency: "₪",
  waterfall: [
    {
      id: "anchor",
      label: "Dealer's Anchor Price",
      value: 312000,
      tone: "anchor",
      detail:
        "The headline figure presented at the showroom. It is engineered to frame every later number as a discount. We treat it as noise, not signal.",
    },
    {
      id: "depreciation",
      label: "Depreciation & Tech Risk",
      value: 88400,
      tone: "depreciation",
      detail:
        "Modeled value loss over the term, adjusted for battery degradation and software obsolescence. The single largest real driver of cost.",
    },
    {
      id: "interest",
      label: "Implied Interest",
      value: 41200,
      tone: "interest",
      detail:
        "The financing cost embedded inside the monthly payment — rarely stated explicitly. Derived from the payment schedule against market value.",
    },
    {
      id: "tco",
      label: "True TCO",
      value: 247600,
      tone: "tco",
      detail:
        "The grounded, all-in cost of ownership over the term. This is the only number that should anchor your decision.",
    },
  ],
  subScores: [
    { label: "Financial", value: 91 },
    { label: "Market", value: 86 },
    { label: "Residual", value: 90 },
    { label: "Supplier", value: 84 },
  ],
}

export const recommendationCopy: Record<Recommendation, { title: string; note: string }> = {
  STRONG_BUY: { title: "Strong Buy", note: "Materially below true market cost." },
  BUY: { title: "Buy", note: "Priced fairly against the true cost of ownership." },
  HOLD: { title: "Hold", note: "Marginal. Worth negotiating before committing." },
  PASS: { title: "Pass", note: "The terms work against you. Walk away." },
}

export function formatCurrency(value: number, currency = "₪") {
  return `${currency}${value.toLocaleString("en-US")}`
}
