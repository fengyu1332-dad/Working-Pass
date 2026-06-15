// ============================================================
// 专业星图 - 共享 UI 模块
// 提取自 index.html 和 majors.html 的重复代码
// ============================================================

import { escapeHtml, getJsonArray, formatXuefengComment, debounce, renderErrorState } from './utils.js';
import { t, onLanguageChange, createLangSwitcher } from './i18n.js';
import '../css/compare-float.css';

// 语言切换时重新渲染用户区域
onLanguageChange(() => {
  updateUserArea();
  // 如果有打开的专业详情弹窗，重新渲染
  if (window._currentMajor) {
    openModal(window._currentMajor);
  }
});

async function updateUserArea() {
  const userArea = document.getElementById('navUserArea');
  if (!userArea) return;

  let user = null;
  if (window.auth && window.auth.getCurrentUser) {
    user = await window.auth.getCurrentUser();
  }

  // 保留 langSwitcher 容器（如果存在）
  const langSwitcherHTML = document.getElementById('langSwitcherContainer') ? '<div id="langSwitcherContainer"></div>' : '';

  if (user) {
    const identifier = user.phone || user.email || '用户';
    let displayName = identifier;
    if (identifier.includes('@')) {
      displayName = identifier.split('@')[0];
    }
    if (displayName.length > 14) displayName = displayName.slice(0, 14);

    userArea.innerHTML = `
            <a href="majors.html" class="nav-link">${t('nav_majors', '专业浏览')}</a>
            <a href="assessment.html" class="nav-link" style="font-weight:600;">${t('nav_assessment', '适配测评')}</a>
            <div class="user-info">
                <a href="/user/dashboard.html" class="user-avatar-link" title="${t('nav_dashboard', '个人中心')}">
                  <div class="user-avatar">👤</div>
                </a>
                <a href="/user/dashboard.html" class="user-name-link" title="${t('nav_dashboard', '个人中心')}">${escapeHtml(displayName)}</a>
                <button class="btn-sm btn-primary-sm" id="logoutBtn">${t('nav_logout', '退出')}</button>
            </div>
            ${langSwitcherHTML}
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
            <a href="majors.html" class="nav-link">${t('nav_majors', '专业浏览')}</a>
            <a href="assessment.html" class="nav-link" style="font-weight:600;">${t('nav_assessment', '适配测评')}</a>
            <a href="login.html" class="nav-link">${t('nav_login', '登录')}</a>
            <a href="register.html" class="btn-sm btn-primary-sm" style="text-decoration: none;">${t('nav_register', '注册')}</a>
            ${langSwitcherHTML}
        `;
  }

  // 重新创建 langSwitcher
  const newLangContainer = document.getElementById('langSwitcherContainer');
  if (newLangContainer) {
    newLangContainer.appendChild(createLangSwitcher());
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
  setText('infoDuration', major.duration ? major.duration + t('major_duration_unit', '年') : '--');
  setText('infoDifficulty', major.difficulty);
  setText('infoSalary', major.salary_range);
  setText('detailOverview', major.overview || t('no_data', '暂无数据'));
  setText('detailWhatYouLearn', major.what_you_learn || t('no_data', '暂无数据'));
  setText('detailSuitable', major.suitable_for || t('no_data', '暂无数据'));
  setText('detailCareerOutlook', major.career_outlook || t('no_data', '暂无数据'));

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
    salaryEl.textContent = t('salary_detail_prefix', '就业薪资范围：') + (major.salary_range || t('no_data', '暂无数据'));
  }

  const commentEl = document.getElementById('detailXuefengComment');
  if (commentEl) {
    commentEl.innerHTML = formatXuefengComment(major.xuefeng_comment) || t('no_data', '暂无数据');
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
                    <p class="uni-label">🇨🇳 ${t('domestic_unis', '国内名校')}</p>
                    <div class="uni-tags">${unis.domestic.map((u) => `<span class="uni-tag chinese">${escapeHtml(u)}</span>`).join('')}</div>
                </div>`;
    }
    if (unis.international) {
      uniEl.innerHTML += `
                <div class="uni-section">
                    <p class="uni-label">🌍 ${t('international_unis', '国际名校')}</p>
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

    // 更新「加入对比」按钮
    const compareBtn = document.getElementById('modalCompareBtn');
    if (compareBtn) {
      const list = window.__compareList || [];
      const inList = list.some((m) => m.code === major.code);
      const isFull = list.length >= 4;
      compareBtn.style.display = '';
      compareBtn.disabled = isFull && !inList;
      compareBtn.classList.toggle('in-list', inList);
      if (inList) {
        compareBtn.textContent = '✅ 已加入对比';
      } else if (isFull) {
        compareBtn.textContent = '对比已满 (4/4)';
      } else {
        compareBtn.textContent = t('compare_add_btn', '加入对比');
      }
      compareBtn.onclick = () => {
        if (isFull && !inList) return;
        if (addToCompare(major)) {
          compareBtn.textContent = '✅ 已加入对比';
          compareBtn.classList.add('in-list');
        }
      };
    }

    // 更新收藏按钮
    const favBtn = document.getElementById('modalFavBtn');
    if (favBtn) {
      favBtn.style.display = '';
      const isFav = window.isFavorited ? window.isFavorited(major.code) : false;
      favBtn.textContent = isFav ? '❤ 已收藏' : '♡ 收藏';
      favBtn.classList.toggle('favorited', isFav);
      favBtn.onclick = async () => {
        if (window.toggleFavorite) {
          const result = await window.toggleFavorite(major.code);
          if (result === true) {
            favBtn.textContent = '❤ 已收藏';
            favBtn.classList.add('favorited');
          } else if (result === false) {
            favBtn.textContent = '♡ 收藏';
            favBtn.classList.remove('favorited');
          }
        }
      };
    }
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
    .chapter-item{display:flex;justify-content:space-between;align-items:flex-start;padding:10px 14px;border-radius:8px;margin-bottom:4px;background:var(--surface-container-low);font-size:14px;gap:12px;}
    .chapter-item:nth-child(even){background:var(--surface-container);}
    .chapter-name{font-weight:500;color:var(--on-surface);}
    .chapter-desc{font-size:12px;color:var(--on-surface-variant);margin-top:2px;line-height:1.4;}
    .report-summary{background:var(--primary-container);border-radius:12px;padding:16px 20px;margin-bottom:20px;line-height:1.7;font-size:14px;color:var(--on-surface);}
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

// 13章报告结构（与 AI 生成报告一致）
const REPORT_CHAPTERS = [
  { name: '专业概述', desc: '学科定位、培养目标与核心价值' },
  { name: '课程安排与学习内容', desc: '分年级课程体系、核心课程详解与实践环节' },
  { name: '就业前景分析', desc: '就业率、主要方向、行业分布与绿牌/红牌评估' },
  { name: '薪资水平与职业发展', desc: '应届到资深各阶段薪资、城市差异与晋升路径' },
  { name: '考研与深造分析', desc: '考研必要性评估、推荐方向与 A+/A/A- 院校推荐' },
  { name: '考公考编分析', desc: '对口岗位梳理、竞争比、上岸难度与体制内待遇' },
  { name: '行业发展与人才需求', desc: '行业生命周期、政策支持力度、人才缺口与5年趋势' },
  { name: '适合人群与适配度', desc: '特质画像、核心能力星级评估与不适合人群警示' },
  { name: '学业难度与学习建议', desc: '课程难度星级、挂科率预警与高效学习策略' },
  { name: '家庭背景与投入回报', desc: '教育总成本、回报周期与普通家庭适合度评估' },
  { name: '城市与地区适配', desc: '首选城市 Top5、产业重镇分布与地区薪资对比' },
  { name: 'AI 影响与未来趋势', desc: 'AI 替代风险评估、新机遇与不可替代核心能力' },
  { name: '雪峰点评', desc: '核心优势、真实痛点、报考建议与一句话总结' },
];

function generateChapterOutline(_major) {
  // 始终返回完整的 13 章结构，不再依赖 major 数据字段
  return REPORT_CHAPTERS;
}

function buildReportSummary(major) {
  return `本报告从专业概述、课程学习到就业前景、薪资发展，从考研深造、考公考编到行业趋势、城市选择，覆盖 13 个核心维度，为你系统评估「${major.name || '该专业'}」是否适合自己，做出更明智的学业与职业选择。`;
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

  title.textContent = t('report_flow_title', '深度分析报告');
  const chapters = generateChapterOutline(major);
  const summaryText = buildReportSummary(major);

  body.innerHTML = `
    <div style="margin-bottom:20px;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;flex-wrap:wrap;">
        <span class="report-code" style="display:inline-block;background:var(--secondary-container);padding:4px 12px;border-radius:20px;font-size:12px;color:var(--secondary);">${escapeHtml(major.code || '--')}</span>
        <span style="color:var(--on-surface-variant);font-size:14px;">${escapeHtml(major.category || '')}</span>
        ${alreadyPurchased ? '<span style="display:inline-block;background:#E8F5E9;color:#2E7D32;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:600;">✓ 已购买</span>' : ''}
      </div>
      <h3 style="color:var(--secondary);font-size:18px;margin:0 0 8px;">${escapeHtml(major.name)}</h3>
    </div>

    ${alreadyPurchased ? `
      <div style="background:linear-gradient(135deg,#E8F5E9,#C8E6C9);border-radius:12px;padding:12px 16px;margin-bottom:16px;display:flex;align-items:center;gap:10px;">
        <span style="font-size:24px;">✅</span>
        <span style="font-size:14px;color:#2E7D32;font-weight:500;">您已解锁此报告，可随时查看完整内容</span>
      </div>
    ` : ''}

    <h4 style="color:var(--secondary);margin:0 0 12px;font-size:15px;">📑 报告章节（共 13 章）</h4>
    <ul class="chapter-list">
      ${chapters.map((ch, i) => `
        <li class="chapter-item">
          <div>
            <span class="chapter-name">${i + 1}. ${ch.name}</span>
            <span class="chapter-desc">${ch.desc}</span>
          </div>
        </li>
      `).join('')}
    </ul>

    <div class="report-summary" style="text-align:left;font-size:14px;line-height:1.7;color:var(--on-surface);">
      📊 ${escapeHtml(summaryText)}
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

  if (alreadyPurchased && reportData) {
    document.getElementById('viewFullReportBtn').addEventListener('click', () => {
      showReportReader(major, reportData.full_content || '');
    });
  } else if (alreadyPurchased) {
    // 已购买但无 reportData（异常情况），尝试用 major 数据展示
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
    let result;
    if (reportData && window.reports && window.reports.unlockReport) {
      result = await window.reports.unlockReport(reportData.id);
    } else {
      throw new Error('报告模块未就绪，请刷新页面重试');
    }

    if (window.auth && window.auth.showToast) {
      window.auth.showToast(result?.alreadyUnlocked ? '您已解锁此报告' : '解锁成功！', 'success');
    }

    const balanceEl = document.getElementById('userBalance');
    if (balanceEl && window.auth && window.auth.getUserProfile) {
      const updated = await window.auth.getUserProfile();
      if (updated) balanceEl.textContent = updated.points_balance || 0;
    }

    // 使用数据库中真实的 AI 生成 full_content，而非拼凑章节
    const realContent = result?.content || reportData?.full_content || '';
    showReportReader(major, realContent);
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

function showReportReader(major, content) {
  const body = document.getElementById('reportFlowBody');
  const title = document.getElementById('reportFlowTitle');
  if (!body || !title) return;

  title.textContent = major.name;

  const isHtmlContent = typeof content === 'string';

  if (isHtmlContent) {
    // 真实 AI 生成的 HTML 报告 → 直接渲染
    body.innerHTML = `
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
        <span class="report-code" style="display:inline-block;background:var(--success-container);padding:4px 12px;border-radius:20px;font-size:12px;color:var(--success);">✓ 已解锁</span>
        <span style="color:var(--on-surface-variant);font-size:13px;">深度分析报告</span>
      </div>
      <div class="reader-content" style="max-height:65vh;">${content || '<p style="text-align:center;color:var(--on-surface-variant);padding:40px;">暂无报告内容</p>'}</div>
    `;
  } else {
    // 向后兼容：章节数组模式（无真实报告时的 fallback）
    const chapters = content;
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
}

async function goToReports(majorCode) {
  let user = null;
  if (window.auth && window.auth.getCurrentUser) {
    user = await window.auth.getCurrentUser();
  }
  if (!user) {
    if (confirm(t('login_required_report', '查看深度报告需要登录，是否前往登录？'))) {
      const loginParams = new URLSearchParams();
      if (majorCode) loginParams.set('code', majorCode);
      loginParams.set('redirect', window.location.pathname);
      const qs = loginParams.toString();
      window.location.href = 'login.html' + (qs ? '?' + qs : '');
    }
    return;
  }

  if (!majorCode && window._currentMajor) {
    majorCode = window._currentMajor.code;
  }

  // 在 closeModal 清除 _currentMajor 之前保存数据
  let major = window._currentMajor;

  // 如果 _currentMajor 未设置但 majorCode 有值，尝试从全局 majorsData 查找
  if (!major && majorCode && window._majorsData) {
    major = window._majorsData.find((m) => m.code === majorCode);
    if (major) window._currentMajor = major;
  }

  if (typeof closeModal === 'function') closeModal();

  if (majorCode) {
    // 并行查询报告数据 + 已解锁列表，减少一次往返延迟
    let report = null;
    let unlockedIds = [];
    try {
      const results = await Promise.all([
        window.reports?.getReportByMajorCode ? window.reports.getReportByMajorCode(majorCode) : Promise.resolve(null),
        window.reports?.getUnlockedReportIds ? window.reports.getUnlockedReportIds() : Promise.resolve([]),
      ]);
      report = results[0];
      unlockedIds = results[1] || [];
    } catch {
      // 查询失败回退到无报告展示
    }

    if (report) {
      const alreadyPurchased = unlockedIds.includes(report.id);
      showReportPreviewModal(major, report, alreadyPurchased);
    } else if (major) {
      // 无报告但有专业数据 → 展示"筹备中"弹窗
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

// ============================================================
// 专业对比 - 浮动栏 + 全局状态
// ============================================================
window.__compareList = window.__compareList || [];

function initCompareBar() {
  if (document.getElementById('compareFloat')) return;

  const float = document.createElement('div');
  float.id = 'compareFloat';
  float.className = 'compare-float collapsed';
  float.innerHTML = `
    <div class="compare-float-collapsed-icon" title="${t('compare_title', '横向对比')}">
      <span class="collapsed-icon-emoji">📊</span>横向对比
    </div>
    <span class="compare-badge" id="compareBadge"></span>
    <div class="compare-float-header">
      <span class="compare-float-title">${t('compare_title', '横向对比')}</span>
      <button class="compare-float-collapse" id="btnCompareCollapse" title="${t('compare_collapse', '收起')}">−</button>
    </div>
    <div class="compare-float-body" id="compareFloatBody"></div>
    <div class="compare-float-hint" id="compareFloatHint"></div>
    <div class="compare-float-footer">
      <button class="btn-float-go" id="btnCompareGo" disabled>${t('compare_start_btn', '开始对比')}</button>
      <button class="btn-float-clear" id="btnCompareClear">${t('compare_clear', '清空')}</button>
    </div>
  `;
  document.body.appendChild(float);

  // 折叠态点击药丸按钮 → 展开
  float.querySelector('.compare-float-collapsed-icon').addEventListener('click', (e) => {
    e.stopPropagation();
    expandCompareFloat();
  });

  // header 折叠按钮 → 收起
  document.getElementById('btnCompareCollapse').addEventListener('click', (e) => {
    e.stopPropagation();
    collapseCompareFloat();
  });

  // 前往对比页
  document.getElementById('btnCompareGo').addEventListener('click', () => {
    const codes = (window.__compareList || []).map((m) => m.code).join(',');
    if (codes) window.location.href = `/compare.html?codes=${codes}`;
  });

  // 清空
  document.getElementById('btnCompareClear').addEventListener('click', () => {
    clearCompareList();
  });

  updateCompareBar();
}

function expandCompareFloat() {
  const float = document.getElementById('compareFloat');
  if (!float) return;
  float.classList.remove('collapsed');
}

function collapseCompareFloat() {
  const float = document.getElementById('compareFloat');
  if (!float) return;
  float.classList.add('collapsed');
}

function addToCompare(major) {
  if (!window.__compareList) window.__compareList = [];

  if (window.__compareList.length >= 4) {
    if (window.auth && window.auth.showToast) {
      window.auth.showToast(t('compare_max_hint', '最多对比 4 个专业'), 'warning');
    }
    return false;
  }
  if (window.__compareList.find((m) => m.code === major.code)) {
    if (window.auth && window.auth.showToast) {
      window.auth.showToast(t('compare_already_in', '该专业已在对比列表中'), 'warning');
    }
    return false;
  }
  window.__compareList.push({
    code: major.code,
    name: major.name,
    category_icon: major.category_icon || '📚',
  });
  updateCompareBar();
  if (window.auth && window.auth.showToast) {
    window.auth.showToast(
      `已加入对比 (${window.__compareList.length}/4)`,
      'success',
    );
  }
  return true;
}

function removeCompare(code) {
  window.__compareList = window.__compareList.filter((m) => m.code !== code);
  updateCompareBar();
}

function clearCompareList() {
  window.__compareList = [];
  updateCompareBar();
}

function updateCompareBar() {
  const float = document.getElementById('compareFloat');
  if (!float) return;

  const list = window.__compareList || [];
  const body = document.getElementById('compareFloatBody');
  const hint = document.getElementById('compareFloatHint');
  const goBtn = document.getElementById('btnCompareGo');
  const clearBtn = document.getElementById('btnCompareClear');
  const badge = document.getElementById('compareBadge');

  // 角标数字
  if (badge) {
    badge.textContent = list.length > 0 ? list.length : '';
  }

  // body: 垂直排列专业条
  if (body) {
    let html = '';
    for (const m of list) {
      const displayName = m.name.length > 10 ? m.name.substring(0, 10) + '…' : m.name;
      html += `<div class="compare-float-slot filled" data-code="${escapeHtml(m.code)}">
        <span class="float-slot-icon">${escapeHtml(m.category_icon)}</span>
        <span class="float-slot-name">${escapeHtml(displayName)}</span>
        <span class="float-slot-remove" data-code="${escapeHtml(m.code)}">✕</span>
      </div>`;
    }
    // 空槽
    const emptyNeeded = Math.max(0, 4 - list.length);
    for (let i = 0; i < emptyNeeded; i++) {
      html += `<div class="compare-float-slot slot-empty">${t('compare_add_empty', '+ 添加专业')}</div>`;
    }
    body.innerHTML = html;

    // 绑定移除
    body.querySelectorAll('.compare-float-slot.filled').forEach((el) => {
      el.addEventListener('click', (e) => {
        e.stopPropagation();
        const code = el.dataset.code;
        if (code) removeCompare(code);
      });
    });

    // 空槽 → 跳转
    body.querySelectorAll('.compare-float-slot.slot-empty').forEach((el) => {
      el.addEventListener('click', (e) => {
        e.stopPropagation();
        window.location.href = '/majors.html';
      });
    });
  }

  // 提示文字
  if (hint) {
    if (list.length === 1) {
      hint.textContent = t('compare_need_one_more', '再选 1 个即可对比');
      hint.style.display = 'block';
    } else {
      hint.style.display = 'none';
    }
  }

  // 按钮
  if (goBtn) {
    goBtn.disabled = list.length < 2;
    goBtn.textContent = list.length >= 2
      ? `${t('compare_start_btn', '开始对比')} (${list.length})`
      : t('compare_start_btn', '开始对比');
  }
  if (clearBtn) {
    clearBtn.style.display = list.length > 0 ? '' : 'none';
  }

  // 空列表折叠，有专业则展开
  if (list.length === 0) {
    collapseCompareFloat();
  } else {
    expandCompareFloat();
  }

  // 通知其他组件
  window.dispatchEvent(new CustomEvent('compareListChanged', {
    detail: { codes: list.map((m) => m.code), count: list.length },
  }));
}

// ---- 专业收藏 ----
window.__userFavorites = new Set();
let _favoritesLoaded = false;

async function loadUserFavorites() {
  if (_favoritesLoaded) return window.__userFavorites;
  try {
    if (window.auth && window.auth.getCurrentUser) {
      const user = await window.auth.getCurrentUser();
      if (user && window.supabaseClient) {
        const { url, key } = window.supabaseClient;
        const res = await fetch(`${url}/rest/v1/user_favorites?select=major_code&user_id=eq.${user.id}`, {
          headers: { apikey: key, Authorization: `Bearer ${key}` },
        });
        if (res.ok) {
          const rows = await res.json();
          window.__userFavorites = new Set(rows.map(r => r.major_code));
        }
      }
    }
  } catch (e) { /* not logged in or network error */ }
  _favoritesLoaded = true;
  return window.__userFavorites;
}

async function toggleFavorite(majorCode) {
  const userId = await getCurrentUserIdForFav();
  if (!userId) {
    window.showToast(t('fav_login_required', '请先登录后再收藏'), 'error');
    return null;
  }
  const { url, key } = window.supabaseClient;
  const isFav = window.__userFavorites.has(majorCode);

  try {
    if (isFav) {
      await fetch(`${url}/rest/v1/user_favorites?user_id=eq.${userId}&major_code=eq.${encodeURIComponent(majorCode)}`, {
        method: 'DELETE', headers: { apikey: key, Authorization: `Bearer ${key}` },
      });
      window.__userFavorites.delete(majorCode);
    } else {
      await fetch(`${url}/rest/v1/user_favorites`, {
        method: 'POST',
        headers: { apikey: key, Authorization: `Bearer ${key}`, 'Content-Type': 'application/json', Prefer: 'return=minimal' },
        body: JSON.stringify({ user_id: userId, major_code: majorCode }),
      });
      window.__userFavorites.add(majorCode);
    }
    return !isFav;
  } catch (e) {
    console.error('Toggle favorite failed:', e);
    return null;
  }
}

async function getCurrentUserIdForFav() {
  try {
    if (window.auth && window.auth.getCurrentUser) {
      const user = await window.auth.getCurrentUser();
      return user ? user.id : null;
    }
  } catch (e) { /* */ }
  return null;
}

window.isFavorited = (code) => window.__userFavorites.has(code);
window.toggleFavorite = toggleFavorite;
window.loadUserFavorites = loadUserFavorites;

// ---- 全局导出 ----
window.initCompareBar = initCompareBar;
window.addToCompare = addToCompare;
window.removeCompare = removeCompare;
window.clearCompareList = clearCompareList;
window.updateCompareBar = updateCompareBar;
window.isInCompareList = function(code) {
  return (window.__compareList || []).some((m) => m.code === code);
};

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
