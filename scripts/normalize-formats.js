// Phase 3: Normalize formats for all 883 majors
// Standardize: difficulty → ⭐, salary_range → ¥Xk-Yk, yearly_courses keys → 大一~大四

const SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co';
const KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4';
const H = { 'apikey': KEY, 'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json' };

const KB = require('./data/knowledge-base.js');

// Normalize difficulty to ⭐ format
function normalizeDifficulty(d) {
  if (!d) return '⭐⭐⭐';
  if (d.startsWith('⭐')) return d; // Already normalized
  // ★★★★★ → ⭐⭐⭐⭐⭐
  if (d.includes('★')) {
    const count = (d.match(/★/g) || []).length;
    return '⭐'.repeat(count);
  }
  // Text → stars
  const textMap = { '极高': 5, '很高': 5, '较高': 4, '中等': 3, '一般': 3, '较低': 2, '很低': 1 };
  return '⭐'.repeat(textMap[d] || 3);
}

// Normalize salary_range to ¥Xk-Yk format
function normalizeSalary(s) {
  if (!s || s === '面议') return s || '面议';
  if (/^¥\d+k-\d+k$/.test(s)) return s; // Already correct: ¥8k-28k
  // "6000-25000元/月" → ¥6k-25k
  const matchYuan = s.match(/(\d+)-(\d+)元\/月/);
  if (matchYuan) {
    const lo = Math.round(parseInt(matchYuan[1]) / 1000);
    const hi = Math.round(parseInt(matchYuan[2]) / 1000);
    return '¥' + lo + 'k-' + hi + 'k';
  }
  // "¥4000-12000" → ¥4k-12k
  const matchPlain = s.match(/¥?(\d+)-(\d+)/);
  if (matchPlain) {
    const lo = Math.round(parseInt(matchPlain[1]) / 1000);
    const hi = Math.round(parseInt(matchPlain[2]) / 1000);
    return '¥' + lo + 'k-' + hi + 'k';
  }
  return s; // Keep as-is if unrecognized
}

// Normalize yearly_courses keys to 大一~大四
const KEY_MAP = {
  '大一': '大一', '大二': '大二', '大三': '大三', '大四': '大四', '大五': '大五',
  'year1': '大一', 'year2': '大二', 'year3': '大三', 'year4': '大四', 'year5': '大五',
};

function normalizeYearlyCourses(yc) {
  if (!yc || Object.keys(yc).length === 0) return null;
  const normalized = {};
  for (const [key, val] of Object.entries(yc)) {
    const newKey = KEY_MAP[key] || key;
    normalized[newKey] = val;
  }
  // Ensure correct year order
  const ordered = {};
  ['大一', '大二', '大三', '大四', '大五'].forEach(y => {
    if (normalized[y]) ordered[y] = normalized[y];
  });
  return Object.keys(ordered).length > 0 ? ordered : null;
}

function getDefaultCourses(code, catCode) {
  const kb = KB[catCode];
  if (kb && kb.courses) return kb.courses;
  return { '大一': ['高等数学', '专业导论', '基础课1', '基础课2'], '大二': ['专业基础1', '专业基础2', '专业基础3', '实验课1'], '大三': ['专业核心1', '专业核心2', '专业核心3', '专业方向1'], '大四': ['毕业设计/论文', '专业实习', '前沿讲座', '选修课'] };
}

async function fetchAll(table, select) {
  const all = [];
  for (let off = 0; off < 2000; off += 1000) {
    const res = await fetch(SUPABASE_URL + '/rest/v1/' + table + '?select=' + select + '&limit=1000&offset=' + off, { headers: H });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const data = await res.json();
    if (!data.length) break;
    all.push(...data);
  }
  return all;
}

async function main() {
  console.log('Fetching all majors...');
  const majors = await fetchAll('majors', 'id,code,name,difficulty,salary_range,yearly_courses');

  console.log('Total: ' + majors.length);

  let normDifficulty = 0, normSalary = 0, normCourses = 0, fillCourses = 0;
  let failed = 0;

  for (let i = 0; i < majors.length; i++) {
    const m = majors[i];
    const catCode = m.code.substring(0, 2);
    const updates = {};

    // Normalize difficulty
    const newDiff = normalizeDifficulty(m.difficulty);
    if (newDiff !== m.difficulty) {
      updates.difficulty = newDiff;
      normDifficulty++;
    }

    // Normalize salary
    const newSalary = normalizeSalary(m.salary_range);
    if (newSalary !== m.salary_range) {
      updates.salary_range = newSalary;
      normSalary++;
    }

    // Normalize yearly_courses keys
    let yc = m.yearly_courses;
    if (yc && typeof yc === 'object') {
      yc = normalizeYearlyCourses(yc);
      if (JSON.stringify(yc) !== JSON.stringify(m.yearly_courses)) {
        updates.yearly_courses = yc;
        normCourses++;
      }
    }

    // Fill missing yearly_courses
    if (!yc || (typeof yc === 'object' && Object.keys(yc).length === 0)) {
      const defCourses = getDefaultCourses(m.code, catCode);
      updates.yearly_courses = defCourses;
      fillCourses++;
    }

    if (Object.keys(updates).length > 0) {
      const res = await fetch(SUPABASE_URL + '/rest/v1/majors?id=eq.' + m.id, {
        method: 'PATCH',
        headers: { ...H, 'Prefer': 'return=minimal' },
        body: JSON.stringify(updates),
      });
      if (!res.ok) {
        const err = await res.text();
        console.log('FAIL ' + m.code + ': ' + err.substring(0, 100));
        failed++;
      }
    }

    if ((i + 1) % 100 === 0) {
      console.log('  Progress: ' + (i + 1) + '/' + majors.length + ' (diff: ' + normDifficulty + ', sal: ' + normSalary + ', courses norm: ' + normCourses + ', fill: ' + fillCourses + ')');
      await new Promise(r => setTimeout(r, 50));
    }
  }

  console.log('\n=== Phase 3 Complete ===');
  console.log('Difficulty normalized: ' + normDifficulty);
  console.log('Salary normalized: ' + normSalary);
  console.log('Course keys normalized: ' + normCourses);
  console.log('Courses filled: ' + fillCourses);
  console.log('Failed: ' + failed);
}

main().catch(e => console.error('FATAL:', e));
