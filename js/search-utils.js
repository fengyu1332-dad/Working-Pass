// ============================================================
// 专业星图 - 共享搜索工具模块 (v2: 拼音 + 别名 + 建议 + 分析)
// ============================================================

const RECENT_KEY = 'starmap_recent_searches';
const MAX_RECENT = 5;
const ANALYTICS_KEY = 'starmap_search_analytics';

// ---- 别名映射 (缩写 → 中文关键词) ----
const ALIAS_MAP = {
  'cs': '计算机科学与技术',
  'ai': '人工智能',
  'it': '计算机 软件 网络 信息',
  'ee': '电子 电气 自动化',
  'iot': '物联网',
  'vr': '虚拟现实',
  'ar': '增强现实',
  'ml': '机器学习',
  'dl': '深度学习',
  'nlp': '自然语言处理',
  'cv': '计算机视觉',
  'fintech': '金融科技 金融工程',
  'biotech': '生物技术 生物工程',
  'mba': '工商管理',
  'cpa': '会计',
  'cfa': '金融',
  'cma': '临床医学',
  'bba': '工商管理',
  'ee cs': '电子信息 计算机',
};

// ---- 拼音工具 ----

const pinyinCache = new Map();

function toPinyinFull(text) {
  if (pinyinCache.has(text)) return pinyinCache.get(text).full;
  let full = '';
  let initial = '';
  for (const c of text) {
    if (typeof window.PINYIN_MAP !== 'undefined' && window.PINYIN_MAP[c] !== undefined) {
      full += window.PINYIN_MAP[c];
      initial += window.PINYIN_MAP[c].charAt(0);
    } else {
      full += c.toLowerCase();
      initial += c.toLowerCase();
    }
  }
  pinyinCache.set(text, { full, initial });
  return full;
}

function toPinyinInitial(text) {
  if (pinyinCache.has(text)) return pinyinCache.get(text).initial;
  toPinyinFull(text); // populate cache
  return pinyinCache.get(text).initial;
}

// ---- 核心匹配 ----

/**
 * 多维度模糊匹配：中文原文 + 全拼 + 首字母 + 别名
 * 返回匹配分数，不匹配返回 0
 */
export function fuzzyMatch(text, query) {
  if (!query) return 1;
  const t = text.toLowerCase();
  const q = query.toLowerCase().trim();

  // 1) 直接中文/原文匹配（权重最高）
  const directScore = charMatch(t, q);
  if (directScore >= 100) return directScore;

  // 2) 拼音全拼匹配
  const pyFull = toPinyinFull(text);
  const pyFullScore = charMatch(pyFull, q);
  if (pyFullScore > 0) return Math.max(directScore, pyFullScore * 0.9);

  // 3) 拼音首字母匹配
  const pyInit = toPinyinInitial(text);
  const pyInitScore = charMatch(pyInit, q);
  if (pyInitScore > 0) return Math.max(directScore, pyInitScore * 0.85);

  // 4) 别名匹配
  const aliasScore = aliasMatch(text, q);
  if (aliasScore > 0) return Math.max(directScore, aliasScore * 0.8);

  return directScore;
}

/**
 * 逐字符顺序模糊匹配（原算法）
 */
function charMatch(text, query) {
  const t = text.toLowerCase();
  const q = query.toLowerCase();
  if (t.includes(q)) return 100 + q.length;
  let score = 0;
  let consecutive = 0;
  let ti = 0;
  for (let qi = 0; qi < q.length; qi++) {
    const qc = q[qi];
    let found = false;
    while (ti < t.length) {
      if (t[ti] === qc) {
        found = true;
        consecutive++;
        score += consecutive * 2;
        ti++;
        break;
      }
      consecutive = 0;
      ti++;
    }
    if (!found) return 0;
  }
  return score;
}

/**
 * 别名匹配：检查 query 是否命中别名表中的 key，然后匹配对应的中文
 */
function aliasMatch(text, query) {
  const q = query.toLowerCase();
  for (const [alias, keywords] of Object.entries(ALIAS_MAP)) {
    if (alias.includes(q) || q.includes(alias)) {
      return charMatch(text.toLowerCase(), keywords.toLowerCase());
    }
  }
  return 0;
}

// ---- 搜索入口 ----

/**
 * 搜索专业列表：name ×3 + code ×2 + category ×1
 */
export function searchMajors(majors, query) {
  if (!query || !query.trim()) return majors;
  const q = query.trim();
  const scored = [];
  for (const m of majors) {
    const nameScore = fuzzyMatch(m.name, q);
    const codeScore = fuzzyMatch(m.code || '', q);
    const catScore = fuzzyMatch(m.category || '', q);
    const total = nameScore * 3 + codeScore * 2 + catScore;
    if (total > 0) {
      scored.push({ major: m, score: total });
    }
  }
  scored.sort((a, b) => b.score - a.score);
  return scored.map(s => s.major);
}

// ---- 搜索建议 ----

/**
 * 搜索建议：返回匹配度最高的 N 个专业名称
 */
export function getSearchSuggestions(majors, query, limit = 5) {
  if (!query || !query.trim()) return getPopularSearches(majors, limit);
  const results = searchMajors(majors, query);
  return results.slice(0, limit).map(m => m.name);
}

/**
 * 热门搜索：从分析数据中提取
 */
function getPopularSearches(majors, limit) {
  const analytics = getSearchAnalytics();
  const sorted = Object.entries(analytics)
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit)
    .map(([q]) => q);
  if (sorted.length >= limit) return sorted;
  // 补齐热门专业
  const popular = ['计算机科学与技术', '临床医学', '法学', '金融学', '英语'];
  for (const name of popular) {
    if (!sorted.includes(name)) sorted.push(name);
    if (sorted.length >= limit) break;
  }
  return sorted;
}

// ---- 无结果建议 ----

/**
 * 无结果时推荐相似专业名（编辑距离启发式）
 */
export function didYouMean(majors, query, limit = 3) {
  if (!query || !query.trim()) return [];
  const q = query.trim().toLowerCase();
  const candidates = [];
  for (const m of majors) {
    const nameLow = m.name.toLowerCase();
    // 前缀匹配
    if (nameLow.startsWith(q.substring(0, 2)) || nameLow.includes(q.substring(0, 2))) {
      candidates.push(m.name);
    }
    if (candidates.length >= limit * 3) break;
  }
  // 去重 + 截取
  return [...new Set(candidates)].slice(0, limit);
}

// ---- 高亮 ----

/**
 * 高亮匹配字符（支持中文和拼音）
 */
export function highlightMatch(text, query) {
  if (!query || !text) return escapeHtml(text);
  const safe = escapeHtml(text);
  const q = escapeHtml(query);
  const regex = new RegExp(`(${q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
  return safe.replace(regex, '<mark class="search-highlight">$1</mark>');
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

// ---- 最近搜索 ----

export function getRecentSearches() {
  try { return JSON.parse(localStorage.getItem(RECENT_KEY) || '[]'); }
  catch { return []; }
}

export function addRecentSearch(term) {
  if (!term || !term.trim()) return;
  const t = term.trim();
  let list = getRecentSearches();
  list = list.filter(item => item !== t);
  list.unshift(t);
  if (list.length > MAX_RECENT) list.pop();
  try { localStorage.setItem(RECENT_KEY, JSON.stringify(list)); }
  catch { /* quota */ }
}

export function clearRecentSearches() {
  localStorage.removeItem(RECENT_KEY);
}

// ---- 搜索分析（localStorage 埋点）----

export function trackSearch(query, resultCount) {
  if (!query || !query.trim()) return;
  const q = query.trim();
  try {
    const data = JSON.parse(localStorage.getItem(ANALYTICS_KEY) || '{}');
    data[q] = (data[q] || 0) + 1;
    // 只保留最近 100 条
    const entries = Object.entries(data).sort((a, b) => b[1] - a[1]).slice(0, 100);
    const trimmed = {};
    entries.forEach(([k, v]) => { trimmed[k] = v; });
    localStorage.setItem(ANALYTICS_KEY, JSON.stringify(trimmed));
  } catch { /* quota */ }
}

export function getSearchAnalytics() {
  try { return JSON.parse(localStorage.getItem(ANALYTICS_KEY) || '{}'); }
  catch { return {}; }
}
