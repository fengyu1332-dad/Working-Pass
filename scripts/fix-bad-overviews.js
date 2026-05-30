// Fix bad overviews: wrong-name attributions + generic template text
// Uses the knowledge-base overview functions to regenerate proper content
const KB = require('./data/knowledge-base.js');

const SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co';
const KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4';
const H = { 'apikey': KEY, 'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json' };

// Dynamic: all major names will be loaded from DB at runtime for mismatch detection
// Category names that are safe to match (broad categories, not specific majors)
const SAFE_STARTS = new Set(['法学','工学','理学','经济学','管理学','医学','文学','哲学','教育学','农学','历史学','艺术学','军事学','交叉学科']);

// Will be populated dynamically
let ALL_MAJOR_NAMES = new Set();

function isBadOverview(overview, name) {
  if (!overview) return true;
  // Generic template pattern
  if (overview.includes('相关理论与实践的专业，培养掌握')) return true;
  if (overview.includes('相关理论研究与实践应用的专业')) return true;
  // Old engineering generic fallback
  if (overview.includes('培养具备工程技术能力和实践经验的专门人才')) return true;
  // New engineering generic fallback
  if (overview.includes('培养具备扎实专业知识和工程实践能力的应用型技术人才')) return true;
  // Generic engineering template with placeholder text
  if (overview.includes('是工学重要分支，主要研究专业理论和实践应用技术')) return true;
  // Wrong name attribution (dynamic: checks against ALL major names)
  // Skip if overview correctly starts with own name
  if (overview.startsWith(name)) return false;
  for (const ref of ALL_MAJOR_NAMES) {
    if (ref !== name && !SAFE_STARTS.has(ref) && overview.startsWith(ref)) return true;
  }
  return false;
}

function genOverview(major, catCode) {
  const kb = KB[catCode];
  if (!kb) return `${major.name}是本科专业，培养该领域的专门人才。`;

  const baseOverview = kb.overview(major);

  // For 工学 (08), check IT override
  if (catCode === '08') {
    const overviewFn = (KB['08'].isIT(major) && KB['08'].overview_IT) ? KB['08'].overview_IT : kb.overview;
    return overviewFn(major).substring(0, 500);
  }

  return baseOverview.substring(0, 500);
}

// Use KB salary defaults for unreasonable values
function getKBSalary(catCode, major) {
  if (catCode === '08' && KB['08'].isIT(major)) return KB['08'].salary_IT;
  const kb = KB[catCode];
  if (kb && kb.salary) return kb.salary;
  return '¥6k-18k';
}

function fixSalary(salary, catCode, major) {
  if (!salary) return getKBSalary(catCode, major);
  const match = salary.match(/¥(\d+)k-(\d+)k/);
  if (!match) return getKBSalary(catCode, major);
  const lo = parseInt(match[1]);
  const hi = parseInt(match[2]);
  // Fix zero/zero-like entries
  if (lo === 0 && hi === 0) return getKBSalary(catCode, major);
  // If upper bound > 50k for non-medical, or > 100k for any, replace with KB default
  if ((catCode !== '10' && hi > 50) || hi > 100) {
    return getKBSalary(catCode, major);
  }
  return salary;
}

async function fetchAll() {
  const all = [];
  for (let off = 0; off < 2000; off += 1000) {
    const res = await fetch(`${SUPABASE_URL}/rest/v1/majors?select=id,code,name,category,overview,salary_range&limit=1000&offset=${off}`, { headers: H });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const data = await res.json();
    if (!data.length) break;
    all.push(...data);
  }
  return all;
}

async function main() {
  console.log('Fetching all majors...');
  const majors = await fetchAll();
  console.log(`Total: ${majors.length}`);

  // Build dynamic name list for mismatch detection (instead of hardcoded MAJOR_NAME_PATTERNS)
  ALL_MAJOR_NAMES = new Set(majors.map(m => m.name));
  console.log(`Detection names: ${ALL_MAJOR_NAMES.size}`);

  let fixedOverview = 0, fixedSalary = 0, failed = 0;

  for (const m of majors) {
    const catCode = m.code.substring(0, 2);
    const updates = {};

    // Check & fix overview
    if (isBadOverview(m.overview, m.name)) {
      const newOv = genOverview(m, catCode);
      if (newOv !== m.overview) {
        updates.overview = newOv;
        fixedOverview++;
      }
    }

    // Check & fix salary
    const newSal = fixSalary(m.salary_range, catCode, m);
    if (newSal !== m.salary_range) {
      updates.salary_range = newSal;
      fixedSalary++;
    }

    if (Object.keys(updates).length > 0) {
      const res = await fetch(`${SUPABASE_URL}/rest/v1/majors?id=eq.${m.id}`, {
        method: 'PATCH',
        headers: { ...H, 'Prefer': 'return=minimal' },
        body: JSON.stringify(updates),
      });
      if (!res.ok) {
        console.log(`FAIL ${m.code} ${m.name}: ${(await res.text()).substring(0, 100)}`);
        failed++;
      }
    }
  }

  console.log(`\n=== Fix Complete ===`);
  console.log(`Overview fixed: ${fixedOverview}`);
  console.log(`Salary fixed: ${fixedSalary}`);
  console.log(`Failed: ${failed}`);
}

main().catch(e => console.error('FATAL:', e));
