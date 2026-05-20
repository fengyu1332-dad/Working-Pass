
const SUPABASE_URL = 'YOUR_SUPABASE_URL';
const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY';

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
