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
      setCachedMajors(fresh);
    }
    // 如果 UI 尚未初始化（首次加载没有缓存），初始化
    if (!forceGraph) initializeUI();
  } catch (error) {
    console.error('Error fetching majors:', error);
    // 首次加载且无缓存时，走缓存兜底
    if (!majorsData.length) {
      const stale = getCachedMajors();
      if (stale && stale.length > 0) {
        majorsData = stale;
        initializeUI();
        return;
      }
    }
    if (!majorsData.length) {
      const loading = document.getElementById('loading');
      if (loading) {
        renderErrorState(loading, `加载失败: ${error.message}`, fetchMajors);
      }
    }
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
  if (viewAllBtn) viewAllBtn.textContent = `查看全部 ${majorsData.length} 个专业 →`;

  const featuredMajors = featuredMajorCodes.map((code) => majorsData.find((m) => m.code === code)).filter(Boolean);
  displayFeaturedMajors(featuredMajors);

  // 初始化力导向关系图
  initForceGraph();
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
        <span class="featured-salary">${(major.salary_range || '薪资面议').replace('¥', '')}</span>
        <p class="featured-preview">${(major.overview || '').substring(0, 80)}...</p>
      </div>
      <div class="featured-footer">
        <button class="card-cta-link">📊 查看报告 →</button>
      </div>
    `;
    card.addEventListener('click', () => openModal(major));
    card.querySelector('.card-cta-link').addEventListener('click', (e) => {
      e.stopPropagation();
      window._currentMajor = major;
      goToReports(major.code);
    });
    grid.appendChild(card);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  if (window.auth) window.auth.initSupabase();
  if (initWebVitals) initWebVitals();
  updateUserArea();
  fetchMajors();

  const searchBtn = document.getElementById('searchBtn');
  const searchInput = document.getElementById('searchInput');
  if (searchBtn && searchInput) {
    searchBtn.addEventListener('click', () => {
      const searchTerm = searchInput.value.trim();
      if (searchTerm) {
        const matches = majorsData.filter(
          (m) =>
            m.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            m.category.toLowerCase().includes(searchTerm.toLowerCase())
        );
        if (matches.length === 1) {
          openModal(matches[0]);
        } else if (matches.length > 1) {
          window.location.href = `majors.html?search=${encodeURIComponent(searchTerm)}`;
        } else {
          window.location.href = 'majors.html';
        }
      } else {
        window.location.href = 'majors.html';
      }
    });

    searchInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') searchBtn.click();
    });

    const searchClear = document.getElementById('searchClear');
    if (searchClear) {
      searchInput.addEventListener('input', () => {
        searchClear.style.display = searchInput.value ? 'flex' : 'none';
      });
      searchClear.addEventListener('click', () => {
        searchInput.value = '';
        searchClear.style.display = 'none';
        searchInput.focus();
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
