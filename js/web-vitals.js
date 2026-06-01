// ============================================================
// 专业星图 - Web Vitals 性能监控（LCP / CLS / INP / FCP / TTFB）
// 使用 PerformanceObserver API，零依赖
// ============================================================

const METRICS_ENDPOINT = 'https://djteatwxjlnbjylynvjh.supabase.co/functions/v1/collect-vitals';
const SAMPLE_RATE = 1.0;       // 采样率

function shouldSample() {
  return Math.random() < SAMPLE_RATE;
}

function sendMetric(name, value, rating) {
  const metric = {
    name,
    value: Math.round(value * 100) / 100,
    rating,
    page: location.pathname,
    timestamp: Date.now(),
  };

  const isDev = typeof import.meta !== 'undefined' && import.meta.env?.DEV;
  const isProd = typeof import.meta !== 'undefined' && import.meta.env?.PROD;

  // 开发环境：打印到控制台
  if (isDev) {
    const emoji = rating === 'good' ? '🟢' : rating === 'needs-improvement' ? '🟡' : '🔴';
    console.debug(`[WebVitals] ${emoji} ${name}: ${metric.value} (${rating})`);
  }

  // 生产环境：发送到分析服务
  if (METRICS_ENDPOINT && isProd && shouldSample()) {
    navigator.sendBeacon(METRICS_ENDPOINT, JSON.stringify(metric));
  }

  return metric;
}

// --- Rating thresholds ---

function ratingLCP(v) {
  return v <= 2500 ? 'good' : v <= 4000 ? 'needs-improvement' : 'poor';
}
function ratingCLS(v) {
  return v <= 0.1 ? 'good' : v <= 0.25 ? 'needs-improvement' : 'poor';
}
function ratingINP(v) {
  return v <= 200 ? 'good' : v <= 500 ? 'needs-improvement' : 'poor';
}
function ratingFCP(v) {
  return v <= 1800 ? 'good' : v <= 3000 ? 'needs-improvement' : 'poor';
}
function ratingTTFB(v) {
  return v <= 800 ? 'good' : v <= 1800 ? 'needs-improvement' : 'poor';
}

// --- Observers ---

let metrics = {};

function observeLCP() {
  try {
    const po = new PerformanceObserver((list) => {
      const entries = list.getEntries();
      if (entries.length > 0) {
        const last = entries[entries.length - 1];
        metrics.LCP = sendMetric('LCP', last.startTime, ratingLCP(last.startTime));
      }
    });
    po.observe({ type: 'largest-contentful-paint', buffered: true });
  } catch (e) { /* 浏览器不支持 */ }
}

function observeCLS() {
  try {
    let clsValue = 0;
    const po = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (!entry.hadRecentInput) clsValue += entry.value;
      }
      metrics.CLS = sendMetric('CLS', clsValue, ratingCLS(clsValue));
    });
    po.observe({ type: 'layout-shift', buffered: true });
  } catch (e) { /* 浏览器不支持 */ }
}

function observeINP() {
  try {
    const po = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        metrics.INP = sendMetric('INP', entry.duration, ratingINP(entry.duration));
      }
    });
    po.observe({ type: 'first-input', buffered: true });
  } catch (e) { /* 浏览器不支持 */ }
}

function observeFCP() {
  try {
    const po = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.name === 'first-contentful-paint') {
          metrics.FCP = sendMetric('FCP', entry.startTime, ratingFCP(entry.startTime));
        }
      }
    });
    po.observe({ type: 'paint', buffered: true });
  } catch (e) { /* 浏览器不支持 */ }
}

// --- TTFB via Navigation Timing ---

function getTTFB() {
  try {
    const [entry] = performance.getEntriesByType('navigation');
    if (entry) {
      const ttfb = entry.responseStart - entry.requestStart;
      metrics.TTFB = sendMetric('TTFB', ttfb, ratingTTFB(ttfb));
    }
  } catch (e) { /* ignore */ }
}

// --- Page Load ---

function getPageLoad() {
  try {
    const [entry] = performance.getEntriesByType('navigation');
    if (entry) {
      const loadTime = entry.loadEventEnd - entry.fetchStart;
      if (loadTime > 0) {
        sendMetric('PageLoad', loadTime, loadTime <= 3000 ? 'good' : loadTime <= 6000 ? 'needs-improvement' : 'poor');
      }
    }
  } catch (e) { /* ignore */ }
}

// --- Init ---

export function initWebVitals() {
  observeLCP();
  observeCLS();
  observeINP();
  observeFCP();

  // TTFB & PageLoad — wait for load complete
  if (document.readyState === 'complete') {
    getTTFB();
    getPageLoad();
  } else {
    window.addEventListener('load', () => {
      getTTFB();
      getPageLoad();
    });
  }
}

export function getMetrics() {
  return { ...metrics };
}

// 向后兼容：挂载到全局 window
if (typeof window !== 'undefined') {
  window.__starmap_webVitals = { initWebVitals, getMetrics };
}
