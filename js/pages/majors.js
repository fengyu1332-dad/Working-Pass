// ============================================================
// 专业星图 - 全部专业列表页（双模式：分类浏览 + 筛选列表）
// ============================================================

import '../supabase-client.js';
import '../auth.js';
import '../common.js';
import '../reports.js';
import '../error-report.js';
import '../web-vitals.js';

const { initWebVitals } = window.__starmap_webVitals || {};

// ---- 数据 & 状态 ----
let majorsData = [];
let currentMode = 'browse';
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
let _listInitialized = false;

// ---- 常量 ----
const CATEGORY_MAP = {
  '01': '🎓', '02': '💰', '03': '⚖️', '04': '📚',
  '05': '📖', '06': '📜', '07': '🔢', '08': '💻',
  '09': '🌾', '10': '🩺', '11': '📋', '12': '🎨',
  '13': '🎭', '14': '🔬',
};

const HOT_PICK_KEYWORDS = [
  { name: '计算机科学与技术', badge: '最热门' },
  { name: '临床医学', badge: '高薪' },
  { name: '金融学', badge: '精英' },
  { name: '法学', badge: '经典' },
];

// ---- 数据加载 ----
async function fetchMajors() {
  try {
    const { url, key } = window.supabaseClient;
    const response = await fetch(`${url}/rest/v1/majors?select=code,name,category,category_icon,salary_range,difficulty,overview,career_outlook,what_you_learn,suitable_for,xuefeng_comment,top_universities,yearly_courses,career_directions,degree,duration`, {
      headers: {
        apikey: key,
        Authorization: `Bearer ${key}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    majorsData = await response.json();

    const urlParams = new URLSearchParams(window.location.search);
    const hashParams = new URLSearchParams(window.location.hash.replace('#', ''));
    const hasUrlSearch = urlParams.get('search');
    const hasHashFilter = hashParams.toString().length > 0;

    if (hasUrlSearch || hasHashFilter) {
      if (hasUrlSearch) currentFilters.search = urlParams.get('search');
      if (hashParams.has('category')) currentFilters.category = hashParams.get('category');
      if (hashParams.has('difficulty')) currentFilters.difficulty = hashParams.get('difficulty');
      if (hashParams.has('salary')) currentFilters.salary = hashParams.get('salary');
      if (hashParams.has('search') && !hasUrlSearch) currentFilters.search = hashParams.get('search');
      if (hashParams.has('sort')) currentSort = hashParams.get('sort');
      showListView();
    } else {
      initBrowseView();
    }
  } catch (error) {
    console.error('Error fetching majors:', error);
    const grid = document.getElementById('categoryGrid');
    if (grid) {
      renderErrorState(grid, `加载失败: ${error.message}`, fetchMajors);
    }
  }
}

// ====== 模式一：分类浏览 ======
function initBrowseView() {
  currentMode = 'browse';
  document.getElementById('browseView').style.display = '';
  document.getElementById('listView').style.display = 'none';

  const totalCount = majorsData.length;
  document.getElementById('browseTotalCount').textContent = totalCount;
  document.getElementById('browseCount').textContent = totalCount;

  renderCategoryCards();
  renderHotPicks();
  setupBrowseEvents();
}

function getCategoryIcon(cat) {
  const code = cat.split(' ')[0];
  return CATEGORY_MAP[code] || '📚';
}

function renderCategoryCards() {
  const grid = document.getElementById('categoryGrid');
  const counts = {};
  majorsData.forEach((m) => {
    counts[m.category] = (counts[m.category] || 0) + 1;
  });

  const categories = Object.keys(counts).sort();
  grid.innerHTML = '';

  categories.forEach((cat) => {
    const icon = getCategoryIcon(cat);
    const card = document.createElement('div');
    card.className = 'category-card';
    card.innerHTML = `
      <span class="category-card-icon">${icon}</span>
      <h3 class="category-card-name">${cat.replace(/^\d+\s/, '')}</h3>
      <p class="category-card-code">${cat}</p>
      <span class="category-card-count">${counts[cat]} 个专业</span>
    `;
    card.addEventListener('click', () => showListView({ category: cat }));
    grid.appendChild(card);
  });
}

function renderHotPicks() {
  const grid = document.getElementById('hotPicksGrid');
  const found = [];

  HOT_PICK_KEYWORDS.forEach((kw) => {
    const match = majorsData.find((m) => m.name.includes(kw.name));
    if (match && !found.some((f) => f.code === match.code)) {
      found.push({ ...match, _badge: kw.badge });
    }
  });

  // 补足 4 个
  if (found.length < 4) {
    const existingCodes = new Set(found.map((f) => f.code));
    const remaining = majorsData.filter((m) => !existingCodes.has(m.code));
    const extras = remaining.slice(0, 4 - found.length);
    extras.forEach((m) => found.push({ ...m, _badge: '推荐' }));
  }

  grid.innerHTML = '';
  found.slice(0, 4).forEach((major) => {
    const card = document.createElement('div');
    card.className = 'hot-pick-card';
    card.innerHTML = `
      <span class="hot-pick-badge">${major._badge}</span>
      <div class="hot-pick-header">
        <div class="hot-pick-icon">${major.category_icon || '📚'}</div>
        <div class="hot-pick-info">
          <h3 class="hot-pick-name">${major.name}</h3>
          <p class="hot-pick-code">${major.code}</p>
          <p class="hot-pick-difficulty">${major.difficulty || ''}</p>
        </div>
      </div>
      <span class="hot-pick-salary">${(major.salary_range || '薪资面议').replace('¥', '')}</span>
      <p class="hot-pick-preview">${(major.overview || '').substring(0, 80)}...</p>
    `;
    card.addEventListener('click', () => openModal(major));
    grid.appendChild(card);
  });
}

function setupBrowseEvents() {
  // 搜索
  document.getElementById('browseSearchBtn').addEventListener('click', () => {
    const term = document.getElementById('browseSearchInput').value.trim();
    if (term) {
      showListView({ search: term });
    } else {
      showListView();
    }
  });

  document.getElementById('browseSearchInput').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const term = e.target.value.trim();
      showListView(term ? { search: term } : {});
    }
  });

  // 清除按钮
  const browseClear = document.getElementById('browseSearchClear');
  const browseInput = document.getElementById('browseSearchInput');
  browseInput.addEventListener('input', () => {
    browseClear.style.display = browseInput.value ? 'flex' : 'none';
  });
  browseClear.addEventListener('click', () => {
    browseInput.value = '';
    browseClear.style.display = 'none';
    browseInput.focus();
  });

  // 快速标签
  document.querySelectorAll('.quick-tag').forEach((tag) => {
    tag.addEventListener('click', () => {
      const category = tag.dataset.category;
      const search = tag.dataset.search;
      showListView({ category, search });
    });
  });

  // 查看全部按钮
  document.getElementById('viewAllMajorsBtn').addEventListener('click', () => {
    showListView();
  });
}

// ====== 模式二：筛选列表 ======
function showListView(options = {}) {
  currentMode = 'list';
  document.getElementById('browseView').style.display = 'none';
  document.getElementById('listView').style.display = '';

  // 重置筛选
  if (options.category) {
    currentFilters.category = options.category;
  } else if (!options.search) {
    currentFilters.category = 'all';
  }
  if (options.search) {
    currentFilters.search = options.search;
  } else if (!options.category) {
    currentFilters.search = '';
  }
  currentFilters.difficulty = 'all';
  currentFilters.salary = 'all';

  // 更新面包屑
  let title = '全部专业';
  if (options.category) {
    title = options.category.replace(/^\d+\s/, '');
  } else if (options.search) {
    title = `搜索: ${options.search}`;
  }
  document.getElementById('breadcrumbTitle').textContent = title;

  if (!_listInitialized) {
    initListView();
    _listInitialized = true;
  } else {
    syncFilterUI();
    applyFiltersAndSort();
  }

  // 同步搜索框
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.value = currentFilters.search || '';
    document.getElementById('searchClear').style.display = currentFilters.search ? 'flex' : 'none';
  }
}

function showBrowseView() {
  // 清除 hash
  history.replaceState(null, '', window.location.pathname + window.location.search);
  currentFilters = { category: 'all', difficulty: 'all', salary: 'all', search: '' };
  initBrowseView();
}

function initListView() {
  document.getElementById('loading').style.display = 'none';

  const categories = [...new Set(majorsData.map((m) => m.category))];
  document.getElementById('resultsCount').textContent = `${majorsData.length} 个专业`;

  const categoryFilters = document.getElementById('categoryFilters');
  categories.forEach((cat) => {
    const code = cat.split(' ')[0];
    const icon = CATEGORY_MAP[code] || '📚';
    const option = document.createElement('button');
    option.className = 'category-option';
    option.dataset.category = cat;
    option.setAttribute('role', 'radio');
    option.setAttribute('aria-checked', 'false');
    option.innerHTML = `<span class="category-icon">${icon}</span><span>${cat}</span>`;
    categoryFilters.appendChild(option);
  });

  syncFilterUI();
  applyFiltersAndSort();
  setupListEvents();
}

function setupListEvents() {
  // 面包屑返回
  document.getElementById('backToBrowse').addEventListener('click', showBrowseView);

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

  // 搜索
  const searchInput = document.getElementById('searchInput');
  const searchClear = document.getElementById('searchClear');
  searchInput.addEventListener('input', debounce((e) => {
    currentFilters.search = e.target.value;
    applyFiltersAndSort();
  }, 300));
  if (searchClear) {
    searchInput.addEventListener('input', () => {
      searchClear.style.display = searchInput.value ? 'flex' : 'none';
    });
    searchClear.addEventListener('click', () => {
      searchInput.value = '';
      searchClear.style.display = 'none';
      currentFilters.search = '';
      applyFiltersAndSort();
      searchInput.focus();
    });
  }

  // 分类筛选
  document.getElementById('categoryFilters').addEventListener('click', (e) => {
    const option = e.target.closest('.category-option');
    if (option) {
      document.querySelectorAll('#categoryFilters .category-option').forEach((o) => {
        o.classList.remove('active');
        o.setAttribute('aria-checked', 'false');
      });
      option.classList.add('active');
      option.setAttribute('aria-checked', 'true');
      currentFilters.category = option.dataset.category;
      document.getElementById('breadcrumbTitle').textContent =
        option.dataset.category === 'all' ? '全部专业' : option.dataset.category.replace(/^\d+\s/, '');
      applyFiltersAndSort();
    }
  });

  // 难度筛选
  document.getElementById('difficultyFilters').addEventListener('click', (e) => {
    if (e.target.classList.contains('difficulty-btn')) {
      document.querySelectorAll('#difficultyFilters .difficulty-btn').forEach((b) => b.classList.remove('active'));
      e.target.classList.add('active');
      currentFilters.difficulty = e.target.dataset.difficulty;
      applyFiltersAndSort();
    }
  });

  // 薪资筛选
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
      applyFiltersAndSort();
    }
  });

  // 重置
  document.getElementById('resetFilters').addEventListener('click', () => {
    currentFilters = { category: 'all', difficulty: 'all', salary: 'all', search: '' };
    document.getElementById('searchInput').value = '';
    document.getElementById('searchClear').style.display = 'none';
    document.querySelectorAll('#categoryFilters .category-option').forEach((o) => {
      o.classList.remove('active');
      o.setAttribute('aria-checked', 'false');
    });
    const allCat = document.querySelector('#categoryFilters .category-option[data-category="all"]');
    if (allCat) { allCat.classList.add('active'); allCat.setAttribute('aria-checked', 'true'); }
    document.querySelectorAll('#difficultyFilters .difficulty-btn').forEach((b) => b.classList.remove('active'));
    const allDiff = document.querySelector('#difficultyFilters .difficulty-btn[data-difficulty="all"]');
    if (allDiff) allDiff.classList.add('active');
    document.querySelectorAll('#salaryFilters .salary-option').forEach((o) => {
      o.classList.remove('active');
      o.setAttribute('aria-checked', 'false');
    });
    const allSal = document.querySelector('#salaryFilters .salary-option[data-salary="all"]');
    if (allSal) { allSal.classList.add('active'); allSal.setAttribute('aria-checked', 'true'); }
    document.getElementById('breadcrumbTitle').textContent = '全部专业';
    applyFiltersAndSort();
  });

  // 排序
  document.getElementById('sortSelect').addEventListener('change', (e) => {
    currentSort = e.target.value;
    applyFiltersAndSort();
  });

  document.getElementById('sortDirection').addEventListener('click', () => {
    currentSortDir = currentSortDir === 'asc' ? 'desc' : 'asc';
    document.getElementById('sortDirection').textContent = currentSortDir === 'asc' ? '⬆️' : '⬇️';
    applyFiltersAndSort(false);
  });

  // 视图切换
  document.querySelectorAll('.view-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.view-btn').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      currentView = btn.dataset.view;
      applyFiltersAndSort();
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
    const term = currentFilters.search.toLowerCase();
    filtered = filtered.filter(
      (m) => m.name.toLowerCase().includes(term) || m.category.toLowerCase().includes(term)
    );
  }

  if (currentFilters.category !== 'all') {
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

  document.getElementById('resultsCount').textContent = `${filtered.length} 个专业`;
  displayMajors(filtered);
  syncFiltersToHash();
}

function displayMajors(majors) {
  const grid = document.getElementById('majorsGrid');
  const list = document.getElementById('majorsList');
  const totalPages = Math.ceil(majors.length / PAGE_SIZE);
  const start = (currentPage - 1) * PAGE_SIZE;
  const pageItems = majors.slice(start, start + PAGE_SIZE);

  grid.innerHTML = '';
  list.innerHTML = '';

  if (majors.length === 0) {
    const emptyMsg = '<p style="text-align:center;padding:60px;color:#8B7E74;font-size:16px;">暂无匹配的专业</p>';
    grid.innerHTML = emptyMsg;
    list.innerHTML = emptyMsg;
  } else {
    pageItems.forEach((major) => {
      grid.appendChild(createGridCard(major));
      list.appendChild(createListItem(major));
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
    document.querySelector('#listView .main-content').appendChild(container);
  }
  if (totalPages <= 1) {
    container.innerHTML = '';
    return;
  }
  let html = `<span class="pagination-info">共 ${totalItems} 个专业，${totalPages} 页</span>`;
  html += `<button class="pagination-prev" ${currentPage === 1 ? 'disabled' : ''}>上一页</button>`;
  for (let i = 1; i <= totalPages; i++) {
    html += `<button class="pagination-btn ${i === currentPage ? 'active' : ''}" data-page="${i}">${i}</button>`;
  }
  html += `<button class="pagination-next" ${currentPage === totalPages ? 'disabled' : ''}>下一页</button>`;
  container.innerHTML = html;

  container.querySelectorAll('.pagination-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      if (btn.disabled) return;
      currentPage = parseInt(btn.dataset.page);
      applyFiltersAndSort(false);
      document.querySelector('#listView .main-content').scrollIntoView({ behavior: 'smooth' });
    });
  });

  const prevBtn = container.querySelector('.pagination-prev');
  const nextBtn = container.querySelector('.pagination-next');
  prevBtn.addEventListener('click', () => {
    if (prevBtn.disabled) return;
    currentPage--;
    applyFiltersAndSort(false);
    document.querySelector('#listView .main-content').scrollIntoView({ behavior: 'smooth' });
  });
  nextBtn.addEventListener('click', () => {
    if (nextBtn.disabled) return;
    currentPage++;
    applyFiltersAndSort(false);
    document.querySelector('#listView .main-content').scrollIntoView({ behavior: 'smooth' });
  });
}

function syncFiltersToHash() {
  if (currentMode !== 'list') return;
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
  if (currentMode !== 'list') return;
  const params = new URLSearchParams(window.location.hash.replace('#', ''));
  if (params.has('category')) currentFilters.category = params.get('category');
  if (params.has('difficulty')) currentFilters.difficulty = params.get('difficulty');
  if (params.has('salary')) currentFilters.salary = params.get('salary');
  if (params.has('search')) currentFilters.search = params.get('search');
  if (params.has('sort')) currentSort = params.get('sort');
  syncFilterUI();
}

function syncFilterUI() {
  document.querySelectorAll('#categoryFilters .category-option').forEach((o) => {
    const isActive = o.dataset.category === currentFilters.category;
    o.classList.toggle('active', isActive);
    o.setAttribute('aria-checked', isActive.toString());
  });
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

function createGridCard(major) {
  const card = document.createElement('div');
  card.className = 'major-card';
  card.dataset.code = major.code;
  card.innerHTML = `
    <div class="card-header">
      <div class="card-cat-icon">${major.category_icon || '📚'}</div>
      <div>
        <h3 class="major-name">${major.name}</h3>
        <p class="major-code">${major.code}</p>
        <p class="difficulty-stars">${major.difficulty || ''}</p>
      </div>
    </div>
    <span class="salary-tag">${(major.salary_range || '薪资面议').replace('¥', '')}</span>
    <p class="employment-desc">${(major.overview || '').substring(0, 60)}...</p>
    <button class="card-cta-link">📊 查看报告 →</button>
  `;
  card.addEventListener('click', () => openModal(major));
  card.querySelector('.card-cta-link').addEventListener('click', (e) => {
    e.stopPropagation();
    window._currentMajor = major;
    goToReports(major.code);
  });
  return card;
}

function createListItem(major) {
  const item = document.createElement('div');
  item.className = 'major-list-item';
  item.dataset.code = major.code;
  item.innerHTML = `
    <div class="list-item-left">
      <div class="list-icon">${major.category_icon || '📚'}</div>
      <div>
        <h3 class="list-name">${major.name}</h3>
        <p class="list-code">${major.code}</p>
        <p class="list-category">${major.category}</p>
      </div>
    </div>
    <div class="list-item-right">
      <span class="list-salary">${(major.salary_range || '薪资面议').replace('¥', '')}</span>
      <p class="list-difficulty">${major.difficulty || ''}</p>
      <button class="card-cta-link" style="margin-top:6px;">📊 查看报告 →</button>
    </div>
  `;
  item.addEventListener('click', () => openModal(major));
  item.querySelector('.card-cta-link').addEventListener('click', (e) => {
    e.stopPropagation();
    window._currentMajor = major;
    goToReports(major.code);
  });
  return item;
}

// ====== 入口 ======
document.addEventListener('DOMContentLoaded', () => {
  window.auth.initSupabase();
  if (initWebVitals) initWebVitals();
  updateUserArea();

  window.addEventListener('hashchange', () => {
    if (currentMode === 'list') {
      applyHashFilters();
      applyFiltersAndSort();
    }
  });

  fetchMajors();

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
