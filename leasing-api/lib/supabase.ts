// =============================================================================
// Supabase client (server-side / edge).
// Uses the SERVICE ROLE key, which bypasses RLS — so this module must NEVER be
// imported into client components. Keep SUPABASE_SERVICE_ROLE_KEY server-only
// (set it in Vercel Project → Settings → Environment Variables, NOT NEXT_PUBLIC_).
// =============================================================================
import { createClient } from '@supabase/supabase-js';
import type { Database } from '@/types/ulease';

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const SERVICE_ROLE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!SUPABASE_URL || !SERVICE_ROLE_KEY) {
  throw new Error(
    'Missing Supabase env vars: NEXT_PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required.'
  );
}

/** Read-side client for the Brain Engine. Server-only. */
export const supabase = createClient<Database>(SUPABASE_URL, SERVICE_ROLE_KEY, {
  auth: { persistSession: false, autoRefreshToken: false },
});
