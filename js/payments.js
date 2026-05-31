// ============================================================
// 专业星图 - 支付模块（ES Module）
// ============================================================

import { SUPABASE_URL } from './supabase-client.js';

export async function getPointPackages() {
  const sb = window.auth ? window.auth.getSupabase() : null;
  if (!sb) throw new Error('Supabase not initialized');

  const { data, error } = await sb
    .from('point_packages')
    .select('*')
    .eq('is_active', true)
    .order('price', { ascending: true });

  if (error) throw error;
  return data;
}

export async function createOrder(packageId) {
  const sb = window.auth ? window.auth.getSupabase() : null;
  if (!sb) throw new Error('Supabase not initialized');

  const user = await window.auth.getCurrentUser();
  if (!user) throw new Error('User not logged in');

  const { data: pkg } = await sb.from('point_packages').select('*').eq('id', packageId).single();
  if (!pkg) throw new Error('Package not found');

  const { data: order, error } = await sb
    .from('orders')
    .insert({ user_id: user.id, package_id: packageId, points: pkg.points, amount: pkg.price, status: 'pending' })
    .select()
    .single();

  if (error) throw error;
  return order;
}

export async function createAlipayOrder(packageId) {
  const sb = window.auth ? window.auth.getSupabase() : null;
  if (!sb) throw new Error('Supabase not initialized');

  const { data: { session } } = await sb.auth.getSession();
  if (!session) throw new Error('请先登录');

  const response = await fetch(`${SUPABASE_URL}/functions/v1/create-alipay-order`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${session.access_token}`,
    },
    body: JSON.stringify({ package_id: packageId }),
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.error || `请求失败 (${response.status})`);
  }

  return response.json();
}

export async function queryOrderStatus(orderId) {
  const sb = window.auth ? window.auth.getSupabase() : null;
  if (!sb) throw new Error('Supabase not initialized');

  const { data, error } = await sb
    .from('orders')
    .select('status, points')
    .eq('id', orderId)
    .single();

  if (error) throw error;
  return data;
}

export async function getOrders() {
  const sb = window.auth ? window.auth.getSupabase() : null;
  if (!sb) throw new Error('Supabase not initialized');

  const user = await window.auth.getCurrentUser();
  if (!user) throw new Error('User not logged in');

  const { data, error } = await sb
    .from('orders')
    .select('*, point_packages(*)')
    .eq('user_id', user.id)
    .order('created_at', { ascending: false });

  if (error) throw error;
  return data;
}

export async function getDownloadRecords() {
  const sb = window.auth ? window.auth.getSupabase() : null;
  if (!sb) throw new Error('Supabase not initialized');

  const user = await window.auth.getCurrentUser();
  if (!user) throw new Error('User not logged in');

  const { data, error } = await sb
    .from('download_records')
    .select('*, reports(*)')
    .eq('user_id', user.id)
    .order('created_at', { ascending: false });

  if (error) throw error;
  return data;
}

// 向后兼容
if (typeof window !== 'undefined') {
  window.payments = { getPointPackages, createOrder, createAlipayOrder, queryOrderStatus, getOrders, getDownloadRecords };
}
