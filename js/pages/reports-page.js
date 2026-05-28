// ============================================================
// 专业星图 - 报告浏览页（在线阅读模式）
// ============================================================

import '../supabase-client.js';
import '../auth.js';
import '../reports.js';
import '../error-report.js';

let currentReports = [];
let currentProfile = null;
let unlockedReports = new Set();
let currentCategory = 'all';
let currentReportSort = 'name';

(async function () {
  window.auth.initSupabase();

  const isLoggedIn = await window.auth.checkAuthAndRedirect();
  if (!isLoggedIn) return;

  currentProfile = await window.auth.getUserProfile();
  if (currentProfile) {
    document.getElementById('reportBalance').textContent = currentProfile.points_balance || 0;
  }

  await loadReports();

  document.getElementById('logoutBtn').addEventListener('click', async (e) => {
    e.preventDefault();
    try { await window.auth.logout(); } catch (error) { window.auth.showToast('退出失败', 'error'); }
  });

  document.getElementById('categoryFilter').addEventListener('change', (e) => {
    currentCategory = e.target.value;
    applyReportFilters();
  });

  document.getElementById('reportSort').addEventListener('change', (e) => {
    currentReportSort = e.target.value;
    applyReportFilters();
  });

  document.getElementById('searchBtn').addEventListener('click', () => {
    const search = document.getElementById('searchInput').value;
    loadReports(search);
  });

  document.getElementById('searchInput').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      loadReports(e.target.value);
    }
  });

  document.getElementById('modalCloseBtn').addEventListener('click', closeModal);

  document.getElementById('reportModal').addEventListener('click', (e) => {
    if (e.target === document.getElementById('reportModal')) closeModal();
  });
})();

async function loadReports(search = null) {
  try {
    const [reports, unlockedIds] = await Promise.all([
      window.reports.getReports(null, search),
      window.reports.getUnlockedReportIds(),
    ]);
    currentReports = reports || [];
    unlockedReports = new Set(unlockedIds || []);

    populateCategoryFilter(currentReports);
    applyReportFilters();
  } catch (error) {
    console.error('Load reports error:', error);
    window.auth.showToast('加载报告失败', 'error');
  }
}

function populateCategoryFilter(reports) {
  const select = document.getElementById('categoryFilter');
  if (!select) return;

  const categories = [...new Set(reports.map((r) => r.category).filter(Boolean))].sort((a, b) =>
    a.localeCompare(b, 'zh-CN')
  );

  const currentValue = select.value;
  select.innerHTML = '<option value="all">全部学科</option>';
  categories.forEach((cat) => {
    const option = document.createElement('option');
    option.value = cat;
    option.textContent = cat;
    select.appendChild(option);
  });
  select.value = currentValue;
}

function applyReportFilters() {
  let filtered = [...currentReports];

  if (currentCategory !== 'all') {
    filtered = filtered.filter((r) => r.category === currentCategory);
  }

  if (currentReportSort === 'name') {
    filtered.sort((a, b) => (a.major_name || '').localeCompare(b.major_name || '', 'zh-CN'));
  } else if (currentReportSort === 'downloads') {
    filtered.sort((a, b) => (b.download_count || 0) - (a.download_count || 0));
  } else if (currentReportSort === 'recent') {
    filtered.sort((a, b) => (b.id || 0) - (a.id || 0));
  }

  renderReports(filtered);
}

function renderReports(reports) {
  const grid = document.getElementById('reportsGrid');

  if (!reports || reports.length === 0) {
    grid.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 60px; color: var(--on-surface-variant);">
        📭 暂无报告数据
      </div>`;
    return;
  }

  grid.innerHTML = reports
    .map(
      (report) => `
    <div class="card report-card" id="report-${report.id}">
      <div class="report-code">${report.major_code || ''}</div>
      <div class="report-title">
        ${report.major_name || '未命名报告'}
        ${unlockedReports.has(report.id) ? '<span class="downloaded-badge">✓ 已解锁</span>' : ''}
      </div>
      <div style="color: var(--on-surface-variant); font-size: 13px; margin-bottom: 8px;">${report.category || ''}</div>
      <div style="color: var(--on-surface-variant); font-size: 13px; line-height: 1.6; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">
        ${report.preview_content || ''}
      </div>
      <div class="report-meta">
        <span>${report.download_count || 0} 次解锁</span>
        <span>消耗 1 点</span>
      </div>
    </div>`
    )
    .join('');

  reports.forEach((report) => {
    const card = document.getElementById(`report-${report.id}`);
    if (card) card.addEventListener('click', () => showReportDetail(report.id));
  });
}

async function showReportDetail(reportId) {
  const report = currentReports.find((r) => r.id === reportId);
  if (!report) return;

  const modal = document.getElementById('reportModal');
  const title = document.getElementById('modalTitle');
  const content = document.getElementById('modalContent');

  title.textContent = report.major_name;

  const isUnlocked = unlockedReports.has(reportId);

  if (isUnlocked) {
    content.innerHTML = `
      <div class="report-code">${report.major_code || ''}</div>
      <div style="color: var(--on-surface-variant); margin-bottom: 16px;">${report.category || ''}</div>
      <div id="reportReaderContainer" style="max-height:60vh;overflow-y:auto;padding:20px;background:#fafafa;border-radius:12px;line-height:1.9;font-size:15px;">
        加载中...
      </div>
      <div style="display:flex;gap:12px;justify-content:flex-end;margin-top:16px;">
        <button class="btn btn-outline" id="detailCloseBtn">关闭</button>
      </div>`;
    modal.classList.add('active');
    document.getElementById('detailCloseBtn').addEventListener('click', closeModal);
    await loadFullReport(reportId);
  } else {
    content.innerHTML = `
      <div class="report-code">${report.major_code || ''}</div>
      <div style="color: var(--on-surface-variant); margin-bottom: 16px;">${report.category || ''}</div>
      <div class="report-preview">
        <div style="font-weight: 600; margin-bottom: 12px; color: var(--secondary);">👁️ 免费预览</div>
        ${report.preview_content || '暂无预览内容'}
      </div>
      <div class="report-locked">
        <div class="report-locked-icon">🔒</div>
        <div style="font-size: 18px; font-weight: 600; margin-bottom: 8px;">解锁完整报告</div>
        <div style="color: var(--on-surface-variant); margin-bottom: 24px;">
          您的点数: <span style="color: var(--primary); font-weight: 700; font-size: 24px;">${currentProfile?.points_balance || 0}</span>
        </div>
        <button class="btn btn-primary" id="unlockBtn">
          消耗 1 点解锁完整报告
        </button>
        ${(currentProfile?.points_balance || 0) < 1 ? `
          <div style="margin-top: 16px;">
            <a href="/user/purchase.html" style="color: var(--primary); text-decoration: none; font-weight: 600;">点数不足？去充值 →</a>
          </div>` : ''}
        <button class="btn btn-outline" id="detailCloseBtn" style="margin-top:12px;">关闭</button>
      </div>`;
    modal.classList.add('active');
    document.getElementById('unlockBtn').addEventListener('click', () => unlockReportWrapper(report.id));
    document.getElementById('detailCloseBtn').addEventListener('click', closeModal);
  }
}

async function loadFullReport(reportId) {
  try {
    const result = await window.reports.unlockReport(reportId);
    const container = document.getElementById('reportReaderContainer');
    if (container) {
      if (result.content) {
        container.innerHTML = result.content;
      } else {
        container.innerHTML = '<p style="text-align:center;color:var(--on-surface-variant);padding:40px;">暂无报告内容</p>';
      }
    }
  } catch (error) {
    console.error('Load full report error:', error);
    const container = document.getElementById('reportReaderContainer');
    if (container) {
      container.innerHTML = `<p style="text-align:center;color:var(--error);padding:40px;">加载失败: ${error.message || '未知错误'}</p>`;
    }
  }
}

async function unlockReportWrapper(reportId) {
  try {
    await window.reports.unlockReport(reportId);
    unlockedReports.add(reportId);
    currentProfile = await window.auth.getUserProfile();
    if (currentProfile) {
      document.getElementById('reportBalance').textContent = currentProfile.points_balance || 0;
    }
    window.auth.showToast('解锁成功！', 'success');
    // 重新打开详情，展示完整报告
    closeModal();
    showReportDetail(reportId);
  } catch (error) {
    console.error('Unlock error:', error);
    window.auth.showToast(error.message || '解锁失败', 'error');
  }
}

function closeModal() {
  document.getElementById('reportModal').classList.remove('active');
}
