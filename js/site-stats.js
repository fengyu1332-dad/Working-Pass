// ============================================================
// 专业星图 - 站点统计（访问计数 + 累计停留时长）
// ============================================================

const VISIT_KEY = 'starmap_last_visit';
const SESSION_INTERVAL = 30 * 60 * 1000; // 30分钟算新访问
const HEARTBEAT_SEC = 30; // 每30秒上报一次停留时间

let lastHeartbeat = Date.now();

export async function initSiteStats() {
  const client = window.supabaseClient;
  const sb = client ? client.get() : null;
  if (!sb) return;

  const statsEl = document.getElementById('siteStats');
  if (!statsEl) return;

  // 读取当前统计并显示
  try {
    const { data, error } = await sb.rpc('get_site_stats');
    if (!error && data) {
      updateDisplay(data.visit_count || 0, data.total_seconds || 0);
    }
  } catch { /* RPC 还没部署到数据库 */ }

  // 防作弊已关闭：每次页面加载均计为新访问
  const now = Date.now();
  try {
    const { data, error } = await sb.rpc('increment_visit');
    if (!error && data !== undefined) {
      document.getElementById('siteVisitCount').textContent = formatNumber(data);
    }
  } catch { /* 忽略 */ }
  localStorage.setItem(VISIT_KEY, now.toString());

  // 心跳上报停留时间
  lastHeartbeat = now;
  const heartbeat = () => {
    const elapsed = Math.round((Date.now() - lastHeartbeat) / 1000);
    if (elapsed >= HEARTBEAT_SEC) {
      lastHeartbeat = Date.now();
      sb.rpc('add_site_time', { p_seconds: elapsed }).then(({ data, error }) => {
        if (!error && data !== undefined) {
          document.getElementById('siteTotalTime').textContent = formatTime(data);
        }
      }).catch(() => {});
    }
  };

  const heartbeatTimer = setInterval(heartbeat, HEARTBEAT_SEC * 1000);

  // 页面关闭时上报剩余时间（fetch + keepalive 在 unload 时可靠发送）
  window.addEventListener('beforeunload', () => {
    clearInterval(heartbeatTimer);
    const remaining = Math.round((Date.now() - lastHeartbeat) / 1000);
    if (remaining > 2) {
      // 用 fetch + keepalive 在 unload 时可靠发送
      fetch(`${client.url}/rest/v1/rpc/add_site_time`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'apikey': client.key,
          'Authorization': `Bearer ${client.key}`,
        },
        body: JSON.stringify({ p_seconds: remaining }),
        keepalive: true,
      }).catch(() => {});
    }
  });

  // 页面隐藏/切后台时也上报
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      const elapsed = Math.round((Date.now() - lastHeartbeat) / 1000);
      if (elapsed >= 5) {
        lastHeartbeat = Date.now();
        sb.rpc('add_site_time', { p_seconds: elapsed }).catch(() => {});
      }
    } else {
      lastHeartbeat = Date.now();
    }
  });
}

function updateDisplay(visits, seconds) {
  const visitEl = document.getElementById('siteVisitCount');
  const timeEl = document.getElementById('siteTotalTime');
  if (visitEl) visitEl.textContent = formatNumber(visits);
  if (timeEl) timeEl.textContent = formatTime(seconds);
}

function formatNumber(n) {
  if (n >= 10000) return (n / 10000).toFixed(1) + ' 万';
  return n.toLocaleString('zh-CN');
}

function formatTime(totalSec) {
  const h = Math.floor(totalSec / 3600);
  const m = Math.floor((totalSec % 3600) / 60);
  if (h >= 10000) return (h / 10000).toFixed(1) + ' 万 小时';
  if (h > 0) return h.toLocaleString('zh-CN') + ' 小时 ' + m + ' 分钟';
  return m + ' 分钟';
}
