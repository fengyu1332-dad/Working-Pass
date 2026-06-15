// ============================================================
// 专业星图 - 专业对比页逻辑
// ============================================================

import '../supabase-client.js';
import '../auth.js';
import '../common.js';
import { escapeHtml, getJsonArray } from '../utils.js';
import { t, createLangSwitcher, onLanguageChange } from '../i18n.js';

const MAJORS_FIELDS =
  'code,name,category,category_icon,salary_range,difficulty,overview,career_outlook,what_you_learn,suitable_for,xuefeng_comment,top_universities,yearly_courses,career_directions,degree,duration';

// ---- 对比维度定义 ----
const COMPARE_SECTIONS = [
  {
    id: 'basic',
    labelKey: 'compare_section_basic',
    fields: [
      { key: 'category', labelKey: 'major_category', type: 'text' },
      { key: 'code', labelKey: 'major_code', type: 'text' },
      { key: 'degree', labelKey: 'major_degree', type: 'text' },
      { key: 'duration', labelKey: 'major_duration', type: 'duration' },
      { key: 'difficulty', labelKey: 'major_difficulty', type: 'text' },
    ],
  },
  {
    id: 'salary',
    labelKey: 'compare_section_salary',
    highlight: true,
    fields: [
      { key: 'salary_range', labelKey: 'major_salary', type: 'salary' },
      { key: 'career_outlook', labelKey: 'career_outlook', type: 'text' },
      { key: 'career_directions', labelKey: 'major_directions', type: 'tags' },
    ],
  },
  {
    id: 'study',
    labelKey: 'compare_section_study',
    fields: [
      { key: 'overview', labelKey: 'major_overview', type: 'text' },
      { key: 'what_you_learn', labelKey: 'major_courses', type: 'text' },
      { key: 'yearly_courses', labelKey: 'yearly_courses', type: 'courses' },
    ],
  },
  {
    id: 'fit',
    labelKey: 'compare_section_fit',
    fields: [
      { key: 'suitable_for', labelKey: 'major_suitable', type: 'text' },
    ],
  },
  {
    id: 'schools',
    labelKey: 'compare_section_schools',
    fields: [
      { key: 'top_universities', labelKey: 'major_universities', type: 'universities' },
    ],
  },
  {
    id: 'comment',
    labelKey: 'compare_section_comment',
    fields: [
      { key: 'xuefeng_comment', labelKey: 'major_comment', type: 'comment' },
    ],
  },
];

// ---- 状态 ----
let majors = [];

function getCodesFromURL() {
  const params = new URLSearchParams(window.location.search);
  const raw = params.get('codes') || '';
  return raw.split(',').filter(Boolean);
}

async function init() {
  window.auth.initSupabase();

  const langContainer = document.getElementById('langSwitcherContainer');
  if (langContainer) {
    langContainer.appendChild(createLangSwitcher());
  }

  // 语言切换时重新渲染
  onLanguageChange(() => {
    if (majors.length) renderCompare();
  });

  await window.auth.getCurrentUser();
  if (typeof window.loadUserFavorites === 'function') window.loadUserFavorites();
  if (typeof window.updateUserArea === 'function') {
    window.updateUserArea();
  }

  const codes = getCodesFromURL();
  if (codes.length >= 2) {
    await loadMajors(codes);
    renderCompare();
  }
}

async function loadMajors(codes) {
  const { url, key } = window.supabaseClient;
  // Supabase 的 in 过滤器
  const codeFilter = codes.map((c) => `"${c}"`).join(',');
  const resp = await fetch(
    `${url}/rest/v1/majors?select=${MAJORS_FIELDS}&code=in.(${codeFilter})`,
    { headers: { apikey: key, Authorization: `Bearer ${key}` } },
  );
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
  const data = await resp.json();

  // 按 URL 参数顺序排列
  const map = new Map(data.map((m) => [m.code, m]));
  majors = codes.map((c) => map.get(c)).filter(Boolean);
}

// ============================================================
// 渲染
// ============================================================

function formatValue(major, field) {
  const val = major[field.key];
  if (!val && val !== 0) return t('no_data', '暂无数据');

  switch (field.type) {
    case 'duration':
      return val + t('major_duration_unit', '年');

    case 'salary': {
      const raw = String(val);
      // 提取 ¥Xk-Yk 中的数字
      const m = raw.match(/¥(\d+)k-(\d+)k/);
      if (m) return `<span class="salary-tag">¥${m[1]}k-¥${m[2]}k</span>`;
      return `<span class="salary-tag">${escapeHtml(raw)}</span>`;
    }

    case 'tags': {
      const arr = getJsonArray(major, field.key);
      if (!arr.length) return t('no_data', '暂无数据');
      return `<div class="direction-tags">${arr.map((d) => `<span class="direction-tag">${escapeHtml(d)}</span>`).join('')}</div>`;
    }

    case 'universities': {
      const unis =
        typeof val === 'string' ? JSON.parse(val) : val;
      const domestic = unis?.domestic || [];
      const intl = unis?.international || [];
      const parts = [];
      if (domestic.length)
        parts.push(`<div class="uni-tags">${domestic.map((u) => `<span class="uni-tag">${escapeHtml(u)}</span>`).join('')}</div>`);
      if (intl.length)
        parts.push(`<div class="uni-tags" style="margin-top:4px;">${intl.map((u) => `<span class="uni-tag">${escapeHtml(u)}</span>`).join('')}</div>`);
      return parts.join('') || t('no_data', '暂无数据');
    }

    case 'courses': {
      let courses = val;
      if (typeof courses === 'string') {
        try { courses = JSON.parse(courses); } catch { return escapeHtml(String(val)); }
      }
      if (!courses || typeof courses !== 'object') return t('no_data', '暂无数据');
      const lines = [];
      for (const [year, items] of Object.entries(courses)) {
        if (Array.isArray(items) && items.length) {
          lines.push(`<strong>${escapeHtml(year)}：</strong>${items.map((i) => escapeHtml(String(i))).join('、')}`);
        }
      }
      return lines.join('<br>') || t('no_data', '暂无数据');
    }

    case 'comment': {
      if (typeof window.formatXuefengComment === 'function') {
        return window.formatXuefengComment(val);
      }
      return escapeHtml(String(val));
    }

    default:
      return escapeHtml(String(val));
  }
}

function renderCompare() {
  const container = document.getElementById('compareContent');
  const toolbar = document.getElementById('compareToolbar');

  if (!majors.length || majors.length < 2) {
    toolbar.style.display = 'none';
    container.innerHTML = `
      <div class="compare-empty">
        <div class="empty-icon">📊</div>
        <h2>${t('compare_empty_title', '选择专业，开始并排对比')}</h2>
        <p>${t('compare_empty_desc', '从专业列表中选择 2-4 个专业，即可开始并排对比')}</p>
        <a href="/majors.html" class="btn-primary">${t('compare_browse_btn', '浏览全部专业 →')}</a>
        <div class="empty-hot-tags">
          <span class="hot-tags-label">热门对比：</span>
          <a href="?codes=080901,080902" class="hot-tag-link">计算机 vs 软件工程</a>
          <a href="?codes=100201K,100301K" class="hot-tag-link">临床 vs 口腔医学</a>
          <a href="?codes=080601,080701" class="hot-tag-link">电气 vs 电子信息</a>
          <a href="?codes=020301K,120203K" class="hot-tag-link">金融 vs 会计</a>
          <a href="?codes=030101K,050101" class="hot-tag-link">法学 vs 汉语言</a>
        </div>
      </div>`;
    return;
  }

  toolbar.style.display = 'flex';

  const isMobile = window.innerWidth < 768;

  if (isMobile) {
    renderMobileView(container);
  } else {
    renderDesktopTable(container);
  }

  // 事件绑定
  document.getElementById('btnClearCompare')?.addEventListener('click', clearCompare);
  document.getElementById('btnShareCompare')?.addEventListener('click', shareCompare);
  container.querySelectorAll('.remove-compare').forEach((btn) => {
    btn.addEventListener('click', () => {
      const code = btn.dataset.code;
      removeFromCompare(code);
    });
  });
  container.querySelectorAll('.compare-fav-btn').forEach((btn) => {
    const code = btn.dataset.code;
    updateCompareFavButtonUI(btn, code);
    btn.addEventListener('click', async () => {
      if (!window.toggleFavorite) return;
      const result = await window.toggleFavorite(code);
      if (result !== null) updateCompareFavButtonUI(btn, code);
    });
  });
}

function updateCompareFavButtonUI(btn, code) {
  if (!btn) return;
  const isFav = window.__userFavorites && window.__userFavorites.has(code);
  btn.textContent = isFav ? '❤' : '♡';
  btn.classList.toggle('favorited', isFav);
}

function renderDesktopTable(container) {
  let html = '<div class="compare-table-wrap"><table class="compare-table">';

  // 表头
  html += '<thead><tr><th>' + t('compare_dimension', '对比维度') + '</th>';
  for (const m of majors) {
    html += `<th>
      ${escapeHtml(m.name)}
      <span class="remove-compare" data-code="${escapeHtml(m.code)}">✕ 移除</span>
      <button class="compare-fav-btn" data-code="${escapeHtml(m.code)}">♡</button>
    </th>`;
  }
  html += '</tr></thead><tbody>';

  // 分组行
  for (const section of COMPARE_SECTIONS) {
    const sectionLabel = t(section.labelKey, section.labelKey);
    html += `<tr class="section-header"><td colspan="${majors.length + 1}">${escapeHtml(sectionLabel)}</td></tr>`;

    for (const field of section.fields) {
      const fieldLabel = t(field.labelKey, field.labelKey);
      const rowClass = section.highlight ? ' class="highlight"' : '';
      html += `<tr${rowClass}><td>${escapeHtml(fieldLabel)}</td>`;
      for (const m of majors) {
        html += `<td>${formatValue(m, field)}</td>`;
      }
      html += '</tr>';
    }
  }

  html += '</tbody></table></div>';
  container.innerHTML = html;
}

function renderMobileView(container) {
  let html = '';

  for (const section of COMPARE_SECTIONS) {
    const sectionLabel = t(section.labelKey, section.labelKey);
    html += `<div class="compare-card-group">
      <div class="group-title">${escapeHtml(sectionLabel)}</div>`;

    for (const field of section.fields) {
      const fieldLabel = t(field.labelKey, field.labelKey);
      html += `<div class="compare-card-item">
        <div class="field-label">${escapeHtml(fieldLabel)}</div>`;
      for (const m of majors) {
        html += `<div class="major-block">
          <div class="major-name">${escapeHtml(m.name)} <button class="compare-fav-btn" data-code="${escapeHtml(m.code)}">♡</button></div>
          <div class="field-value">${formatValue(m, field)}</div>
        </div>`;
      }
      html += '</div>';
    }

    html += '</div>';
  }

  container.innerHTML = html;
}

// ============================================================
// 操作
// ============================================================

function clearCompare() {
  window.location.href = '/compare.html';
}

function shareCompare() {
  const url = window.location.href;
  navigator.clipboard.writeText(url).then(() => {
    if (window.auth?.showToast) {
      window.auth.showToast(t('share_success', '对比链接已复制到剪贴板'), 'success');
    }
  }).catch(() => {
    // 降级
    const input = document.createElement('input');
    input.value = url;
    document.body.appendChild(input);
    input.select();
    document.execCommand('copy');
    document.body.removeChild(input);
    if (window.auth?.showToast) {
      window.auth.showToast(t('share_success', '对比链接已复制到剪贴板'), 'success');
    }
  });
}

function removeFromCompare(code) {
  majors = majors.filter((m) => m.code !== code);
  if (majors.length < 2) {
    window.location.href = '/compare.html';
    return;
  }
  const newCodes = majors.map((m) => m.code).join(',');
  window.history.replaceState(null, '', `/compare.html?codes=${newCodes}`);
  renderCompare();
}

// 响应窗口大小变化
let resizeTimer;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    if (majors.length >= 2) renderCompare();
  }, 300);
});

// 启动
init();
