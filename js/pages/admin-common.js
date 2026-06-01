// ============================================================
// 专业星图 - 管理后台共享模块
// ============================================================

import '../supabase-client.js';
import '../auth.js';
import '../utils.js';

// --- Auth Guard ---
export async function requireAdmin() {
  const ok = await window.auth.checkAuthAndRedirect();
  if (!ok) return null;
  const isAdmin = await window.auth.isAdmin();
  if (!isAdmin) {
    window.auth.showToast('无权访问管理后台', 'error');
    window.location.href = '/user/dashboard.html';
    return null;
  }
  await initAdminJwt();
  return await window.auth.getUserProfile();
}

// --- Sidebar ---
export function renderAdminSidebar(activePage) {
  const nav = document.getElementById('adminSidebar');
  if (!nav) return;

  const items = [
    ['dashboard', '/admin/index.html', '📊 数据概览'],
    ['users', '/admin/users.html', '👥 用户管理'],
    ['reports', '/admin/reports.html', '📚 报告管理'],
    ['majors', '/admin/majors.html', '🎓 专业库管理'],
    ['packages', '/admin/packages.html', '💎 点数套餐'],
    ['orders', '/admin/orders.html', '📦 订单管理'],
  ];

  nav.innerHTML = `
    <div class="admin-sidebar">
      <div style="padding: 0 24px; margin-bottom: 24px;">
        <div style="font-size: 20px; font-weight: 700; color: var(--secondary);">专业星图</div>
        <div style="font-size: 14px; color: var(--on-surface-variant); margin-top: 4px;">管理后台</div>
      </div>
      <div class="admin-sidebar-nav">
        ${items
          .map(
            ([key, url, label]) =>
              `<a href="${url}" class="admin-nav-item${key === activePage ? ' active' : ''}">${label}</a>`
          )
          .join('')}
      </div>
      <div style="margin-top: 24px; padding: 0 24px; border-top: 1px solid var(--outline); padding-top: 24px;">
        <a href="/user/dashboard.html" class="admin-nav-item">← 返回用户端</a>
        <a href="#" id="adminLogoutBtn" class="admin-nav-item" style="color: var(--error);">退出登录</a>
      </div>
    </div>
  `;

  document.getElementById('adminLogoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    window.auth.logout();
  });
}

// --- Modal System ---
export function openAdminModal(title, bodyHTML) {
  const modal = document.getElementById('adminModal');
  if (!modal) return;
  document.getElementById('adminModalTitle').textContent = title;
  document.getElementById('adminModalBody').innerHTML = bodyHTML;
  modal.classList.add('active');
  document.getElementById('adminModalClose').focus();
}

// 关闭按钮事件
document.addEventListener('click', (e) => {
  if (e.target.id === 'adminModalClose') {
    closeAdminModal();
  }
});

export function closeAdminModal() {
  const modal = document.getElementById('adminModal');
  if (modal) modal.classList.remove('active');
}

// --- Confirm Dialog ---
export function showConfirmDialog(message) {
  return new Promise((resolve) => {
    const overlay = document.createElement('div');
    overlay.className = 'confirm-overlay';
    overlay.innerHTML = `
      <div class="confirm-dialog">
        <p style="margin:0 0 20px;font-size:15px;line-height:1.6;">${message}</p>
        <div style="display:flex;gap:12px;justify-content:flex-end;">
          <button class="btn btn-secondary" id="confirmCancelBtn">取消</button>
          <button class="btn btn-primary" id="confirmOkBtn">确认</button>
        </div>
      </div>`;
    document.body.appendChild(overlay);

    overlay.querySelector('#confirmCancelBtn').addEventListener('click', () => {
      document.body.removeChild(overlay);
      resolve(false);
    });
    overlay.querySelector('#confirmOkBtn').addEventListener('click', () => {
      document.body.removeChild(overlay);
      resolve(true);
    });
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) {
        document.body.removeChild(overlay);
        resolve(false);
      }
    });
  });
}

// --- Helpers ---
export function renderEmptyState(container, colspan, message) {
  container.innerHTML = `<tr><td colspan="${colspan}" style="text-align:center;padding:48px;color:var(--on-surface-variant);">${message}</td></tr>`;
}

export function formatDate(dateString) {
  if (!dateString) return '--';
  return new Date(dateString).toLocaleString('zh-CN', {
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit',
  });
}

// --- API Helper: 使用 anon key 直连（绕过 Supabase 客户端 JWT） ---
// 用户端页面使用原生 fetch + anon key，不会附带用户 JWT
// 管理后台如使用 Supabase 客户端则自动附带 JWT，可能被 RLS 拦截
// 统一使用此 helper 确保与用户端行为一致

async function initAdminJwt() {
  // 仅触发 session 检查，确保后续 getAuthHeaders 可用
  const sb = window.auth.getSupabase();
  await sb.auth.getSession();
}

async function getAuthHeaders() {
  const { key } = window.supabaseClient;
  const sb = window.auth.getSupabase();
  if (sb) {
    const { data: { session } } = await sb.auth.getSession();
    if (session?.access_token) {
      return {
        apikey: key,
        Authorization: `Bearer ${session.access_token}`,
        'Content-Type': 'application/json',
      };
    }
  }
  return {
    apikey: key,
    Authorization: `Bearer ${key}`,
    'Content-Type': 'application/json',
  };
}

function restUrl(table) {
  const { url } = window.supabaseClient;
  return `${url}/rest/v1/${table}`;
}

export const adminApi = {
  async get(table, { select = '*', eq = null, filters = [], order = null, limit = null } = {}) {
    let url = `${restUrl(table)}?select=${select}`;
    if (eq) url += `&${eq.col}=eq.${encodeURIComponent(eq.val)}`;
    for (const f of filters) {
      url += `&${f.col}=${f.op}.${encodeURIComponent(f.val)}`;
    }
    if (order) url += `&order=${order.col}.${order.dir || 'asc'}`;
    if (limit) url += `&limit=${limit}`;
    const res = await fetch(url, { headers: await getAuthHeaders() });
    if (!res.ok) {
      const body = await res.text().catch(() => '');
      throw new Error(`[${table}] GET ${res.status}: ${body}`);
    }
    return res.json();
  },

  async count(table, { eq = null, filters = [] } = {}) {
    let url = `${restUrl(table)}?select=*`;
    if (eq) url += `&${eq.col}=eq.${encodeURIComponent(eq.val)}`;
    for (const f of filters) {
      url += `&${f.col}=${f.op}.${encodeURIComponent(f.val)}`;
    }
    const res = await fetch(url, { headers: { ...(await getAuthHeaders()), Prefer: 'count=exact' } });
    if (!res.ok) {
      const body = await res.text().catch(() => '');
      throw new Error(`[${table}] COUNT ${res.status}: ${body}`);
    }
    const range = res.headers.get('content-range');
    if (range) {
      const parts = range.split('/');
      return parseInt(parts[parts.length - 1]) || 0;
    }
    const data = await res.json();
    return data.length;
  },

  async insert(table, payload) {
    const res = await fetch(restUrl(table), {
      method: 'POST',
      headers: { ...(await getAuthHeaders()), Prefer: 'return=representation' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ message: res.statusText }));
      throw new Error(err.message || `[${table}] INSERT ${res.status}`);
    }
    return res.json();
  },

  async update(table, payload, eq) {
    let url = `${restUrl(table)}?${eq.col}=eq.${encodeURIComponent(eq.val)}`;
    const res = await fetch(url, {
      method: 'PATCH',
      headers: { ...(await getAuthHeaders()), Prefer: 'return=representation' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ message: res.statusText }));
      throw new Error(err.message || `[${table}] UPDATE ${res.status}`);
    }
    return res.json();
  },

  async delete(table, eq) {
    let url = `${restUrl(table)}?${eq.col}=eq.${encodeURIComponent(eq.val)}`;
    const res = await fetch(url, { method: 'DELETE', headers: await getAuthHeaders() });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ message: res.statusText }));
      throw new Error(err.message || `[${table}] DELETE ${res.status}`);
    }
  },

  // 审计日志
  async logAction(action, resource, resourceId = null, detail = null) {
    const body = {
      p_action: action,
      p_resource: resource,
      p_resource_id: resourceId,
      p_detail: detail,
    };
    const res = await fetch(`${restUrl('rpc/log_admin_action')}`, {
      method: 'POST',
      headers: { ...(await getAuthHeaders()), 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!res.ok) {
      console.error('[Audit] log failed:', res.status);
    }
  },
};

// --- Global Escape key for admin modal + confirm dialog ---
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    const confirmOverlay = document.querySelector('.confirm-overlay');
    if (confirmOverlay) {
      confirmOverlay.remove();
      return;
    }
    const modal = document.getElementById('adminModal');
    if (modal && modal.classList.contains('active')) {
      closeAdminModal();
    }
  }
});
