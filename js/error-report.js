// ============================================================
// 专业星图 - 前端错误监控模块
// 捕获全局 JS 错误、Promise 拒绝和资源加载失败
// ============================================================

(function () {
  const MAX_LOG_ENTRIES = 50;
  const STORAGE_KEY = 'starmap_error_log';

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

  function addLog(entry) {
    var logs = getStoredLogs();
    logs.push(entry);
    persistLogs(logs);
  }

  // 包装 console.error 以持久化最近的错误日志
  var _origError = console.error.bind(console);
  console.error = function () {
    var args = Array.prototype.slice.call(arguments);
    addLog({
      type: 'console.error',
      message: args.map(String).join(' '),
      time: new Date().toISOString(),
    });
    return _origError.apply(console, args);
  };

  // 全局 JS 运行时错误
  window.addEventListener('error', function (event) {
    if (event.target && (event.target.tagName === 'SCRIPT' || event.target.tagName === 'LINK')) {
      addLog({
        type: 'resource_load',
        message: 'Failed to load: ' + (event.target.src || event.target.href),
        time: new Date().toISOString(),
      });
      return;
    }

    addLog({
      type: 'runtime_error',
      message: event.message,
      source: event.filename,
      line: event.lineno,
      column: event.colno,
      stack: event.error ? event.error.stack : null,
      time: new Date().toISOString(),
    });
    return false;
  });

  // 未处理的 Promise 拒绝
  window.addEventListener('unhandledrejection', function (event) {
    addLog({
      type: 'unhandled_rejection',
      message: event.reason ? (event.reason.message || String(event.reason)) : 'Unknown rejection',
      stack: event.reason && event.reason.stack ? event.reason.stack : null,
      time: new Date().toISOString(),
    });
  });

  // 暴露调试接口（仅开发环境使用）
  window.__starmap_errors = {
    getAll: getStoredLogs,
    clear: function () {
      localStorage.removeItem(STORAGE_KEY);
    },
  };
})();
