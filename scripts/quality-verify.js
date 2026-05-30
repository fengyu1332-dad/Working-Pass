// ============================================================
// 专业星图 — 全字段质量验证脚本
// 用途: 每次数据变更后运行，确保883条专业数据完整、一致、格式正确
// 用法: node scripts/quality-verify.js
// ============================================================
const https = require('https');

const SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co';
const KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4';
const H = { 'apikey': KEY, 'Authorization': 'Bearer ' + KEY };

const SAFE_STARTS = new Set(['法学','工学','理学','经济学','管理学','医学','文学','哲学','教育学','农学','历史学','艺术学','军事学','交叉学科']);

function fetchAPI(path) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, SUPABASE_URL);
    https.get(url, { headers: H }, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(body)); } catch(e) { reject(new Error(`Parse error: ${body.substring(0, 200)}`)); }
      });
    }).on('error', reject);
  });
}

const CHECKS = [];
function addCheck(name, fn) { CHECKS.push({ name, fn }); }

// ============================================================
// Check definitions
// ============================================================

// C0: Row count must match MOE reference
addCheck('总数为883', async (ctx) => {
  const moeCount = await fetchAPI('/rest/v1/moe_2026_reference?select=count');
  const moe = moeCount[0].count;
  if (ctx.majors.length !== moe) {
    return { pass: false, msg: `majors=${ctx.majors.length} != MOE=${moe}` };
  }
  return { pass: true };
});

// C1: Every major code must exist in MOE reference
addCheck('code与MOE一致', async (ctx) => {
  const missing = [];
  for (const m of ctx.majors) {
    if (!ctx.moeMap.has(m.code)) {
      missing.push(`${m.code} ${m.name}`);
    }
  }
  if (missing.length > 0) {
    return { pass: false, msg: `${missing.length}个code不在MOE中: ${missing.slice(0, 5).join(', ')}` };
  }
  return { pass: true };
});

// C2: Name must match MOE reference exactly
addCheck('name与MOE一致', (ctx) => {
  const mismatches = [];
  for (const m of ctx.majors) {
    const moe = ctx.moeMap.get(m.code);
    if (moe && m.name !== moe.name) {
      mismatches.push(`${m.code}: majors="${m.name}" != MOE="${moe.name}"`);
    }
  }
  if (mismatches.length > 0) {
    return { pass: false, msg: `${mismatches.length}个名称不一致: ${mismatches.slice(0, 5).join(', ')}` };
  }
  return { pass: true };
});

// C3: All 12 content fields are non-null
addCheck('12个内容字段完整', (ctx) => {
  const CONTENT_FIELDS = Object.keys(ctx.majors[0]).filter(k => !['id', 'code', 'name', 'category', 'created_at', 'updated_at'].includes(k));
  const incomplete = [];
  for (const m of ctx.majors) {
    for (const field of CONTENT_FIELDS) {
      if (m[field] === null || m[field] === undefined || m[field] === '') {
        incomplete.push(`${m.code} ${m.name}: ${field}为空`);
      }
    }
  }
  if (incomplete.length > 0) {
    return { pass: false, msg: `${incomplete.length}个空字段: ${incomplete.slice(0, 5).join('; ')}` };
  }
  return { pass: true, msg: `${ctx.majors.length} × ${CONTENT_FIELDS.length}字段全部非空` };
});

// C4: salary_range matches ¥Xk-Yk format
addCheck('salary_range格式', (ctx) => {
  const bad = [];
  for (const m of ctx.majors) {
    const s = m.salary_range || '';
    if (!/^¥\d+k-\d+k$/.test(s)) {
      bad.push(`${m.code} ${m.name}: "${s}"`);
    } else {
      const [lo, hi] = s.match(/\d+/g).map(Number);
      if (lo === 0 && hi === 0) bad.push(`${m.code} ${m.name}: ¥0k-0k`);
      if (lo >= hi) bad.push(`${m.code} ${m.name}: ${s} (lo>=hi)`);
    }
  }
  if (bad.length > 0) {
    return { pass: false, msg: `${bad.length}个格式异常: ${bad.slice(0, 5).join('; ')}` };
  }
  return { pass: true };
});

// C5: difficulty is ⭐ format (1-5)
addCheck('difficulty格式', (ctx) => {
  const bad = [];
  for (const m of ctx.majors) {
    const d = m.difficulty || '';
    if (!/^⭐+$/.test(d) || d.length < 1 || d.length > 5) {
      bad.push(`${m.code} ${m.name}: "${d}"`);
    }
  }
  if (bad.length > 0) {
    return { pass: false, msg: `${bad.length}个格式异常: ${bad.slice(0, 5).join('; ')}` };
  }
  return { pass: true };
});

// C6: duration is integer 4 or 5
addCheck('duration类型', (ctx) => {
  const bad = [];
  for (const m of ctx.majors) {
    const d = m.duration;
    if (typeof d !== 'number' || (d !== 4 && d !== 5)) {
      bad.push(`${m.code} ${m.name}: ${d} (${typeof d})`);
    }
  }
  if (bad.length > 0) {
    return { pass: false, msg: `${bad.length}个类型异常: ${bad.slice(0, 5).join('; ')}` };
  }
  return { pass: true };
});

// C7: yearly_courses is valid JSON with Chinese keys
addCheck('yearly_courses有效性', (ctx) => {
  const bad = [];
  const VALID_KEYS = new Set(['大一', '大二', '大三', '大四', '大五']);
  for (const m of ctx.majors) {
    let yc = m.yearly_courses;
    if (typeof yc === 'string') {
      try { yc = JSON.parse(yc); } catch { bad.push(`${m.code} ${m.name}: JSON解析失败`); continue; }
    }
    if (!yc || typeof yc !== 'object') { bad.push(`${m.code} ${m.name}: 不是对象`); continue; }
    const keys = Object.keys(yc);
    const badKeys = keys.filter(k => !VALID_KEYS.has(k));
    if (badKeys.length > 0) bad.push(`${m.code} ${m.name}: 键名异常 ${badKeys.join(',')}`);
    const totalCourses = Object.values(yc).flat().length;
    if (totalCourses < 10) bad.push(`${m.code} ${m.name}: 仅${totalCourses}门课`);
  }
  if (bad.length > 0) {
    return { pass: false, msg: `${bad.length}个异常: ${bad.slice(0, 5).join('; ')}` };
  }
  return { pass: true };
});

// C8: top_universities is valid JSON with domestic/international
addCheck('top_universities有效性', (ctx) => {
  const bad = [];
  for (const m of ctx.majors) {
    let tu = m.top_universities;
    if (typeof tu === 'string') {
      try { tu = JSON.parse(tu); } catch { bad.push(`${m.code} ${m.name}: JSON解析失败`); continue; }
    }
    if (!tu || !tu.domestic || !tu.international) {
      bad.push(`${m.code} ${m.name}: 缺少domestic/international`);
      continue;
    }
    if (!Array.isArray(tu.domestic) || tu.domestic.length < 3) bad.push(`${m.code} ${m.name}: 国内院校不足3所`);
    if (!Array.isArray(tu.international) || tu.international.length < 3) bad.push(`${m.code} ${m.name}: 国际院校不足3所`);
  }
  if (bad.length > 0) {
    return { pass: false, msg: `${bad.length}个异常: ${bad.slice(0, 5).join('; ')}` };
  }
  return { pass: true };
});

// C9: career_directions is valid JSON array
addCheck('career_directions有效性', (ctx) => {
  const bad = [];
  for (const m of ctx.majors) {
    let cd = m.career_directions;
    if (typeof cd === 'string') {
      try { cd = JSON.parse(cd); } catch { bad.push(`${m.code} ${m.name}: JSON解析失败`); continue; }
    }
    if (!Array.isArray(cd) || cd.length < 2) {
      bad.push(`${m.code} ${m.name}: 不是数组或不足2项`);
    }
  }
  if (bad.length > 0) {
    return { pass: false, msg: `${bad.length}个异常: ${bad.slice(0, 5).join('; ')}` };
  }
  return { pass: true };
});

// C10: overview starts with correct major name (张冠李戴检测)
addCheck('TEXT字段名实一致', (ctx) => {
  const TEXT_FIELDS = ['overview', 'what_you_learn', 'suitable_for', 'career_outlook', 'xuefeng_comment'];
  const allNames = ctx.allNames;
  const bad = [];
  for (const m of ctx.majors) {
    for (const field of TEXT_FIELDS) {
      const text = m[field] || '';
      if (!text) continue;
      if (text.startsWith(m.name)) continue;
      for (const other of allNames) {
        if (other === m.name || SAFE_STARTS.has(other)) continue;
        if (text.startsWith(other)) {
          bad.push(`${m.code} ${m.name}: ${field}以"${other}"开头`);
          break;
        }
      }
    }
  }
  if (bad.length > 0) {
    return { pass: false, msg: `${bad.length}个名实不符: ${bad.slice(0, 5).join('; ')}` };
  }
  return { pass: true };
});

// C11: degree ends with "学士"
addCheck('degree格式', (ctx) => {
  const bad = [];
  for (const m of ctx.majors) {
    const d = m.degree || '';
    if (!d.includes('学士')) {
      bad.push(`${m.code} ${m.name}: "${d}"`);
    }
  }
  if (bad.length > 0) {
    return { pass: false, msg: `${bad.length}个缺少"学士"后缀: ${bad.slice(0, 5).join('; ')}` };
  }
  return { pass: true };
});

// ============================================================
// Main
// ============================================================
async function main() {
  console.log('========================================');
  console.log('  专业星图 — 全字段质量验证');
  console.log('========================================\n');

  // Load data
  console.log('[1/3] 加载 MOE 参考数据...');
  const moeData = [];
  for (let off = 0; off < 2000; off += 1000) {
    const batch = await fetchAPI(`/rest/v1/moe_2026_reference?select=code,name,category_code,category_name&limit=1000&offset=${off}`);
    if (!batch.length) break;
    moeData.push(...batch);
  }
  const moeMap = new Map(moeData.map(r => [r.code, r]));

  console.log('[2/3] 加载 majors 全量数据...');
  const majors = [];
  for (let off = 0; off < 2000; off += 1000) {
    const batch = await fetchAPI(`/rest/v1/majors?select=*&limit=1000&offset=${off}`);
    if (!batch.length) break;
    majors.push(...batch);
  }

  console.log('[3/3] 执行质量检查...\n');

  const ctx = {
    majors,
    moeMap,
    allNames: new Set(majors.map(m => m.name)),
  };

  let passed = 0, failed = 0;
  const failures = [];

  for (const check of CHECKS) {
    try {
      const result = await check.fn(ctx);
      if (result.pass) {
        console.log(`  [PASS] ${check.name}${result.msg ? ' — ' + result.msg : ''}`);
        passed++;
      } else {
        console.log(`  [FAIL] ${check.name} — ${result.msg}`);
        failed++;
        failures.push(check.name);
      }
    } catch (e) {
      console.log(`  [ERR!] ${check.name} — ${e.message}`);
      failed++;
      failures.push(`${check.name} (${e.message})`);
    }
  }

  console.log(`\n========================================`);
  console.log(`  结果: ${passed} PASS, ${failed} FAIL (${CHECKS.length} 项检查)`);
  if (failures.length > 0) {
    console.log(`  失败项: ${failures.join(', ')}`);
  }
  console.log(`========================================`);

  process.exit(failed > 0 ? 1 : 0);
}

main().catch(e => { console.error('FATAL:', e); process.exit(1); });
