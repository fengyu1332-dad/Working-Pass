// ============================================================
// 专业星图 - 管理后台：用户管理
// ============================================================

import {
  requireAdmin,
  renderAdminSidebar,
  openAdminModal,
  closeAdminModal,
  showConfirmDialog,
  renderEmptyState,
  formatDate,
  adminApi,
} from './admin-common.js';

const ROLE_OPTIONS = [
  { value: 'user', label: '普通用户' },
  { value: 'paid', label: '付费用户' },
  { value: 'admin', label: '管理员' },
];

let allUsers = [];

async function init() {
  const profile = await requireAdmin();
  if (!profile) return;
  renderAdminSidebar('users');

  document.getElementById('addUserBtn').addEventListener('click', openAddUserModal);
  await loadUsers();
  document.getElementById('userSearch').addEventListener('input', onSearch);
}

async function loadUsers() {
  try {
    allUsers = await adminApi.get('user_profiles');
    allUsers.sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0));
    renderUsers(allUsers);
  } catch (err) {
    console.error('Failed to load users:', err);
    window.auth.showToast('加载用户失败: ' + err.message, 'error');
  }
}

function renderUsers(users) {
  const tbody = document.getElementById('usersTableBody');
  if (!users.length) {
    renderEmptyState(tbody, 6, '暂无用户');
    return;
  }

  tbody.innerHTML = users
    .map(
      (u) => `
    <tr>
      <td>${u.email || '--'}</td>
      <td>${u.phone || '--'}</td>
      <td>${u.points_balance ?? 0}</td>
      <td>
        <select class="role-select" data-uid="${u.id}" style="font-size:12px;padding:3px 6px;border-radius:4px;border:1px solid #ddd;">
          ${ROLE_OPTIONS.map(r => `<option value="${r.value}" ${u.role === r.value ? 'selected' : ''}>${r.label}</option>`).join('')}
        </select>
      </td>
      <td>${formatDate(u.created_at)}</td>
      <td class="action-btns">
        <button class="btn btn-sm btn-primary adjust-btn" data-uid="${u.id}" data-name="${u.email || u.phone || '--'}" data-points="${u.points_balance || 0}">调整点数</button>
        <button class="btn btn-sm btn-danger del-user-btn" data-uid="${u.id}" data-name="${u.email || u.phone || '--'}">删除</button>
      </td>
    </tr>`
    )
    .join('');

  // Role change handlers
  tbody.querySelectorAll('.role-select').forEach((sel) => {
    sel.addEventListener('change', async () => {
      const uid = sel.dataset.uid;
      const newRole = sel.value;
      try {
        const oldRole = allUsers.find(u => u.id === uid)?.role || 'unknown';
        await adminApi.update('user_profiles', { role: newRole }, { col: 'id', val: uid });
        adminApi.logAction('update_role', 'user', uid, { old_role: oldRole, new_role: newRole });
        window.auth.showToast('角色已更新', 'success');
      } catch (err) {
        window.auth.showToast('更新失败: ' + err.message, 'error');
      }
    });
  });

  // Adjust points
  tbody.querySelectorAll('.adjust-btn').forEach((btn) => {
    btn.addEventListener('click', () =>
      openAdjustModal(btn.dataset.uid, btn.dataset.name, parseInt(btn.dataset.points))
    );
  });

  // Delete user
  tbody.querySelectorAll('.del-user-btn').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const ok = await showConfirmDialog(`确定删除用户 "<strong>${btn.dataset.name}</strong>" 吗？此操作不可恢复。`);
      if (!ok) return;
      try {
        // 1. Delete user_profiles first (FK constraints), then auth.users via Edge Function
        await adminApi.delete('user_profiles', { col: 'id', val: btn.dataset.uid });

        // 2. Delete auth.users record via Edge Function (uses service_role internally)
        try {
          const sb = window.auth.getSupabase();
          const { data: { session } } = await sb.auth.getSession();
          const jwt = session?.access_token;
          const { url: supabaseUrl, key: anonKey } = window.supabaseClient;

          if (jwt) {
            const res = await fetch(`${supabaseUrl}/functions/v1/admin-delete-user`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${jwt}`, apikey: anonKey },
              body: JSON.stringify({ user_id: btn.dataset.uid }),
            });
            const result = await res.json().catch(() => ({}));
            if (!res.ok) {
              console.warn('auth.users 删除失败（user_profiles 已删除）:', result.error || res.statusText);
            }
          }
        } catch (authErr) {
          console.warn('调用 admin-delete-user 失败（user_profiles 已删除）:', authErr.message);
        }

        window.auth.showToast('用户已删除', 'success');
        adminApi.logAction('delete_user', 'user', btn.dataset.uid, { name: btn.dataset.name });
        await loadUsers();
      } catch (err) {
        window.auth.showToast('删除失败: ' + err.message, 'error');
      }
    });
  });
}

function onSearch() {
  const q = document.getElementById('userSearch').value.trim().toLowerCase();
  const filtered = q ? allUsers.filter((u) => (u.email || '').toLowerCase().includes(q) || (u.phone || '').toLowerCase().includes(q)) : allUsers;
  renderUsers(filtered);
}

// --- 添加用户 ---
function openAddUserModal() {
  openAdminModal(
    '添加用户',
    `
    <form id="addUserForm" style="display:flex;flex-direction:column;gap:14px;">
      <div>
        <label style="font-weight:600;display:block;margin-bottom:4px;">邮箱 <span style="color:var(--error);">*</span></label>
        <input type="email" id="newUserEmail" class="form-input" placeholder="请输入邮箱地址" required style="width:100%;box-sizing:border-box;">
      </div>
      <div>
        <label style="font-weight:600;display:block;margin-bottom:4px;">密码 <span style="color:var(--error);">*</span></label>
        <input type="password" id="newUserPassword" class="form-input" placeholder="至少6位" required minlength="6" style="width:100%;box-sizing:border-box;">
      </div>
      <div>
        <label style="font-weight:600;display:block;margin-bottom:4px;">手机号</label>
        <input type="text" id="newUserPhone" class="form-input" placeholder="选填" style="width:100%;box-sizing:border-box;">
      </div>
      <div>
        <label style="font-weight:600;display:block;margin-bottom:4px;">角色</label>
        <select id="newUserRole" class="form-input" style="width:100%;box-sizing:border-box;">
          ${ROLE_OPTIONS.map(r => `<option value="${r.value}">${r.label}</option>`).join('')}
        </select>
      </div>
      <div style="display:flex;gap:12px;justify-content:flex-end;">
        <button type="button" class="btn btn-secondary" id="cancelAddUserBtn">取消</button>
        <button type="submit" class="btn btn-primary">创建</button>
      </div>
    </form>`
  );

  document.getElementById('cancelAddUserBtn').addEventListener('click', closeAdminModal);

  document.getElementById('addUserForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('newUserEmail').value.trim();
    const password = document.getElementById('newUserPassword').value;
    const phone = document.getElementById('newUserPhone').value.trim();
    const role = document.getElementById('newUserRole').value;

    const sb = window.auth.getSupabase();
    const { data: { session } } = await sb.auth.getSession();
    const jwt = session?.access_token;
    const { url: supabaseUrl, key: anonKey } = window.supabaseClient;

    let res;
    try {
      res = await fetch(`${supabaseUrl}/functions/v1/admin-create-user`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${jwt}`, apikey: anonKey },
        body: JSON.stringify({ email, password, phone, role }),
      });
    } catch (fetchErr) {
      window.auth.showToast('网络异常，请检查网络后重试', 'error');
      return;
    }

    const result = await res.json().catch(() => ({}));
    if (!res.ok || !result.success) {
      window.auth.showToast(result.error || '创建失败', 'error');
      return;
    }

    closeAdminModal();
    adminApi.logAction('create_user', 'user', result.user_id, { email, role });
    window.auth.showToast('用户创建成功', 'success');
    await loadUsers();
  });
}

// --- 调整点数 ---
function openAdjustModal(userId, name, currentPoints) {
  openAdminModal(
    '调整点数',
    `
    <div style="display:flex;flex-direction:column;gap:16px;">
      <p style="margin:0;color:var(--on-surface-variant);">用户: <strong>${name}</strong> | 当前余额: <strong>${currentPoints}</strong></p>
      <div>
        <label style="font-weight:600;display:block;margin-bottom:6px;">调整量</label>
        <input type="number" id="adjustAmount" class="form-input" placeholder="正数为增加,负数扣除" style="width:100%;box-sizing:border-box;">
      </div>
      <div>
        <label style="font-weight:600;display:block;margin-bottom:6px;">备注</label>
        <input type="text" id="adjustReason" class="form-input" placeholder="调整原因..." style="width:100%;box-sizing:border-box;">
      </div>
      <button class="btn btn-primary" id="submitAdjustBtn" style="align-self:flex-end;">确认调整</button>
    </div>`
  );

  document.getElementById('submitAdjustBtn').addEventListener('click', async () => {
    const amount = parseInt(document.getElementById('adjustAmount').value);
    if (isNaN(amount)) {
      window.auth.showToast('请输入有效的调整量', 'error');
      return;
    }

    try {
      const users = await adminApi.get('user_profiles', {
        select: 'points_balance',
        eq: { col: 'id', val: userId },
      });
      if (!users.length) {
        window.auth.showToast('用户不存在', 'error');
        return;
      }

      const newBalance = Math.max(0, users[0].points_balance + amount);
      await adminApi.update('user_profiles', { points_balance: newBalance }, { col: 'id', val: userId });

      closeAdminModal();
      adminApi.logAction('adjust_points', 'user', userId, { amount, new_balance: newBalance, reason: document.getElementById('adjustReason').value.trim() });
      window.auth.showToast(`点数已调整 (${amount >= 0 ? '+' : ''}${amount})`, 'success');
      await loadUsers();
    } catch (err) {
      window.auth.showToast('调整失败: ' + err.message, 'error');
    }
  });
}

// --- 查看记录 ---
async function openRecordsModal(userId, phone, type) {
  const title = type === 'downloads' ? `下载记录 - ${phone}` : `充值记录 - ${phone}`;
  openAdminModal(title, '<p style="text-align:center;padding:24px;color:var(--on-surface-variant);">加载中...</p>');

  try {
    if (type === 'downloads') {
      let records = await adminApi.get('download_records', {
        select: 'id,report_id,points_spent,created_at,reports(major_name)',
        eq: { col: 'user_id', val: userId },
      });
      records.sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0));
      records = records.slice(0, 100);

      openAdminModal(
        title,
        records.length === 0
          ? '<p style="text-align:center;padding:48px;color:var(--on-surface-variant);">暂无下载记录</p>'
          : `
        <table class="admin-table" style="margin-top:0;">
          <thead><tr><th>报告</th><th>消耗点数</th><th>下载时间</th></tr></thead>
          <tbody>
            ${records
              .map(
                (r) => `
              <tr>
                <td>${(r.reports && r.reports.major_name) || r.report_id}</td>
                <td>${r.points_spent}</td>
                <td>${formatDate(r.created_at)}</td>
              </tr>`
              )
              .join('')}
          </tbody>
        </table>`
      );
    } else {
      let records = await adminApi.get('orders', {
        select: 'id,package_id,amount,status,created_at,point_packages(name)',
        eq: { col: 'user_id', val: userId },
      });
      records.sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0));
      records = records.slice(0, 100);

      openAdminModal(
        title,
        records.length === 0
          ? '<p style="text-align:center;padding:48px;color:var(--on-surface-variant);">暂无充值记录</p>'
          : `
        <table class="admin-table" style="margin-top:0;">
          <thead><tr><th>套餐</th><th>金额</th><th>状态</th><th>时间</th></tr></thead>
          <tbody>
            ${records
              .map(
                (r) => `
              <tr>
                <td>${(r.point_packages && r.point_packages.name) || r.package_id}</td>
                <td>¥${r.amount}</td>
                <td>${r.status === 'paid' ? '<span class="status-badge published">已支付</span>' : '<span class="status-badge draft">未支付</span>'}</td>
                <td>${formatDate(r.created_at)}</td>
              </tr>`
              )
              .join('')}
          </tbody>
        </table>`
      );
    }
  } catch (err) {
    openAdminModal(title, `<p style="text-align:center;padding:48px;color:var(--error);">加载失败: ${err.message}</p>`);
  }
}

init();
