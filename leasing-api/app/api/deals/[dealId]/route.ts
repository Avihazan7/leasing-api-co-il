// =============================================================================
// GET /api/deals/[dealId]
// Read-only endpoint. Returns the PRE-COMPUTED intelligence for a deal straight
// from the CQRS read model (deal_intelligence). It performs NO calculations —
// all scoring happens in the database pipeline (see the SQL migration). This is
// what keeps the "Ambient UI" lightning fast.
// =============================================================================
import { NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';
import type { DealIntelligence } from '@/types/ulease';

// Edge runtime for minimum latency at the CDN edge.
export const runtime = 'edge';
// Always reflect the latest projection (no full-route static caching).
export const dynamic = 'force-dynamic';

export async function GET(
  _request: Request,
  // Next.js 15 App Router: route params are async.
  context: { params: Promise<{ dealId: string }> }
) {
  const { dealId } = await context.params;

  if (!dealId) {
    return NextResponse.json({ error: 'dealId is required' }, { status: 400 });
  }

  // Pure read from the query model — never recompute here.
  const { data, error } = await supabase
    .from('deal_intelligence')
    .select(
      'deal_id, financial_score, risk_score, market_score, supplier_score, residual_score, total_score, confidence, recommendation, computed_at'
    )
    .eq('deal_id', dealId)
    .maybeSingle();

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
  if (!data) {
    return NextResponse.json({ error: 'Deal intelligence not found' }, { status: 404 });
  }

  // Short edge cache: fast repeat reads, refreshed shortly after a re-score.
  return NextResponse.json(data as DealIntelligence, {
    status: 200,
    headers: { 'Cache-Control': 'public, s-maxage=30, stale-while-revalidate=60' },
  });
}
