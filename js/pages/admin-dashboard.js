// ============================================================
// 专业星图 - 管理后台：数据概览
// ============================================================

import { requireAdmin, renderAdminSidebar, adminApi } from './admin-common.js';

async function init() {
  const profile = await requireAdmin();
  if (!profile) return;
  renderAdminSidebar('dashboard');

  await Promise.all([loadStats(), loadTopReports(), loadTodayStats(), loadRevenueChart()]);
}

async function loadStats() {
  const [usersCount, majorsCount, reportsCount, ordersCount, downloadsCount, ordersData] = await Promise.all([
    adminApi.count('user_profiles'),
    adminApi.count('majors'),
    adminApi.count('reports'),
    adminApi.count('orders', { eq: { col: 'status', val: 'paid' } }),
    adminApi.count('download_records'),
    adminApi.get('orders', { select: 'amount', eq: { col: 'status', val: 'paid' } }),
  ]);

  setStat('totalUsers', usersCount);
  setStat('totalMajors', majorsCount);
  setStat('totalReports', reportsCount);
  setStat('totalOrders', ordersCount);
  setStat('totalDownloads', downloadsCount);

  const revenue = (ordersData || []).reduce((sum, o) => sum + (o.amount || 0), 0);
  setStat('totalRevenue', revenue.toFixed(2));
}

function setStat(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}

async function loadTopReports() {
  let data = await adminApi.get('reports', {
    select: 'major_code,major_name,download_count',
  });
  data.sort((a, b) => (b.download_count || 0) - (a.download_count || 0));
  data = data.slice(0, 10);

  const tbody = document.getElementById('topReportsBody');
  if (!data || !data.length) {
    tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:48px;color:var(--on-surface-variant);">暂无数据</td></tr>';
    return;
  }

  const maxDownloads = Math.max(data[0].download_count, 1);

  tbody.innerHTML = data
    .map(
      (r, i) => `
    <tr>
      <td>${i + 1}</td>
      <td>${r.major_code}</td>
      <td>${r.major_name}</td>
      <td>${r.download_count}</td>
      <td>
        <div class="progress-bar">
          <div class="progress-bar-fill" style="width:${((r.download_count / maxDownloads) * 100).toFixed(1)}%"></div>
        </div>
      </td>
    </tr>`
    )
    .join('');
}

async function loadTodayStats() {
  const today = new Date().toISOString().slice(0, 10);
  const tomorrow = new Date(Date.now() + 86400000).toISOString().slice(0, 10);
  const dateFilters = [
    { col: 'created_at', op: 'gte', val: today },
    { col: 'created_at', op: 'lt', val: tomorrow },
  ];

  const [downloadsCount, ordersData] = await Promise.all([
    adminApi.count('download_records', { filters: dateFilters }),
    adminApi.get('orders', {
      select: 'amount',
      eq: { col: 'status', val: 'paid' },
      filters: dateFilters,
    }),
  ]);

  setStat('todayDownloads', downloadsCount);

  const todayRevenue = (ordersData || []).reduce((sum, o) => sum + (o.amount || 0), 0);
  setStat('todayRevenue', todayRevenue.toFixed(2));
}

async function loadRevenueChart() {
  const days = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date(Date.now() - i * 86400000);
    days.push(d.toISOString().slice(0, 10));
  }

  const start = days[0];
  const end = new Date(Date.now() + 86400000).toISOString().slice(0, 10);

  const data = await adminApi.get('orders', {
    select: 'amount,created_at',
    eq: { col: 'status', val: 'paid' },
    filters: [
      { col: 'created_at', op: 'gte', val: start },
      { col: 'created_at', op: 'lt', val: end },
    ],
  });

  const dailyRevenue = days.map((day) => {
    const dayOrders = (data || []).filter((o) => o.created_at && o.created_at.startsWith(day));
    return dayOrders.reduce((sum, o) => sum + (o.amount || 0), 0);
  });

  const maxRev = Math.max(...dailyRevenue, 1);

  const container = document.getElementById('revenueBarChart');
  if (!container) return;

  container.innerHTML = dailyRevenue
    .map(
      (rev, i) => `
    <div class="bar-chart-item">
      <div class="bar-chart-value">¥${rev.toFixed(0)}</div>
      <div class="bar-chart-bar" style="height:${Math.max((rev / maxRev) * 130, 4)}px;"></div>
      <div class="bar-chart-label">${days[i].slice(5)}</div>
    </div>`
    )
    .join('');
}

init();
