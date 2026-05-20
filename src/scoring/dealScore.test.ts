import { describe, it, expect } from 'vitest';
import { scoreDeal, scoreDeals } from './dealScore';
import { LeaseDealSchema, type LeaseDeal } from '../schemas';

function makeDeal(overrides: Partial<LeaseDeal> = {}): LeaseDeal {
  return LeaseDealSchema.parse({
    listPrice: 200000,
    sellingPrice: 180000,
    monthlyPayment: 2200,
    downPayment: 10000,
    termMonths: 36,
    annualMileage: 15000,
    residualValue: 120000,
    moneyFactor: 0.001,
    incentives: 0,
    fees: 1000,
    ...overrides,
  });
}

describe('scoreDeal', () => {
  it('returns a score within 0-100 and a valid rating', () => {
    const result = scoreDeal(makeDeal());
    expect(result.score).toBeGreaterThanOrEqual(0);
    expect(result.score).toBeLessThanOrEqual(100);
    expect(['excellent', 'good', 'fair', 'weak', 'poor']).toContain(result.rating);
  });

  it('rates a strongly discounted, low-cost deal higher than a bad one', () => {
    const good = scoreDeal(
      makeDeal({ sellingPrice: 170000, monthlyPayment: 1900, moneyFactor: 0.0005, residualValue: 130000 }),
    );
    const bad = scoreDeal(
      makeDeal({ sellingPrice: 200000, monthlyPayment: 3500, moneyFactor: 0.004, residualValue: 70000 }),
    );
    expect(good.score).toBeGreaterThan(bad.score);
  });

  it('computes APR from the money factor', () => {
    const result = scoreDeal(makeDeal({ moneyFactor: 0.002 }));
    expect(result.metrics.apr).toBeCloseTo(4.8, 5);
  });

  it('defaults sellingPrice to listPrice when omitted', () => {
    const result = scoreDeal(makeDeal({ sellingPrice: undefined }));
    expect(result.metrics.sellingPrice).toBe(200000);
    expect(result.metrics.discountPct).toBe(0);
  });

  it('echoes back the reference when provided', () => {
    const result = scoreDeal(makeDeal({ reference: 'deal-42' }));
    expect(result.reference).toBe('deal-42');
  });

  it('scores a batch of deals', () => {
    const results = scoreDeals([makeDeal(), makeDeal({ reference: 'b' })]);
    expect(results).toHaveLength(2);
  });
});

describe('LeaseDealSchema', () => {
  it('rejects a residual value greater than list price', () => {
    expect(() => makeDeal({ residualValue: 250000 })).toThrow();
  });

  it('rejects a non-positive monthly payment', () => {
    expect(() => makeDeal({ monthlyPayment: 0 })).toThrow();
  });
});
