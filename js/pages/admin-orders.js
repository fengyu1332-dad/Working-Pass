// ============================================================
// 专业星图 - 管理后台：订单管理
// ============================================================

import '../supabase-client.js';
import '../auth.js';
import { requireAdmin, renderAdminSidebar, formatDate, showConfirmDialog } from './admin-common.js';

let currentFilter = 'all';
let currentPage = 0;
const PAGE_SIZE = 30;

const STATUS_MAP = {
  paid: '已支付',
  pending: '待支付',
  expired: '已过期',
  cancelled: '已取消',
};
const STATUS_CLASS = {
  paid: 'status-paid',
  pending: 'status-pending',
  expired: 'status-expired',
  cancelled: 'status-cancelled',
};

(async function () {
  const profile = await requireAdmin();
  if (!profile) return;

  renderAdminSidebar('orders');
  initFilters();
  await loadStats();
  await loadOrders();
})();

function initFilters() {
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentFilter = btn.dataset.filter;
      currentPage = 0;
      document.getElementById('ordersTableBody').innerHTML = '';
      loadOrders();
    });
  });

  document.getElementById('loadMoreBtn').addEventListener('click', () => {
    loadOrders();
  });
}

async function loadStats() {
  const { url, key } = window.supabaseClient;
  const sb = window.auth.getSupabase();
  const { data: { session } } = await sb.auth.getSession();
  const headers = {
    apikey: key,
    Authorization: `Bearer ${session.access_token}`,
  };

  try {
    // 总订单数
    const countRes = await fetch(`${url}/rest/v1/orders?select=count`, { headers: { ...headers, Prefer: 'count=exact' } });
    const countRange = countRes.headers.get('content-range');
    const totalOrders = countRange ? parseInt(countRange.split('/')[1]) : 0;
    document.getElementById('statTotalOrders').textContent = totalOrders;

    // 已支付订单数
    const paidRes = await fetch(`${url}/rest/v1/orders?select=count&status=eq.paid`, { headers: { ...headers, Prefer: 'count=exact' } });
    const paidRange = paidRes.headers.get('content-range');
    const paidOrders = paidRange ? parseInt(paidRange.split('/')[1]) : 0;
    document.getElementById('statPaidOrders').textContent = paidOrders;

    // 总营收
    const paidList = await fetch(`${url}/rest/v1/orders?select=amount&status=eq.paid&limit=10000`, { headers });
    const paidData = await paidList.json();
    const totalRevenue = paidData.reduce((sum, o) => sum + (parseFloat(o.amount) || 0), 0);
    document.getElementById('statTotalRevenue').textContent = `¥${totalRevenue.toFixed(2)}`;

    // 今日营收
    const today = new Date().toISOString().slice(0, 10);
    const todayRes = await fetch(`${url}/rest/v1/orders?select=amount&status=eq.paid&paid_at=gte.${today}T00:00:00`, { headers });
    const todayData = await todayRes.json();
    const todayRevenue = todayData.reduce((sum, o) => sum + (parseFloat(o.amount) || 0), 0);
    document.getElementById('statTodayRevenue').textContent = `¥${todayRevenue.toFixed(2)}`;
  } catch (error) {
    console.error('Load stats error:', error);
  }
}

async function loadOrders() {
  const { url, key } = window.supabaseClient;
  const sb = window.auth.getSupabase();
  const { data: { session } } = await sb.auth.getSession();
  const headers = {
    apikey: key,
    Authorization: `Bearer ${session.access_token}`,
  };

  try {
    // 构建查询
    let queryUrl = `${url}/rest/v1/orders?select=*,user_profiles!inner(email,phone),point_packages(name)&order=created_at.desc&limit=${PAGE_SIZE}&offset=${currentPage * PAGE_SIZE}`;
    if (currentFilter !== 'all') {
      queryUrl += `&status=eq.${currentFilter}`;
    }

    const res = await fetch(queryUrl, { headers });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const orders = await res.json();
    const tbody = document.getElementById('ordersTableBody');

    if (orders.length === 0 && currentPage === 0) {
      tbody.innerHTML = `<tr><td colspan="11" style="text-align:center;padding:48px;color:var(--on-surface-variant);">暂无订单数据</td></tr>`;
      document.getElementById('loadMoreBtn').style.display = 'none';
      return;
    }

    const rows = orders.map(order => {
      const userEmail = order.user_profiles?.email || '--';
      const userPhone = order.user_profiles?.phone || '';
      const userName = userEmail !== '--' ? userEmail : (userPhone || '--');
      const packageName = order.point_packages?.name || '--';

      return `
        <tr>
          <td title="${order.id}">${order.id.slice(0, 8)}...</td>
          <td>${escapeHtml(userName)}</td>
          <td>${escapeHtml(packageName)}</td>
          <td>¥${parseFloat(order.amount).toFixed(2)}</td>
          <td>${order.points}</td>
          <td><span class="status-badge ${STATUS_CLASS[order.status] || ''}">${STATUS_MAP[order.status] || order.status}</span></td>
          <td>${order.payment_method || '--'}</td>
          <td><span class="trade-no-mono">${order.alipay_trade_no ? order.alipay_trade_no.slice(-12) : '--'}</span></td>
          <td>${formatDate(order.created_at)}</td>
          <td>${order.paid_at ? formatDate(order.paid_at) : '--'}</td>
          <td>
            ${order.status === 'pending'
              ? `<button class="btn btn-outline" style="padding:4px 12px;font-size:12px;" onclick="window.cancelOrder('${order.id}')">取消</button>`
              : '--'}
          </td>
        </tr>`;
    }).join('');

    if (currentPage === 0) {
      tbody.innerHTML = rows;
    } else {
      tbody.innerHTML += rows;
    }

    const loadMoreBtn = document.getElementById('loadMoreBtn');
    if (orders.length === PAGE_SIZE) {
      loadMoreBtn.style.display = 'inline-flex';
      currentPage++;
    } else {
      loadMoreBtn.style.display = 'none';
    }
  } catch (error) {
    console.error('Load orders error:', error);
    document.getElementById('ordersTableBody').innerHTML =
      `<tr><td colspan="11" style="text-align:center;padding:48px;color:var(--error);">加载失败: ${error.message}</td></tr>`;
  }
}

// 全局取消订单函数
window.cancelOrder = async function (orderId) {
  const confirmed = await showConfirmDialog('确认取消此订单？此操作不可撤销。');
  if (!confirmed) return;

  const { url, key } = window.supabaseClient;
  const sb = window.auth.getSupabase();
  const { data: { session } } = await sb.auth.getSession();
  const headers = {
    apikey: key,
    Authorization: `Bearer ${session.access_token}`,
    'Content-Type': 'application/json',
  };

  try {
    const res = await fetch(`${url}/rest/v1/orders?id=eq.${orderId}`, {
      method: 'PATCH',
      headers,
      body: JSON.stringify({ status: 'cancelled' }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.message || `HTTP ${res.status}`);
    }

    window.auth.showToast('订单已取消', 'success');
    // 重新加载
    currentPage = 0;
    document.getElementById('ordersTableBody').innerHTML = '';
    await loadOrders();
    await loadStats();
  } catch (error) {
    console.error('Cancel order error:', error);
    window.auth.showToast('取消失败: ' + error.message, 'error');
  }
};

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
