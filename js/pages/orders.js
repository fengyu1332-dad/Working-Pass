// ============================================================
// 专业星图 - 历史记录页
// ============================================================

import '../supabase-client.js';
import '../auth.js';
import '../payments.js';
import '../error-report.js';

let currentTab = 'orders';

(async function () {
  window.auth.initSupabase();

  const isLoggedIn = await window.auth.checkAuthAndRedirect();
  if (!isLoggedIn) return;

  await loadOrders();

  document.getElementById('logoutBtn').addEventListener('click', async (e) => {
    e.preventDefault();
    try {
      await window.auth.logout();
    } catch (error) {
      window.auth.showToast('退出失败', 'error');
    }
  });
})();

function switchTab(tab) {
  currentTab = tab;

  document.querySelectorAll('.tab-btn').forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.tab === tab);
  });

  document.getElementById('ordersTab').style.display = tab === 'orders' ? 'block' : 'none';
  document.getElementById('downloadsTab').style.display = tab === 'downloads' ? 'block' : 'none';

  if (tab === 'orders') {
    loadOrders();
  } else {
    loadDownloads();
  }
}

async function loadOrders() {
  const list = document.getElementById('ordersList');

  try {
    let orders = await window.payments.getOrders();

    if (!orders || orders.length === 0) {
      console.warn('订单数据为空，请检查数据库 orders 表');
    }

    if (orders.length === 0) {
      list.innerHTML = `
        <div class="empty-state">
          <div class="empty-state-icon">📦</div>
          <div>暂无订单记录</div>
        </div>`;
      return;
    }

    list.innerHTML = orders
      .map(
        (order) => `
      <div class="record-item">
        <div>
          <div class="record-title">${order.point_packages?.name || order.package_name || '点数充值'}</div>
          <div class="record-meta">
            ${formatDate(order.created_at)} ·
            ${order.status === 'paid' ? '✓ 已支付' : order.status === 'pending' ? '⏳ 待支付' : order.status === 'cancelled' ? '✗ 已取消' : order.status === 'expired' ? '⏰ 已过期' : order.status}
            ${order.alipay_trade_no ? ` · 交易号: ${order.alipay_trade_no.slice(-16)}` : ''}
          </div>
        </div>
        <div class="record-points positive">
          +${order.points}
        </div>
      </div>`
      )
      .join('');
  } catch (error) {
    console.error('Load orders error:', error);
    list.innerHTML = `
      <div class="empty-state">
        <div class="empty-state-icon">⚠️</div>
        <div>加载失败，请稍后重试</div>
      </div>`;
  }
}

async function loadDownloads() {
  const list = document.getElementById('downloadsList');

  try {
    let downloads = await window.payments.getDownloadRecords();

    if (!downloads || downloads.length === 0) {
      console.warn('下载记录为空，请检查数据库 download_records 表');
    }

    if (downloads.length === 0) {
      list.innerHTML = `
        <div class="empty-state">
          <div class="empty-state-icon">📚</div>
          <div>暂无下载记录</div>
        </div>`;
      return;
    }

    list.innerHTML = downloads
      .map(
        (record) => `
      <div class="record-item">
        <div>
          <div class="record-title">${record.reports?.major_name || record.report_name || '专业报告'}</div>
          <div class="record-meta">
            ${record.reports?.major_code || record.report_code || ''} ·
            ${formatDate(record.created_at)}
          </div>
        </div>
        <div class="record-points negative">
          -${record.points_spent}
        </div>
      </div>`
      )
      .join('');
  } catch (error) {
    console.error('Load downloads error:', error);
    list.innerHTML = `
      <div class="empty-state">
        <div class="empty-state-icon">⚠️</div>
        <div>加载失败，请稍后重试</div>
      </div>`;
  }
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
}

// 导出到全局供 onclick 使用
window.switchTab = switchTab;
