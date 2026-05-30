-- Fix RLS: Allow anon read access to moe_2026_reference
-- The table is not exposed in the public API, but we use the anon key internally
ALTER TABLE public.moe_2026_reference ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Internal access only" ON public.moe_2026_reference;

-- Allow read access to anyone with the anon key (used internally)
CREATE POLICY "Allow anon read" ON public.moe_2026_reference
  FOR SELECT
  TO anon
  USING (true);

-- Allow full access to authenticated users
CREATE POLICY "Allow auth full access" ON public.moe_2026_reference
  FOR ALL
  TO authenticated
  USING (true)
  WITH CHECK (true);
