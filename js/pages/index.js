// ============================================================
// 专业星图 - 首页入口
// ============================================================

import '../supabase-client.js';
import '../auth.js';
import '../common.js';
import '../reports.js';
import '../error-report.js';
import '../web-vitals.js';
import { ForceGraph } from '../force-graph.js';
import { debounce } from '../utils.js';
import { searchMajors, highlightMatch, getRecentSearches, addRecentSearch, clearRecentSearches, getSearchSuggestions, didYouMean, trackSearch } from '../search-utils.js';
import { initSiteStats } from '../site-stats.js';
import { t, createLangSwitcher, applyTranslations, onLanguageChange } from '../i18n.js';
import { startOnboarding } from '../onboarding.js';

const { initWebVitals } = window.__starmap_webVitals || {};

let majorsData = [];
let forceGraph = null;

const featuredMajorCodes = [
  '080901', '080701', '100201K',
  '081301', '080601', '050303',
  '081001', '080801', '070101',
];

const badges = [
  '🔥 老师推荐', '💰 高薪专业', '📈 热门方向',
  '🎯 前景广阔', '🌟 特色专业', '💡 新兴行业',
  '🚀 潜力无限', '💼 就业无忧', '🎓 名校首选',
];

// --- localStorage 缓存 ---
const CACHE_KEY = 'starmap_majors_cache';
const CACHE_TTL = 24 * 60 * 60 * 1000; // 24 小时

function getCachedMajors() {
  try {
    const raw = localStorage.getItem(CACHE_KEY);
    if (!raw) return null;
    const cache = JSON.parse(raw);
    if (Date.now() - cache.timestamp > CACHE_TTL) {
      localStorage.removeItem(CACHE_KEY);
      return null;
    }
    return cache.data;
  } catch {
    return null;
  }
}

function setCachedMajors(data) {
  try {
    localStorage.setItem(CACHE_KEY, JSON.stringify({ data, timestamp: Date.now() }));
  } catch { /* 存储满了则静默失败 */ }
}

const MAJORS_QUERY = 'select=code,name,category,category_icon,salary_range,difficulty,overview,career_outlook,what_you_learn,suitable_for,xuefeng_comment,top_universities,yearly_courses,career_directions,degree,duration';

async function fetchMajors(forceRefresh = false) {
  // 优先使用缓存
  if (!forceRefresh) {
    const cached = getCachedMajors();
    if (cached && cached.length > 0) {
      majorsData = cached;
      window._majorsData = majorsData;
      initializeUI();
      // 后台静默更新缓存
      fetchFreshMajors();
      return;
    }
  }

  await fetchFreshMajors();
}

async function fetchFreshMajors() {
  try {
    const { url, key } = window.supabaseClient;
    const response = await fetch(`${url}/rest/v1/majors?${MAJORS_QUERY}`, {
      headers: {
        apikey: key,
        Authorization: `Bearer ${key}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    const fresh = await response.json();
    if (fresh.length > 0) {
      majorsData = fresh;
      window._majorsData = majorsData;
      setCachedMajors(fresh);
    }
    // 如果 UI 已初始化（缓存命中后后台刷新），更新图谱数据；否则初始化
    if (forceGraph) {
      forceGraph.setData(majorsData);
      checkCodeParam();
    } else {
      initializeUI();
    }
  } catch (error) {
    console.error('Error fetching majors:', error);
    // 首次加载且无缓存时，走缓存兜底
    if (!majorsData.length) {
      const stale = getCachedMajors();
      if (stale && stale.length > 0) {
        majorsData = stale;
        window._majorsData = majorsData;
        initializeUI();
        return;
      }
    }
    if (!majorsData.length) {
      const loading = document.getElementById('loading');
      if (loading) {
        renderErrorState(loading, `${t('load_error', '加载失败')}: ${error.message}`, fetchMajors);
      }
    }
  }
}

let _codeParamChecked = false;

function checkCodeParam() {
  if (_codeParamChecked) return;
  _codeParamChecked = true;

  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get('code');
  if (!code) return;

  const major = majorsData.find((m) => m.code === code);
  if (major) {
    window._currentMajor = major;
    // 清除 URL 参数
    window.history.replaceState(null, '', window.location.pathname);
    // 延迟确保 auth 已初始化
    setTimeout(() => {
      if (window.goToReports) window.goToReports(code);
    }, 500);
  }
}

function initializeUI() {
  const loading = document.getElementById('loading');
  const featuredGrid = document.getElementById('featuredGrid');
  if (loading) loading.style.display = 'none';
  if (featuredGrid) featuredGrid.style.display = 'grid';

  const categories = [...new Set(majorsData.map((m) => m.category))];
  const totalMajors = document.getElementById('totalMajors');
  const totalCategories = document.getElementById('totalCategories');
  if (totalMajors) totalMajors.textContent = majorsData.length;
  if (totalCategories) totalCategories.textContent = categories.length;

  const viewAllBtn = document.querySelector('.view-all-btn');
  if (viewAllBtn) viewAllBtn.textContent = `${t('view_all')} ${majorsData.length} ${t('major_count_unit')} →`;

  const featuredMajors = featuredMajorCodes.map((code) => majorsData.find((m) => m.code === code)).filter(Boolean);
  displayFeaturedMajors(featuredMajors);

  // 初始化力导向关系图
  initForceGraph();

  checkCodeParam();
}

function initForceGraph() {
  const container = document.getElementById('forceGraphContainer');
  const loadingEl = document.getElementById('graphLoading');
  if (!container || !majorsData.length) return;

  if (forceGraph) forceGraph.destroy();

  forceGraph = new ForceGraph(container, {
    onMajorClick(major) {
      if (typeof window.openModal === 'function') {
        window.openModal(major);
      }
    },
    onCategoryClick(categoryName) {
      // 点击学科门类：图谱内部已处理高亮逻辑
    },
  });
  forceGraph.setData(majorsData);

  if (loadingEl) {
    loadingEl.classList.add('done');
    setTimeout(() => { loadingEl.style.display = 'none'; }, 500);
  }
}

function displayFeaturedMajors(majors) {
  const grid = document.getElementById('featuredGrid');
  if (!grid) return;
  grid.innerHTML = '';

  majors.forEach((major, index) => {
    const card = document.createElement('div');
    card.className = 'featured-card';
    card.dataset.code = major.code;
    card.innerHTML = `
      <div class="card-badge">${badges[index]}</div>
      <div class="featured-header">
        <div class="featured-icon">${major.category_icon || '📚'}</div>
        <div class="featured-info">
          <h3 class="featured-name">${major.name}</h3>
          <p class="featured-code">${major.code}</p>
          <p class="featured-difficulty">${major.difficulty || ''}</p>
        </div>
      </div>
      <div class="featured-body">
        <span class="featured-salary">${(major.salary_range || t('salary_negotiable', '薪资面议')).replace('¥', '')}</span>
        <p class="featured-preview">${(major.overview || '').substring(0, 80)}...</p>
      </div>
    `;
    card.addEventListener('click', () => openModal(major));
    grid.appendChild(card);
  });
}


function showNewUserWelcome() {
  if (sessionStorage.getItem('starmap_new_user') !== '1') return;
  sessionStorage.removeItem('starmap_new_user');

  const banner = document.createElement('div');
  banner.className = 'welcome-banner';
  banner.innerHTML = '<span>🎉 ' + t('welcome_new_user', '欢迎加入专业星图！新用户赠送3点积分，完成测评发现最适合你的专业') + '</span><a href="assessment.html" class="welcome-banner-cta">' + t('dash_go_assessment', '去测评') + ' →</a><button class="welcome-banner-close" aria-label="' + t('close', '关闭') + '">×</button>';
  document.body.prepend(banner);

  banner.querySelector('.welcome-banner-close').addEventListener('click', () => {
    banner.classList.add('welcome-banner-exit');
    setTimeout(() => banner.remove(), 300);
  });

  // Auto-dismiss after 15s
  setTimeout(() => {
    if (banner.parentNode) {
      banner.classList.add('welcome-banner-exit');
      setTimeout(() => banner.remove(), 300);
    }
  }, 15000);
}

document.addEventListener('DOMContentLoaded', () => {
  if (window.auth) window.auth.initSupabase();

  // Inject welcome banner styles
  if (!document.getElementById('welcome-banner-styles')) {
    const style = document.createElement('style');
    style.id = 'welcome-banner-styles';
    style.textContent = '.welcome-banner{position:fixed;top:0;left:0;right:0;z-index:9998;background:linear-gradient(135deg,#E67E22,#D35400);color:#fff;padding:14px 24px;display:flex;align-items:center;justify-content:center;gap:16px;font-size:15px;font-weight:500;animation:welcome-slide-in 0.5s ease;box-shadow:0 2px 16px rgba(230,126,34,0.3);}.welcome-banner-exit{animation:welcome-slide-out 0.3s ease forwards;}@keyframes welcome-slide-in{from{transform:translateY(-100%);}to{transform:translateY(0);}}@keyframes welcome-slide-out{to{transform:translateY(-100%);}}.welcome-banner-cta{display:inline-flex;align-items:center;gap:4px;padding:8px 18px;background:rgba(255,255,255,0.2);color:#fff;text-decoration:none;border-radius:10px;font-weight:600;font-size:14px;transition:background 0.2s;white-space:nowrap;}.welcome-banner-cta:hover{background:rgba(255,255,255,0.3);}.welcome-banner-close{background:none;border:none;color:rgba(255,255,255,0.7);font-size:22px;cursor:pointer;padding:0 4px;line-height:1;}.welcome-banner-close:hover{color:#fff;}@media(max-width:768px){.welcome-banner{flex-wrap:wrap;text-align:center;font-size:14px;padding:12px 16px;gap:10px;}}';
    document.head.appendChild(style);
  }
  if (initWebVitals) initWebVitals();

  // 语言切换器
  const langContainer = document.getElementById('langSwitcherContainer');
  if (langContainer) {
    langContainer.appendChild(createLangSwitcher());
  }

  // 语言切换时更新动态文本
  onLanguageChange(() => {
    const viewAllBtn = document.querySelector('.view-all-btn');
    if (viewAllBtn && majorsData.length) {
      viewAllBtn.textContent = `${t('view_all')} ${majorsData.length} ${t('major_count_unit')} →`;
    }
    // 更新推荐卡片中的薪资面议文本
    document.querySelectorAll('.featured-salary').forEach(el => {
      if (el.textContent === '薪资面议' || el.textContent === 'Negotiable') {
        el.textContent = t('salary_negotiable', '薪资面议');
      }
    });
  });

  updateUserArea();
  fetchMajors();
  initSiteStats();
  if (typeof window.initCompareBar === 'function') window.initCompareBar();

  const searchBtn = document.getElementById('searchBtn');
  const searchInput = document.getElementById('searchInput');
  const searchDropdown = document.getElementById('searchDropdown');
  const searchClear = document.getElementById('searchClear');
  let dropdownActiveIndex = -1;

  if (searchBtn && searchInput) {
    // 搜索按钮：跳转到全部专业页查看完整结果
    searchBtn.addEventListener('click', () => {
      const term = searchInput.value.trim();
      if (term) addRecentSearch(term);
      closeDropdown();
      if (term) {
        window.location.href = `majors.html?search=${encodeURIComponent(term)}`;
      } else {
        window.location.href = 'majors.html';
      }
    });

    // 输入时显示下拉建议
    searchInput.addEventListener('input', debounce(() => {
      const term = searchInput.value.trim();
      searchClear.style.display = term ? 'flex' : 'none';
      if (term) {
        renderSearchDropdown(term);
      } else {
        renderRecentSearches();
      }
    }, 250));

    // 键盘导航
    searchInput.addEventListener('keydown', (e) => {
      const items = searchDropdown.querySelectorAll('.search-dropdown-item');
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        dropdownActiveIndex = Math.min(dropdownActiveIndex + 1, items.length - 1);
        updateDropdownActive(items);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        dropdownActiveIndex = Math.max(dropdownActiveIndex - 1, 0);
        updateDropdownActive(items);
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (dropdownActiveIndex >= 0 && items.length > 0) {
          items[dropdownActiveIndex]?.click();
        } else {
          searchBtn.click();
        }
      } else if (e.key === 'Escape') {
        closeDropdown();
      }
    });

    // 聚焦时显示最近搜索
    searchInput.addEventListener('focus', () => {
      if (!searchInput.value.trim()) {
        renderRecentSearches();
      }
    });

    // 清除按钮
    if (searchClear) {
      searchClear.addEventListener('click', () => {
        searchInput.value = '';
        searchClear.style.display = 'none';
        closeDropdown();
        searchInput.focus();
      });
    }

    // 点击外部关闭下拉
    document.addEventListener('click', (e) => {
      if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target) && e.target !== searchBtn) {
        closeDropdown();
      }
    });
  }

  function closeDropdown() {
    searchDropdown.classList.remove('show');
    dropdownActiveIndex = -1;
  }

  function updateDropdownActive(items) {
    items.forEach((item, i) => {
      item.classList.toggle('active', i === dropdownActiveIndex);
      if (i === dropdownActiveIndex) item.scrollIntoView({ block: 'nearest' });
    });
  }

  function renderSearchDropdown(term) {
    const results = searchMajors(majorsData, term).slice(0, 8);
    dropdownActiveIndex = -1;
    trackSearch(term, results.length);
    if (results.length === 0) {
      const suggestions = didYouMean(majorsData, term, 3);
      const tip = suggestions.length > 0
        ? `${t('did_you_mean_prefix', '未找到')}"${term}"。${t('did_you_mean', '你是不是想找')}：<strong>${suggestions.join('、')}</strong>？`
        : t('no_results_tip', '未找到匹配的专业，试试其他关键词（支持拼音、首字母、英文缩写如 CS/AI）');
      searchDropdown.innerHTML = `<div class="search-dropdown-empty">${tip}</div>`;
    } else {
      const items = results.map((m) => {
        const icon = m.category_icon || '📚';
        const hlName = highlightMatch(m.name, term);
        const hlCode = highlightMatch(m.code || '', term);
        const salary = (m.salary_range || '').replace('¥', '');
        return `<div class="search-dropdown-item" data-code="${m.code}">
          <span class="sd-icon">${icon}</span>
          <div class="sd-info">
            <div class="sd-name">${hlName}</div>
            <div class="sd-meta">${hlCode} · ${m.category}</div>
          </div>
          <span class="sd-salary">${salary}</span>
        </div>`;
      }).join('');
      const footer = `<div class="search-dropdown-footer">
        <a href="majors.html?search=${encodeURIComponent(term)}">${t('view_all_results', '查看全部')} ${results.length} ${t('result_count_unit', '个结果')} →</a>
      </div>`;
      searchDropdown.innerHTML = items + footer;
    }
    searchDropdown.classList.add('show');

    // 点击结果项
    searchDropdown.querySelectorAll('.search-dropdown-item').forEach((itemEl) => {
      itemEl.addEventListener('click', () => {
        const code = itemEl.dataset.code;
        const major = majorsData.find(m => m.code === code);
        if (major) {
          addRecentSearch(term);
          closeDropdown();
          searchInput.value = '';
          searchClear.style.display = 'none';
          openModal(major);
        }
      });
    });
  }

  function renderRecentSearches() {
    const recent = getRecentSearches();
    if (recent.length === 0) {
      closeDropdown();
      return;
    }
    const items = recent.map((t) =>
      `<div class="search-recent-item" data-term="${t.replace(/"/g, '&quot;')}">
        <span>🕐</span><span>${t}</span>
      </div>`
    ).join('');
    const footer = `<div class="search-dropdown-footer">
      <span>${t('recent_searches', '最近搜索')}</span>
      <button id="clearRecentBtn">${t('clear_recent', '清除记录')}</button>
    </div>`;
    searchDropdown.innerHTML = items + footer;
    searchDropdown.classList.add('show');
    dropdownActiveIndex = -1;

    searchDropdown.querySelectorAll('.search-recent-item').forEach((el) => {
      el.addEventListener('click', () => {
        const term = el.dataset.term;
        searchInput.value = term;
        searchClear.style.display = 'flex';
        renderSearchDropdown(term);
      });
    });
    const clearBtn = document.getElementById('clearRecentBtn');
    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        clearRecentSearches();
        closeDropdown();
      });
    }
  }

  const closeModalBtn = document.getElementById('closeModal');
  if (closeModalBtn) closeModalBtn.addEventListener('click', closeModal);

  const modal = document.getElementById('modal');
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });
  }

  document.querySelectorAll('.tab-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach((b) => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach((tab) => tab.classList.remove('active'));
      btn.classList.add('active');
      const tabEl = document.getElementById(btn.dataset.tab + 'Tab');
      if (tabEl) tabEl.classList.add('active');
    });
  });

  const preheatModal = document.getElementById('preheatModal');
  if (preheatModal) {
    preheatModal.addEventListener('click', (e) => {
      if (e.target === preheatModal) closePreheatModal();
    });
  }
});
