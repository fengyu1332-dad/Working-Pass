// ============================================================
// 专业星图 - 共享工具函数（ES Module）
// 消除 common.js / admin-majors.js / Vue 组件间的代码重复
// ============================================================

export function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

export function getJsonArray(obj, key) {
  if (!obj || !obj[key]) return [];
  try {
    const v = typeof obj[key] === 'string' ? JSON.parse(obj[key]) : obj[key];
    return Array.isArray(v) ? v : [];
  } catch {
    return [];
  }
}

export function formatXuefengComment(comment) {
  if (!comment) return '';
  let html = escapeHtml(comment);
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\n\n/g, '</p><p>');
  html = html.replace(/\n/g, '<br>');
  html = html.replace(/^- /gm, '<span style="display:inline-block;width:16px;">•</span>');
  html = html.replace(/^\d+\.\s/gm, '<span style="display:inline-block;width:24px;font-weight:bold;">$&</span>');
  html = '<p>' + html + '</p>';
  html = html.replace(/<p><\/p>/g, '');
  return html;
}

export function debounce(fn, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

export function renderErrorState(container, message, retryFn) {
  container.innerHTML = `
    <div style="text-align:center;padding:60px;">
      <div style="font-size:48px;margin-bottom:16px;">😞</div>
      <p style="color:var(--on-surface-variant);margin-bottom:24px;">${escapeHtml(message)}</p>
      ${retryFn ? '<button class="btn btn-primary" id="retryBtn">🔄 重试</button>' : ''}
    </div>`;
  if (retryFn) {
    const btn = container.querySelector('#retryBtn');
    if (btn) btn.addEventListener('click', retryFn);
  }
}

export function renderLoadingState(container, message = '加载中...') {
  container.innerHTML = `
    <div style="text-align:center;padding:60px;">
      <div style="display:inline-block;width:40px;height:40px;border:3px solid var(--outline);border-top-color:var(--primary);border-radius:50%;animation:spin 0.8s linear infinite;margin-bottom:16px;"></div>
      <p style="color:var(--on-surface-variant);font-size:14px;">${escapeHtml(message)}</p>
    </div>`;
}

// 向后兼容全局引用
if (typeof window !== 'undefined') {
  window.escapeHtml = escapeHtml;
  window.getJsonArray = getJsonArray;
  window.formatXuefengComment = formatXuefengComment;
  window.debounce = debounce;
  window.renderErrorState = renderErrorState;
  window.renderLoadingState = renderLoadingState;
}
