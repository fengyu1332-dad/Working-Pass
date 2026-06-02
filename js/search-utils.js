// ============================================================
// 专业星图 - 共享搜索工具模块
// ============================================================

const RECENT_KEY = 'starmap_recent_searches';
const MAX_RECENT = 5;

/**
 * 模糊匹配分数：字符逐字匹配，query 中每个字符在 text 中按顺序出现即匹配
 * 返回匹配分数（连续匹配得分更高），不匹配返回 0
 */
export function fuzzyMatch(text, query) {
  if (!query) return 1;
  const t = text.toLowerCase();
  const q = query.toLowerCase();
  if (t.includes(q)) return 100 + q.length; // 完全子串匹配最高分
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
 * 搜索专业列表：按 name、code、category 匹配，带评分排序
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

/**
 * 高亮文本中的匹配字符，返回 HTML 字符串
 */
export function highlightMatch(text, query) {
  if (!query || !text) return escapeHtml(text);
  const t = escapeHtml(text);
  const q = escapeHtml(query);
  const regex = new RegExp(`(${q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
  return t.replace(regex, '<mark class="search-highlight">$1</mark>');
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

// ---- 最近搜索 ----

export function getRecentSearches() {
  try {
    return JSON.parse(localStorage.getItem(RECENT_KEY) || '[]');
  } catch {
    return [];
  }
}

export function addRecentSearch(term) {
  if (!term || !term.trim()) return;
  const t = term.trim();
  let list = getRecentSearches();
  list = list.filter(item => item !== t);
  list.unshift(t);
  if (list.length > MAX_RECENT) list.pop();
  try {
    localStorage.setItem(RECENT_KEY, JSON.stringify(list));
  } catch { /* quota exceeded, ignore */ }
}

export function clearRecentSearches() {
  localStorage.removeItem(RECENT_KEY);
}
