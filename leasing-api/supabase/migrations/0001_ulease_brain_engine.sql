-- =============================================================================
-- ULease Brain Engine — Phase 1 (100% Deterministic, CQRS)
-- Migration: 0001_ulease_brain_engine
-- Target: Supabase / PostgreSQL 15+
-- -----------------------------------------------------------------------------
-- DATA FLOW (CQRS, event-driven):
--   WRITE  ──▶ public.deal_proposals  (Command model — a proposed deal)
--             │  AFTER INSERT/UPDATE trigger
--             ▼
--   PIPELINE ▶ Financial ▶ Risk ▶ Market ▶ Supplier ▶ Residual ▶ Aggregate
--             │  (PL/pgSQL functions, all weights/defaults from system_config)
--             ▼
--   READ   ──▶ public.deal_intelligence  (Query model — pre-computed scores)
--             └─▶ public.audit_logs      (append-only transparency trail)
--
-- DETERMINISM CONTRACT: no LLM, no random, no hardcoded business variables.
-- Every weight, default and threshold is fetched live from system_config.
-- =============================================================================

create extension if not exists pgcrypto;   -- gen_random_uuid()

-- =============================================================================
-- SECTION 1 — TABLES
-- =============================================================================

-- 1.1 system_config — single source of truth for every tunable business value.
create table if not exists public.system_config (
    key          text        primary key,
    value        numeric      not null,
    category     text         not null default 'general',
    description  text,
    updated_at   timestamptz  not null default now()
);
comment on table public.system_config is
    'Tunable business variables (weights, defaults, thresholds). Zero hardcoding: the engine reads everything from here.';

-- 1.2 market_anchor — market reference data per vehicle (read-side anchor).
create table if not exists public.market_anchor (
    vehicle_id        text        primary key,
    stratum_group     text        not null,
    market_price      numeric(12,2) not null,
    median_deal       numeric(12,2),
    percentile_25     numeric(12,2),
    percentile_75     numeric(12,2),
    depreciation_rate numeric(5,4) not null default 0.15
                      check (depreciation_rate >= 0 and depreciation_rate <= 1),
    updated_at        timestamptz not null default now()
);
comment on table public.market_anchor is 'Per-vehicle market anchors: price bands and annual depreciation rate.';

-- 1.3 supplier_metrics — supplier reputation & risk anchor.
create table if not exists public.supplier_metrics (
    supplier_id         text        primary key,
    reputation_score    numeric(5,2) not null default 50
                        check (reputation_score >= 0 and reputation_score <= 100),
    default_risk_factor numeric(5,4) not null default 0.10
                        check (default_risk_factor >= 0 and default_risk_factor <= 1),
    updated_at          timestamptz not null default now()
);
comment on table public.supplier_metrics is 'Supplier reputation (0-100) and probability-of-default factor (0-1).';

-- 1.4 deal_proposals — WRITE / Command model. A write here kicks off the pipeline.
create table if not exists public.deal_proposals (
    deal_id            uuid        primary key default gen_random_uuid(),
    vehicle_id         text        references public.market_anchor(vehicle_id)   on delete set null,
    supplier_id        text        references public.supplier_metrics(supplier_id) on delete set null,
    market_value       numeric(12,2) not null check (market_value >= 0),  -- agreed vehicle value
    list_price         numeric(12,2),                                     -- sticker / מחירון
    duration_months    integer      not null check (duration_months > 0),
    monthly_payment    numeric(12,2) not null check (monthly_payment >= 0),
    down_payment       numeric(12,2) not null default 0 check (down_payment >= 0),
    annual_insurance   numeric(12,2),   -- nullable → falls back to system_config
    annual_maintenance numeric(12,2),   -- nullable → falls back to system_config
    annual_km          integer,
    status             text         not null default 'pending',
    created_at         timestamptz  not null default now(),
    updated_at         timestamptz  not null default now()
);
comment on table public.deal_proposals is 'CQRS write model. INSERT/UPDATE triggers the deterministic scoring pipeline.';

-- 1.5 deal_intelligence — READ / Query model. Pre-computed, served by the API.
--     residual_score is persisted (the aggregate formula has a Residual term).
create table if not exists public.deal_intelligence (
    deal_id         uuid        primary key references public.deal_proposals(deal_id) on delete cascade,
    financial_score numeric(6,2) not null,
    risk_score      numeric(6,2) not null,
    market_score    numeric(6,2) not null,
    supplier_score  numeric(6,2) not null,
    residual_score  numeric(6,2) not null,
    total_score     numeric(6,2) not null,
    confidence      numeric(4,3) not null check (confidence >= 0 and confidence <= 1),
    recommendation  text         not null
                    check (recommendation in ('STRONG_BUY','BUY','HOLD','PASS')),
    computed_at     timestamptz  not null default now()
);
comment on table public.deal_intelligence is 'CQRS read model. The API reads ONLY from here — never recomputes.';

-- 1.6 audit_logs — append-only trail of every score computation.
create table if not exists public.audit_logs (
    id          bigint      generated always as identity primary key,
    deal_id     uuid,
    event_type  text        not null,
    payload     jsonb       not null,
    created_at  timestamptz not null default now()
);
comment on table public.audit_logs is 'Append-only transparency log: full input + output snapshot per score run.';

create index if not exists idx_audit_logs_deal_id   on public.audit_logs (deal_id);
create index if not exists idx_audit_logs_created_at on public.audit_logs (created_at desc);
create index if not exists idx_deal_proposals_vehicle  on public.deal_proposals (vehicle_id);
create index if not exists idx_deal_proposals_supplier on public.deal_proposals (supplier_id);

-- =============================================================================
-- SECTION 2 — ROW LEVEL SECURITY
-- RLS is enabled on all tables (Supabase best practice). No public policies are
-- granted: the read API must use the SERVICE ROLE key (server-side / edge), which
-- bypasses RLS. Add explicit policies before exposing any table to anon clients.
-- =============================================================================
alter table public.system_config    enable row level security;
alter table public.market_anchor     enable row level security;
alter table public.supplier_metrics  enable row level security;
alter table public.deal_proposals     enable row level security;
alter table public.deal_intelligence  enable row level security;
alter table public.audit_logs         enable row level security;

-- =============================================================================
-- SECTION 3 — BASELINE CONFIG (weights sum to 1.00)
-- =============================================================================
insert into public.system_config (key, value, category, description) values
    ('weight_tco',       0.40, 'weights', 'Financial / TCO weight in the aggregate score'),
    ('weight_risk',      0.20, 'weights', 'Risk weight in the aggregate score'),
    ('weight_demand',    0.15, 'weights', 'Market / demand weight in the aggregate score'),
    ('weight_supplier',  0.15, 'weights', 'Supplier weight in the aggregate score'),
    ('weight_residual',  0.10, 'weights', 'Residual-value weight in the aggregate score'),
    ('default_annual_insurance',   6000, 'defaults', 'Fallback annual insurance (ILS) when a deal omits it'),
    ('default_annual_maintenance', 3000, 'defaults', 'Fallback annual maintenance (ILS) when a deal omits it'),
    ('default_depreciation_rate',  0.15, 'defaults', 'Fallback annual depreciation rate when no market_anchor row'),
    ('default_risk_factor',        0.10, 'defaults', 'Fallback supplier probability-of-default factor'),
    ('neutral_score',              50,   'defaults', 'Neutral 0-100 score used when an anchor is missing'),
    ('tco_par_ratio',     0.60, 'financial', 'TCO/market-value ratio that maps to a neutral 50 score'),
    ('tco_sensitivity',   150,  'financial', 'Score points gained/lost per 1.0 of TCO ratio vs par'),
    ('risk_downpayment_weight', 0.30, 'risk', 'How much down-payment coverage offsets supplier default risk'),
    ('rec_threshold_strong', 85, 'recommendation', 'total_score >= this → STRONG_BUY'),
    ('rec_threshold_buy',    70, 'recommendation', 'total_score >= this → BUY'),
    ('rec_threshold_hold',   55, 'recommendation', 'total_score >= this → HOLD (else PASS)'),
    ('confidence_penalty_missing_market',   0.25, 'confidence', 'Confidence penalty when market_anchor is missing'),
    ('confidence_penalty_missing_supplier', 0.20, 'confidence', 'Confidence penalty when supplier_metrics is missing'),
    ('confidence_penalty_defaulted_cost',   0.10, 'confidence', 'Confidence penalty when insurance/maintenance were defaulted')
on conflict (key) do nothing;

-- =============================================================================
-- SECTION 4 — HELPERS
-- =============================================================================

-- 4.1 ulease_cfg: read a config value, with a safe in-code fallback default.
create or replace function public.ulease_cfg(p_key text, p_default numeric)
returns numeric
language sql
stable
as $$
    select coalesce((select value from public.system_config where key = p_key), p_default);
$$;

-- 4.2 ulease_clamp: bound a value to [lo, hi].
create or replace function public.ulease_clamp(v numeric, lo numeric, hi numeric)
returns numeric
language sql
immutable
as $$
    select least(greatest(v, lo), hi);
$$;

-- =============================================================================
-- SECTION 5 — SCORING MODULES (pure, deterministic, 0-100)
-- =============================================================================

-- 5.1 calculate_financial_score — TCO + Depreciation Engine.
--     depreciation = market_value * depreciation_rate * (duration_months / 12)
--     TCO = payments + insurance + maintenance - residual_value
--     Lower TCO relative to vehicle value ⇒ higher score (config-driven mapping).
create or replace function public.calculate_financial_score(
    p_vehicle_id      text,
    p_market_value    numeric,
    p_duration_months integer,
    p_monthly_payment numeric,
    p_insurance       numeric,
    p_maintenance     numeric
) returns numeric
language plpgsql
stable
as $$
declare
    v_years          numeric := p_duration_months::numeric / 12.0;
    v_dep_rate       numeric;
    v_insurance      numeric;
    v_maintenance    numeric;
    v_depreciation   numeric;
    v_residual_value numeric;
    v_tco            numeric;
    v_ratio          numeric;
    v_score          numeric;
begin
    -- depreciation rate: prefer the vehicle's market anchor, else config default
    select depreciation_rate into v_dep_rate
        from public.market_anchor where vehicle_id = p_vehicle_id;
    v_dep_rate := coalesce(v_dep_rate, public.ulease_cfg('default_depreciation_rate', 0.15));

    -- insurance / maintenance: fall back to config when the proposal omits them
    v_insurance   := coalesce(p_insurance,   public.ulease_cfg('default_annual_insurance',   6000));
    v_maintenance := coalesce(p_maintenance, public.ulease_cfg('default_annual_maintenance', 3000));

    -- Depreciation Engine (per blueprint)
    v_depreciation   := p_market_value * v_dep_rate * v_years;
    v_residual_value := greatest(p_market_value - v_depreciation, 0);

    -- Total Cost of Ownership across the lease term
    v_tco := (p_monthly_payment * p_duration_months)
           + (v_insurance   * v_years)
           + (v_maintenance * v_years)
           - v_residual_value;

    -- Map TCO → 0..100. ratio = TCO / market_value; par maps to 50.
    v_ratio := case when p_market_value > 0 then v_tco / p_market_value else 1 end;
    v_score := 50 + (public.ulease_cfg('tco_par_ratio', 0.60) - v_ratio)
                    * public.ulease_cfg('tco_sensitivity', 150);

    return public.ulease_clamp(round(v_score, 2), 0, 100);
end;
$$;

-- 5.2 calculate_risk_score — supplier default risk offset by down-payment coverage.
create or replace function public.calculate_risk_score(
    p_supplier_id  text,
    p_market_value numeric,
    p_down_payment numeric
) returns numeric
language plpgsql
stable
as $$
declare
    v_drf      numeric;
    v_dp_ratio numeric;
    v_w_dp     numeric := public.ulease_cfg('risk_downpayment_weight', 0.30);
    v_score    numeric;
begin
    select default_risk_factor into v_drf
        from public.supplier_metrics where supplier_id = p_supplier_id;
    v_drf := coalesce(v_drf, public.ulease_cfg('default_risk_factor', 0.10));

    v_dp_ratio := case when p_market_value > 0
                       then public.ulease_clamp(p_down_payment / p_market_value, 0, 1)
                       else 0 end;

    -- base creditworthiness 100*(1-drf), blended with down-payment coverage
    v_score := (100 * (1 - v_drf)) * (1 - v_w_dp) + (100 * v_dp_ratio) * v_w_dp;

    return public.ulease_clamp(round(v_score, 2), 0, 100);
end;
$$;

-- 5.3 calculate_market_score — where the deal price sits in the market band.
--     <= p25 ⇒ 100 (great price) ; >= p75 ⇒ 0 (expensive) ; linear between.
create or replace function public.calculate_market_score(
    p_vehicle_id text,
    p_deal_price numeric
) returns numeric
language plpgsql
stable
as $$
declare
    v_p25   numeric;
    v_p75   numeric;
    v_score numeric;
begin
    select percentile_25, percentile_75 into v_p25, v_p75
        from public.market_anchor where vehicle_id = p_vehicle_id;

    if v_p25 is null or v_p75 is null or v_p75 <= v_p25 then
        return public.ulease_cfg('neutral_score', 50);
    end if;

    v_score := 100 * (v_p75 - p_deal_price) / (v_p75 - v_p25);
    return public.ulease_clamp(round(v_score, 2), 0, 100);
end;
$$;

-- 5.4 calculate_supplier_score — direct reputation read.
create or replace function public.calculate_supplier_score(
    p_supplier_id text
) returns numeric
language plpgsql
stable
as $$
declare
    v_rep numeric;
begin
    select reputation_score into v_rep
        from public.supplier_metrics where supplier_id = p_supplier_id;
    return public.ulease_clamp(round(coalesce(v_rep, public.ulease_cfg('neutral_score', 50)), 2), 0, 100);
end;
$$;

-- 5.5 calculate_residual_score — value retention (higher residual ⇒ higher score).
create or replace function public.calculate_residual_score(
    p_vehicle_id      text,
    p_market_value    numeric,
    p_duration_months integer
) returns numeric
language plpgsql
stable
as $$
declare
    v_years    numeric := p_duration_months::numeric / 12.0;
    v_dep_rate numeric;
    v_residual numeric;
    v_score    numeric;
begin
    select depreciation_rate into v_dep_rate
        from public.market_anchor where vehicle_id = p_vehicle_id;
    v_dep_rate := coalesce(v_dep_rate, public.ulease_cfg('default_depreciation_rate', 0.15));

    v_residual := greatest(p_market_value - (p_market_value * v_dep_rate * v_years), 0);
    v_score := case when p_market_value > 0 then 100 * v_residual / p_market_value else 0 end;

    return public.ulease_clamp(round(v_score, 2), 0, 100);
end;
$$;

-- =============================================================================
-- SECTION 6 — AGGREGATE
--   Final = 0.4·Financial + 0.2·Risk + 0.15·Market + 0.15·Supplier + 0.1·Residual
--   Weights are read from system_config and normalised defensively.
-- =============================================================================
create or replace function public.aggregate_total_score(
    p_financial numeric,
    p_risk      numeric,
    p_market    numeric,
    p_supplier  numeric,
    p_residual  numeric
) returns numeric
language plpgsql
stable
as $$
declare
    w_tco numeric := public.ulease_cfg('weight_tco',      0.40);
    w_rsk numeric := public.ulease_cfg('weight_risk',     0.20);
    w_dmd numeric := public.ulease_cfg('weight_demand',   0.15);
    w_sup numeric := public.ulease_cfg('weight_supplier', 0.15);
    w_res numeric := public.ulease_cfg('weight_residual', 0.10);
    w_sum numeric;
    v_total numeric;
begin
    w_sum := w_tco + w_rsk + w_dmd + w_sup + w_res;
    v_total := (w_tco * p_financial)
             + (w_rsk * p_risk)
             + (w_dmd * p_market)
             + (w_sup * p_supplier)
             + (w_res * p_residual);
    return round(case when w_sum > 0 then v_total / w_sum else 0 end, 2);
end;
$$;

-- =============================================================================
-- SECTION 7 — MASTER ORCHESTRATOR (trigger function)
--   SECURITY DEFINER so the WRITE→READ projection works regardless of caller RLS.
-- =============================================================================
create or replace function public.fn_ulease_score_deal()
returns trigger
language plpgsql
security definer
set search_path = public, pg_temp
as $$
declare
    v_financial numeric;
    v_risk      numeric;
    v_market    numeric;
    v_supplier  numeric;
    v_residual  numeric;
    v_total     numeric;
    v_confidence numeric := 1.0;
    v_recommendation text;
    v_has_market   boolean;
    v_has_supplier boolean;
    v_defaulted_cost boolean;
begin
    -- data availability (drives the confidence score)
    v_has_market     := exists (select 1 from public.market_anchor    where vehicle_id  = new.vehicle_id);
    v_has_supplier   := exists (select 1 from public.supplier_metrics  where supplier_id = new.supplier_id);
    v_defaulted_cost := (new.annual_insurance is null or new.annual_maintenance is null);

    -- COMMAND → PIPELINE: Financial → Risk → Market → Supplier → Residual → Aggregate
    v_financial := public.calculate_financial_score(new.vehicle_id, new.market_value, new.duration_months,
                                                     new.monthly_payment, new.annual_insurance, new.annual_maintenance);
    v_risk      := public.calculate_risk_score(new.supplier_id, new.market_value, new.down_payment);
    v_market    := public.calculate_market_score(new.vehicle_id, new.market_value);
    v_supplier  := public.calculate_supplier_score(new.supplier_id);
    v_residual  := public.calculate_residual_score(new.vehicle_id, new.market_value, new.duration_months);
    v_total     := public.aggregate_total_score(v_financial, v_risk, v_market, v_supplier, v_residual);

    -- confidence: deterministic, penalised by missing/defaulted inputs
    if not v_has_market   then v_confidence := v_confidence - public.ulease_cfg('confidence_penalty_missing_market',   0.25); end if;
    if not v_has_supplier then v_confidence := v_confidence - public.ulease_cfg('confidence_penalty_missing_supplier', 0.20); end if;
    if v_defaulted_cost   then v_confidence := v_confidence - public.ulease_cfg('confidence_penalty_defaulted_cost',   0.10); end if;
    v_confidence := public.ulease_clamp(round(v_confidence, 3), 0, 1);

    -- recommendation bands (config-driven)
    v_recommendation := case
        when v_total >= public.ulease_cfg('rec_threshold_strong', 85) then 'STRONG_BUY'
        when v_total >= public.ulease_cfg('rec_threshold_buy',    70) then 'BUY'
        when v_total >= public.ulease_cfg('rec_threshold_hold',   55) then 'HOLD'
        else 'PASS'
    end;

    -- WRITE → READ projection (CQRS upsert)
    insert into public.deal_intelligence as di
        (deal_id, financial_score, risk_score, market_score, supplier_score,
         residual_score, total_score, confidence, recommendation, computed_at)
    values
        (new.deal_id, v_financial, v_risk, v_market, v_supplier,
         v_residual, v_total, v_confidence, v_recommendation, now())
    on conflict (deal_id) do update set
        financial_score = excluded.financial_score,
        risk_score      = excluded.risk_score,
        market_score    = excluded.market_score,
        supplier_score  = excluded.supplier_score,
        residual_score  = excluded.residual_score,
        total_score     = excluded.total_score,
        confidence      = excluded.confidence,
        recommendation  = excluded.recommendation,
        computed_at     = now();

    -- transparency: append-only audit snapshot
    insert into public.audit_logs (deal_id, event_type, payload)
    values (new.deal_id, 'SCORE_COMPUTED', jsonb_build_object(
        'inputs', jsonb_build_object(
            'vehicle_id', new.vehicle_id, 'supplier_id', new.supplier_id,
            'market_value', new.market_value, 'duration_months', new.duration_months,
            'monthly_payment', new.monthly_payment, 'down_payment', new.down_payment,
            'annual_insurance', new.annual_insurance, 'annual_maintenance', new.annual_maintenance),
        'scores', jsonb_build_object(
            'financial', v_financial, 'risk', v_risk, 'market', v_market,
            'supplier', v_supplier, 'residual', v_residual, 'total', v_total),
        'confidence', v_confidence,
        'recommendation', v_recommendation,
        'data_availability', jsonb_build_object(
            'market_anchor', v_has_market, 'supplier_metrics', v_has_supplier,
            'defaulted_cost', v_defaulted_cost),
        'tg_op', tg_op
    ));

    return new;
end;
$$;

-- 7.1 the Master Trigger
drop trigger if exists trg_ulease_score_deal on public.deal_proposals;
create trigger trg_ulease_score_deal
    after insert or update on public.deal_proposals
    for each row
    execute function public.fn_ulease_score_deal();

-- =============================================================================
-- END OF MIGRATION
-- =============================================================================
