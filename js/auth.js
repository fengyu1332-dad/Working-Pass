// ============================================================
// 专业星图 - 认证模块（ES Module）
// ============================================================

import { getSupabase, initSupabase } from './supabase-client.js';

export async function loginWithEmail(email, password) {
  const sb = getSupabase();
  if (!sb) throw new Error('Supabase not initialized');

  const { data, error } = await sb.auth.signInWithPassword({ email, password });
  if (error) throw error;
  return data;
}

export async function loginWithPhone(phone, password) {
  const sb = getSupabase();
  if (!sb) throw new Error('Supabase not initialized');

  const { data, error } = await sb.auth.signInWithPassword({ phone, password });
  if (error) throw error;
  return data;
}

export async function registerWithEmail(email, password, phone) {
  const sb = getSupabase();
  if (!sb) throw new Error('Supabase not initialized');

  const { data, error } = await sb.auth.signUp({
    email,
    password,
    options: { data: { phone } },
  });
  if (error) throw error;

  if (data.user) {
    await createUserProfile(data.user.id, phone);
  }
  return data;
}

export async function registerWithPhone(phone, password) {
  const sb = getSupabase();
  if (!sb) throw new Error('Supabase not initialized');

  const { data, error } = await sb.auth.signUp({ phone, password });
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
    .upsert({ id: userId, phone, points_balance: 1, role: 'user' })
    .select()
    .single();

  if (error) {
    console.error('Error creating user profile:', error);
  }
  return data;
}

export async function logout() {
  const sb = getSupabase();
  if (!sb) throw new Error('Supabase not initialized');

  const { error } = await sb.auth.signOut();
  if (error) throw error;

  window.location.href = '/login.html';
}

export async function getCurrentUser() {
  const sb = getSupabase();
  if (!sb) return null;

  try {
    const {
      data: { user },
      error,
    } = await sb.auth.getUser();
    if (error) {
      return null;
    }
    return user;
  } catch (error) {
    return null;
  }
}

export async function getUserProfile() {
  const user = await getCurrentUser();
  if (!user) return null;

  const sb = getSupabase();
  if (!sb) return null;

  const { data, error } = await sb.from('user_profiles').select('*').eq('id', user.id).single();

  if (error) {
    // PGRST116: 查询返回 0 行，说明 profile 尚未创建，自动创建一个
    if (error.code === 'PGRST116') {
      console.log('User profile not found, auto-creating...');
      const phone = user.phone || '';
      const { data: newProfile, error: insertError } = await sb
        .from('user_profiles')
        .upsert({ id: user.id, phone, points_balance: 1, role: 'user' })
        .select()
        .single();
      if (insertError) {
        console.error('Error auto-creating user profile:', insertError);
        return null;
      }
      return newProfile;
    }
    console.error('Error fetching user profile:', error);
    return null;
  }
  return data;
}

export function checkAuthState(callback) {
  const sb = getSupabase();
  if (!sb) return;

  sb.auth.onAuthStateChange((event, session) => {
    if (callback) callback(session);
  });
}

export async function checkAuthAndRedirect(redirectTo = '/login.html') {
  const user = await getCurrentUser();
  if (!user) {
    window.location.href = redirectTo;
    return false;
  }
  return true;
}

export async function isAdmin() {
  const profile = await getUserProfile();
  return profile && profile.role === 'admin';
}

export function showToast(message, type = 'success') {
  const container = document.querySelector('.toast-container') || createToastContainer();

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  container.appendChild(toast);

  setTimeout(() => toast.remove(), 3000);
}

function createToastContainer() {
  const container = document.createElement('div');
  container.className = 'toast-container';
  document.body.appendChild(container);
  return container;
}

// 向后兼容：挂载到全局 window
if (typeof window !== 'undefined') {
  window.auth = {
    initSupabase: () => (window.supabaseClient ? window.supabaseClient.init() : null),
    getSupabase: () => (window.supabaseClient ? window.supabaseClient.get() : null),
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
    showToast,
  };
}
