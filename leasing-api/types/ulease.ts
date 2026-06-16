// =============================================================================
// ULease Brain Engine — TypeScript contracts
// Mirrors the Supabase schema in supabase/migrations/0001_ulease_brain_engine.sql
// Keep this file in sync with the migration (the SQL is the source of truth).
// =============================================================================

/** Recommendation bands emitted by the aggregate scorer. */
export type Recommendation = 'STRONG_BUY' | 'BUY' | 'HOLD' | 'PASS';

/** system_config — every tunable business value (weights, defaults, thresholds). */
export interface SystemConfig {
  key: string;
  value: number;
  category: string;
  description: string | null;
  updated_at: string; // ISO-8601 timestamptz
}

/** market_anchor — per-vehicle market reference data. */
export interface MarketAnchor {
  vehicle_id: string;
  stratum_group: string;
  market_price: number;
  median_deal: number | null;
  percentile_25: number | null;
  percentile_75: number | null;
  depreciation_rate: number; // 0..1
  updated_at: string;
}

/** supplier_metrics — supplier reputation & risk anchor. */
export interface SupplierMetrics {
  supplier_id: string;
  reputation_score: number;     // 0..100
  default_risk_factor: number;  // 0..1
  updated_at: string;
}

/** deal_proposals — CQRS WRITE model. Inserting/updating triggers scoring. */
export interface DealProposal {
  deal_id: string; // uuid
  vehicle_id: string | null;
  supplier_id: string | null;
  market_value: number;
  list_price: number | null;
  duration_months: number;
  monthly_payment: number;
  down_payment: number;
  annual_insurance: number | null;
  annual_maintenance: number | null;
  annual_km: number | null;
  status: string;
  created_at: string;
  updated_at: string;
}

/** Fields a client supplies when creating a proposal (server fills the rest). */
export type NewDealProposal = Pick<
  DealProposal,
  'vehicle_id' | 'supplier_id' | 'market_value' | 'duration_months' | 'monthly_payment'
> &
  Partial<
    Pick<
      DealProposal,
      'list_price' | 'down_payment' | 'annual_insurance' | 'annual_maintenance' | 'annual_km' | 'status'
    >
  >;

/** deal_intelligence — CQRS READ model. Pre-computed; served by the API. */
export interface DealIntelligence {
  deal_id: string;
  financial_score: number;
  risk_score: number;
  market_score: number;
  supplier_score: number;
  residual_score: number;
  total_score: number;
  confidence: number; // 0..1
  recommendation: Recommendation;
  computed_at: string;
}

/** audit_logs — append-only transparency trail. */
export interface AuditLog {
  id: number;
  deal_id: string | null;
  event_type: string;
  payload: AuditPayload;
  created_at: string;
}

/** Structured snapshot written to audit_logs.payload on every score run. */
export interface AuditPayload {
  inputs: {
    vehicle_id: string | null;
    supplier_id: string | null;
    market_value: number;
    duration_months: number;
    monthly_payment: number;
    down_payment: number;
    annual_insurance: number | null;
    annual_maintenance: number | null;
  };
  scores: {
    financial: number;
    risk: number;
    market: number;
    supplier: number;
    residual: number;
    total: number;
  };
  confidence: number;
  recommendation: Recommendation;
  data_availability: {
    market_anchor: boolean;
    supplier_metrics: boolean;
    defaulted_cost: boolean;
  };
  tg_op: 'INSERT' | 'UPDATE';
}

/**
 * Minimal typed surface of the public schema for the Supabase client.
 * (For the full generated type, run: supabase gen types typescript.)
 */
export interface Database {
  public: {
    Tables: {
      system_config: { Row: SystemConfig };
      market_anchor: { Row: MarketAnchor };
      supplier_metrics: { Row: SupplierMetrics };
      deal_proposals: { Row: DealProposal; Insert: NewDealProposal };
      deal_intelligence: { Row: DealIntelligence };
      audit_logs: { Row: AuditLog };
    };
  };
}
