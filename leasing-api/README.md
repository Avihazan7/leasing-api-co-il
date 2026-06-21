# ULease Brain Engine — Phase 1 (Deterministic Scoring, CQRS)

Production-ready backend for **Leasing.co.il**. Phase 1 is a **100% deterministic**
deal-scoring engine — no LLM in the pricing path, no hardcoded business variables.
All weights, defaults and thresholds live in the `system_config` table and are read
live by the database pipeline.

> ⚠️ **SUPERSEDED — historical prototype, do NOT copy into `leasing-api`.**
> This was the *Phase-1 in-database* approach (scoring as a PL/pgSQL trigger
> pipeline over `deal_proposals`/`deal_intelligence`). The `leasing-api` repo has
> since adopted a **different, canonical architecture**: the Deal Brain runs in
> **TypeScript** — `src/engines/orchestrator.ts` + 9 deterministic engines
> (`economic`, `trust`, `risk`, `urgency`, `market`, `bigfive`, `gametheory`,
> `decision`) — reading live `users`/`offers`/`suppliers` from Supabase and wired
> to `/api/deal-score` and `/api/match-agent`. Importing this migration would add a
> second, unwired, competing engine. Kept here only as a methodology record of the
> in-DB CQRS design (the original "copy these files there" instruction no longer
> applies).

## Architecture — Event-driven CQRS

```
WRITE  ──▶ deal_proposals        (Command model)
            │  AFTER INSERT/UPDATE trigger: fn_ulease_score_deal()
            ▼
PIPELINE ▶ Financial ▶ Risk ▶ Market ▶ Supplier ▶ Residual ▶ Aggregate
            │  (PL/pgSQL, all tunables from system_config)
            ▼
READ   ──▶ deal_intelligence     (Query model — pre-computed)
            └─▶ audit_logs        (append-only transparency trail)

API    ──▶ GET /api/deals/[dealId]  → reads ONLY deal_intelligence (edge, fast)
```

The write side and read side never share a query path: the API performs **zero**
calculation, so reads are lightning fast and "Ambient UI" ready.

## Files

| File | Goes to (`leasing-api` repo) | Purpose |
| --- | --- | --- |
| `supabase/migrations/0001_ulease_brain_engine.sql` | same path | Schema + config + PL/pgSQL pipeline + trigger |
| `supabase/seed.sql` | same path | Sample data to smoke-test the engine (dev only) |
| `types/ulease.ts` | `types/ulease.ts` | TypeScript contracts for every table |
| `lib/supabase.ts` | `lib/supabase.ts` | Server-only Supabase client (service role) |
| `app/api/deals/[dealId]/route.ts` | same path | Read-only edge API for the read model |

## The scoring model

`total_score (0–100) = 0.40·Financial + 0.20·Risk + 0.15·Market + 0.15·Supplier + 0.10·Residual`

| Module | Reads from | Logic (Phase 1) |
| --- | --- | --- |
| **Financial** | proposal + `market_anchor` + config | TCO with a depreciation engine: `depreciation = market_value · rate · (months/12)`; lower TCO/value ⇒ higher score |
| **Risk** | `supplier_metrics` + proposal | supplier default factor offset by down-payment coverage |
| **Market** | `market_anchor` | where the deal price sits in the p25–p75 band |
| **Supplier** | `supplier_metrics` | reputation score (0–100) |
| **Residual** | `market_anchor` + config | retained value after depreciation |

`confidence (0–1)` is reduced deterministically when an anchor row is missing or
insurance/maintenance had to be defaulted. `recommendation ∈ {STRONG_BUY, BUY,
HOLD, PASS}` from config thresholds.

> `deal_proposals.vehicle_id` / `supplier_id` are foreign keys: a proposal must
> reference an existing `market_anchor` / `supplier_metrics` row **or be `NULL`**.
> When `NULL`, the engine falls back to `system_config` defaults and lowers
> `confidence` — so a deal is always scorable, never blocked.

**Tuning is data, not code** — change a weight/threshold with one `UPDATE` on
`system_config`; no redeploy:

```sql
update public.system_config set value = 0.45 where key = 'weight_tco';
```

## Deploy (review from mobile, then run)

1. **DB** — apply the migration (Supabase Dashboard → SQL Editor, paste the file;
   or `supabase db push` with the CLI). Optionally run `seed.sql` to verify.
2. **App** — copy the TS files into `leasing-api`, then set Vercel env vars:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY` *(server-only — never expose to the client)*
   - requires `@supabase/supabase-js` in dependencies.
3. **Verify** — `GET /api/deals/00000000-0000-0000-0000-000000000001` returns the
   pre-computed scores after seeding.

## Security notes

- RLS is **enabled** on all tables with no public policies (deny by default). The
  API uses the **service role** server-side, which bypasses RLS. Add explicit
  `select` policies before exposing any table to anon clients.
- The trigger function is `SECURITY DEFINER` with a pinned `search_path` so the
  WRITE→READ projection succeeds regardless of the caller's RLS context.
- Add authentication/authorization in front of `GET /api/deals/[dealId]` before
  production — it currently returns intelligence for any known `dealId`.

## Phase 2 (not in scope tonight)

Awaiting approval before: richer Risk/Market models, `comparables` via pgvector
(`ULEASE_SPEC.md §7.1`), second-price auction, and the Match engine.
