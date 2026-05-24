
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

async function loginWithEmail(email, password) {
  const sb = getSupabase();
  if (!sb) throw new Error('Supabase not initialized');
  
  const { data, error } = await sb.auth.signInWithPassword({
    email,
    password
  });
  
  if (error) throw error;
  return data;
}

async function loginWithPhone(phone, password) {
  const sb = getSupabase();
  if (!sb) throw new Error('Supabase not initialized');
  
  const { data, error } = await sb.auth.signInWithPassword({
    phone,
    password
  });
  
  if (error) throw error;
  return data;
}

async function registerWithEmail(email, password, phone) {
  const sb = getSupabase();
  if (!sb) throw new Error('Supabase not initialized');
  
  const { data, error } = await sb.auth.signUp({
    email,
    password,
    options: {
      data: {
        phone: phone
      }
    }
  });
  
  if (error) throw error;
  
  if (data.user) {
    await createUserProfile(data.user.id, phone);
  }
  
  return data;
}

async function registerWithPhone(phone, password) {
  const sb = getSupabase();
  if (!sb) throw new Error('Supabase not initialized');
  
  const { data, error } = await sb.auth.signUp({
    phone,
    password
  });
  
  if (error) throw error;
  
  if (data.user) {
    await createUserProfile(data.user.id, phone);
  }
  
  return data;
}

async function createUserProfile(userId, phone) {
  const sb = getSupabase();
  if (!sb) throw new Error('Supabase not initialized');
  
  const { data, error } = await sb
    .from('user_profiles')
    .upsert({
      id: userId,
      phone: phone,
      points_balance: 0,
      role: 'user'
    })
    .select()
    .single();
  
  if (error) {
    console.error('Error creating user profile:', error);
  }
  
  return data;
}

async function logout() {
  const sb = getSupabase();
  if (!sb) throw new Error('Supabase not initialized');
  
  const { error } = await sb.auth.signOut();
  if (error) throw error;
  
  window.location.href = '/login.html';
}

async function getCurrentUser() {
  const sb = getSupabase();
  if (!sb) return null;
  
  try {
    const { data: { user }, error } = await sb.auth.getUser();
    if (error) {
      console.log('No active session:', error.message);
      return null;
    }
    return user;
  } catch (error) {
    console.log('Error getting current user:', error);
    return null;
  }
}

async function getUserProfile() {
  const user = await getCurrentUser();
  if (!user) return null;
  
  const sb = getSupabase();
  if (!sb) return null;
  
  const { data, error } = await sb
    .from('user_profiles')
    .select('*')
    .eq('id', user.id)
    .single();
  
  if (error) {
    console.error('Error fetching user profile:', error);
    return null;
  }
  
  return data;
}

async function checkAuthState(callback) {
  const sb = getSupabase();
  if (!sb) return;
  
  sb.auth.onAuthStateChange((event, session) =&gt; {
    if (callback) {
      callback(session);
    }
  });
}

async function checkAuthAndRedirect(redirectTo = '/login.html') {
  const user = await getCurrentUser();
  if (!user) {
    window.location.href = redirectTo;
    return false;
  }
  return true;
}

async function isAdmin() {
  const profile = await getUserProfile();
  return profile &amp;&amp; profile.role === 'admin';
}

function showToast(message, type = 'success') {
  const container = document.querySelector('.toast-container') || createToastContainer();
  
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  
  container.appendChild(toast);
  
  setTimeout(() =&gt; {
    toast.remove();
  }, 3000);
}

function createToastContainer() {
  const container = document.createElement('div');
  container.className = 'toast-container';
  document.body.appendChild(container);
  return container;
}

// 导出到全局作用域
window.auth = {
  initSupabase,
  getSupabase,
  loginWithEmail,
  loginWithPhone,
  registerWithEmail,
  registerWithPhone,
  logout,
  getCurrentUser,
  getUserProfile,
  checkAuthState,
  checkAuthAndRedirect,
  isAdmin,
  showToast
};

