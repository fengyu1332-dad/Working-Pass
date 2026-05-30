// Fix ALL content field name mismatches: xuefeng_comment, what_you_learn, suitable_for, career_outlook
// Dynamically loads all major names for detection, uses KB template functions for regeneration
const KB = require('./data/knowledge-base.js');
const https = require('https');

const SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co';
const KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4';
const H = { 'apikey': KEY, 'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json' };

const SAFE_STARTS = new Set(['法学','工学','理学','经济学','管理学','医学','文学','哲学','教育学','农学','历史学','艺术学','军事学','交叉学科']);

// Will be populated dynamically
let ALL_MAJOR_NAMES = new Set();
let CAT_MAP = {};  // catCode -> category name

// ============================================================
// Network helpers
// ============================================================
function fetchAPI(path) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, SUPABASE_URL);
    https.get(url, { headers: H }, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(body)); } catch(e) { reject(new Error(body)); }
      });
    }).on('error', reject);
  });
}

function patchAPI(path, data) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, SUPABASE_URL);
    const body = JSON.stringify(data);
    const options = { method: 'PATCH', headers: { ...H, 'Prefer': 'return=minimal' } };
    const req = https.request(url, options, (res) => {
      let respBody = '';
      res.on('data', chunk => respBody += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) resolve(true);
        else reject(new Error(`HTTP ${res.statusCode}: ${respBody.substring(0, 100)}`));
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// ============================================================
// Content generation functions (mirrored from generate-content.js)
// ============================================================
function generateWhatYouLearn(code, courses) {
  const courseList = [];
  Object.entries(courses).forEach(([year, list]) => {
    courseList.push(...list);
  });
  const theory = courseList.filter(c => c.match(/原理|概论|导论|基础|史|理论/)).slice(0, 4);
  const methods = courseList.filter(c => c.match(/方法|统计|分析|研究|实验|调查|测量/)).slice(0, 3);
  const applied = courseList.filter(c => !theory.includes(c) && !methods.includes(c) && !c.includes('毕业') && !c.includes('实习')).slice(0, 4);

  let result = '';
  if (theory.length > 0) result += '1）理论基础：' + theory.join('、') + '；';
  if (methods.length > 0) result += '2）分析方法：' + methods.join('、') + '；';
  if (applied.length > 0) result += '3）应用领域：' + applied.join('、') + '；';

  const competences = {
    '01': ['文本分析能力', '批判性思维', '逻辑推理', '跨文化理解'],
    '02': ['数学建模能力', '数据分析能力', '经济直觉', '政策解读能力'],
    '03': ['法律思维', '文书写作能力', '逻辑论证', '谈判与辩论能力'],
    '04': ['教学设计能力', '教育研究能力', '沟通表达能力', '心理辅导能力'],
    '05': ['文字表达与编辑能力', '跨文化交际能力', '信息采集与整合能力', '创意思维'],
    '06': ['文献研究能力', '史料分析能力', '历史思维', '文化解读能力'],
    '07': ['数学建模与计算能力', '实验设计与操作能力', '科学思维', '数据分析能力'],
    '08': ['工程设计与实践能力', '编程与算法能力', '问题分析与解决能力', '项目协作能力'],
    '09': ['实验设计与田间操作能力', '生物信息分析能力', '农业技术推广能力', '生态思维'],
    '10': ['临床思维与操作能力', '医患沟通能力', '医学文献检索能力', '循证医学思维'],
    '12': ['商业分析能力', '组织协调能力', '数据驱动决策能力', '战略思维'],
    '13': ['创意设计与审美能力', '技术工具应用能力', '项目管理能力', '艺术鉴赏力'],
    '14': ['跨学科整合能力', '系统工程思维', '前沿技术学习能力', '创新研发能力'],
  };
  const catCode = code.substring(0, 2);
  const comps = competences[catCode] || ['专业实践能力', '综合分析能力', '创新思维', '团队协作能力'];
  result += '核心能力：' + comps.join('、') + '。';
  return result;
}

// ============================================================
// Detection: check if a field starts with wrong major name
// ============================================================
function hasWrongStart(text, ownName) {
  if (!text) return false;
  if (text.startsWith(ownName)) return false;

  for (const otherName of ALL_MAJOR_NAMES) {
    if (otherName === ownName) continue;
    if (SAFE_STARTS.has(otherName)) continue;
    if (text.startsWith(otherName)) return true;
  }
  return false;
}

// ============================================================
// Regenerate content for a single field
// ============================================================
function regenerateField(major, field) {
  const catCode = major.code.substring(0, 2);
  const kb = KB[catCode];
  if (!kb) return null;

  // Build a mock major object for KB functions that expect .name
  const m = { name: major.name, code: major.code };

  switch (field) {
    case 'xuefeng_comment':
      if (typeof kb.xuefeng === 'function') {
        return kb.xuefeng(m);
      }
      return null;

    case 'suitable_for':
      if (typeof kb.suitable === 'function') {
        return kb.suitable(m);
      }
      return null;

    case 'career_outlook':
      // Use KB careers.tiers
      if (kb.careers && kb.careers.tiers) {
        return kb.careers.tiers.substring(0, 600);
      }
      return null;

    case 'what_you_learn':
      // Use generateWhatYouLearn with KB courses
      if (kb.courses) {
        return generateWhatYouLearn(major.code, kb.courses);
      }
      return null;

    default:
      return null;
  }
}

// ============================================================
// Main
// ============================================================
async function main() {
  console.log('=== Step 1: Fetch all majors ===');
  const allMajors = [];
  for (let off = 0; off < 2000; off += 1000) {
    const data = await fetchAPI(`/rest/v1/majors?select=id,code,name,category,xuefeng_comment,what_you_learn,suitable_for,career_outlook&limit=1000&offset=${off}`);
    if (!data.length) break;
    allMajors.push(...data);
  }
  console.log(`  Total: ${allMajors.length} majors`);

  // Build dynamic name detection list
  ALL_MAJOR_NAMES = new Set(allMajors.map(m => m.name));
  console.log(`  Detection names: ${ALL_MAJOR_NAMES.size}`);

  console.log('\n=== Step 2: Detect mismatches ===');
  const fields = ['xuefeng_comment', 'what_you_learn', 'career_outlook', 'suitable_for'];
  const toFix = {};

  for (const field of fields) {
    toFix[field] = [];
    for (const m of allMajors) {
      const text = m[field] || '';
      if (!text) continue;
      if (hasWrongStart(text, m.name)) {
        toFix[field].push(m);
      }
    }
    console.log(`  ${field}: ${toFix[field].length} to fix`);
  }

  const totalToFix = Object.values(toFix).reduce((s, a) => s + a.length, 0);
  console.log(`  Total fixes needed: ${totalToFix}`);

  if (totalToFix === 0) {
    console.log('\nNothing to fix!');
    return;
  }

  console.log('\n=== Step 3: Regenerate and patch ===');
  let fixed = 0, failed = 0;

  for (const field of fields) {
    const majors = toFix[field];
    if (majors.length === 0) continue;
    console.log(`\n--- ${field} (${majors.length} items) ---`);

    for (const m of majors) {
      try {
        const newContent = regenerateField(m, field);
        if (!newContent || newContent === m[field]) continue;

        await patchAPI(`/rest/v1/majors?id=eq.${m.id}`, { [field]: newContent });
        console.log(`  [OK] ${m.code} ${m.name}`);
        fixed++;
      } catch (e) {
        console.log(`  [FAIL] ${m.code} ${m.name}: ${e.message}`);
        failed++;
      }
    }
  }

  console.log(`\n=== Done ===`);
  console.log(`Fixed: ${fixed}`);
  console.log(`Failed: ${failed}`);
}

main().catch(e => console.error('FATAL:', e));
