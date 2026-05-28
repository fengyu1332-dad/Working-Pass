// ============================================================
// 专业星图 - 首页入口
// ============================================================

import '../supabase-client.js';
import '../auth.js';
import '../common.js';
import '../reports.js';
import '../error-report.js';
import { ForceGraph } from '../force-graph.js';

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

async function fetchMajors() {
  try {
    console.log('Fetching majors from Supabase...');
    const { url, key } = window.supabaseClient;
    const response = await fetch(`${url}/rest/v1/majors?select=*`, {
      headers: {
        apikey: key,
        Authorization: `Bearer ${key}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    majorsData = await response.json();
    console.log('Fetched', majorsData.length, 'majors');
    initializeUI();
  } catch (error) {
    console.error('Error fetching majors:', error);
    const loading = document.getElementById('loading');
    if (loading) {
      renderErrorState(loading, `加载失败: ${error.message}`, fetchMajors);
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
    `;
    card.addEventListener('click', () => openModal(major));
    grid.appendChild(card);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  if (window.auth) window.auth.initSupabase();
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
