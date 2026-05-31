// ============================================================
// 专业星图 - 购买点数页
// ============================================================

import '../supabase-client.js';
import '../auth.js';
import '../payments.js';
import '../error-report.js';

let currentPackages = [];
let purchasing = false;

(async function () {
  window.auth.initSupabase();

  const isLoggedIn = await window.auth.checkAuthAndRedirect();
  if (!isLoggedIn) return;

  await refreshBalance();
  await loadPackages();

  document.getElementById('logoutBtn').addEventListener('click', async (e) => {
    e.preventDefault();
    try { await window.auth.logout(); } catch (error) { window.auth.showToast('退出失败', 'error'); }
  });
})();

async function refreshBalance() {
  const profile = await window.auth.getUserProfile();
  if (profile) {
    document.getElementById('currentBalance').textContent = profile.points_balance || 0;
  }
}

function showFeedback(message, type) {
  const el = document.getElementById('purchaseFeedback');
  el.textContent = message;
  el.className = 'purchase-feedback ' + type + ' show';
  setTimeout(() => el.classList.remove('show'), 3000);
}

async function loadPackages() {
  try {
    const packages = await window.payments.getPointPackages();
    currentPackages = packages || [];
    renderPackages(currentPackages);
  } catch (error) {
    console.error('Load packages error:', error);
    showFeedback('加载套餐失败：' + (error.message || '未知错误'), 'error');
    document.getElementById('packagesGrid').innerHTML =
      '<p style="text-align:center;padding:40px;color:var(--on-surface-variant);">暂无可用套餐，请联系管理员</p>';
  }
}

function renderPackages(packages) {
  const grid = document.getElementById('packagesGrid');
  if (!packages || packages.length === 0) {
    grid.innerHTML =
      '<p style="text-align:center;padding:40px;color:var(--on-surface-variant);">暂无可用套餐</p>';
    return;
  }

  grid.innerHTML = packages
    .map(
      (pkg) => `
    <div class="package-card ${pkg.featured ? 'featured' : ''}" id="pkg-${pkg.id}">
      ${pkg.featured ? '<div class="package-badge">推荐</div>' : ''}
      <div class="package-points">${pkg.points}</div>
      <div class="package-unit">点数</div>
      <div class="package-price">¥${pkg.price}</div>
      ${pkg.original_price ? `<div class="package-original-price">¥${pkg.original_price}</div>` : '<div style="margin-bottom:16px;"></div>'}
      <div class="package-desc">${pkg.description || '解锁专业深度报告'}</div>
    </div>`
    )
    .join('');

  // 直接绑定点击购买
  packages.forEach((pkg) => {
    document.getElementById(`pkg-${pkg.id}`).addEventListener('click', () => purchasePackage(pkg));
  });
}

async function purchasePackage(pkg) {
  if (purchasing) return;
  purchasing = true;

  const card = document.getElementById(`pkg-${pkg.id}`);
  card.classList.add('busy');
  const originalText = card.querySelector('.package-desc').textContent;
  card.querySelector('.package-desc').textContent = '创建订单...';

  try {
    const result = await window.payments.createAlipayOrder(pkg.id);

    // 保存订单 ID 供回调页面使用
    sessionStorage.setItem('pendingOrderId', result.order.id);

    // 跳转到支付宝支付页
    window.location.href = result.payment_url;
  } catch (error) {
    console.error('Purchase error:', error);
    card.querySelector('.package-desc').textContent = originalText;
    showFeedback(error.message || '创建订单失败，请重试', 'error');
    card.classList.remove('busy');
    purchasing = false;
  }
}
