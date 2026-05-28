// ============================================================
// 专业星图 - 前端错误监控模块
// 捕获全局 JS 错误、Promise 拒绝和资源加载失败
// 支持错误分类、去重、节流上报
// ============================================================

(function () {
  const MAX_LOG_ENTRIES = 100;
  const STORAGE_KEY = 'starmap_error_log';
  const DEDUP_WINDOW_MS = 5000;
  const SESSION_ID = 'sess_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2, 8);

  // 错误类别
  const CATEGORY = {
    NETWORK: 'network',
    AUTH: 'auth',
    DATA: 'data',
    SCRIPT: 'script',
    RENDER: 'render',
    UNKNOWN: 'unknown',
  };

  function categorizeError(message, source) {
    const msg = (message || '').toLowerCase();
    if (msg.includes('fetch') || msg.includes('network') || msg.includes('timeout') || msg.includes('abort')) return CATEGORY.NETWORK;
    if (msg.includes('auth') || msg.includes('jwt') || msg.includes('token') || msg.includes('login') || msg.includes('unauthorized')) return CATEGORY.AUTH;
    if (msg.includes('json') || msg.includes('parse') || msg.includes('undefined') || msg.includes('null')) return CATEGORY.DATA;
    if (source && (source.includes('supabase') || source.includes('rest/v1'))) return CATEGORY.DATA;
    return CATEGORY.UNKNOWN;
  }

  function getStoredLogs() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    } catch (_) {
      return [];
    }
  }

  function persistLogs(logs) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(logs.slice(-MAX_LOG_ENTRIES)));
    } catch (_) {
      /* storage full or unavailable */
    }
  }

  // 去重：相同消息在时间窗口内不重复记录
  function isDuplicate(logs, message, windowMs) {
    if (logs.length === 0) return false;
    const last = logs[logs.length - 1];
    if (last.message !== message) return false;
    const lastTime = new Date(last.time).getTime();
    return (Date.now() - lastTime) < windowMs;
  }

  function addLog(entry) {
    var logs = getStoredLogs();
    if (isDuplicate(logs, entry.message, DEDUP_WINDOW_MS)) {
      // 更新最后一条的 count
      logs[logs.length - 1].count = (logs[logs.length - 1].count || 1) + 1;
      logs[logs.length - 1].lastTime = entry.time;
      persistLogs(logs);
      return;
    }
    logs.push(entry);
    persistLogs(logs);
  }

  // 包装 console.error 以持久化最近的错误日志
  var _origError = console.error.bind(console);
  var _reportThrottle = 0;
  console.error = function () {
    var args = Array.prototype.slice.call(arguments);
    var message = args.map(String).join(' ');
    addLog({
      type: 'console.error',
      category: categorizeError(message),
      message: message,
      time: new Date().toISOString(),
      sessionId: SESSION_ID,
      count: 1,
    });
    return _origError.apply(console, args);
  };

  // 全局 JS 运行时错误
  window.addEventListener('error', function (event) {
    // 资源加载失败
    if (event.target && (event.target.tagName === 'SCRIPT' || event.target.tagName === 'LINK' || event.target.tagName === 'IMG')) {
      addLog({
        type: 'resource_load',
        category: CATEGORY.NETWORK,
        message: 'Failed to load: ' + (event.target.src || event.target.href),
        tagName: event.target.tagName,
        time: new Date().toISOString(),
        sessionId: SESSION_ID,
        count: 1,
      });
      return;
    }

    var message = event.message || 'Unknown error';
    var source = event.filename || '';
    addLog({
      type: 'runtime_error',
      category: categorizeError(message, source),
      message: message,
      source: source,
      line: event.lineno,
      column: event.colno,
      stack: event.error ? event.error.stack : null,
      time: new Date().toISOString(),
      sessionId: SESSION_ID,
      count: 1,
    });
    return false;
  });

  // 未处理的 Promise 拒绝
  window.addEventListener('unhandledrejection', function (event) {
    var message = event.reason ? (event.reason.message || String(event.reason)) : 'Unknown rejection';
    addLog({
      type: 'unhandled_rejection',
      category: categorizeError(message),
      message: message,
      stack: event.reason && event.reason.stack ? event.reason.stack : null,
      time: new Date().toISOString(),
      sessionId: SESSION_ID,
      count: 1,
    });
  });

  // 暴露调试接口
  window.__starmap_errors = {
    getAll: getStoredLogs,
    clear: function () {
      localStorage.removeItem(STORAGE_KEY);
    },
    getStats: function () {
      var logs = getStoredLogs();
      var stats = { total: logs.length, byCategory: {}, byType: {} };
      logs.forEach(function (log) {
        var cat = log.category || 'unknown';
        stats.byCategory[cat] = (stats.byCategory[cat] || 0) + 1;
        stats.byType[log.type] = (stats.byType[log.type] || 0) + 1;
      });
      return stats;
    },
    sessionId: SESSION_ID,
  };
})();
