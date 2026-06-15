// ============================================================
// 专业星图 - 个人中心页
// ============================================================

import '../supabase-client.js';
import '../auth.js';
import '../payments.js';
import '../error-report.js';
import { t } from '../i18n.js';

(async function () {
  window.auth.initSupabase();

  const isLoggedIn = await window.auth.checkAuthAndRedirect();
  if (!isLoggedIn) return;

  const profile = await window.auth.getUserProfile();
  if (profile) {
    const displayEmail = profile.email || t('unknown_user', '未知用户');
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
    await loadFavoritesPreview();
    await loadAssessmentPreview();
    await loadRecentOrders();
    await loadRecentDownloads();
  }

  document.getElementById('logoutBtn').addEventListener('click', async (e) => {
    e.preventDefault();
    try { await window.auth.logout(); } catch (error) { window.auth.showToast(t('logout_fail', '退出失败'), 'error'); }
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

async function loadFavoritesPreview() {
  const container = document.getElementById('favoritesPreview');
  if (!container) return;
  try {
    const user = await window.auth.getCurrentUser();
    if (!user) return;
    const { url, key } = window.supabaseClient;
    const res = await fetch(
      `${url}/rest/v1/user_favorites?select=major_code&user_id=eq.${user.id}&order=created_at.desc&limit=6`,
      { headers: { apikey: key, Authorization: `Bearer ${key}` } },
    );
    if (!res.ok) return;
    const rows = await res.json();
    if (!rows.length) {
      container.innerHTML = `
        <div style="text-align:center;padding:24px;">
          <p style="color:var(--on-surface-variant);margin-bottom:12px;" data-i18n="fav_empty">还没有收藏任何专业</p>
          <a href="/majors.html" style="color:var(--primary);font-weight:600;text-decoration:none;" data-i18n="fav_browse">去浏览专业 →</a>
        </div>`;
      return;
    }
    const codes = rows.map(r => `"${r.major_code}"`).join(',');
    const majorsRes = await fetch(
      `${url}/rest/v1/majors?select=code,name,category,category_icon,salary_range,difficulty&code=in.(${codes})`,
      { headers: { apikey: key, Authorization: `Bearer ${key}` } },
    );
    if (!majorsRes.ok) return;
    const majorsData = await majorsRes.json();
    const majorMap = new Map(majorsData.map(m => [m.code, m]));

    const favs = rows.map(r => ({ code: r.major_code, major: majorMap.get(r.major_code) })).filter(f => f.major);

    container.innerHTML = `
      <div style="display:grid;grid-template-columns:repeat(auto-fill, minmax(200px, 1fr));gap:10px;padding:8px;">
        ${favs.map(f => {
          const m = f.major;
          return `<div class="fav-preview-card" data-code="${m.code}" style="background:var(--surface);border-radius:10px;padding:12px;cursor:pointer;transition:all 0.2s;border:1px solid var(--outline);" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--outline)'">
            <div style="font-weight:600;color:var(--secondary);font-size:13px;margin-bottom:2px;">${m.name}</div>
            <div style="font-size:11px;color:var(--on-surface-variant);">${m.category || ''}</div>
            <div style="margin-top:4px;font-size:11px;color:var(--primary);">${m.salary_range || ''}</div>
          </div>`;
        }).join('')}
      </div>
      <div style="text-align:center;margin-top:8px;">
        <a href="/user/favorites.html" style="color:var(--primary);font-weight:600;text-decoration:none;font-size:14px;" data-i18n="fav_view_all">查看全部收藏 →</a>
      </div>`;
    container.querySelectorAll('.fav-preview-card').forEach(card => {
      card.addEventListener('click', () => {
        const fav = favs.find(f => f.code === card.dataset.code);
        if (fav && fav.major && window.openModal) window.openModal(fav.major);
      });
    });
  } catch (e) { console.error('Load favorites preview error:', e); }
}

async function loadAssessmentPreview() {
  const container = document.getElementById('assessmentPreview');
  if (!container) return;
  try {
    const sb = window.auth.getSupabase();
    if (!sb) return;
    const user = await window.auth.getCurrentUser();
    if (!user) return;
    const { data, error } = await sb.from('assessment_results')
      .select('results,created_at')
      .eq('user_id', user.id)
      .maybeSingle();
    if (error || !data || !data.results || !data.results.length) {
      container.innerHTML = `
        <div style="text-align:center;padding:24px;">
          <p style="color:var(--on-surface-variant);margin-bottom:12px;" data-i18n="dash_no_assessment">还没有做过专业适配测评</p>
          <a href="/assessment.html" style="color:var(--primary);font-weight:600;text-decoration:none;" data-i18n="dash_go_assessment">去测评 →</a>
        </div>`;
      return;
    }
    const top3 = data.results.slice(0, 3);
    const dateStr = data.created_at ? new Date(data.created_at).toLocaleDateString('zh-CN') : '--';
    container.innerHTML = `
      <div style="padding:8px;">
        <div style="font-size:13px;color:var(--on-surface-variant);margin-bottom:10px;">📅 ${t('dash_assessment_date')}: ${dateStr}</div>
        <div style="display:flex;flex-direction:column;gap:6px;margin-bottom:12px;">
          ${top3.map((r, i) => `
            <div style="display:flex;align-items:center;gap:8px;padding:6px 10px;background:var(--surface);border-radius:8px;">
              <span style="font-weight:700;color:${i === 0 ? 'var(--primary)' : 'var(--secondary)'};font-size:14px;">#${r.rank}</span>
              <span style="flex:1;font-size:13px;color:var(--on-surface);">${r.name}</span>
              <span style="font-weight:700;color:var(--primary);font-size:13px;">${r.percentage}%</span>
            </div>
          `).join('')}
        </div>
        <div style="display:flex;gap:8px;justify-content:center;">
          <a href="/assessment.html" style="padding:8px 16px;border-radius:10px;background:var(--primary);color:#fff;text-decoration:none;font-size:13px;font-weight:600;" data-i18n="dash_view_result">查看完整结果</a>
          <a href="/assessment.html" style="padding:8px 16px;border-radius:10px;border:1.5px solid var(--outline);color:var(--on-surface-variant);text-decoration:none;font-size:13px;font-weight:600;" data-i18n="dash_retake">重新测评</a>
        </div>
      </div>`;
  } catch (e) { console.error('Load assessment preview error:', e); }
}

async function loadRecentOrders() {
  const container = document.getElementById('recentOrders');
  try {
    const orders = await window.payments.getOrders();
    if (!orders || orders.length === 0) {
      container.innerHTML = `<p style="color:var(--on-surface-variant);text-align:center;padding:24px;">${t('no_orders', '暂无订单')}</p>`;
      return;
    }
    const recent = orders.slice(0, 3);
    container.innerHTML = recent.map((o) => `
      <div style="display:flex;justify-content:space-between;align-items:center;padding:14px 0;border-bottom:1px solid var(--outline);">
        <div>
          <div style="font-weight:600;color:var(--secondary);">${o.point_packages?.name || t('points_recharge', '点数充值')}</div>
          <div style="font-size:13px;color:var(--on-surface-variant);">${formatDate(o.created_at)}</div>
        </div>
        <div style="font-weight:700;color:var(--success);">+${o.points} 点</div>
      </div>
    `).join('');
  } catch (error) {
    console.error('Load recent orders error:', error);
    container.innerHTML = `<p style="color:var(--on-surface-variant);text-align:center;padding:24px;">${t('load_failed', '加载失败')}</p>`;
  }
}

async function loadRecentDownloads() {
  const container = document.getElementById('recentDownloads');
  try {
    const downloads = await window.payments.getDownloadRecords();
    if (!downloads || downloads.length === 0) {
      container.innerHTML = `<p style="color:var(--on-surface-variant);text-align:center;padding:24px;">${t('no_unlocked', '暂无已解锁报告')}</p>`;
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
          <a href="/user/reports.html?code=${d.reports?.major_code || ''}" style="font-weight:600;color:var(--secondary);text-decoration:none;" onmouseover="this.style.color='var(--primary)'" onmouseout="this.style.color='var(--secondary)'">${d.reports?.major_name || t('major_report', '专业报告')}</a>
          <div style="font-size:13px;color:var(--on-surface-variant);">${d.reports?.major_code || ''} · ${formatDate(d.created_at)}</div>
        </div>
        <span style="display:inline-flex;align-items:center;gap:4px;background:#E8F5E9;color:#2E7D32;padding:4px 12px;border-radius:20px;font-size:13px;white-space:nowrap;">✓ ${t('report_unlocked', '已解锁')}</span>
      </div>
    `).join('');
  } catch (error) {
    console.error('Load recent downloads error:', error);
    container.innerHTML = `<p style="color:var(--on-surface-variant);text-align:center;padding:24px;">${t('load_failed', '加载失败')}</p>`;
  }
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleString('zh-CN', {
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit',
  });
}
