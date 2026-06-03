// ============================================================
// 专业星图 - 个人中心页
// ============================================================

import '../supabase-client.js';
import '../auth.js';
import '../payments.js';
import '../error-report.js';

(async function () {
  window.auth.initSupabase();

  const isLoggedIn = await window.auth.checkAuthAndRedirect();
  if (!isLoggedIn) return;

  const profile = await window.auth.getUserProfile();
  if (profile) {
    const displayEmail = profile.email || '未知用户';
    document.getElementById('pointsBalance').textContent = profile.points_balance || 0;
    document.getElementById('userPhone').textContent = profile.phone || '';
    document.getElementById('userName').textContent = displayEmail;
    document.getElementById('userAvatar').textContent = displayEmail[0].toUpperCase();

    // admin 入口
    if (profile.role === 'admin') {
      const adminEntry = document.getElementById('adminEntry');
      if (adminEntry) adminEntry.style.display = '';
    }

    await loadUserStats(profile.id);
    await loadRecentOrders();
    await loadRecentDownloads();
  }

  document.getElementById('logoutBtn').addEventListener('click', async (e) => {
    e.preventDefault();
    try { await window.auth.logout(); } catch (error) { window.auth.showToast('退出失败', 'error'); }
  });
})();

async function loadUserStats(userId) {
  const sb = window.auth.getSupabase();
  if (!sb) return;

  try {
    const { data: orders, error: ordersErr } = await sb
      .from('orders')
      .select('id', { count: 'exact' })
      .eq('user_id', userId)
      .eq('status', 'paid');
    if (!ordersErr) {
      document.getElementById('totalOrders').textContent = orders ? orders.length : 0;
    }

    const { data: downloads, error: dlErr } = await sb
      .from('download_records')
      .select('report_id', { count: 'exact' })
      .eq('user_id', userId);
    if (!dlErr && downloads) {
      const uniqueReports = new Set(downloads.map((d) => d.report_id));
      document.getElementById('totalDownloads').textContent = uniqueReports.size;
    }
  } catch (error) {
    console.error('Load stats error:', error);
  }
}

async function loadRecentOrders() {
  const container = document.getElementById('recentOrders');
  try {
    const orders = await window.payments.getOrders();
    if (!orders || orders.length === 0) {
      container.innerHTML = '<p style="color:var(--on-surface-variant);text-align:center;padding:24px;">暂无订单</p>';
      return;
    }
    const recent = orders.slice(0, 3);
    container.innerHTML = recent.map((o) => `
      <div style="display:flex;justify-content:space-between;align-items:center;padding:14px 0;border-bottom:1px solid var(--outline);">
        <div>
          <div style="font-weight:600;color:var(--secondary);">${o.point_packages?.name || '点数充值'}</div>
          <div style="font-size:13px;color:var(--on-surface-variant);">${formatDate(o.created_at)}</div>
        </div>
        <div style="font-weight:700;color:var(--success);">+${o.points} 点</div>
      </div>
    `).join('');
  } catch (error) {
    console.error('Load recent orders error:', error);
    container.innerHTML = '<p style="color:var(--on-surface-variant);text-align:center;padding:24px;">加载失败</p>';
  }
}

async function loadRecentDownloads() {
  const container = document.getElementById('recentDownloads');
  try {
    const downloads = await window.payments.getDownloadRecords();
    if (!downloads || downloads.length === 0) {
      container.innerHTML = '<p style="color:var(--on-surface-variant);text-align:center;padding:24px;">暂无已购报告</p>';
      return;
    }
    const unique = [];
    const seen = new Set();
    for (const d of downloads) {
      const rid = d.report_id;
      if (!seen.has(rid)) {
        seen.add(rid);
        unique.push(d);
      }
    }
    container.innerHTML = unique.map((d) => `
      <div style="display:flex;justify-content:space-between;align-items:center;padding:14px 0;border-bottom:1px solid var(--outline);">
        <div>
          <a href="/user/reports.html?code=${d.reports?.major_code || ''}" style="font-weight:600;color:var(--secondary);text-decoration:none;" onmouseover="this.style.color='var(--primary)'" onmouseout="this.style.color='var(--secondary)'">${d.reports?.major_name || '专业报告'}</a>
          <div style="font-size:13px;color:var(--on-surface-variant);">${d.reports?.major_code || ''} · ${formatDate(d.created_at)}</div>
        </div>
        <span style="display:inline-flex;align-items:center;gap:4px;background:#E8F5E9;color:#2E7D32;padding:4px 12px;border-radius:20px;font-size:13px;white-space:nowrap;">✓ 已解锁</span>
      </div>
    `).join('');
  } catch (error) {
    console.error('Load recent downloads error:', error);
    container.innerHTML = '<p style="color:var(--on-surface-variant);text-align:center;padding:24px;">加载失败</p>';
  }
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleString('zh-CN', {
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit',
  });
}
