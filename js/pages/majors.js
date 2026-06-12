// ============================================================
// 专业星图 - 全部专业列表页
// 按需加载：初始展示14个学科门类入口，点击后才加载该门类专业
// ============================================================

import '../supabase-client.js';
import '../auth.js';
import '../common.js';
import '../reports.js';
import '../error-report.js';
import '../web-vitals.js';
import { searchMajors, highlightMatch, addRecentSearch, didYouMean, trackSearch } from '../search-utils.js';
import { t, createLangSwitcher, onLanguageChange } from '../i18n.js';

const { initWebVitals } = window.__starmap_webVitals || {};

// ---- 数据 & 状态 ----
let majorsData = [];
let categoryCounts = {};
let currentLoadedCategory = null; // null | 'all' | '08 工学'
let currentView = 'grid';
let currentFilters = {
  category: 'all',
  difficulty: 'all',
  salary: 'all',
  search: '',
};
let currentSort = 'name';
let currentSortDir = 'desc';
const PAGE_SIZE = 12;
let currentPage = 1;

// ---- 常量 ----
const CATEGORY_MAP = {
  '01': '🎓', '02': '💰', '03': '⚖️', '04': '📚',
  '05': '📖', '06': '📜', '07': '🔢', '08': '💻',
  '09': '🌾', '10': '🩺', '11': '📋', '12': '🎨',
  '13': '🎭', '14': '🔬',
};

const MAJORS_FIELDS = 'code,name,category,category_icon,salary_range,difficulty,overview,career_outlook,what_you_learn,suitable_for,xuefeng_comment,top_universities,yearly_courses,career_directions,degree,duration';

function getCategoryIcon(cat) {
  const code = cat.split(' ')[0];
  return CATEGORY_MAP[code] || '📚';
}

// ====== Phase 1: 轻量获取学科门类计数 ======
async function fetchCategoryCounts() {
  const { url, key } = window.supabaseClient;
  const response = await fetch(`${url}/rest/v1/majors?select=category`, {
    headers: { apikey: key, Authorization: `Bearer ${key}` },
  });
  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  const rows = await response.json();
  const counts = {};
  rows.forEach((r) => { counts[r.category] = (counts[r.category] || 0) + 1; });
  return counts;
}

// ====== Phase 2: 按需加载完整专业数据 ======
async function loadCategoryMajors(categoryName) {
  currentLoadedCategory = categoryName;
  showLoadingState();

  const { url, key } = window.supabaseClient;
  const encoded = encodeURIComponent(categoryName);
  const response = await fetch(
    `${url}/rest/v1/majors?select=${MAJORS_FIELDS}&category=eq.${encoded}&order=name`,
    { headers: { apikey: key, Authorization: `Bearer ${key}` } },
  );

  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  majorsData = await response.json();
  window._majorsData = majorsData;

  finishDataLoad();
}

async function loadAllMajors() {
  currentLoadedCategory = 'all';
  showLoadingState();

  const { url, key } = window.supabaseClient;
  const response = await fetch(
    `${url}/rest/v1/majors?select=${MAJORS_FIELDS}&order=name`,
    { headers: { apikey: key, Authorization: `Bearer ${key}` } },
  );

  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  majorsData = await response.json();
  window._majorsData = majorsData;

  // 检查 URL 中是否有 ?code= 参数（来自登录后跳转）
  const urlParams = new URLSearchParams(window.location.search);
  const initCode = urlParams.get('code');
  if (initCode) {
    const major = majorsData.find((m) => m.code === initCode);
    if (major) {
      window._currentMajor = major;
      window.history.replaceState(null, '', window.location.pathname);
      setTimeout(() => {
        if (window.goToReports) window.goToReports(initCode);
      }, 500);
    }
  }

  finishDataLoad();
}

function showLoadingState() {
  document.getElementById('categoryEntries').style.display = 'none';
  document.getElementById('loading').style.display = '';
  document.getElementById('majorsGrid').style.display = 'none';
  document.getElementById('majorsList').style.display = 'none';
  const pagination = document.getElementById('pagination');
  if (pagination) pagination.innerHTML = '';
}

function finishDataLoad() {
  document.getElementById('resultsCount').textContent = `${majorsData.length} ${t('major_count_unit', '个专业')}`;
  applyFiltersAndSort();
}

// ====== 学科门类入口卡片 ======
function renderCategoryEntries(counts) {
  const grid = document.getElementById('categoryEntries');
  const sorted = Object.keys(counts).sort();
  grid.innerHTML = '';

  // 提示文字
  const hint = document.createElement('p');
  hint.className = 'category-entry-hint';
  hint.textContent = t('category_hint', '选择一个学科门类开始浏览 — 仅加载该门类专业，更快更精准');
  grid.appendChild(hint);

  sorted.forEach((cat) => {
    const icon = getCategoryIcon(cat);
    const name = cat.replace(/^\d+\s/, '');
    const card = document.createElement('div');
    card.className = 'category-entry-card';
    card.dataset.category = cat;
    card.innerHTML = `
      <span class="category-entry-icon">${icon}</span>
      <h3 class="category-entry-name">${name}</h3>
      <span class="category-entry-count">${counts[cat]} ${t('major_count_unit', '个专业')}</span>
    `;
    card.addEventListener('click', () => selectCategory(cat));
    grid.appendChild(card);
  });
}

// ====== 侧边栏初始化 ======
function initSidebar(counts) {
  const container = document.getElementById('categoryFilters');
  container.innerHTML = '';

  const sorted = Object.keys(counts).sort();
  sorted.forEach((cat) => {
    const icon = getCategoryIcon(cat);
    const btn = document.createElement('button');
    btn.className = 'category-option';
    btn.dataset.category = cat;
    btn.setAttribute('role', 'radio');
    btn.setAttribute('aria-checked', 'false');
    btn.innerHTML = `<span class="category-icon">${icon}</span><span>${cat}</span>`;
    container.appendChild(btn);
  });

  // 分隔线 + "全部学科"放在最底部
  const divider = document.createElement('div');
  divider.style.cssText = 'border-top:1px solid var(--outline);margin:8px 0;';
  container.appendChild(divider);

  const allBtn = document.createElement('button');
  allBtn.className = 'category-option';
  allBtn.dataset.category = 'all';
  allBtn.setAttribute('role', 'radio');
  allBtn.setAttribute('aria-checked', 'false');
  allBtn.innerHTML = `<span class="category-icon">📖</span><span>${t('filter_all', '全部学科')}（${Object.values(counts).reduce((a, b) => a + b, 0)}${t('major_count_short', '个')}）</span>`;
  container.appendChild(allBtn);
}

// ====== 选择学科门类 ======
function selectCategory(cat) {
  if (cat === currentLoadedCategory) return;

  currentFilters.category = cat;
  syncCategoryFilterUI(cat);

  if (cat === 'all') {
    loadAllMajors();
  } else {
    loadCategoryMajors(cat);
  }
}

function syncCategoryFilterUI(activeCat) {
  document.querySelectorAll('#categoryFilters .category-option').forEach((o) => {
    const isActive = o.dataset.category === activeCat;
    o.classList.toggle('active', isActive);
    o.setAttribute('aria-checked', isActive.toString());
  });
}

// ====== 列表事件 ======
function setupListEvents() {
  // 侧边栏切换（移动端）
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('sidebar');
  let sidebarOverlay;

  if (sidebarToggle && sidebar) {
    const closeSidebar = () => {
      sidebar.classList.remove('open');
      if (sidebarOverlay) sidebarOverlay.classList.remove('show');
    };
    sidebarToggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      if (sidebar.classList.contains('open')) {
        if (!sidebarOverlay) {
          sidebarOverlay = document.createElement('div');
          sidebarOverlay.className = 'sidebar-overlay show';
          document.body.appendChild(sidebarOverlay);
          sidebarOverlay.addEventListener('click', closeSidebar);
        } else {
          sidebarOverlay.classList.add('show');
        }
      } else {
        closeSidebar();
      }
    });
  }

  // 搜索 — 仅在已有数据时客户端过滤；若需全量搜索则触发全部加载
  const searchInput = document.getElementById('searchInput');
  const searchClear = document.getElementById('searchClear');
  let searchDebounceTimer;
  searchInput.addEventListener('input', (e) => {
    searchClear.style.display = e.target.value ? 'flex' : 'none';
    clearTimeout(searchDebounceTimer);
    searchDebounceTimer = setTimeout(() => {
      const term = e.target.value.trim();
      currentFilters.search = term;
      if (term) {
        addRecentSearch(term);
        // 如果当前没有数据或只加载了部分门类，搜索需要全量数据
        if (currentLoadedCategory && currentLoadedCategory !== 'all') {
          currentFilters.category = 'all';
          syncCategoryFilterUI('all');
          loadAllMajors(); // finishDataLoad 内部已调用 applyFiltersAndSort
          return;
        }
      }
      if (currentLoadedCategory) applyFiltersAndSort();
    }, 250);
  });
  if (searchClear) {
    searchClear.addEventListener('click', () => {
      searchInput.value = '';
      searchClear.style.display = 'none';
      currentFilters.search = '';
      if (currentLoadedCategory) applyFiltersAndSort();
      searchInput.focus();
    });
  }

  // 分类筛选 — 触发数据加载
  document.getElementById('categoryFilters').addEventListener('click', (e) => {
    const option = e.target.closest('.category-option');
    if (option) {
      const cat = option.dataset.category;
      if (cat === currentLoadedCategory) return;
      selectCategory(cat);
    }
  });

  // 难度筛选 — 纯客户端
  document.getElementById('difficultyFilters').addEventListener('click', (e) => {
    if (e.target.classList.contains('difficulty-btn')) {
      document.querySelectorAll('#difficultyFilters .difficulty-btn').forEach((b) => b.classList.remove('active'));
      e.target.classList.add('active');
      currentFilters.difficulty = e.target.dataset.difficulty;
      if (currentLoadedCategory) applyFiltersAndSort();
    }
  });

  // 薪资筛选 — 纯客户端
  document.getElementById('salaryFilters').addEventListener('click', (e) => {
    const option = e.target.closest('.salary-option');
    if (option) {
      document.querySelectorAll('#salaryFilters .salary-option').forEach((o) => {
        o.classList.remove('active');
        o.setAttribute('aria-checked', 'false');
      });
      option.classList.add('active');
      option.setAttribute('aria-checked', 'true');
      currentFilters.salary = option.dataset.salary;
      if (currentLoadedCategory) applyFiltersAndSort();
    }
  });

  // 重置
  document.getElementById('resetFilters').addEventListener('click', () => {
    currentFilters.difficulty = 'all';
    currentFilters.salary = 'all';
    currentFilters.search = '';
    document.getElementById('searchInput').value = '';
    document.getElementById('searchClear').style.display = 'none';
    document.querySelectorAll('#difficultyFilters .difficulty-btn').forEach((b) => b.classList.remove('active'));
    const allDiff = document.querySelector('#difficultyFilters .difficulty-btn[data-difficulty="all"]');
    if (allDiff) allDiff.classList.add('active');
    document.querySelectorAll('#salaryFilters .salary-option').forEach((o) => {
      o.classList.remove('active');
      o.setAttribute('aria-checked', 'false');
    });
    const allSal = document.querySelector('#salaryFilters .salary-option[data-salary="all"]');
    if (allSal) { allSal.classList.add('active'); allSal.setAttribute('aria-checked', 'true'); }
    if (currentLoadedCategory) applyFiltersAndSort();
  });

  // 排序
  document.getElementById('sortSelect').addEventListener('change', (e) => {
    currentSort = e.target.value;
    if (currentLoadedCategory) applyFiltersAndSort();
  });

  document.getElementById('sortDirection').addEventListener('click', () => {
    currentSortDir = currentSortDir === 'asc' ? 'desc' : 'asc';
    document.getElementById('sortDirection').textContent = currentSortDir === 'asc' ? '⬆️' : '⬇️';
    if (currentLoadedCategory) applyFiltersAndSort(false);
  });

  // 视图切换
  document.querySelectorAll('.view-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.view-btn').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      currentView = btn.dataset.view;
      if (currentLoadedCategory) applyFiltersAndSort();
    });
  });
}

// ====== 筛选/排序/渲染 ======
function parseSalaryRange(salaryText) {
  const cleaned = salaryText.replace(/[¥\s]/g, '').toLowerCase();
  if (cleaned.includes('以上')) {
    const num = parseFloat(cleaned);
    return isNaN(num) ? null : { min: num, max: Infinity };
  }
  if (cleaned.includes('以下')) {
    const num = parseFloat(cleaned);
    return isNaN(num) ? null : { min: 0, max: num };
  }
  const match = cleaned.match(/(\d+\.?\d*)k?\s*[-–—到]\s*(\d+\.?\d*)k?/i);
  if (match) {
    return { min: parseFloat(match[1]), max: parseFloat(match[2]) };
  }
  const single = cleaned.match(/(\d+\.?\d*)/);
  if (single) {
    const v = parseFloat(single[1]);
    return { min: v, max: v + 5 };
  }
  return null;
}

function applyFiltersAndSort(resetPage = true) {
  if (resetPage) currentPage = 1;
  let filtered = [...majorsData];

  if (currentFilters.search) {
    filtered = searchMajors(filtered, currentFilters.search);
    trackSearch(currentFilters.search, filtered.length);
  }

  // 分类筛选仅在"全部学科"模式下才有意义（按需加载时数据已过滤）
  if (currentLoadedCategory === 'all' && currentFilters.category !== 'all') {
    filtered = filtered.filter((m) => m.category === currentFilters.category);
  }

  if (currentFilters.difficulty !== 'all') {
    const targetStars = parseInt(currentFilters.difficulty);
    filtered = filtered.filter(
      (m) => (m.difficulty || '').length >= targetStars && (m.difficulty || '').length <= targetStars
    );
  }

  if (currentFilters.salary !== 'all') {
    filtered = filtered.filter((m) => {
      const parsed = parseSalaryRange(m.salary_range || '');
      if (!parsed) return false;
      const avgSalary = (parsed.min + parsed.max) / 2;
      if (currentFilters.salary === '10k') return parsed.max <= 10;
      if (currentFilters.salary === '20k') return avgSalary >= 10 && avgSalary < 20;
      if (currentFilters.salary === '30k') return avgSalary >= 20 && avgSalary < 30;
      if (currentFilters.salary === 'above') return parsed.min >= 30;
      return true;
    });
  }

  const dir = currentSortDir === 'asc' ? 1 : -1;
  if (currentSort === 'name') {
    filtered.sort((a, b) => dir * a.name.localeCompare(b.name, 'zh-CN'));
  } else if (currentSort === 'salary') {
    filtered.sort((a, b) => {
      const salaryA = parseFloat((a.salary_range || '0').replace(/[^0-9.]/g, ''));
      const salaryB = parseFloat((b.salary_range || '0').replace(/[^0-9.]/g, ''));
      return dir * (salaryA - salaryB);
    });
  } else if (currentSort === 'difficulty') {
    filtered.sort((a, b) => dir * ((a.difficulty || '').length - (b.difficulty || '').length));
  }

  document.getElementById('resultsCount').textContent = `${filtered.length} ${t('major_count_unit', '个专业')}`;
  displayMajors(filtered);
  syncFiltersToHash();
}

function displayMajors(majors) {
  document.getElementById('loading').style.display = 'none';
  const grid = document.getElementById('majorsGrid');
  const list = document.getElementById('majorsList');
  const totalPages = Math.ceil(majors.length / PAGE_SIZE);
  const start = (currentPage - 1) * PAGE_SIZE;
  const pageItems = majors.slice(start, start + PAGE_SIZE);

  grid.innerHTML = '';
  list.innerHTML = '';

  if (majors.length === 0) {
    let emptyMsg = `<p style="text-align:center;padding:40px 60px;color:#8B7E74;font-size:16px;">${t('no_matching_majors', '暂无匹配的专业')}</p>`;
    if (currentFilters.search) {
      const suggestions = didYouMean(majorsData, currentFilters.search, 3);
      if (suggestions.length > 0) {
        emptyMsg = `<div style="text-align:center;padding:40px 60px;color:#8B7E74;font-size:16px;">
          <p style="margin-bottom:8px;">${t('no_results_prefix', '未找到')}"<strong>${currentFilters.search}</strong>"${t('no_results_suffix', '相关专业')}</p>
          <p>${t('did_you_mean', '你是不是想找')}：${suggestions.map(s => `<button class="suggestion-link" onclick="document.getElementById('searchInput').value='${s.replace(/'/g, "\\'")}';document.getElementById('searchInput').dispatchEvent(new Event('input'))" style="background:none;border:none;color:#E67E22;cursor:pointer;font-size:16px;text-decoration:underline;">${s}</button>`).join('、')}</p>
        </div>`;
      }
    }
    grid.innerHTML = emptyMsg;
    list.innerHTML = emptyMsg;
  } else {
    const searchTerm = currentFilters.search || '';
    pageItems.forEach((major) => {
      grid.appendChild(createGridCard(major, searchTerm));
      list.appendChild(createListItem(major, searchTerm));
    });
  }

  if (currentView === 'grid') {
    grid.style.display = 'grid';
    list.style.display = 'none';
  } else {
    grid.style.display = 'none';
    list.style.display = 'flex';
  }

  renderPagination(majors.length, totalPages);
}

function renderPagination(totalItems, totalPages) {
  let container = document.getElementById('pagination');
  if (!container) {
    container = document.createElement('div');
    container.id = 'pagination';
    container.className = 'pagination';
    document.querySelector('.list-container .main-content').appendChild(container);
  }
  if (totalPages <= 1) {
    container.innerHTML = '';
    return;
  }
  let html = `<span class="pagination-info">${t('pagination_info', '共')} ${totalItems} ${t('major_count_unit_short', '个专业')}，${totalPages} ${t('pagination_pages', '页')}</span>`;
  html += `<button class="pagination-prev" ${currentPage === 1 ? 'disabled' : ''}>${t('pagination_prev', '上一页')}</button>`;
  for (let i = 1; i <= totalPages; i++) {
    html += `<button class="pagination-btn ${i === currentPage ? 'active' : ''}" data-page="${i}">${i}</button>`;
  }
  html += `<button class="pagination-next" ${currentPage === totalPages ? 'disabled' : ''}>${t('pagination_next', '下一页')}</button>`;
  container.innerHTML = html;

  container.querySelectorAll('.pagination-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      if (btn.disabled) return;
      currentPage = parseInt(btn.dataset.page);
      applyFiltersAndSort(false);
      document.querySelector('.list-container .main-content').scrollIntoView({ behavior: 'smooth' });
    });
  });

  const prevBtn = container.querySelector('.pagination-prev');
  const nextBtn = container.querySelector('.pagination-next');
  prevBtn.addEventListener('click', () => {
    if (prevBtn.disabled) return;
    currentPage--;
    applyFiltersAndSort(false);
    document.querySelector('.list-container .main-content').scrollIntoView({ behavior: 'smooth' });
  });
  nextBtn.addEventListener('click', () => {
    if (nextBtn.disabled) return;
    currentPage++;
    applyFiltersAndSort(false);
    document.querySelector('.list-container .main-content').scrollIntoView({ behavior: 'smooth' });
  });
}

function syncFiltersToHash() {
  if (!currentLoadedCategory) return;
  const params = new URLSearchParams();
  if (currentFilters.category !== 'all') params.set('category', currentFilters.category);
  if (currentFilters.difficulty !== 'all') params.set('difficulty', currentFilters.difficulty);
  if (currentFilters.salary !== 'all') params.set('salary', currentFilters.salary);
  if (currentFilters.search) params.set('search', currentFilters.search);
  if (currentSort !== 'name') params.set('sort', currentSort);
  const hash = params.toString();
  history.replaceState(null, '', hash ? '#' + hash : window.location.pathname + window.location.search);
}

function applyHashFilters() {
  const params = new URLSearchParams(window.location.hash.replace('#', ''));
  let targetCat = null;
  if (params.has('category')) {
    currentFilters.category = params.get('category');
    targetCat = currentFilters.category === 'all' ? 'all' : currentFilters.category;
  }
  if (params.has('difficulty')) currentFilters.difficulty = params.get('difficulty');
  if (params.has('salary')) currentFilters.salary = params.get('salary');
  if (params.has('search')) currentFilters.search = params.get('search');
  if (params.has('sort')) currentSort = params.get('sort');
  syncFilterUI();

  if (targetCat && targetCat !== currentLoadedCategory) {
    selectCategory(targetCat);
  } else if (currentLoadedCategory) {
    applyFiltersAndSort();
  }
}

function syncFilterUI() {
  syncCategoryFilterUI(currentFilters.category);
  document.querySelectorAll('#difficultyFilters .difficulty-btn').forEach((b) => {
    b.classList.toggle('active', b.dataset.difficulty === currentFilters.difficulty);
  });
  document.querySelectorAll('#salaryFilters .salary-option').forEach((o) => {
    const isActive = o.dataset.salary === currentFilters.salary;
    o.classList.toggle('active', isActive);
    o.setAttribute('aria-checked', isActive.toString());
  });
  const searchInput = document.getElementById('searchInput');
  if (searchInput) searchInput.value = currentFilters.search || '';
  const searchClear = document.getElementById('searchClear');
  if (searchClear) searchClear.style.display = currentFilters.search ? 'flex' : 'none';
  const sortSelect = document.getElementById('sortSelect');
  if (sortSelect) sortSelect.value = currentSort;
}

function createGridCard(major, searchTerm = '') {
  const card = document.createElement('div');
  card.className = 'major-card';
  card.dataset.code = major.code;
  card.innerHTML = `
    <div class="card-header">
      <div class="card-cat-icon">${major.category_icon || '📚'}</div>
      <div>
        <h3 class="major-name">${highlightMatch(major.name, searchTerm)}</h3>
        <p class="major-code">${highlightMatch(major.code, searchTerm)}</p>
        <p class="difficulty-stars">${major.difficulty || ''}</p>
      </div>
    </div>
    <span class="salary-tag">${(major.salary_range || t('salary_negotiable', '薪资面议')).replace('¥', '')}</span>
    <p class="employment-desc">${highlightMatch((major.overview || '').substring(0, 60), searchTerm)}...</p>
  `;
  card.addEventListener('click', () => openModal(major));
  return card;
}

function createListItem(major, searchTerm = '') {
  const item = document.createElement('div');
  item.className = 'major-list-item';
  item.dataset.code = major.code;
  item.innerHTML = `
    <div class="list-item-left">
      <div class="list-icon">${major.category_icon || '📚'}</div>
      <div>
        <h3 class="list-name">${highlightMatch(major.name, searchTerm)}</h3>
        <p class="list-code">${highlightMatch(major.code, searchTerm)}</p>
        <p class="list-category">${major.category}</p>
      </div>
    </div>
    <div class="list-item-right">
      <span class="list-salary">${(major.salary_range || t('salary_negotiable', '薪资面议')).replace('¥', '')}</span>
      <p class="list-difficulty">${major.difficulty || ''}</p>
    </div>
  `;
  item.addEventListener('click', () => openModal(major));
  return item;
}

// ====== 入口 ======
document.addEventListener('DOMContentLoaded', async () => {
  window.auth.initSupabase();
  if (initWebVitals) initWebVitals();

  const langContainer = document.getElementById('langSwitcherContainer');
  if (langContainer) {
    langContainer.appendChild(createLangSwitcher());
  }

  // 语言切换时刷新动态文本
  onLanguageChange(() => {
    if (currentLoadedCategory) {
      applyFiltersAndSort(false);
    } else if (Object.keys(categoryCounts).length) {
      const totalAll = Object.values(categoryCounts).reduce((a, b) => a + b, 0);
      document.getElementById('resultsCount').textContent = `${totalAll} ${t('major_count_unit', '个专业')} · ${t('select_category_prompt', '请选择学科门类')}`;
      renderCategoryEntries(categoryCounts);
    }
  });

  updateUserArea();

  window.addEventListener('hashchange', () => {
    if (currentLoadedCategory) {
      applyHashFilters();
    }
  });

  // Phase 1: 轻量获取门类计数
  try {
    categoryCounts = await fetchCategoryCounts();
    initSidebar(categoryCounts);
    setupListEvents();

    // 初始显示入口卡片
    const totalAll = Object.values(categoryCounts).reduce((a, b) => a + b, 0);
    document.getElementById('resultsCount').textContent = `${totalAll} ${t('major_count_unit', '个专业')} · ${t('select_category_prompt', '请选择学科门类')}`;

    // 检查 URL 参数
    const urlParams = new URLSearchParams(window.location.search);
    const hashParams = new URLSearchParams(window.location.hash.replace('#', ''));
    const hasSearch = urlParams.get('search');
    const hasCode = urlParams.get('code');
    const hashCategory = hashParams.get('category');

    if (hasCode || hasSearch) {
      // 需要全量数据（搜索或 code 跳转）
      if (hasSearch) currentFilters.search = hasSearch;
      currentFilters.category = 'all';
      syncCategoryFilterUI('all');
      await loadAllMajors();
    } else if (hashCategory && hashCategory !== 'all' && categoryCounts[hashCategory]) {
      // 通过 hash 指定了具体门类
      currentFilters.category = hashCategory;
      if (hashParams.has('difficulty')) currentFilters.difficulty = hashParams.get('difficulty');
      if (hashParams.has('salary')) currentFilters.salary = hashParams.get('salary');
      if (hashParams.has('sort')) currentSort = hashParams.get('sort');
      syncFilterUI();
      await loadCategoryMajors(hashCategory);
    } else {
      // 默认：展示入口卡片
      renderCategoryEntries(categoryCounts);
    }
  } catch (error) {
    console.error('Error initializing page:', error);
    const grid = document.getElementById('categoryEntries');
    if (grid) {
      grid.innerHTML = `<p style="text-align:center;padding:60px;color:#8B7E74;font-size:16px;">${t('load_error', '加载失败')}: ${error.message}<br><button onclick="location.reload()" style="margin-top:16px;padding:8px 24px;background:var(--primary);color:white;border:none;border-radius:12px;cursor:pointer;">${t('retry', '重试')}</button></p>`;
    }
  }

  // 弹窗事件（始终绑定）
  document.getElementById('closeModal').addEventListener('click', closeModal);
  document.getElementById('modal').addEventListener('click', (e) => {
    if (e.target === document.getElementById('modal')) closeModal();
  });

  document.querySelectorAll('.tab-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach((b) => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach((tab) => tab.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(btn.dataset.tab + 'Tab').classList.add('active');
    });
  });

  document.getElementById('preheatModal').addEventListener('click', (e) => {
    if (e.target === document.getElementById('preheatModal')) closePreheatModal();
  });
});
