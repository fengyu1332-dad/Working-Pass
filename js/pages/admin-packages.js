// ============================================================
// 专业星图 - 管理后台：点数套餐管理
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

let allPackages = [];

async function init() {
  const profile = await requireAdmin();
  if (!profile) return;
  renderAdminSidebar('packages');

  document.getElementById('addPackageBtn').addEventListener('click', () => openEditModal(null));
  await loadPackages();
}

async function loadPackages() {
  try {
    allPackages = await adminApi.get('point_packages');
    allPackages.sort((a, b) => (a.points || 0) - (b.points || 0));
    renderTable();
  } catch (err) {
    console.error('Failed to load packages:', err);
    window.auth.showToast('加载套餐失败: ' + err.message, 'error');
  }
}

function renderTable() {
  const tbody = document.getElementById('packagesTableBody');
  if (!allPackages.length) {
    renderEmptyState(tbody, 6, '暂无套餐');
    return;
  }

  tbody.innerHTML = allPackages
    .map(
      (p) => `
    <tr>
      <td>${p.name}</td>
      <td>${p.points}</td>
      <td>¥${p.price}</td>
      <td>${p.description || '--'}</td>
      <td>
        <label class="toggle-switch" style="vertical-align:middle;">
          <input type="checkbox" class="toggle-active" data-id="${p.id}" ${p.is_active ? 'checked' : ''}>
          <span class="toggle-slider"></span>
        </label>
      </td>
      <td class="action-btns">
        <button class="btn btn-sm btn-primary edit-btn" data-id="${p.id}">编辑</button>
        <button class="btn btn-sm btn-danger del-btn" data-id="${p.id}" data-name="${p.name}">删除</button>
      </td>
    </tr>`
    )
    .join('');

  tbody.querySelectorAll('.toggle-active').forEach((toggle) => {
    toggle.addEventListener('change', async () => {
      const isActive = toggle.checked;
      try {
        await adminApi.update('point_packages', { is_active: isActive }, { col: 'id', val: toggle.dataset.id });
        window.auth.showToast(isActive ? '已上架' : '已下架', 'success');
      } catch (err) {
        window.auth.showToast('切换失败: ' + err.message, 'error');
        toggle.checked = !isActive;
      }
    });
  });

  tbody.querySelectorAll('.edit-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      const p = allPackages.find((x) => x.id === btn.dataset.id);
      if (p) openEditModal(p);
    });
  });

  tbody.querySelectorAll('.del-btn').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const ok = await showConfirmDialog(`确定删除套餐 "<strong>${btn.dataset.name}</strong>" 吗？`);
      if (!ok) return;
      await deletePackage(btn.dataset.id);
    });
  });
}

// --- 编辑弹窗 ---
function openEditModal(pkg) {
  const isNew = !pkg;
  openAdminModal(
    isNew ? '新增套餐' : '编辑套餐',
    `
    <form id="packageForm" style="display:flex;flex-direction:column;gap:14px;">
      <div>
        <label style="font-weight:600;display:block;margin-bottom:4px;">套餐名称 *</label>
        <input type="text" id="pkgName" class="form-input" value="${pkg ? pkg.name || '' : ''}" required style="width:100%;box-sizing:border-box;">
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
        <div>
          <label style="font-weight:600;display:block;margin-bottom:4px;">点数 *</label>
          <input type="number" id="pkgPoints" class="form-input" value="${pkg ? pkg.points || '' : ''}" required min="1" style="width:100%;box-sizing:border-box;">
        </div>
        <div>
          <label style="font-weight:600;display:block;margin-bottom:4px;">价格 (元) *</label>
          <input type="number" id="pkgPrice" class="form-input" value="${pkg ? pkg.price || '' : ''}" required min="0" step="0.01" style="width:100%;box-sizing:border-box;">
        </div>
      </div>
      <div>
        <label style="font-weight:600;display:block;margin-bottom:4px;">描述</label>
        <input type="text" id="pkgDesc" class="form-input" value="${pkg ? pkg.description || '' : ''}" style="width:100%;box-sizing:border-box;">
      </div>
      <div>
        <label class="toggle-switch" style="display:inline-flex;align-items:center;gap:8px;">
          <input type="checkbox" id="pkgActive" ${!pkg || pkg.is_active ? 'checked' : ''}>
          <span class="toggle-slider"></span>
          <span style="font-weight:600;font-size:14px;">上架</span>
        </label>
      </div>
      <div style="display:flex;gap:12px;justify-content:flex-end;">
        <button type="button" class="btn btn-secondary" id="cancelPkgBtn">取消</button>
        <button type="submit" class="btn btn-primary" id="savePkgBtn">${isNew ? '创建' : '保存'}</button>
      </div>
    </form>`
  );

  document.getElementById('cancelPkgBtn').addEventListener('click', closeAdminModal);

  document.getElementById('packageForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('pkgName').value.trim();
    const points = parseInt(document.getElementById('pkgPoints').value);
    const price = parseFloat(document.getElementById('pkgPrice').value);

    if (!name || isNaN(points) || isNaN(price)) {
      window.auth.showToast('请填写所有必填字段', 'error');
      return;
    }

    const payload = {
      name,
      points,
      price,
      description: document.getElementById('pkgDesc').value.trim(),
      is_active: document.getElementById('pkgActive').checked,
    };

    try {
      if (isNew) {
        await adminApi.insert('point_packages', payload);
      } else {
        await adminApi.update('point_packages', payload, { col: 'id', val: pkg.id });
      }
      closeAdminModal();
      window.auth.showToast(isNew ? '套餐已创建' : '套餐已更新', 'success');
      await loadPackages();
    } catch (err) {
      window.auth.showToast('保存失败: ' + err.message, 'error');
    }
  });
}

// --- 删除 ---
async function deletePackage(id) {
  try {
    await adminApi.delete('point_packages', { col: 'id', val: id });
    window.auth.showToast('套餐已删除', 'success');
    await loadPackages();
  } catch (err) {
    window.auth.showToast('删除失败: ' + err.message, 'error');
  }
}

init();
