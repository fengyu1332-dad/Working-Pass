
const SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4';

let supabaseClient = null;

function initSupabase() {
  if (typeof supabase !== 'undefined') {
    supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
    return supabaseClient;
  }
  return null;
}

function getSupabase() {
  if (!supabaseClient) {
    initSupabase();
  }
  return supabaseClient;
}

function configureSupabase(url, key) {
  if (typeof supabase !== 'undefined') {
    supabaseClient = supabase.createClient(url, key);
  }
}

if (typeof window) {
  window.supabaseClient = {
    init: initSupabase,
    get: getSupabase,
    configure: configureSupabase
  };
}

