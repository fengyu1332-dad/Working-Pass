// ============================================================
// 专业星图 - 报告模块（ES Module）
// 报告解锁后在线阅读，不提供下载
// ============================================================

import { getSupabase } from './supabase-client.js';
import { getCurrentUser } from './auth.js';

function requireSB() {
  const sb = getSupabase();
  if (!sb) throw new Error('Supabase not initialized');
  return sb;
}

const REPORT_COLUMNS = 'id, major_code, major_name, category, preview_content, full_content, download_count, status';

export async function getReports(category = null, search = null) {
  const sb = requireSB();

  let query = sb
    .from('reports')
    .select(REPORT_COLUMNS)
    .eq('status', 'published');

  if (category) query = query.eq('category', category);
  if (search) query = query.or(`major_name.ilike.%${search}%,major_code.ilike.%${search}%,category.ilike.%${search}%`);

  const { data, error } = await query.order('major_name');
  if (error) throw error;
  return data;
}

export async function getTopReports(limit = 6) {
  const sb = requireSB();
  const { data, error } = await sb
    .from('reports')
    .select(REPORT_COLUMNS)
    .eq('status', 'published')
    .order('download_count', { ascending: false })
    .limit(limit);
  if (error) throw error;
  return data;
}

export async function getReportByMajorCode(majorCode) {
  const sb = requireSB();

  const { data, error } = await sb
    .from('reports')
    .select(REPORT_COLUMNS)
    .eq('major_code', majorCode)
    .eq('status', 'published')
    .maybeSingle();

  if (error) throw error;
  return data;
}

export async function getReport(reportId) {
  const sb = requireSB();

  const { data, error } = await sb.from('reports').select(REPORT_COLUMNS).eq('id', reportId).single();
  if (error) throw error;
  return data;
}

export async function unlockReport(reportId) {
  const sb = requireSB();

  const user = await getCurrentUser();
  if (!user) throw new Error('User not logged in');

  // 先检查是否已解锁（避免 RPC 调用报错）
  const alreadyUnlocked = await checkUnlocked(reportId);
  if (alreadyUnlocked) {
    const { data: report } = await sb.from('reports').select(REPORT_COLUMNS).eq('id', reportId).single();
    return { content: report?.full_content || '', alreadyUnlocked: true };
  }

  // 调用数据库原子化积分消费函数
  const { data: result, error } = await sb.rpc('spend_points', { p_report_id: reportId });

  if (error) throw new Error(error.message || '解锁失败');
  if (!result.success) throw new Error(result.error || '解锁失败');

  const { data: report } = await sb.from('reports').select(REPORT_COLUMNS).eq('id', reportId).single();

  return { content: report?.full_content || '', alreadyUnlocked: false };
}

export async function getUnlockedReportIds() {
  const sb = window.auth ? window.auth.getSupabase() : null;
  if (!sb) return [];

  const user = await getCurrentUser();
  if (!user) return [];

  const { data, error } = await sb
    .from('download_records')
    .select('report_id')
    .eq('user_id', user.id);

  if (error) return [];
  return (data || []).map((r) => r.report_id);
}

export async function checkUnlocked(reportId) {
  const sb = window.auth ? window.auth.getSupabase() : null;
  if (!sb) return false;

  const user = await getCurrentUser();
  if (!user) return false;

  const { data } = await sb
    .from('download_records')
    .select('id')
    .eq('user_id', user.id)
    .eq('report_id', reportId)
    .maybeSingle();

  return !!data;
}

// 向后兼容
if (typeof window !== 'undefined') {
  window.reports = {
    getReports,
    getReport,
    getReportByMajorCode,
    getUnlockedReportIds,
    unlockReport,
    downloadReport: unlockReport,
    checkUnlocked,
    checkDownloaded: checkUnlocked,
  };
}
