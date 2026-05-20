import type { LeaseDeal } from '../schemas';

export type Rating = 'excellent' | 'good' | 'fair' | 'weak' | 'poor';

export interface ScoreBreakdown {
  discount: number;
  financing: number;
  residual: number;
  cost: number;
}

export interface ScoreMetrics {
  sellingPrice: number;
  discountPct: number;
  apr: number;
  residualPct: number;
  totalCost: number;
  effectiveMonthlyCost: number;
}

export interface DealScore {
  reference?: string;
  score: number;
  rating: Rating;
  breakdown: ScoreBreakdown;
  metrics: ScoreMetrics;
  reasons: string[];
}

const WEIGHTS = {
  discount: 0.25,
  financing: 0.2,
  residual: 0.2,
  cost: 0.35,
} as const;

const clamp = (value: number, min = 0, max = 100): number =>
  Math.min(max, Math.max(min, value));

const round = (value: number, digits = 2): number => {
  const f = 10 ** digits;
  return Math.round(value * f) / f;
};

function ratingFor(score: number): Rating {
  if (score >= 80) return 'excellent';
  if (score >= 65) return 'good';
  if (score >= 50) return 'fair';
  if (score >= 35) return 'weak';
  return 'poor';
}

/**
 * Score a single leasing deal on a 0-100 scale.
 *
 * The score blends four independent sub-scores: the negotiated discount off
 * list price, the financing cost (money factor expressed as APR), how well the
 * vehicle holds value (residual percentage), and the overall cost efficiency of
 * the lease relative to the vehicle's depreciation.
 */
export function scoreDeal(deal: LeaseDeal): DealScore {
  const sellingPrice = deal.sellingPrice ?? deal.listPrice;

  // --- Discount: how far below list price the deal was negotiated. ---
  const discountPct = clamp((deal.listPrice - sellingPrice) / deal.listPrice, 0, 1);
  const discountScore = clamp((discountPct / 0.12) * 100);

  // --- Financing: lower money factor (APR) is better. ---
  const apr = deal.moneyFactor * 2400;
  const financingScore = clamp((1 - apr / 8) * 100);

  // --- Residual: higher retained value lowers depreciation cost. ---
  const residualPct = clamp(deal.residualValue / deal.listPrice, 0, 1);
  const residualScore = clamp(((residualPct - 0.3) / (0.65 - 0.3)) * 100);

  // --- Cost efficiency: annual outlay relative to the vehicle price. ---
  const totalCost =
    deal.downPayment + deal.monthlyPayment * deal.termMonths + deal.fees - deal.incentives;
  const years = deal.termMonths / 12;
  const annualCostPct = totalCost / sellingPrice / years;
  const costScore = clamp(((0.28 - annualCostPct) / (0.28 - 0.12)) * 100);

  const breakdown: ScoreBreakdown = {
    discount: round(discountScore),
    financing: round(financingScore),
    residual: round(residualScore),
    cost: round(costScore),
  };

  const score = round(
    discountScore * WEIGHTS.discount +
      financingScore * WEIGHTS.financing +
      residualScore * WEIGHTS.residual +
      costScore * WEIGHTS.cost,
    0,
  );

  const reasons: string[] = [];
  if (discountPct >= 0.1) reasons.push('Strong discount off list price.');
  else if (discountPct < 0.03) reasons.push('Little to no discount off list price.');
  if (apr <= 2) reasons.push('Very low financing cost.');
  else if (apr >= 6) reasons.push('High financing cost (money factor).');
  if (residualPct >= 0.6) reasons.push('Excellent residual value retention.');
  else if (residualPct <= 0.35) reasons.push('Low residual value increases depreciation cost.');
  if (annualCostPct <= 0.13) reasons.push('Total cost is low relative to the vehicle price — efficient lease.');
  else if (annualCostPct >= 0.24) reasons.push('Total cost is high relative to the vehicle price.');

  return {
    ...(deal.reference !== undefined ? { reference: deal.reference } : {}),
    score,
    rating: ratingFor(score),
    breakdown,
    metrics: {
      sellingPrice: round(sellingPrice),
      discountPct: round(discountPct * 100, 1),
      apr: round(apr, 2),
      residualPct: round(residualPct * 100, 1),
      totalCost: round(totalCost),
      effectiveMonthlyCost: round(totalCost / deal.termMonths),
    },
    reasons,
  };
}

export function scoreDeals(deals: LeaseDeal[]): DealScore[] {
  return deals.map(scoreDeal);
}
