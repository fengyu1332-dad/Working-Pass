// ============================================================
// 专业星图 - 报告浏览页（在线阅读模式）
// ============================================================

import '../supabase-client.js';
import '../auth.js';
import '../reports.js';
import '../error-report.js';
import { sanitizeHTML } from '../sanitize-html.js';
import { highlightMatch } from '../search-utils.js';

let currentReports = [];
let currentProfile = null;
let unlockedReports = new Set();
let currentCategory = 'all';
let currentReportSort = 'name';
let currentSearchTerm = '';
let searchTimer = null;

(async function () {
  window.auth.initSupabase();

  const isLoggedIn = await window.auth.checkAuthAndRedirect();
  if (!isLoggedIn) return;

  currentProfile = await window.auth.getUserProfile();
  if (currentProfile) {
    document.getElementById('reportBalance').textContent = currentProfile.points_balance || 0;
  }

  await loadReports();

  // 如果 URL 携带 ?code= 参数，自动定位到对应专业报告
  const urlParams = new URLSearchParams(window.location.search);
  const targetCode = urlParams.get('code');
  if (targetCode) {
    const targetReport = currentReports.find(
      (r) => r.major_code === targetCode
    );
    if (targetReport) {
      showReportDetail(targetReport.id);
    } else {
      // 报告不存在时静默回退到列表页，不做额外提示
      window.history.replaceState(null, '', window.location.pathname);
    }
  }

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
    const search = document.getElementById('searchInput').value.trim();
    currentSearchTerm = search;
    loadReports(search || null);
  });

  document.getElementById('searchInput').addEventListener('input', (e) => {
    const val = e.target.value.trim();
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      currentSearchTerm = val;
      loadReports(val || null);
    }, 350);
  });

  document.getElementById('searchInput').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      clearTimeout(searchTimer);
      const val = e.target.value.trim();
      currentSearchTerm = val;
      loadReports(val || null);
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
    const emptyMsg = currentSearchTerm
      ? `未找到匹配"${currentSearchTerm}"的报告，请尝试其他关键词`
      : '暂无报告数据';
    const emptyIcon = currentSearchTerm ? '🔍' : '📭';
    grid.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 60px; color: var(--on-surface-variant);">
        <div style="font-size:48px;margin-bottom:12px;">${emptyIcon}</div>
        <div>${emptyMsg}</div>
        ${currentSearchTerm ? '<button class="btn btn-secondary" style="margin-top:16px;" id="clearSearchBtn">清除搜索</button>' : ''}
      </div>`;
    if (currentSearchTerm) {
      document.getElementById('clearSearchBtn').addEventListener('click', () => {
        document.getElementById('searchInput').value = '';
        currentSearchTerm = '';
        loadReports(null);
      });
    }
    return;
  }

  grid.innerHTML = reports
    .map(
      (report) => `
    <div class="card report-card" id="report-${report.id}">
      <div class="report-code">${highlightMatch(report.major_code || '', currentSearchTerm)}</div>
      <div class="report-title">
        ${highlightMatch(report.major_name || '未命名报告', currentSearchTerm)}
        ${unlockedReports.has(report.id) ? '<span class="downloaded-badge">✓ 已解锁</span>' : ''}
      </div>
      <div style="color: var(--on-surface-variant); font-size: 13px; margin-bottom: 8px;">${highlightMatch(report.category || '', currentSearchTerm)}</div>
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

function buildShareContent(report) {
  const shareText = report.preview_content || '';
  // 提取纯文本摘要（去除 HTML 标签）
  const plainText = shareText.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
  const excerpt = plainText.length > 300 ? plainText.slice(0, 300) + '...' : plainText;
  return `📊【${report.major_name}】深度分析报告\n\n${excerpt}\n\n🔗 查看更多专业深度分析报告 → ${window.location.origin}/\n\n—— 专业星图 · 大学专业职业前景查询平台`;
}

async function handleShare(report) {
  const shareContent = buildShareContent(report);
  try {
    await navigator.clipboard.writeText(shareContent);
    window.auth.showToast('分享内容已复制到剪贴板', 'success');
  } catch {
    // fallback: 使用传统方法
    const ta = document.createElement('textarea');
    ta.value = shareContent;
    ta.style.position = 'fixed';
    ta.style.left = '-9999px';
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    window.auth.showToast('分享内容已复制到剪贴板', 'success');
  }
}

async function showReportDetail(reportId) {
  const report = currentReports.find((r) => r.id === reportId);
  if (!report) return;

  const modal = document.getElementById('reportModal');
  const title = document.getElementById('modalTitle');
  const badge = document.getElementById('modalBadge');
  const catEl = document.getElementById('modalCategory');
  const content = document.getElementById('modalContent');

  title.textContent = report.major_name;
  badge.textContent = report.major_code || '';
  badge.style.display = report.major_code ? '' : 'none';
  catEl.textContent = report.category || '';

  const isUnlocked = unlockedReports.has(reportId);

  if (isUnlocked) {
    content.innerHTML = `
      <div class="report-unlocked-layout">
        <div id="reportReaderContainer" class="report-reader-container">加载中...</div>
        <div class="report-share-bar">
          <button class="share-btn" id="shareReportBtn" style="margin-left:auto;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.59 13.51l6.83 3.98M15.41 6.51l-6.82 3.98"/></svg>
            分享报告
          </button>
        </div>
      </div>`;
    modal.classList.add('active');

    const shareBtn = document.getElementById('shareReportBtn');
    shareBtn.addEventListener('click', async () => {
      await handleShare(report);
      shareBtn.classList.add('copied');
      shareBtn.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
        已复制
      `;
      setTimeout(() => {
        shareBtn.classList.remove('copied');
        shareBtn.innerHTML = `
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.59 13.51l6.83 3.98M15.41 6.51l-6.82 3.98"/></svg>
          分享报告
        `;
      }, 2000);
    });

    await loadFullReport(reportId);
  } else {
    content.innerHTML = `
      <div style="flex:1;display:flex;flex-direction:column;min-height:0;overflow-y:auto;">
        <div class="report-preview-content" id="previewScroll">
          <div style="font-weight: 600; margin-bottom: 12px; color: var(--secondary); font-size: 16px;">👁️ 免费预览</div>
          ${sanitizeHTML(report.preview_content || '暂无预览内容')}
        </div>
        <div class="report-locked-area">
          <div style="font-size: 18px; font-weight: 600; margin-bottom: 8px;">🔒 解锁完整深度分析报告</div>
          <div style="color: var(--on-surface-variant); margin-bottom: 16px;">
            您的点数: <span style="color: var(--primary); font-weight: 700; font-size: 24px;">${currentProfile?.points_balance || 0}</span>
          </div>
          <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
            <button class="btn btn-primary" id="unlockBtn">消耗 1 点解锁</button>
            ${(currentProfile?.points_balance || 0) < 1 ? `
              <a href="/user/purchase.html" class="btn btn-secondary">充值获取点数</a>` : ''}
          </div>
        </div>
      </div>
      <div class="preview-share-bar">
        <button class="share-btn" id="shareReportBtn" style="margin-left:auto;">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.59 13.51l6.83 3.98M15.41 6.51l-6.82 3.98"/></svg>
          分享报告
        </button>
      </div>`;
    modal.classList.add('active');

    document.getElementById('unlockBtn').addEventListener('click', () => unlockReportWrapper(report.id));

    const shareBtn = document.getElementById('shareReportBtn');
    shareBtn.addEventListener('click', async () => {
      await handleShare(report);
      shareBtn.classList.add('copied');
      shareBtn.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
        已复制
      `;
      setTimeout(() => {
        shareBtn.classList.remove('copied');
        shareBtn.innerHTML = `
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.59 13.51l6.83 3.98M15.41 6.51l-6.82 3.98"/></svg>
          分享报告
        `;
      }, 2000);
    });
  }
}

async function loadFullReport(reportId) {
  try {
    const result = await window.reports.unlockReport(reportId);
    const container = document.getElementById('reportReaderContainer');
    if (container) {
      if (result.content) {
        container.innerHTML = sanitizeHTML(result.content);
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
