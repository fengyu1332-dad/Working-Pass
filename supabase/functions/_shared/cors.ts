// ============================================================
// 共享 CORS 头 — 所有 Edge Function 统一使用
// ============================================================

export const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};
