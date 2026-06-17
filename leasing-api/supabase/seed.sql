-- =============================================================================
-- ULease Brain Engine — sample seed for smoke-testing (dev only).
-- Run AFTER 0001_ulease_brain_engine.sql. Safe & idempotent.
-- Inserting the proposal fires the trigger → deal_intelligence + audit_logs.
-- =============================================================================

insert into public.market_anchor
    (vehicle_id, stratum_group, market_price, median_deal, percentile_25, percentile_75, depreciation_rate)
values
    ('TESLA-MODEL3-2026', 'EV-PREMIUM', 250000, 235000, 225000, 248000, 0.18)
on conflict (vehicle_id) do nothing;

insert into public.supplier_metrics
    (supplier_id, reputation_score, default_risk_factor)
values
    ('IMPORTER-ALPHA', 88, 0.05)
on conflict (supplier_id) do nothing;

insert into public.deal_proposals
    (deal_id, vehicle_id, supplier_id, market_value, list_price, duration_months,
     monthly_payment, down_payment, annual_insurance, annual_maintenance, annual_km)
values
    ('00000000-0000-0000-0000-000000000001', 'TESLA-MODEL3-2026', 'IMPORTER-ALPHA',
     235000, 250000, 36, 3200, 30000, 6500, 3200, 20000)
on conflict (deal_id) do update set monthly_payment = excluded.monthly_payment;

-- Verify the read model + audit trail:
--   select * from public.deal_intelligence where deal_id = '00000000-0000-0000-0000-000000000001';
--   select payload from public.audit_logs order by created_at desc limit 1;
