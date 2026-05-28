// ============================================================
// 专业星图 - 报告模块（ES Module）
// 报告解锁后在线阅读，不提供下载
// ============================================================

const REPORT_COLUMNS = 'id, major_code, major_name, category, preview_content, full_content, download_count, status';

export async function getReports(category = null, search = null) {
  const sb = window.auth ? window.auth.getSupabase() : null;
  if (!sb) throw new Error('Supabase not initialized');

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

export async function getReport(reportId) {
  const sb = window.auth ? window.auth.getSupabase() : null;
  if (!sb) throw new Error('Supabase not initialized');

  const { data, error } = await sb.from('reports').select(REPORT_COLUMNS).eq('id', reportId).single();
  if (error) throw error;
  return data;
}

export async function unlockReport(reportId) {
  const sb = window.auth ? window.auth.getSupabase() : null;
  if (!sb) throw new Error('Supabase not initialized');

  const user = await window.auth.getCurrentUser();
  if (!user) throw new Error('User not logged in');

  const profile = await window.auth.getUserProfile();
  if (!profile || profile.points_balance < 1) {
    throw new Error('点数不足，请先充值');
  }

  const { data: report } = await sb.from('reports').select(REPORT_COLUMNS).eq('id', reportId).single();
  if (!report) throw new Error('Report not found');

  const { data: existingRecord } = await sb
    .from('download_records')
    .select('id')
    .eq('user_id', user.id)
    .eq('report_id', reportId)
    .maybeSingle();

  if (existingRecord) {
    return {
      content: report.full_content || '',
      alreadyUnlocked: true,
    };
  }

  await sb.from('user_profiles').update({ points_balance: profile.points_balance - 1 }).eq('id', user.id);
  await sb.from('download_records').insert({ user_id: user.id, report_id: reportId, points_spent: 1 });
  await sb
    .from('reports')
    .update({ download_count: (report.download_count || 0) + 1 })
    .eq('id', reportId);

  return { content: report.full_content || '', alreadyUnlocked: false };
}

export async function getUnlockedReportIds() {
  const sb = window.auth ? window.auth.getSupabase() : null;
  if (!sb) return [];

  const user = await window.auth.getCurrentUser();
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

  const user = await window.auth.getCurrentUser();
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
    getUnlockedReportIds,
    unlockReport,
    downloadReport: unlockReport,
    checkUnlocked,
    checkDownloaded: checkUnlocked,
  };
}
