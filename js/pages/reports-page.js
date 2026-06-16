// ============================================================
// 专业星图 - 报告浏览页（在线阅读模式）
// ============================================================

import '../supabase-client.js';
import '../auth.js';
import '../reports.js';
import '../error-report.js';
import { sanitizeHTML } from '../sanitize-html.js';
import { highlightMatch, trackSearch } from '../search-utils.js';
import { t, createLangSwitcher, onLanguageChange } from '../i18n.js';

let currentReports = [];
let currentProfile = null;
let unlockedReports = new Set();
let currentCategory = 'all';
let currentReportSort = 'name';
let currentSearchTerm = '';
let unlockedOnly = false;
let searchTimer = null;
const FONT_SIZE_KEY = 'starmap_report_font_size';
const FONT_SIZES = { small: 15, medium: 18, large: 22 };

(async function () {
  window.auth.initSupabase();

  const langContainer = document.getElementById('langSwitcherContainer');
  if (langContainer) {
    langContainer.appendChild(createLangSwitcher());
  }

  // 语言切换时刷新报告卡片与 UI 文本
  onLanguageChange(() => {
    if (currentReports.length) {
      populateCategoryFilter(currentReports);
      applyReportFilters();
    }
    // 更新底部余额栏
    const balanceEl = document.getElementById('reportBalance');
    if (balanceEl && currentProfile) {
      balanceEl.textContent = currentProfile.points_balance || 0;
    }
    // 更新空状态提示
    const grid = document.getElementById('reportsGrid');
    if (grid && !currentReports.length) {
      grid.innerHTML = `<p style="text-align:center;padding:60px;color:var(--on-surface-variant);font-size:16px;">${t('report_no_data', '暂无报告数据')}</p>`;
    }
  });

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

  // 如果 URL 携带 ?unlocked=1，自动开启"仅显示已解锁"
  if (urlParams.get('unlocked') === '1') {
    const unlockedToggle = document.getElementById('unlockedOnlyFilter');
    if (unlockedToggle) {
      unlockedToggle.checked = true;
      unlockedOnly = true;
      applyReportFilters();
    }
  }

  document.getElementById('logoutBtn').addEventListener('click', async (e) => {
    e.preventDefault();
    try { await window.auth.logout(); } catch (error) { window.auth.showToast(t('logout_fail', '退出失败'), 'error'); }
  });

  document.getElementById('categoryFilter').addEventListener('change', (e) => {
    currentCategory = e.target.value;
    applyReportFilters();
  });

  document.getElementById('reportSort').addEventListener('change', (e) => {
    currentReportSort = e.target.value;
    applyReportFilters();
  });

  document.getElementById('unlockedOnlyFilter').addEventListener('change', (e) => {
    unlockedOnly = e.target.checked;
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
    }, 250);
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
    if (search) trackSearch(search, (reports || []).length);

    populateCategoryFilter(currentReports);
    applyReportFilters();
  } catch (error) {
    console.error('Load reports error:', error);
    window.auth.showToast(t('report_load_error', '加载报告失败'), 'error');
  }
}

function populateCategoryFilter(reports) {
  const select = document.getElementById('categoryFilter');
  if (!select) return;

  const categories = [...new Set(reports.map((r) => r.category).filter(Boolean))].sort((a, b) =>
    a.localeCompare(b, 'zh-CN')
  );

  const currentValue = select.value;
  select.innerHTML = `<option value="all">${t('filter_all', '全部学科')}</option>`;
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

  if (unlockedOnly) {
    filtered = filtered.filter((r) => unlockedReports.has(r.id));
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
      ? `${t('report_search_empty', '未找到匹配')}"${currentSearchTerm}"${t('report_search_empty_suffix', '的报告，请尝试其他关键词')}`
      : t('report_no_data', '暂无报告数据');
    const emptyIcon = currentSearchTerm ? '🔍' : '📭';
    grid.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 60px; color: var(--on-surface-variant);">
        <div style="font-size:48px;margin-bottom:12px;">${emptyIcon}</div>
        <div>${emptyMsg}</div>
        ${currentSearchTerm ? `<button class="btn btn-secondary" style="margin-top:16px;" id="clearSearchBtn">${t('clear_search', '清除搜索')}</button>` : ''}
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
        ${highlightMatch(report.major_name || t('report_unnamed', '未命名报告'), currentSearchTerm)}
        ${unlockedReports.has(report.id) ? `<span class="downloaded-badge">✓ ${t('report_unlocked', '已解锁')}</span>` : ''}
      </div>
      <div style="color: var(--on-surface-variant); font-size: 13px; margin-bottom: 8px;">${highlightMatch(report.category || '', currentSearchTerm)}</div>
      <div style="color: var(--on-surface-variant); font-size: 13px; line-height: 1.6; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">
        ${highlightMatch(report.preview_content || '', currentSearchTerm)}
      </div>
      <div class="report-meta">
        <span>${report.download_count || 0} ${t('report_downloads', '次解锁')}</span>
        <span>${t('report_cost', '消耗 1 点')}</span>
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
    const savedFont = localStorage.getItem(FONT_SIZE_KEY) || 'medium';
    content.innerHTML = `
      <div class="report-unlocked-layout">
        <div id="reportReaderContainer" class="report-reader-container" style="--report-font-size:${FONT_SIZES[savedFont] || 18}px;">${t('report_loading', '加载中...')}</div>
        <div class="report-share-bar">
          <div class="reading-toolbar" id="readingToolbar">
            <button class="font-btn small${savedFont === 'small' ? ' active' : ''}" data-size="small" title="小号字体 (15px)">A</button>
            <button class="font-btn${savedFont === 'medium' ? ' active' : ''}" data-size="medium" title="中号字体 (18px)">A</button>
            <button class="font-btn large${savedFont === 'large' ? ' active' : ''}" data-size="large" title="大号字体 (22px)">A</button>
          </div>
          <button class="fullscreen-btn" id="fullscreenBtn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>
            ${t('fullscreen_on', '全屏阅读')}
          </button>
          <button class="share-btn" id="shareReportBtn" style="margin-left:auto;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.59 13.51l6.83 3.98M15.41 6.51l-6.82 3.98"/></svg>
            ${t('report_share', '分享报告')}
          </button>
        </div>
      </div>`;
    modal.classList.add('active');

    setupReadingControls();

    const shareBtn = document.getElementById('shareReportBtn');
    shareBtn.addEventListener('click', async () => {
      await handleShare(report);
      shareBtn.classList.add('copied');
      shareBtn.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
        ${t('report_copied', '已复制')}
      `;
      setTimeout(() => {
        shareBtn.classList.remove('copied');
        shareBtn.innerHTML = `
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.59 13.51l6.83 3.98M15.41 6.51l-6.82 3.98"/></svg>
          ${t('report_share', '分享报告')}
        `;
      }, 2000);
    });

    await loadFullReport(reportId);
  } else {
    content.innerHTML = `
      <div style="flex:1;display:flex;flex-direction:column;min-height:0;overflow-y:auto;">
        <div class="report-preview-content" id="previewScroll">
          <div style="font-weight: 600; margin-bottom: 12px; color: var(--secondary); font-size: 16px;">👁️ ${t('report_preview', '免费预览')}</div>
          ${sanitizeHTML(report.preview_content || t('report_no_content', '暂无预览内容'))}
        </div>
        <div class="report-locked-area">
          <div style="font-size: 18px; font-weight: 600; margin-bottom: 8px;">🔒 ${t('report_unlock_btn', '解锁完整深度分析报告')}</div>
          <div style="color: var(--on-surface-variant); margin-bottom: 16px;">
            ${t('your_points', '您的点数')}: <span style="color: var(--primary); font-weight: 700; font-size: 24px;">${currentProfile?.points_balance || 0}</span>
          </div>
          <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
            <button class="btn btn-primary" id="unlockBtn">${t('report_unlock', '消耗 1 点解锁')}</button>
            ${(currentProfile?.points_balance || 0) < 1 ? `
              <a href="/user/purchase.html" class="btn btn-secondary">${t('report_buy_points', '充值获取点数')}</a>` : ''}
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
        ${t('report_copied', '已复制')}
      `;
      setTimeout(() => {
        shareBtn.classList.remove('copied');
        shareBtn.innerHTML = `
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.59 13.51l6.83 3.98M15.41 6.51l-6.82 3.98"/></svg>
          ${t('report_share', '分享报告')}
        `;
      }, 2000);
    });
  }
}

function setupReadingControls() {
  const toolbar = document.getElementById('readingToolbar');
  const container = document.getElementById('reportReaderContainer');
  const fullscreenBtn = document.getElementById('fullscreenBtn');
  const modalContent = document.querySelector('.report-modal-content');
  if (!toolbar || !container) return;

  // 字体缩放按钮
  toolbar.querySelectorAll('.font-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const size = btn.dataset.size;
      const px = FONT_SIZES[size] || 18;
      container.style.setProperty('--report-font-size', px + 'px');
      toolbar.querySelectorAll('.font-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      localStorage.setItem(FONT_SIZE_KEY, size);
    });
  });

  // 全屏阅读切换
  if (fullscreenBtn && modalContent) {
    let isFullscreen = false;
    fullscreenBtn.addEventListener('click', () => {
      isFullscreen = !isFullscreen;
      modalContent.classList.toggle('fullscreen-reading', isFullscreen);
      fullscreenBtn.innerHTML = isFullscreen
        ? `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="4 8 4 4 8 4"/><polyline points="20 16 20 20 16 20"/><line x1="4" y1="4" x2="9" y2="9"/><line x1="20" y1="20" x2="15" y2="15"/></svg> ${t('fullscreen_off', '退出全屏')}`
        : `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg> ${t('fullscreen_on', '全屏阅读')}`;
    });
  }

  // ESC 退出全屏
  const escHandler = (e) => {
    if (e.key === 'Escape' && modalContent && modalContent.classList.contains('fullscreen-reading')) {
      modalContent.classList.remove('fullscreen-reading');
      if (fullscreenBtn) {
        fullscreenBtn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg> ${t('fullscreen_on', '全屏阅读')}`;
      }
    }
  };

  // ---- 防窃取保护 ----
  const blockKeys = ['c', 'C', 's', 'S', 'p', 'P', 'u', 'U', 'a', 'A'];
  const protectHandler = (e) => {
    // 阻止右键菜单
    if (e.type === 'contextmenu') { e.preventDefault(); return; }
    // 阻止拖拽
    if (e.type === 'dragstart') { e.preventDefault(); return; }
    // 阻止 Ctrl/⌘ + 复制/保存/打印/全选/查看源码
    if (e.type === 'keydown') {
      if (e.key === 'F12' || (e.ctrlKey && e.key === 'F12')) { e.preventDefault(); return; }
      if ((e.ctrlKey || e.metaKey) && blockKeys.includes(e.key)) {
        // 允许 toolbar 内按钮的快捷键
        if (e.target.closest && e.target.closest('.reading-toolbar, .report-share-bar, .nav, #logoutBtn')) return;
        e.preventDefault();
      }
    }
  };

  container.addEventListener('contextmenu', protectHandler);
  container.addEventListener('dragstart', protectHandler);
  document.addEventListener('keydown', protectHandler);

  // 对预览区也加保护
  const previewEl = document.getElementById('previewScroll');
  if (previewEl) {
    previewEl.addEventListener('contextmenu', protectHandler);
    previewEl.addEventListener('dragstart', protectHandler);
  }

  // 水印
  applyWatermark(container);

  // 关弹窗时清理所有监听器
  const modal = document.getElementById('reportModal');
  if (modal) {
    const obs = new MutationObserver(() => {
      if (!modal.classList.contains('active')) {
        document.removeEventListener('keydown', escHandler);
        document.removeEventListener('keydown', protectHandler);
        obs.disconnect();
      }
    });
    obs.observe(modal, { attributes: true, attributeFilter: ['class'] });
  }
}

function applyWatermark(container) {
  if (!container || !currentProfile) return;
  try {
    const canvas = document.createElement('canvas');
    const w = 320;
    const h = 200;
    canvas.width = w;
    canvas.height = h;
    const ctx = canvas.getContext('2d');
    ctx.save();
    ctx.rotate(-22 * Math.PI / 180);
    ctx.font = '15px "Microsoft YaHei", "PingFang SC", sans-serif';
    ctx.fillStyle = 'rgba(0, 0, 0, 0.06)';
    const uid = currentProfile.email || currentProfile.username || currentProfile.id || '专业星图';
    for (let row = -1; row < 5; row++) {
      for (let col = -1; col < 6; col++) {
        ctx.fillText(uid, col * 130, row * 70);
      }
    }
    ctx.restore();
    const dataUrl = canvas.toDataURL('image/png');
    container.style.backgroundImage = `url(${dataUrl})`;
    container.classList.add('watermarked');
  } catch {
    // 水印生成失败不影响正常使用
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
        container.innerHTML = `<p style="text-align:center;color:var(--on-surface-variant);padding:40px;">${t('report_no_content', '暂无报告内容')}</p>`;
      }
    }
  } catch (error) {
    console.error('Load full report error:', error);
    const container = document.getElementById('reportReaderContainer');
    if (container) {
      container.innerHTML = `<p style="text-align:center;color:var(--error);padding:40px;">${t('report_load_error', '加载失败')}: ${error.message || t('unknown_error', '未知错误')}</p>`;
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
    window.auth.showToast(t('report_unlock_success', '解锁成功！'), 'success');
    // 重新打开详情，展示完整报告
    closeModal();
    showReportDetail(reportId);
  } catch (error) {
    console.error('Unlock error:', error);
    window.auth.showToast(error.message || t('report_unlock_fail', '解锁失败'), 'error');
  }
}

function closeModal() {
  document.getElementById('reportModal').classList.remove('active');
}
