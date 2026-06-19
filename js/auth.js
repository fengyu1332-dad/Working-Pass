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

export async function registerWithEmail(email, password, phone, referrerId = null) {
  const sb = getSupabase();
  if (!sb) throw new Error('Supabase not initialized');

  const { data, error } = await sb.auth.signUp({
    email,
    password,
    options: { data: { phone, referred_by: referrerId } },
  });
  if (error) throw error;

  if (data.user) {
    await createUserProfile(data.user.id, phone, referrerId);
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

async function createUserProfile(userId, phone, referrerId = null) {
  const sb = getSupabase();
  if (!sb) throw new Error('Supabase not initialized');

  const { data, error } = await sb
    .from('user_profiles')
    .upsert({ id: userId, phone, points_balance: 10, role: 'user', referred_by: referrerId || null })
    .select()
    .single();

  if (error) {
    console.error('Error creating user profile:', error);
  }

  // 如果存在推荐人，奖励推荐人 3 点
  if (referrerId && referrerId !== userId) {
    await awardReferralPoints(referrerId, userId);
  }

  return data;
}

// 推荐奖励：推荐人获得 3 点
async function awardReferralPoints(referrerId, newUserId) {
  const sb = getSupabase();
  if (!sb) return;

  try {
    // 1. 检查新用户是否已被其他人推荐过（防止重复奖励）
    const { data: newUserProfile } = await sb
      .from('user_profiles')
      .select('referred_by')
      .eq('id', newUserId)
      .maybeSingle();

    if (!newUserProfile || newUserProfile.referred_by !== referrerId) return;

    // 2. 检查推荐人是否已为此用户获得过奖励（防止重放）
    const { data: existing } = await sb
      .from('referral_rewards')
      .select('id')
      .eq('referrer_id', referrerId)
      .eq('referred_user_id', newUserId)
      .maybeSingle();
    if (existing) return;

    // 3. 原子化奖励：插入奖励记录 + 更新推荐人点数
    const { error: insertError } = await sb
      .from('referral_rewards')
      .insert({ referrer_id: referrerId, referred_user_id: newUserId, points_awarded: 3 });

    if (insertError) {
      console.error('Insert referral reward error:', insertError);
      return;
    }

    // 4. 更新推荐人点数
    const { error: updateError } = await sb.rpc('add_points', { p_user_id: referrerId, p_points: 3 });
    if (updateError) {
      console.error('Add points error:', updateError);
    }
  } catch (e) {
    console.error('Award referral points error:', e);
  }
}

export async function logout() {
  const sb = getSupabase();
  if (!sb) throw new Error('Supabase not initialized');

  const { error } = await sb.auth.signOut();
  if (error) throw error;

  clearUserCache();
  window.location.href = '/login.html';
}

let _cachedUser = null;
let _cachedUserAt = 0;
const USER_CACHE_TTL = 30000; // 30秒缓存，避免同一流程中重复 auth API 调用

export async function getCurrentUser() {
  if (_cachedUser && Date.now() - _cachedUserAt < USER_CACHE_TTL) {
    return _cachedUser;
  }

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
    _cachedUser = user;
    _cachedUserAt = Date.now();
    return user;
  } catch (error) {
    return null;
  }
}

// 供外部强制刷新缓存（如登录/登出后）
export function clearUserCache() {
  _cachedUser = null;
  _cachedUserAt = 0;
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
        .upsert({ id: user.id, phone, points_balance: 10, role: 'user' })
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
  toast.setAttribute('role', 'status');
  toast.textContent = message;
  container.appendChild(toast);

  setTimeout(() => toast.remove(), 3000);
}

function createToastContainer() {
  const container = document.createElement('div');
  container.className = 'toast-container';
  container.setAttribute('aria-live', 'polite');
  container.setAttribute('aria-atomic', 'false');
  document.body.appendChild(container);
  return container;
}

// --- 社交登录 ---

export async function signInWithGoogle() {
  const sb = getSupabase();
  if (!sb) throw new Error('Supabase not initialized');

  const { data, error } = await sb.auth.signInWithOAuth({
    provider: 'google',
    options: {
      redirectTo: window.location.origin + '/user/dashboard.html',
      queryParams: { access_type: 'offline', prompt: 'consent' },
    },
  });
  if (error) throw error;
  return data;
}

// --- 密码重置 ---

export async function sendPasswordResetEmail(email) {
  const sb = getSupabase();
  if (!sb) throw new Error('Supabase not initialized');

  const { data, error } = await sb.auth.resetPasswordForEmail(email, {
    redirectTo: window.location.origin + '/update-password.html',
  });
  if (error) throw error;
  return data;
}

export async function updatePassword(newPassword) {
  const sb = getSupabase();
  if (!sb) throw new Error('Supabase not initialized');

  const { data, error } = await sb.auth.updateUser({ password: newPassword });
  if (error) throw error;
  return data;
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
    clearUserCache,
    getUserProfile,
    checkAuthState,
    checkAuthAndRedirect,
    isAdmin,
    showToast,
    sendPasswordResetEmail,
    updatePassword,
    signInWithGoogle,
  };
}
