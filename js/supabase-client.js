// ============================================================
// 专业星图 - Supabase 客户端配置（ES Module）
// 环境变量通过 Vite 注入，参考 .env.example
// ============================================================

export const SUPABASE_URL =
  (typeof import.meta !== 'undefined' && import.meta.env?.VITE_SUPABASE_URL) || 'https://djteatwxjlnbjylynvjh.supabase.co';
export const SUPABASE_ANON_KEY =
  (typeof import.meta !== 'undefined' && import.meta.env?.VITE_SUPABASE_ANON_KEY) || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4';

let supabaseClient = null;

export function initSupabase() {
  if (typeof supabase !== 'undefined') {
    supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
    return supabaseClient;
  }
  return null;
}

export function getSupabase() {
  if (!supabaseClient) {
    initSupabase();
  }
  return supabaseClient;
}

export function configureSupabase(url, key) {
  if (typeof supabase !== 'undefined') {
    supabaseClient = supabase.createClient(url, key);
  }
}

// 向后兼容：也挂载到全局 window
if (typeof window !== 'undefined') {
  window.supabaseClient = {
    init: initSupabase,
    get: getSupabase,
    configure: configureSupabase,
    url: SUPABASE_URL,
    key: SUPABASE_ANON_KEY,
  };
}
