// ============================================================
// 专业星图 - 共享 UI 模块
// 提取自 index.html 和 majors.html 的重复代码
// ============================================================

import { escapeHtml, getJsonArray, formatXuefengComment, debounce, renderErrorState } from './utils.js';

async function updateUserArea() {
  const userArea = document.getElementById('navUserArea');
  if (!userArea) return;

  let user = null;
  if (window.auth && window.auth.getCurrentUser) {
    user = await window.auth.getCurrentUser();
  }

  if (user) {
    const identifier = user.phone || user.email || '用户';
    // 邮箱取 @ 前部分，手机号保持原样，均限长14字
    let displayName = identifier;
    if (identifier.includes('@')) {
      displayName = identifier.split('@')[0];
    }
    if (displayName.length > 14) displayName = displayName.slice(0, 14);

    userArea.innerHTML = `
            <div class="user-info">
                <a href="/user/dashboard.html" class="user-avatar-link" title="个人中心">
                  <div class="user-avatar">👤</div>
                </a>
                <a href="/user/dashboard.html" class="user-name-link" title="个人中心">${escapeHtml(displayName)}</a>
                <button class="btn-sm btn-primary-sm" id="logoutBtn">退出</button>
            </div>
        `;

    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
      logoutBtn.addEventListener('click', async () => {
        if (window.auth && window.auth.logout) {
          await window.auth.logout();
        }
        updateUserArea();
      });
    }
  } else {
    userArea.innerHTML = `
            <a href="login.html" class="nav-link">登录</a>
            <a href="register.html" class="btn-sm btn-primary-sm" style="text-decoration: none;">注册</a>
        `;
  }
}

let _previouslyFocused = null;

function openModal(major) {
  window._currentMajor = major;

  const setText = (id, text) => {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
  };

  setText('modalIcon', major.category_icon || '📚');
  setText('modalCategory', major.category);
  setText('modalTitle', major.name);
  setText('infoCategory', major.category);
  setText('infoCode', major.code);
  setText('infoDegree', major.degree || '--');
  setText('infoDuration', major.duration ? major.duration + '年' : '--');
  setText('infoDifficulty', major.difficulty);
  setText('infoSalary', major.salary_range);
  setText('detailOverview', major.overview || '暂无数据');
  setText('detailWhatYouLearn', major.what_you_learn || '暂无数据');
  setText('detailSuitable', major.suitable_for || '暂无数据');
  setText('detailCareerOutlook', major.career_outlook || '暂无数据');

  // 就业方向标签
  const dirs = getJsonArray(major, 'career_directions');
  ['detailCareerDirections', 'detailCareerDirections2'].forEach((id) => {
    const dirEl = document.getElementById(id);
    if (dirEl) {
      dirEl.innerHTML = dirs.length
        ? dirs.map((d) => `<span style="background:var(--surface-container);padding:6px 14px;border-radius:20px;font-size:13px;color:var(--on-surface);">${escapeHtml(d)}</span>`).join('')
        : '';
    }
  });
  const dirSection = document.getElementById('careerDirectionsSection');
  if (dirSection) dirSection.style.display = dirs.length ? '' : 'none';
  const dirSection2 = document.getElementById('careerDirectionsSection2');
  if (dirSection2) dirSection2.style.display = dirs.length ? '' : 'none';

  const salaryEl = document.getElementById('detailSalaryRange');
  if (salaryEl) {
    salaryEl.textContent = '就业薪资范围：' + (major.salary_range || '暂无数据');
  }

  const commentEl = document.getElementById('detailXuefengComment');
  if (commentEl) {
    commentEl.innerHTML = formatXuefengComment(major.xuefeng_comment) || '暂无数据';
  }

  const yearlyEl = document.getElementById('detailYearlyCourses');
  if (yearlyEl) {
    yearlyEl.innerHTML = '';
    if (major.yearly_courses) {
      const courses =
        typeof major.yearly_courses === 'string' ? JSON.parse(major.yearly_courses) : major.yearly_courses;
      for (const [year, items] of Object.entries(courses)) {
        yearlyEl.innerHTML += `<ul class="year-list"><li><strong>${escapeHtml(year)}：</strong>${items.map((i) => escapeHtml(i)).join('、')}</li></ul>`;
      }
    }
  }

  const unis = major.top_universities
    ? typeof major.top_universities === 'string'
      ? JSON.parse(major.top_universities)
      : major.top_universities
    : {};

  const uniEl = document.getElementById('detailUniversities');
  if (uniEl) {
    uniEl.innerHTML = '';
    if (unis.domestic) {
      uniEl.innerHTML += `
                <div class="uni-section">
                    <p class="uni-label">🇨🇳 国内名校</p>
                    <div class="uni-tags">${unis.domestic.map((u) => `<span class="uni-tag chinese">${escapeHtml(u)}</span>`).join('')}</div>
                </div>`;
    }
    if (unis.international) {
      uniEl.innerHTML += `
                <div class="uni-section">
                    <p class="uni-label">🌍 国际名校</p>
                    <div class="uni-tags">${unis.international.map((u) => `<span class="uni-tag foreign">${escapeHtml(u)}</span>`).join('')}</div>
                </div>`;
    }
  }

  // Reset to overview tab
  document.querySelectorAll('.tab-btn').forEach((btn) => btn.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach((tab) => tab.classList.remove('active'));
  const overviewBtn = document.querySelector('[data-tab="overview"]');
  const overviewTab = document.getElementById('overviewTab');
  if (overviewBtn) overviewBtn.classList.add('active');
  if (overviewTab) overviewTab.classList.add('active');

  const modal = document.getElementById('modal');
  if (modal) {
    _previouslyFocused = document.activeElement;
    modal.classList.add('show');
    const closeBtn = document.getElementById('closeModal');
    if (closeBtn) closeBtn.focus();
  }
}

function closeModal() {
  const modal = document.getElementById('modal');
  if (modal) modal.classList.remove('show');
  window._currentMajor = null;
  if (_previouslyFocused && typeof _previouslyFocused.focus === 'function') {
    _previouslyFocused.focus();
    _previouslyFocused = null;
  }
}

function trapFocusInModal(e) {
  const modal = document.getElementById('modal');
  if (!modal || !modal.classList.contains('show')) return;
  if (e.key !== 'Tab') return;

  const focusable = modal.querySelectorAll(
    'button:not([disabled]), [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  if (focusable.length === 0) return;

  const first = focusable[0];
  const last = focusable[focusable.length - 1];

  if (e.shiftKey) {
    if (document.activeElement === first) {
      e.preventDefault();
      last.focus();
    }
  } else {
    if (document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  }
}

function closePreheatModal() {
  const modal = document.getElementById('preheatModal');
  if (modal) modal.classList.remove('show');
}

// ============================================================
// 深度分析报告 - 三步购买流程
// ============================================================

function injectReportFlowStyles() {
  if (document.getElementById('report-flow-styles')) return;
  const style = document.createElement('style');
  style.id = 'report-flow-styles';
  style.textContent = `
    .report-flow-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:1001;display:flex;align-items:center;justify-content:center;opacity:0;visibility:hidden;transition:all 0.3s;}
    .report-flow-overlay.active{opacity:1;visibility:visible;}
    .report-flow-modal{background:var(--surface);border-radius:16px;width:92vw;max-width:660px;max-height:85vh;overflow-y:auto;box-shadow:0 16px 48px rgba(0,0,0,0.25);display:flex;flex-direction:column;}
    .report-flow-header{padding:20px 24px 16px;border-bottom:1px solid var(--outline);display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;background:var(--surface);z-index:2;border-radius:16px 16px 0 0;}
    .report-flow-header h2{font-size:19px;color:var(--secondary);margin:0;}
    .report-flow-close{background:none;border:none;font-size:26px;cursor:pointer;color:var(--on-surface-variant);padding:4px 8px;line-height:1;border-radius:8px;transition:all 0.2s;}
    .report-flow-close:hover{background:var(--surface-container);color:var(--on-surface);}
    .report-flow-body{padding:24px;}
    .chapter-list{list-style:none;padding:0;margin:0 0 20px;}
    .chapter-item{display:flex;justify-content:space-between;align-items:center;padding:10px 14px;border-radius:8px;margin-bottom:4px;background:var(--surface-container-low);font-size:14px;}
    .chapter-item:nth-child(even){background:var(--surface-container);}
    .chapter-name{font-weight:500;color:var(--on-surface);}
    .chapter-pages{font-size:12px;color:var(--on-surface-variant);white-space:nowrap;margin-left:12px;}
    .report-summary{background:var(--primary-container);border-radius:12px;padding:16px 20px;margin-bottom:20px;display:flex;justify-content:space-around;text-align:center;}
    .summary-value{font-size:24px;font-weight:700;color:var(--primary);}
    .summary-label{font-size:13px;color:var(--on-surface-variant);margin-top:2px;}
    .confirm-warning{background:#FFF3E0;border:1px solid #FFB74D;border-radius:12px;padding:14px 18px;margin-bottom:20px;color:#E65100;font-size:14px;line-height:1.6;display:flex;align-items:flex-start;gap:10px;}
    .reader-tabs{display:flex;gap:2px;border-bottom:2px solid var(--outline);margin-bottom:20px;overflow-x:auto;position:sticky;top:69px;background:var(--surface);z-index:1;}
    .reader-tab{padding:10px 14px;border:none;background:none;cursor:pointer;font-size:13px;font-weight:500;white-space:nowrap;color:var(--on-surface-variant);border-bottom:3px solid transparent;margin-bottom:-2px;transition:all 0.2s;font-family:inherit;}
    .reader-tab:hover{color:var(--secondary);}
    .reader-tab.active{color:var(--primary);border-bottom-color:var(--primary);}
    .reader-content{line-height:1.85;color:var(--on-surface);max-height:50vh;overflow-y:auto;white-space:pre-wrap;font-size:14px;}
    .reader-content h3{color:var(--secondary);margin-bottom:12px;font-size:17px;}
    .btn-block{width:100%;justify-content:center;}
    .report-flow-back{display:inline-flex;align-items:center;gap:4px;background:none;border:none;color:var(--primary);cursor:pointer;font-size:13px;padding:4px 0;margin-bottom:16px;font-family:inherit;}
    .report-flow-back:hover{text-decoration:underline;}
  `;
  document.head.appendChild(style);
}

function createReportFlowModal() {
  injectReportFlowStyles();
  let overlay = document.getElementById('reportFlowOverlay');
  if (overlay) return overlay;

  overlay = document.createElement('div');
  overlay.id = 'reportFlowOverlay';
  overlay.className = 'report-flow-overlay';
  overlay.innerHTML = `
    <div class="report-flow-modal" id="reportFlowModal" role="dialog" aria-modal="true" aria-label="深度分析报告">
      <div class="report-flow-header">
        <h2 id="reportFlowTitle">深度分析报告</h2>
        <button class="report-flow-close" id="reportFlowClose" aria-label="关闭">&times;</button>
      </div>
      <div class="report-flow-body" id="reportFlowBody"></div>
    </div>
  `;
  document.body.appendChild(overlay);

  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) closeReportFlow();
  });
  document.getElementById('reportFlowClose').addEventListener('click', closeReportFlow);

  return overlay;
}

function closeReportFlow() {
  const overlay = document.getElementById('reportFlowOverlay');
  if (overlay) overlay.classList.remove('active');
}

function openReportFlow() {
  createReportFlowModal().classList.add('active');
  setTimeout(() => {
    const closeBtn = document.getElementById('reportFlowClose');
    if (closeBtn) closeBtn.focus();
  }, 100);
}

function generateChapterOutline(major) {
  const chapters = [];
  if (major.overview) chapters.push({ name: '专业概览', field: 'overview' });
  if (major.what_you_learn) chapters.push({ name: '核心课程与技能', field: 'what_you_learn' });
  if (major.career_outlook) chapters.push({ name: '职业发展前景', field: 'career_outlook' });
  if (major.salary_range) chapters.push({ name: '薪资待遇分析', field: 'salary_range' });
  if (major.suitable_for) chapters.push({ name: '适合人群分析', field: 'suitable_for' });
  if (major.xuefeng_comment) chapters.push({ name: '雪峰老师点评', field: 'xuefeng_comment' });
  if (major.top_universities) chapters.push({ name: '推荐院校指南', field: 'top_universities' });
  if (major.yearly_courses) chapters.push({ name: '学年课程规划', field: 'yearly_courses' });
  return chapters;
}

function estimateChapterPages(major, field) {
  const val = major[field];
  if (!val) return 1;
  const text = typeof val === 'string' ? val : JSON.stringify(val);
  return Math.max(1, Math.ceil(text.length / 500));
}

function buildFullContentChapters(major) {
  const chapters = [];
  if (major.overview) chapters.push({ title: '专业概览', content: major.overview });
  if (major.what_you_learn) chapters.push({ title: '核心课程与技能', content: major.what_you_learn });
  if (major.career_outlook) chapters.push({ title: '职业发展前景', content: major.career_outlook });
  if (major.salary_range) chapters.push({ title: '薪资待遇分析', content: `该专业毕业生薪资范围：${major.salary_range}` });
  if (major.suitable_for) chapters.push({ title: '适合人群分析', content: major.suitable_for });
  if (major.xuefeng_comment) chapters.push({ title: '雪峰老师点评', content: major.xuefeng_comment });
  if (major.top_universities) {
    let unis = major.top_universities;
    if (typeof unis === 'string') { try { unis = JSON.parse(unis); } catch (e) {} }
    let text = '';
    if (unis.domestic) text += '【国内名校】\n' + unis.domestic.map((u) => '• ' + u).join('\n') + '\n\n';
    if (unis.international) text += '【国际名校】\n' + unis.international.map((u) => '• ' + u).join('\n');
    chapters.push({ title: '推荐院校指南', content: text || '暂无数据' });
  }
  if (major.yearly_courses) {
    let courses = major.yearly_courses;
    if (typeof courses === 'string') { try { courses = JSON.parse(courses); } catch (e) {} }
    let text = '';
    for (const [year, items] of Object.entries(courses)) {
      text += `${year}：${Array.isArray(items) ? items.join('、') : items}\n`;
    }
    chapters.push({ title: '学年课程规划', content: text });
  }
  return chapters;
}

function showReportPreviewModal(major, reportData, alreadyPurchased) {
  openReportFlow();
  const body = document.getElementById('reportFlowBody');
  const title = document.getElementById('reportFlowTitle');
  if (!body || !title) return;

  title.textContent = '深度分析报告';
  const chapters = generateChapterOutline(major);
  const totalPages = chapters.reduce((sum, ch) => sum + estimateChapterPages(major, ch.field), 0);

  body.innerHTML = `
    <div style="margin-bottom:20px;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <span class="report-code" style="display:inline-block;background:var(--secondary-container);padding:4px 12px;border-radius:20px;font-size:12px;color:var(--secondary);">${escapeHtml(major.code || '--')}</span>
        <span style="color:var(--on-surface-variant);font-size:14px;">${escapeHtml(major.category || '')}</span>
      </div>
      <h3 style="color:var(--secondary);font-size:18px;margin:0 0 8px;">${escapeHtml(major.name)}</h3>
      <p style="color:var(--on-surface-variant);font-size:14px;line-height:1.6;margin:0;">
        本报告涵盖专业概况、课程设置、就业前景、薪资待遇、适合人群、院校推荐等核心维度，帮助您全面评估该专业。
      </p>
    </div>

    <h4 style="color:var(--secondary);margin:0 0 12px;font-size:15px;">📑 报告章节</h4>
    <ul class="chapter-list">
      ${chapters.map((ch, i) => `
        <li class="chapter-item">
          <span class="chapter-name">${i + 1}. ${ch.name}</span>
          <span class="chapter-pages">≈ ${estimateChapterPages(major, ch.field)} 页</span>
        </li>
      `).join('')}
    </ul>

    <div class="report-summary">
      <div><div class="summary-value">${chapters.length}</div><div class="summary-label">章节数</div></div>
      <div><div class="summary-value">≈ ${totalPages}</div><div class="summary-label">总页数</div></div>
      <div><div class="summary-value">1 💎</div><div class="summary-label">消耗点数</div></div>
    </div>

    ${alreadyPurchased ? `
      <button class="btn btn-primary btn-block" id="viewFullReportBtn">📖 查看完整报告</button>
      <p style="text-align:center;margin:12px 0 0;font-size:13px;color:var(--on-surface-variant);">您已解锁此报告，可随时查看</p>
    ` : reportData ? `
      <button class="btn btn-primary btn-block" id="unlockReportBtn">💎 消耗 1 点解锁完整报告</button>
      <p style="text-align:center;margin:12px 0 0;font-size:13px;color:var(--on-surface-variant);">解锁后可在个人中心随时查看</p>
    ` : `
      <div class="confirm-warning">
        <span style="font-size:20px;flex-shrink:0;">📝</span>
        <span>该专业的深度分析报告<strong>正在筹备中</strong>，敬请期待。您也可以<strong>浏览其他专业的已上线报告</strong>。</span>
      </div>
      <a href="user/reports.html" class="btn btn-primary btn-block" style="display:flex;text-decoration:none;">📋 浏览已上线报告</a>
    `}
  `;

  if (alreadyPurchased) {
    document.getElementById('viewFullReportBtn').addEventListener('click', () => {
      showReportReader(major, buildFullContentChapters(major));
    });
  } else if (reportData) {
    document.getElementById('unlockReportBtn').addEventListener('click', () => {
      showConfirmPaymentModal(major, reportData);
    });
  }
}

function showConfirmPaymentModal(major, reportData) {
  const body = document.getElementById('reportFlowBody');
  const title = document.getElementById('reportFlowTitle');
  if (!body || !title) return;

  title.textContent = '确认支付';

  body.innerHTML = `
    <button class="report-flow-back" id="backToPreview">← 返回报告预览</button>

    <div style="margin-bottom:20px;">
      <div style="font-size:16px;font-weight:600;color:var(--secondary);margin-bottom:6px;">${escapeHtml(major.name)}</div>
      <div style="color:var(--on-surface-variant);font-size:13px;">专业代码：${escapeHtml(major.code || '--')}　|　${escapeHtml(major.category || '')}</div>
    </div>

    <div class="report-summary">
      <div><div class="summary-label">报告名称</div><div style="font-weight:600;color:var(--secondary);font-size:14px;margin-top:2px;">${major.name}</div></div>
      <div><div class="summary-value">1 💎</div><div class="summary-label">消耗点数</div></div>
    </div>

    <div class="confirm-warning">
      <span style="font-size:20px;flex-shrink:0;">⚠️</span>
      <span>一旦解锁，<strong>点数不予退还</strong>。请确认您要购买的报告名称无误，支付后无法撤销。</span>
    </div>

    <div style="display:flex;gap:12px;">
      <button class="btn btn-outline" id="cancelPaymentBtn" style="flex:1;">取消</button>
      <button class="btn btn-primary" id="confirmPaymentBtn" style="flex:1;">确认支付 1 点</button>
    </div>
  `;

  document.getElementById('backToPreview').addEventListener('click', () => {
    showReportPreviewModal(major, reportData, false);
  });
  document.getElementById('cancelPaymentBtn').addEventListener('click', () => {
    showReportPreviewModal(major, reportData, false);
  });
  document.getElementById('confirmPaymentBtn').addEventListener('click', () => {
    performReportPurchase(major, reportData);
  });
}

async function performReportPurchase(major, reportData) {
  const body = document.getElementById('reportFlowBody');
  const confirmBtn = document.getElementById('confirmPaymentBtn');
  if (!body) return;

  if (confirmBtn) {
    confirmBtn.disabled = true;
    confirmBtn.textContent = '处理中...';
  }

  try {
    // 统一走原子化 RPC 扣点（带防重复检查）
    if (reportData && window.reports && window.reports.unlockReport) {
      await window.reports.unlockReport(reportData.id);
    } else {
      throw new Error('报告模块未就绪，请刷新页面重试');
    }

    if (window.auth && window.auth.showToast) {
      window.auth.showToast('解锁成功！', 'success');
    }

    const balanceEl = document.getElementById('userBalance');
    if (balanceEl && window.auth && window.auth.getUserProfile) {
      const updated = await window.auth.getUserProfile();
      if (updated) balanceEl.textContent = updated.points_balance || 0;
    }

    showReportReader(major, buildFullContentChapters(major));
  } catch (error) {
    console.error('Purchase error:', error);
    if (window.auth && window.auth.showToast) {
      window.auth.showToast(error.message || '支付失败，请重试', 'error');
    }
    if (confirmBtn) {
      confirmBtn.disabled = false;
      confirmBtn.textContent = '确认支付 1 点';
    }
  }
}

function showReportReader(major, chapters) {
  const body = document.getElementById('reportFlowBody');
  const title = document.getElementById('reportFlowTitle');
  if (!body || !title) return;

  title.textContent = major.name;

  let currentChapter = 0;

  const renderChapter = (idx) => {
    currentChapter = idx;
    const ch = chapters[idx];
    document.getElementById('readerContent').innerHTML = `<h3>${escapeHtml(ch.title)}</h3>${ch.content}`;
    document.querySelectorAll('.reader-tab').forEach((t, i) => t.classList.toggle('active', i === idx));
  };

  body.innerHTML = `
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
      <span class="report-code" style="display:inline-block;background:var(--success-container);padding:4px 12px;border-radius:20px;font-size:12px;color:var(--success);">✓ 已解锁</span>
      <span style="color:var(--on-surface-variant);font-size:13px;">${chapters.length} 个章节</span>
    </div>
    <div class="reader-tabs" id="readerTabs">
      ${chapters.map((ch, i) => `
        <button class="reader-tab${i === 0 ? ' active' : ''}" data-index="${i}">${escapeHtml(ch.title)}</button>
      `).join('')}
    </div>
    <div class="reader-content" id="readerContent">
      <h3>${escapeHtml(chapters[0].title)}</h3>${chapters[0].content}
    </div>
  `;

  document.querySelectorAll('.reader-tab').forEach((tab) => {
    tab.addEventListener('click', () => renderChapter(parseInt(tab.dataset.index)));
  });
}

async function goToReports(majorCode) {
  let user = null;
  if (window.auth && window.auth.getCurrentUser) {
    user = await window.auth.getCurrentUser();
  }
  if (!user) {
    if (confirm('查看深度报告需要登录，是否前往登录？')) {
      window.location.href = 'login.html';
    }
    return;
  }

  if (!majorCode && window._currentMajor) {
    majorCode = window._currentMajor.code;
  }

  // 在 closeModal 清除 _currentMajor 之前保存数据
  const major = window._currentMajor;

  if (typeof closeModal === 'function') closeModal();

  if (majorCode) {
    // 先检查数据库是否有该专业的报告
    let report = null;
    try {
      if (window.reports?.getReportByMajorCode) {
        report = await window.reports.getReportByMajorCode(majorCode);
      }
    } catch {
      // 查询失败时回退到跳转 reports 页面
    }

    if (report) {
      // 数据库有报告 → 跳转到报告浏览页
      window.location.href = `user/reports.html?code=${encodeURIComponent(majorCode)}`;
    } else if (major) {
      // 无报告但有专业数据 → 就地展示预览弹窗
      showReportPreviewModal(major, null, false);
    } else {
      window.location.href = 'user/reports.html';
    }
  } else {
    window.location.href = 'user/reports.html';
  }
}

// 导出到全局供 HTML onclick 使用
if (typeof window !== 'undefined') {
  window.updateUserArea = updateUserArea;
  window.openModal = openModal;
  window.closeModal = closeModal;
  window.closePreheatModal = closePreheatModal;
  window.goToReports = goToReports;
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    const reportFlow = document.getElementById('reportFlowOverlay');
    const modal = document.getElementById('modal');
    const preheatModal = document.getElementById('preheatModal');
    if (reportFlow && reportFlow.classList.contains('active')) {
      closeReportFlow();
    } else if (preheatModal && preheatModal.classList.contains('show')) {
      closePreheatModal();
    } else if (modal && modal.classList.contains('show')) {
      closeModal();
    }
  }
  trapFocusInModal(e);
});
