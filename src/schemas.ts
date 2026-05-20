import { z } from 'zod';

/**
 * A single leasing deal to be scored. All monetary values are in the same
 * currency (ILS by convention) and represent the quoted offer.
 */
export const LeaseDealSchema = z
  .object({
    // Manufacturer list price / MSRP of the vehicle.
    listPrice: z.number().positive(),
    // Negotiated selling (capitalized) price. Defaults to listPrice when omitted.
    sellingPrice: z.number().positive().optional(),
    // Monthly lease payment.
    monthlyPayment: z.number().positive(),
    // Up-front payment / capitalized cost reduction.
    downPayment: z.number().min(0).default(0),
    // Lease length in months.
    termMonths: z.number().int().min(1).max(120),
    // Contracted annual mileage allowance (km).
    annualMileage: z.number().int().min(0).default(15000),
    // Vehicle value at lease end.
    residualValue: z.number().min(0),
    // Lease money factor (multiply by 2400 to approximate APR %).
    moneyFactor: z.number().min(0).max(1),
    // One-off manufacturer / dealer incentives applied to the deal.
    incentives: z.number().min(0).default(0),
    // One-off acquisition / disposition fees.
    fees: z.number().min(0).default(0),
    // Optional free-form identifier echoed back in the response.
    reference: z.string().max(120).optional(),
  })
  .refine((d) => (d.sellingPrice ?? d.listPrice) <= d.listPrice * 1.5, {
    message: 'sellingPrice is unrealistically higher than listPrice',
    path: ['sellingPrice'],
  })
  .refine((d) => d.residualValue <= d.listPrice, {
    message: 'residualValue cannot exceed listPrice',
    path: ['residualValue'],
  });

export type LeaseDeal = z.infer<typeof LeaseDealSchema>;

/** Request body for the scoring endpoint: a single deal or a batch. */
export const ScoreRequestSchema = z.union([
  LeaseDealSchema,
  z.object({ deals: z.array(LeaseDealSchema).min(1).max(100) }),
]);

export type ScoreRequest = z.infer<typeof ScoreRequestSchema>;
