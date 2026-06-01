// ============================================================
// 专业星图 - 管理后台：报告管理
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
import { SUPABASE_URL } from '../supabase-client.js';

const STATUS_LABELS = { published: '已发布', draft: '草稿', archived: '已归档' };
let allReports = [];
let allMajors = [];

async function init() {
  const profile = await requireAdmin();
  if (!profile) return;
  renderAdminSidebar('reports');

  document.getElementById('addReportBtn').addEventListener('click', () => openEditModal(null));
  document.getElementById('generateReportBtn').addEventListener('click', openGenerateModal);
  await loadAllData();
}

async function loadAllData() {
  try {
    const [reports, majors] = await Promise.all([
      adminApi.get('reports'),
      adminApi.get('majors'),
    ]);
    allReports = reports;
    allReports.sort((a, b) => (a.major_name || '').localeCompare(b.major_name || ''));
    allMajors = majors;
    allMajors.sort((a, b) => (a.name || '').localeCompare(b.name || ''));
    renderTable();
  } catch (err) {
    console.error('Failed to load data:', err);
    window.auth.showToast('加载数据失败: ' + err.message, 'error');
  }
}

function renderTable() {
  const tbody = document.getElementById('reportsTableBody');
  if (!allReports.length) {
    renderEmptyState(tbody, 6, '暂无报告');
    return;
  }

  tbody.innerHTML = allReports
    .map(
      (r) => `
    <tr>
      <td>${r.major_code}</td>
      <td>${r.major_name}</td>
      <td>${r.category || '--'}</td>
      <td><span class="status-badge ${r.status || 'draft'}">${STATUS_LABELS[r.status] || r.status}</span></td>
      <td>${r.download_count || 0}</td>
      <td class="action-btns">
        <button class="btn btn-sm btn-primary edit-btn" data-id="${r.id}">编辑</button>
        <button class="btn btn-sm btn-secondary preview-btn" data-id="${r.id}">预览</button>
        <button class="btn btn-sm btn-danger del-btn" data-id="${r.id}" data-name="${r.major_name}">删除</button>
      </td>
    </tr>`
    )
    .join('');

  tbody.querySelectorAll('.edit-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      const r = allReports.find((x) => x.id === btn.dataset.id);
      if (r) openEditModal(r);
    });
  });

  tbody.querySelectorAll('.preview-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      const r = allReports.find((x) => x.id === btn.dataset.id);
      if (r) previewReport(r);
    });
  });

  tbody.querySelectorAll('.del-btn').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const ok = await showConfirmDialog(`确定删除报告 "<strong>${btn.dataset.name}</strong>" 吗？此操作不可恢复。`);
      if (!ok) return;
      await deleteReport(btn.dataset.id);
    });
  });
}

// --- AI 深度分析报告生成 ---
async function generateWithAI(major) {
  const sb = window.auth.getSupabase();
  const { data: { session } } = await sb.auth.getSession();
  const jwt = session?.access_token;
  if (!jwt) throw new Error('登录已过期，请重新登录');

  const statusEl = document.getElementById('genStatus');

  statusEl.textContent = '正在调用AI分析引擎（预计60-90秒）...';

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 100000);

  try {
    const res = await fetch(`${SUPABASE_URL}/functions/v1/generate-report`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${jwt}`,
      },
      body: JSON.stringify({ major }),
      signal: controller.signal,
    });
    clearTimeout(timeoutId);

    if (!res.ok) {
      const errBody = await res.json().catch(() => ({}));
      throw new Error(errBody.error || `服务异常(${res.status})`);
    }

    const result = await res.json();
    if (!result.success) {
      throw new Error(result.error || 'AI生成失败');
    }
    return result;
  } catch (err) {
    clearTimeout(timeoutId);
    if (err.name === 'AbortError') {
      throw new Error('AI分析超时，请重试或选择其他专业');
    }
    throw err;
  }
}

// --- 从专业数据生成报告草稿 ---
async function openGenerateModal() {
  openAdminModal(
    'AI 深度分析报告生成',
    `
    <div style="display:flex;flex-direction:column;gap:16px;">
      <div>
        <label style="font-weight:600;display:block;margin-bottom:6px;">选择专业</label>
        <select id="genMajorSelect" class="form-input" style="width:100%;box-sizing:border-box;">
          <option value="">-- 请选择 --</option>
          ${allMajors
            .map((m) => `<option value="${m.id}">${m.code || ''} - ${m.name || ''} (${m.category || ''})</option>`)
            .join('')}
        </select>
      </div>
      <p style="font-size:13px;color:var(--on-surface-variant);margin:0;">
        调用 AI 分析引擎，基于专业库数据生成包含 13 个章节的深度分析报告，约 8000 字。生成耗时约 45-90 秒，请耐心等待。
      </p>
      <div id="genStatus" style="display:none;font-size:13px;color:var(--primary);"></div>
      <div style="display:flex;gap:12px;justify-content:flex-end;">
        <button type="button" class="btn btn-secondary" id="cancelGenBtn">取消</button>
        <button type="button" class="btn btn-primary" id="doGenBtn" disabled>生成报告</button>
      </div>
    </div>`
  );

  document.getElementById('cancelGenBtn').addEventListener('click', closeAdminModal);

  const selectEl = document.getElementById('genMajorSelect');
  const genBtn = document.getElementById('doGenBtn');
  selectEl.addEventListener('change', () => { genBtn.disabled = !selectEl.value; });

  genBtn.addEventListener('click', async () => {
    const majorId = selectEl.value;
    if (!majorId) return;

    genBtn.disabled = true;
    genBtn.textContent = '生成中...';
    document.getElementById('genStatus').style.display = '';
    document.getElementById('genStatus').textContent = '正在读取专业数据...';

    try {
      const majors = await adminApi.get('majors', { eq: { col: 'id', val: majorId } });
      if (!majors.length) throw new Error('专业不存在');
      const major = majors[0];

      const result = await generateWithAI(major);

      closeAdminModal();
      adminApi.logAction('generate_report', 'report', major.code || major.id, { major_name: major.name });

      // 若该专业已有报告则更新，否则新建
      const existingReport = allReports.find(r => r.major_code === (major.code || ''));
      openEditModalWithContent({
        major_code: major.code || '',
        major_name: major.name || '',
        category: major.category || '',
        preview_content: result.preview,
        full_content: result.html,
        status: 'draft',
      }, existingReport ? existingReport.id : null);
    } catch (err) {
      document.getElementById('genStatus').textContent = '生成失败: ' + err.message;
      document.getElementById('genStatus').style.color = 'var(--error)';
      genBtn.disabled = false;
      genBtn.textContent = '重试';
    }
  });
}

// --- 编辑弹窗 ---
function openEditModal(report) {
  const isNew = !report;
  openEditModalForm(isNew, {
    major_code: report ? report.major_code : '',
    major_name: report ? report.major_name : '',
    category: report ? report.category : '',
    preview_content: report ? report.preview_content || '' : '',
    full_content: report ? report.full_content || '' : '',
    status: report ? report.status : 'draft',
  }, report ? report.id : null);
}

function openEditModalWithContent(data, existingId = null) {
  openEditModalForm(existingId ? false : true, data, existingId);
}

function openEditModalForm(isNew, data, existingId) {
  openAdminModal(
    isNew ? '新增报告' : '编辑报告',
    `
    <form id="reportForm" style="display:flex;flex-direction:column;gap:14px;max-height:70vh;overflow-y:auto;padding-right:4px;">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
        <div>
          <label style="font-weight:600;display:block;margin-bottom:4px;">关联专业</label>
          <select id="reportMajorCode" class="form-input" style="width:100%;box-sizing:border-box;">
            <option value="">-- 选择专业 --</option>
            ${allMajors
              .map(
                (m) =>
                  `<option value="${m.code || ''}" data-name="${m.name || ''}" data-category="${m.category || ''}" ${data.major_code === m.code ? 'selected' : ''}>${m.code || ''} - ${m.name || ''}</option>`
              )
              .join('')}
          </select>
        </div>
        <div>
          <label style="font-weight:600;display:block;margin-bottom:4px;">状态</label>
          <select id="reportStatus" class="form-input" style="width:100%;box-sizing:border-box;">
            <option value="published" ${data.status === 'published' ? 'selected' : ''}>已发布</option>
            <option value="draft" ${data.status === 'draft' ? 'selected' : ''}>草稿</option>
            <option value="archived" ${data.status === 'archived' ? 'selected' : ''}>已归档</option>
          </select>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
        <div>
          <label style="font-weight:600;display:block;margin-bottom:4px;">专业代码</label>
          <input type="text" id="reportCode" class="form-input" value="${data.major_code || ''}" style="width:100%;box-sizing:border-box;" readonly>
        </div>
        <div>
          <label style="font-weight:600;display:block;margin-bottom:4px;">专业名称</label>
          <input type="text" id="reportName" class="form-input" value="${data.major_name || ''}" style="width:100%;box-sizing:border-box;" readonly>
        </div>
      </div>
      <div>
        <label style="font-weight:600;display:block;margin-bottom:4px;">学科门类</label>
        <input type="text" id="reportCategory" class="form-input" value="${data.category || ''}" style="width:100%;box-sizing:border-box;" readonly>
      </div>
      <div>
        <label style="font-weight:600;display:block;margin-bottom:4px;">预览/摘要内容</label>
        <textarea id="reportPreview" class="form-input" rows="4" style="width:100%;box-sizing:border-box;resize:vertical;">${data.preview_content || ''}</textarea>
      </div>
      <div>
        <label style="font-weight:600;display:block;margin-bottom:4px;">完整报告内容 (HTML)</label>
        <textarea id="reportFullContent" class="form-input" rows="12" style="width:100%;box-sizing:border-box;resize:vertical;">${data.full_content || ''}</textarea>
      </div>
      <div style="display:flex;gap:12px;justify-content:flex-end;">
        <button type="button" class="btn btn-secondary" id="cancelReportBtn">取消</button>
        <button type="submit" class="btn btn-primary" id="saveReportBtn">${isNew ? '创建' : '保存'}</button>
      </div>
    </form>`
  );

  const majorSelect = document.getElementById('reportMajorCode');
  majorSelect.addEventListener('change', () => {
    const opt = majorSelect.selectedOptions[0];
    document.getElementById('reportCode').value = opt.value;
    document.getElementById('reportName').value = opt.dataset.name || '';
    document.getElementById('reportCategory').value = opt.dataset.category || '';
  });

  document.getElementById('cancelReportBtn').addEventListener('click', closeAdminModal);

  document.getElementById('reportForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const majorCode = document.getElementById('reportCode').value.trim();
    const majorName = document.getElementById('reportName').value.trim();
    if (!majorCode || !majorName) {
      window.auth.showToast('请选择关联专业', 'error');
      return;
    }

    const payload = {
      major_code: majorCode,
      major_name: majorName,
      category: document.getElementById('reportCategory').value.trim(),
      preview_content: document.getElementById('reportPreview').value.trim(),
      full_content: document.getElementById('reportFullContent').value.trim(),
      status: document.getElementById('reportStatus').value,
    };

    try {
      if (isNew) {
        const created = await adminApi.insert('reports', payload);
        adminApi.logAction('create_report', 'report', created?.[0]?.id || majorCode, { major_name: majorName, status: payload.status });
      } else {
        await adminApi.update('reports', payload, { col: 'id', val: existingId });
        adminApi.logAction('update_report', 'report', existingId, { major_name: majorName, status: payload.status });
      }
      closeAdminModal();
      window.auth.showToast(isNew ? '报告已创建' : '报告已更新', 'success');
      await loadAllData();
    } catch (err) {
      window.auth.showToast('保存失败: ' + err.message, 'error');
    }
  });
}

// --- 预览 ---
function previewReport(report) {
  openAdminModal(
    `预览: ${report.major_name}`,
    `
    <div style="display:flex;flex-direction:column;gap:12px;">
      <div style="display:flex;gap:16px;flex-wrap:wrap;font-size:14px;color:var(--on-surface-variant);">
        <span>代码: <strong>${escapeHtml(report.major_code)}</strong></span>
        <span>门类: <strong>${escapeHtml(report.category || '--')}</strong></span>
        <span>状态: <span class="status-badge ${report.status || 'draft'}">${escapeHtml(STATUS_LABELS[report.status] || report.status)}</span></span>
        <span>解锁: <strong>${report.download_count || 0}</strong> 次</span>
      </div>
      <div class="admin-sub-section">
        <h4 style="margin:0 0 8px;">摘要内容</h4>
        <div style="white-space:pre-wrap;font-size:14px;line-height:1.8;">${escapeHtml(report.preview_content) || '(空)'}</div>
      </div>
      <div class="admin-sub-section">
        <h4 style="margin:0 0 8px;">完整内容</h4>
        <div style="font-size:14px;line-height:1.8;max-height:400px;overflow-y:auto;">${report.full_content || '(空)'}</div>
      </div>
    </div>`
  );
}

// --- 删除 ---
async function deleteReport(id) {
  try {
    await adminApi.delete('reports', { col: 'id', val: id });
    adminApi.logAction('delete_report', 'report', id);
    window.auth.showToast('报告已删除', 'success');
    await loadAllData();
  } catch (err) {
    window.auth.showToast('删除失败: ' + err.message, 'error');
  }
}

init();
