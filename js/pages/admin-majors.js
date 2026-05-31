// ============================================================
// 专业星图 - 管理后台：专业库管理
// 数据库字段: code, name, category, category_icon, degree, duration,
//   difficulty, salary_range, overview, what_you_learn, suitable_for,
//   career_outlook, xuefeng_comment, yearly_courses, top_universities,
//   career_directions, status
// ============================================================

import {
  requireAdmin,
  renderAdminSidebar,
  openAdminModal,
  closeAdminModal,
  showConfirmDialog,
  renderEmptyState,
  adminApi,
} from './admin-common.js';
import '../utils.js';

let allMajors = [];
let currentPage = 1;
const PAGE_SIZE = 15;
let categoryFilter = '';
let searchQuery = '';

const DIFFICULTY_STARS = ['', '★☆☆☆☆', '★★☆☆☆', '★★★☆☆', '★★★★☆', '★★★★★'];

async function init() {
  const profile = await requireAdmin();
  if (!profile) return;
  renderAdminSidebar('majors');

  document.getElementById('addMajorBtn').addEventListener('click', () => openEditModal(null));
  document.getElementById('majorSearch').addEventListener('input', onSearch);
  document.getElementById('categoryFilterSelect').addEventListener('change', onFilterChange);
  await loadMajors();
}

async function loadMajors() {
  try {
    allMajors = await adminApi.get('majors');
    allMajors.sort((a, b) => (a.code || '').localeCompare(b.code || ''));
    populateCategoryFilter();
    renderTable();
  } catch (err) {
    console.error('Failed to load majors:', err);
    window.auth.showToast('加载专业数据失败: ' + err.message, 'error');
  }
}

function populateCategoryFilter() {
  const select = document.getElementById('categoryFilterSelect');
  if (!select) return;
  const cats = [...new Set(allMajors.map((m) => m.category).filter(Boolean))].sort();
  select.innerHTML = '<option value="">全部分类</option>' + cats.map((c) => `<option value="${c}">${c}</option>`).join('');
}

function getFilteredMajors() {
  let list = allMajors;
  if (categoryFilter) list = list.filter((m) => m.category === categoryFilter);
  if (searchQuery) {
    const q = searchQuery;
    list = list.filter(
      (m) =>
        (m.name || '').toLowerCase().includes(q) ||
        (m.code || '').toLowerCase().includes(q) ||
        (m.category || '').toLowerCase().includes(q)
    );
  }
  return list;
}

function renderTable() {
  const filtered = getFilteredMajors();
  const totalPages = Math.ceil(filtered.length / PAGE_SIZE) || 1;
  if (currentPage > totalPages) currentPage = totalPages;
  const start = (currentPage - 1) * PAGE_SIZE;
  const pageData = filtered.slice(start, start + PAGE_SIZE);

  const tbody = document.getElementById('majorsTableBody');
  if (!pageData.length) {
    renderEmptyState(tbody, 7, '暂无专业数据');
    renderPagination(0, 1);
    return;
  }

  tbody.innerHTML = pageData
    .map(
      (m) => `
    <tr>
      <td>${m.code || '--'}</td>
      <td>${m.name || '--'}</td>
      <td>${m.category || '--'}</td>
      <td>${m.degree || '--'}</td>
      <td>${m.salary_range || '--'}</td>
      <td>${m.difficulty || '--'}</td>
      <td class="action-btns">
        <button class="btn btn-sm btn-primary edit-btn" data-id="${m.id}">编辑</button>
        <button class="btn btn-sm btn-danger del-btn" data-id="${m.id}" data-name="${m.name || ''}">删除</button>
      </td>
    </tr>`
    )
    .join('');

  tbody.querySelectorAll('.edit-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      const m = allMajors.find((x) => x.id === btn.dataset.id);
      if (m) openEditModal(m);
    });
  });

  tbody.querySelectorAll('.del-btn').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const ok = await showConfirmDialog(`确定删除专业 "<strong>${btn.dataset.name}</strong>" 吗？`);
      if (!ok) return;
      await deleteMajor(btn.dataset.id);
    });
  });

  renderPagination(filtered.length, currentPage, totalPages);
}

function renderPagination(total, page, totalPages) {
  const container = document.getElementById('majorsPagination');
  if (!container) return;
  if (totalPages <= 1) { container.innerHTML = ''; return; }
  let html = '';
  for (let i = 1; i <= totalPages; i++) {
    html += `<button class="${i === page ? 'active' : ''}" data-page="${i}">${i}</button>`;
  }
  container.innerHTML = html;
  container.querySelectorAll('button').forEach((btn) => {
    btn.addEventListener('click', () => {
      currentPage = parseInt(btn.dataset.page);
      renderTable();
    });
  });
}

function onSearch() {
  searchQuery = document.getElementById('majorSearch').value.trim().toLowerCase();
  currentPage = 1;
  renderTable();
}

function onFilterChange() {
  categoryFilter = document.getElementById('categoryFilterSelect').value;
  currentPage = 1;
  renderTable();
}

function getVal(obj, key) { return obj ? (obj[key] ?? '') : ''; }

function diffStarsToNum(d) {
  if (!d) return '';
  const idx = DIFFICULTY_STARS.indexOf(d);
  return idx > 0 ? idx : '';
}

// --- 编辑弹窗 ---
function openEditModal(major) {
  const isNew = !major;

  openAdminModal(
    isNew ? '新增专业' : '编辑专业',
    `
    <form id="majorForm" style="display:flex;flex-direction:column;gap:14px;max-height:70vh;overflow-y:auto;padding-right:4px;">
      <div class="admin-sub-section">
        <h4 style="margin:0 0 10px;font-size:15px;color:var(--secondary);">基本信息</h4>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
          <div>
            <label style="font-weight:600;display:block;margin-bottom:4px;">专业代码 *</label>
            <input type="text" id="majorCode" class="form-input" value="${getVal(major, 'code')}" required style="width:100%;box-sizing:border-box;">
          </div>
          <div>
            <label style="font-weight:600;display:block;margin-bottom:4px;">专业名称 *</label>
            <input type="text" id="majorName" class="form-input" value="${getVal(major, 'name')}" required style="width:100%;box-sizing:border-box;">
          </div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-top:14px;">
          <div>
            <label style="font-weight:600;display:block;margin-bottom:4px;">学科门类</label>
            <input type="text" id="majorCategory" class="form-input" value="${getVal(major, 'category')}" style="width:100%;box-sizing:border-box;">
          </div>
          <div>
            <label style="font-weight:600;display:block;margin-bottom:4px;">分类图标(emoji)</label>
            <input type="text" id="majorIcon" class="form-input" value="${getVal(major, 'category_icon')}" placeholder="📚" style="width:100%;box-sizing:border-box;">
          </div>
          <div>
            <label style="font-weight:600;display:block;margin-bottom:4px;">状态</label>
            <select id="majorStatus" class="form-input" style="width:100%;box-sizing:border-box;">
              <option value="active" ${(!major || major.status === 'active') ? 'selected' : ''}>上架</option>
              <option value="inactive" ${(major && major.status === 'inactive') ? 'selected' : ''}>下架</option>
            </select>
          </div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-top:14px;">
          <div>
            <label style="font-weight:600;display:block;margin-bottom:4px;">学位</label>
            <input type="text" id="majorDegree" class="form-input" value="${getVal(major, 'degree')}" placeholder="如: 工学学士" style="width:100%;box-sizing:border-box;">
          </div>
          <div>
            <label style="font-weight:600;display:block;margin-bottom:4px;">学制(年)</label>
            <input type="number" id="majorDuration" class="form-input" value="${getVal(major, 'duration')}" style="width:100%;box-sizing:border-box;">
          </div>
          <div>
            <label style="font-weight:600;display:block;margin-bottom:4px;">薪资范围</label>
            <input type="text" id="majorSalary" class="form-input" value="${getVal(major, 'salary_range')}" placeholder="如: ¥8000-20000" style="width:100%;box-sizing:border-box;">
          </div>
        </div>
        <div style="margin-top:14px;">
          <label style="font-weight:600;display:block;margin-bottom:4px;">学习难度</label>
          <select id="majorDifficulty" class="form-input" style="width:100%;box-sizing:border-box;">
            <option value="">-- 不设置 --</option>
            ${DIFFICULTY_STARS.slice(1).map((s, i) => `<option value="${s}" ${major && major.difficulty === s ? 'selected' : ''}>${s} (${i + 1}星)</option>`).join('')}
          </select>
        </div>
      </div>

      <div class="admin-sub-section">
        <h4 style="margin:0 0 10px;font-size:15px;color:var(--secondary);">内容编辑</h4>
        <div>
          <label style="font-weight:600;display:block;margin-bottom:4px;">专业概况</label>
          <textarea id="majorOverview" class="form-input" rows="4" style="width:100%;box-sizing:border-box;resize:vertical;">${getVal(major, 'overview')}</textarea>
        </div>
        <div style="margin-top:14px;">
          <label style="font-weight:600;display:block;margin-bottom:4px;">学习内容 (what_you_learn)</label>
          <textarea id="majorLearn" class="form-input" rows="4" style="width:100%;box-sizing:border-box;resize:vertical;">${getVal(major, 'what_you_learn')}</textarea>
        </div>
        <div style="margin-top:14px;">
          <label style="font-weight:600;display:block;margin-bottom:4px;">适合人群 (suitable_for)</label>
          <textarea id="majorSuitable" class="form-input" rows="3" style="width:100%;box-sizing:border-box;resize:vertical;">${getVal(major, 'suitable_for')}</textarea>
        </div>
        <div style="margin-top:14px;">
          <label style="font-weight:600;display:block;margin-bottom:4px;">就业前景 (career_outlook)</label>
          <textarea id="majorOutlook" class="form-input" rows="4" style="width:100%;box-sizing:border-box;resize:vertical;">${getVal(major, 'career_outlook')}</textarea>
        </div>
        <div style="margin-top:14px;">
          <label style="font-weight:600;display:block;margin-bottom:4px;">雪峰点评 (xuefeng_comment)</label>
          <textarea id="majorXuefeng" class="form-input" rows="5" style="width:100%;box-sizing:border-box;resize:vertical;">${getVal(major, 'xuefeng_comment')}</textarea>
        </div>
      </div>

      <div class="admin-sub-section">
        <h4 style="margin:0 0 10px;font-size:15px;color:var(--secondary);">JSON 结构化数据</h4>
        <div>
          <label style="font-weight:600;display:block;margin-bottom:4px;">课程安排（JSON对象: {"大一":["课1","课2"], ...}）</label>
          <div id="coursesContainer" class="admin-sub-section" style="max-height:200px;"></div>
          <button type="button" class="btn btn-sm btn-secondary" id="addCourseRowBtn" style="margin-top:8px;">+ 添加学年</button>
        </div>
        <div style="margin-top:14px;">
          <label style="font-weight:600;display:block;margin-bottom:4px;">顶尖院校（JSON对象: {"domestic":["北大","清华"],"international":["MIT"]}）</label>
          <div id="unisContainer" class="admin-sub-section" style="max-height:200px;"></div>
          <button type="button" class="btn btn-sm btn-secondary" id="addUniRowBtn" style="margin-top:8px;">+ 添加院校</button>
        </div>
        <div style="margin-top:14px;">
          <label style="font-weight:600;display:block;margin-bottom:4px;">就业方向（JSON数组: ["方向1","方向2",...]）</label>
          <div id="careersContainer" class="admin-sub-section" style="max-height:200px;"></div>
          <button type="button" class="btn btn-sm btn-secondary" id="addCareerRowBtn" style="margin-top:8px;">+ 添加就业方向</button>
        </div>
      </div>

      <div style="display:flex;gap:12px;justify-content:flex-end;padding-top:8px;border-top:1px solid var(--outline);">
        <button type="button" class="btn btn-secondary" id="cancelMajorBtn">取消</button>
        <button type="submit" class="btn btn-primary" id="saveMajorBtn">${isNew ? '创建' : '保存'}</button>
      </div>
    </form>`
  );

  initJsonRows('coursesContainer', 'addCourseRowBtn', parseJsonMap(major, 'yearly_courses'));
  initUniRows('unisContainer', 'addUniRowBtn', parseJsonMap(major, 'top_universities'));
  initJsonRows('careersContainer', 'addCareerRowBtn', getJsonArray(major, 'career_directions'));

  document.getElementById('cancelMajorBtn').addEventListener('click', closeAdminModal);

  document.getElementById('majorForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const code = document.getElementById('majorCode').value.trim();
    const name = document.getElementById('majorName').value.trim();
    if (!code || !name) {
      window.auth.showToast('专业代码和名称为必填项', 'error');
      return;
    }

    const payload = {
      code,
      name,
      category: document.getElementById('majorCategory').value.trim(),
      category_icon: document.getElementById('majorIcon').value.trim(),
      status: document.getElementById('majorStatus').value,
      degree: document.getElementById('majorDegree').value.trim() || null,
      duration: parseInt(document.getElementById('majorDuration').value) || null,
      salary_range: document.getElementById('majorSalary').value.trim(),
      difficulty: document.getElementById('majorDifficulty').value,
      overview: document.getElementById('majorOverview').value.trim(),
      what_you_learn: document.getElementById('majorLearn').value.trim(),
      suitable_for: document.getElementById('majorSuitable').value.trim(),
      career_outlook: document.getElementById('majorOutlook').value.trim(),
      xuefeng_comment: document.getElementById('majorXuefeng').value.trim(),
      yearly_courses: collectJsonMap('coursesContainer'),
      top_universities: collectJsonMap('unisContainer'),
      career_directions: collectJsonRows('careersContainer'),
    };

    try {
      if (isNew) {
        await adminApi.insert('majors', payload);
      } else {
        await adminApi.update('majors', payload, { col: 'id', val: major.id });
      }
      closeAdminModal();
      window.auth.showToast(isNew ? '专业已创建' : '专业已更新', 'success');
      await loadMajors();
    } catch (err) {
      window.auth.showToast('保存失败: ' + err.message, 'error');
    }
  });
}

function initJsonRows(containerId, addBtnId, values) {
  const container = document.getElementById(containerId);
  container.innerHTML = (values.length ? values : [''])
    .map(
      (v, i) => `
    <div class="json-row">
      <input type="text" class="form-input" value="${window.escapeHtml(typeof v === 'string' ? v : JSON.stringify(v))}">
      <button type="button" class="btn btn-sm btn-danger json-remove-btn" data-idx="${i}">x</button>
    </div>`
    )
    .join('');
  bindRemoveButtons(container);
  document.getElementById(addBtnId).onclick = () => {
    const row = document.createElement('div');
    row.className = 'json-row';
    row.innerHTML = '<input type="text" class="form-input" value=""><button type="button" class="btn btn-sm btn-danger json-remove-btn">x</button>';
    container.appendChild(row);
    bindRemoveButtons(container);
  };
}

function collectJsonRows(containerId) {
  const container = document.getElementById(containerId);
  const values = [];
  container.querySelectorAll('.json-row input').forEach((input) => {
    const v = input.value.trim();
    if (v) values.push(v);
  });
  return values.length ? values : [];
}

// --- JSON 辅助：Map 格式 (yearly_courses, top_universities) ---
function parseJsonMap(major, key) {
  if (!major || !major[key]) return {};
  try {
    const v = typeof major[key] === 'string' ? JSON.parse(major[key]) : major[key];
    return v && typeof v === 'object' && !Array.isArray(v) ? v : {};
  } catch {
    return {};
  }
}

function initUniRows(containerId, addBtnId, map) {
  // top_universities: { "domestic": ["北大","清华"], "international": ["MIT","Stanford"] }
  const container = document.getElementById(containerId);
  const entries = Object.entries(map);
  const items = entries.length
    ? entries
    : [['domestic', []], ['international', []]];

  container.innerHTML = items
    .map(
      ([key, arr]) => `
    <div class="json-map-group" data-key="${key}" style="margin-bottom:10px;border:1px solid var(--outline);border-radius:8px;padding:10px;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
        <label style="font-weight:600;font-size:13px;min-width:50px;">键名:</label>
        <input type="text" class="form-input map-key" value="${key}" style="flex:1;">
        <button type="button" class="btn btn-sm btn-danger map-group-remove-btn">x</button>
      </div>
      <div class="map-values" style="display:flex;flex-direction:column;gap:6px;">
        ${(arr.length ? arr : ['']).map((v) => `
        <div class="json-row">
          <input type="text" class="form-input map-val" value="${(typeof v === 'string' ? v : JSON.stringify(v)).replace(/"/g, '&quot;')}">
          <button type="button" class="btn btn-sm btn-danger json-remove-btn">x</button>
        </div>`).join('')}
      </div>
      <button type="button" class="btn btn-sm btn-secondary add-map-val-btn" style="margin-top:6px;">+ 添加值</button>
    </div>`
    )
    .join('');

  bindMapRemoveButtons(container);
  bindMapAddValueButtons(container);

  document.getElementById(addBtnId).onclick = () => {
    const group = document.createElement('div');
    group.className = 'json-map-group';
    group.setAttribute('data-key', '');
    group.style.cssText = 'margin-bottom:10px;border:1px solid var(--outline);border-radius:8px;padding:10px;';
    group.innerHTML = `
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
        <label style="font-weight:600;font-size:13px;min-width:50px;">键名:</label>
        <input type="text" class="form-input map-key" value="" style="flex:1;">
        <button type="button" class="btn btn-sm btn-danger map-group-remove-btn">x</button>
      </div>
      <div class="map-values" style="display:flex;flex-direction:column;gap:6px;">
        <div class="json-row">
          <input type="text" class="form-input map-val" value="">
          <button type="button" class="btn btn-sm btn-danger json-remove-btn">x</button>
        </div>
      </div>
      <button type="button" class="btn btn-sm btn-secondary add-map-val-btn" style="margin-top:6px;">+ 添加值</button>`;
    container.appendChild(group);
    bindMapRemoveButtons(container);
    bindMapAddValueButtons(container);
  };
}

function bindMapRemoveButtons(container) {
  container.querySelectorAll('.map-group-remove-btn').forEach((btn) => {
    btn.onclick = () => btn.closest('.json-map-group').remove();
  });
  container.querySelectorAll('.json-remove-btn').forEach((btn) => {
    btn.onclick = () => {
      const rows = btn.closest('.map-values').querySelectorAll('.json-row');
      if (rows.length <= 1) {
        rows[0].querySelector('input').value = '';
        return;
      }
      btn.closest('.json-row').remove();
    };
  });
}

function bindMapAddValueButtons(container) {
  container.querySelectorAll('.add-map-val-btn').forEach((btn) => {
    btn.onclick = () => {
      const valuesDiv = btn.closest('.json-map-group').querySelector('.map-values');
      const row = document.createElement('div');
      row.className = 'json-row';
      row.innerHTML = '<input type="text" class="form-input map-val" value=""><button type="button" class="btn btn-sm btn-danger json-remove-btn">x</button>';
      row.querySelector('.json-remove-btn').onclick = () => {
        const rows = valuesDiv.querySelectorAll('.json-row');
        if (rows.length <= 1) {
          rows[0].querySelector('input').value = '';
          return;
        }
        row.remove();
      };
      valuesDiv.appendChild(row);
    };
  });
}

function collectJsonMap(containerId) {
  const container = document.getElementById(containerId);
  const map = {};
  container.querySelectorAll('.json-map-group').forEach((group) => {
    const key = group.querySelector('.map-key').value.trim();
    if (!key) return;
    const vals = [];
    group.querySelectorAll('.map-val').forEach((input) => {
      const v = input.value.trim();
      if (v) vals.push(v);
    });
    if (vals.length) map[key] = vals;
  });
  return Object.keys(map).length ? map : {};
}

// --- 通用 ---
function bindRemoveButtons(container) {
  container.querySelectorAll('.json-remove-btn').forEach((btn) => {
    btn.onclick = () => {
      const rows = container.querySelectorAll('.json-row');
      if (rows.length <= 1) {
        rows[0].querySelector('input').value = '';
        return;
      }
      btn.parentElement.remove();
    };
  });
}

// --- 删除 ---
async function deleteMajor(id) {
  try {
    await adminApi.delete('majors', { col: 'id', val: id });
    window.auth.showToast('专业已删除', 'success');
    await loadMajors();
  } catch (err) {
    window.auth.showToast('删除失败: ' + err.message, 'error');
  }
}

init();
