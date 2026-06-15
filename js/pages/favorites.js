// ============================================================
// 专业星图 - 我的收藏列表页
// ============================================================

import '../supabase-client.js';
import '../auth.js';
import '../common.js';
import { escapeHtml } from '../utils.js';
import { t } from '../i18n.js';

const CATEGORY_ICONS = {
  '01': '🎓', '02': '💰', '03': '⚖️', '04': '📚',
  '05': '📖', '06': '📜', '07': '🔢', '08': '💻',
  '09': '🌾', '10': '🩺', '12': '📋', '13': '🎭', '14': '🔬',
};

let favorites = [];
let activeCategory = 'all';

(async function () {
  window.auth.initSupabase();

  const isLoggedIn = await window.auth.checkAuthAndRedirect();
  if (!isLoggedIn) return;

  document.getElementById('logoutBtn').addEventListener('click', async (e) => {
    e.preventDefault();
    try { await window.auth.logout(); } catch (e) { /* */ }
  });

  await loadFavorites();
  renderPage();
})();

async function loadFavorites() {
  try {
    const { url, key } = window.supabaseClient;
    const user = await window.auth.getCurrentUser();
    if (!user) return;

    const res = await fetch(
      `${url}/rest/v1/user_favorites?select=major_code,created_at&user_id=eq.${user.id}&order=created_at.desc`,
      { headers: { apikey: key, Authorization: `Bearer ${key}` } },
    );
    if (!res.ok) return;
    const rows = await res.json();
    if (!rows.length) return;

    // 加载对应的专业信息
    const codes = rows.map(r => `"${r.major_code}"`).join(',');
    const majorsRes = await fetch(
      `${url}/rest/v1/majors?select=code,name,category,category_icon,salary_range,difficulty,overview&code=in.(${codes})`,
      { headers: { apikey: key, Authorization: `Bearer ${key}` } },
    );
    if (!majorsRes.ok) return;

    const majorsData = await majorsRes.json();
    const majorMap = new Map(majorsData.map(m => [m.code, m]));

    favorites = rows
      .map(r => ({ ...r, major: majorMap.get(r.major_code) }))
      .filter(r => r.major);

    // 同步到全局收藏集合
    if (window.__userFavorites) {
      window.__userFavorites = new Set(favorites.map(f => f.major_code));
    }
  } catch (e) {
    console.error('Load favorites error:', e);
  }
}

function renderPage() {
  const grid = document.getElementById('favGrid');
  const empty = document.getElementById('favEmpty');
  const countEl = document.getElementById('favCount');

  if (!favorites.length) {
    grid.innerHTML = '';
    empty.style.display = '';
    countEl.textContent = '';
    return;
  }

  empty.style.display = 'none';
  countEl.textContent = `${t('fav_count')} · ${favorites.length} ${t('major_count_unit_short', '个')}`;

  // 渲染门类筛选栏
  renderCategoryFilter();

  // 筛选
  const filtered = activeCategory === 'all'
    ? favorites
    : favorites.filter(f => (f.major?.category || '').startsWith(activeCategory));

  grid.innerHTML = filtered.map(f => {
    const m = f.major;
    const catCode = (m.category || '').split(' ')[0];
    const icon = m.category_icon || CATEGORY_ICONS[catCode] || '📚';
    return `
      <div class="fav-card" data-code="${escapeHtml(m.code)}">
        <button class="fav-remove-btn" data-code="${escapeHtml(m.code)}" title="取消收藏">✕</button>
        <div class="fav-card-header">
          <span class="fav-icon">${icon}</span>
          <div>
            <div class="fav-name">${escapeHtml(m.name)}</div>
            <div class="fav-category">${escapeHtml(m.category)} · ${escapeHtml(m.code)}</div>
          </div>
        </div>
        <div class="fav-meta">
          <span class="fav-meta-tag">${escapeHtml(m.difficulty || '')}</span>
          <span class="fav-meta-tag">${escapeHtml(m.salary_range || '')}</span>
        </div>
      </div>
    `;
  }).join('');

  // 点击卡片查看详情
  grid.querySelectorAll('.fav-card').forEach(card => {
    card.addEventListener('click', (e) => {
      if (e.target.closest('.fav-remove-btn')) return;
      const code = card.dataset.code;
      const fav = favorites.find(f => f.major_code === code);
      if (fav && fav.major && window.openModal) {
        window.openModal(fav.major);
      }
    });
  });

  // 取消收藏按钮
  grid.querySelectorAll('.fav-remove-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.stopPropagation();
      const code = btn.dataset.code;
      if (window.toggleFavorite) {
        await window.toggleFavorite(code);
        favorites = favorites.filter(f => f.major_code !== code);
        renderPage();
      }
    });
  });
}

function renderCategoryFilter() {
  const bar = document.getElementById('categoryFilterBar');
  const cats = new Map();
  favorites.forEach(f => {
    const catCode = (f.major?.category || '').split(' ')[0];
    if (catCode) cats.set(catCode, (cats.get(catCode) || 0) + 1);
  });

  if (cats.size <= 1) { bar.innerHTML = ''; return; }

  let html = `<button class="category-filter-chip${activeCategory === 'all' ? ' active' : ''}" data-cat="all">全部 (${favorites.length})</button>`;
  for (const [code, count] of cats) {
    html += `<button class="category-filter-chip${activeCategory === code ? ' active' : ''}" data-cat="${code}">${code} (${count})</button>`;
  }
  bar.innerHTML = html;

  bar.querySelectorAll('.category-filter-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      activeCategory = chip.dataset.cat;
      renderPage();
    });
  });
}
