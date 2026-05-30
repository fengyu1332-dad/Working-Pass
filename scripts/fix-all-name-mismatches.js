// Fix ALL name-mismatched overviews using dynamic detection
// Uses the KB template functions to regenerate proper content
const KB = require('./data/knowledge-base.js');
const https = require('https');

const SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co';
const KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4';
const H = { 'apikey': KEY, 'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json' };

function fetchAPI(path) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, SUPABASE_URL);
    const req = https.get(url.toString(), { headers: H }, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(body)); } catch(e) { reject(new Error(body)); }
      });
    });
    req.on('error', reject);
  });
}

function patchAPI(path, data) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, SUPABASE_URL);
    const body = JSON.stringify(data);
    const options = {
      method: 'PATCH',
      headers: { ...H, 'Prefer': 'return=minimal' },
    };
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

// Known generic template patterns to detect
function isGenericTemplate(overview) {
  if (!overview) return true;
  if (overview.includes('是工学重要分支，主要研究专业理论和实践应用技术，课程包括理论基础、专业核心、实践环节等模块')) return true;
  if (overview.includes('相关理论与实践的专业，培养掌握')) return true;
  if (overview.includes('培养具备扎实专业知识和工程实践能力的应用型技术人才')) return true;
  if (overview.includes('培养具备工程技术能力和实践经验的专门人才')) return true;
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

async function main() {
  console.log('=== Step 1: Fetch all majors dynamically ===');
  const allMajors = [];
  for (let off = 0; off < 2000; off += 1000) {
    const data = await fetchAPI(`/rest/v1/majors?select=id,code,name,category,overview&limit=1000&offset=${off}`);
    if (!data.length) break;
    allMajors.push(...data);
    console.log(`  Fetched ${allMajors.length} so far...`);
  }
  console.log(`  Total: ${allMajors.length} majors`);

  // Build the full name list (dynamically, no hardcoded list!)
  const ALL_NAMES = new Set(allMajors.map(m => m.name));
  console.log(`  Unique names for detection: ${ALL_NAMES.size}`);

  // Category names are safe to match in overviews
  const CAT_NAMES = new Set(['法学','工学','理学','经济学','管理学','医学','文学','哲学','教育学','农学','历史学','艺术学','军事学','交叉学科']);

  console.log('\n=== Step 2: Detect mismatches ===');
  const toFix = [];
  for (const m of allMajors) {
    const overview = m.overview || '';
    let needsFix = false;
    let reason = '';

    // Check 1: overview starts with wrong major name
    if (overview) {
      for (const otherName of ALL_NAMES) {
        if (otherName === m.name) continue;
        if (CAT_NAMES.has(otherName)) continue;
        if (overview.startsWith(otherName)) {
          needsFix = true;
          reason = `starts with '${otherName}'`;
          break;
        }
      }
    }

    // Check 2: generic template
    if (!needsFix && isGenericTemplate(overview)) {
      needsFix = true;
      reason = 'generic template pattern';
    }

    // Check 3: empty overview
    if (!needsFix && !overview) {
      needsFix = true;
      reason = 'empty overview';
    }

    if (needsFix) {
      toFix.push(m);
    }
  }

  console.log(`  Mismatches to fix: ${toFix.length}`);
  for (const m of toFix) {
    console.log(`  [${m.code}] ${m.name} (${m.category}) — ${(m.overview||'').substring(0, 60)}`);
  }

  console.log(`\n=== Step 3: Regenerate and patch ===`);
  let fixed = 0, failed = 0;
  for (const m of toFix) {
    const catCode = m.code.substring(0, 2);
    try {
      const newOverview = genOverview(m, catCode);
      if (newOverview === m.overview) continue;

      await patchAPI(`/rest/v1/majors?id=eq.${m.id}`, { overview: newOverview });
      console.log(`  [OK] ${m.code} ${m.name}: "${newOverview.substring(0, 60)}..."`);
      fixed++;
    } catch(e) {
      console.log(`  [FAIL] ${m.code} ${m.name}: ${e.message}`);
      failed++;
    }
  }

  console.log(`\n=== Done ===`);
  console.log(`Fixed: ${fixed}`);
  console.log(`Failed: ${failed}`);
}

main().catch(e => console.error('FATAL:', e));
