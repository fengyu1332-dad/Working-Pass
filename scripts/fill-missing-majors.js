// Compare DB majors with MOE 2026 directory (883 entries)
// Insert missing majors, verify existing ones

const fs = require('fs');

const SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co';
const KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4';
const H = { 'apikey': KEY, 'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json' };

const moeData = JSON.parse(fs.readFileSync(__dirname + '/moe-2026-directory.json', 'utf8'));
const moeByCode = {};
moeData.forEach(m => { moeByCode[m.code] = m; });

const CATEGORY_ICONS = {
  '哲学': '🎓', '经济学': '💰', '法学': '⚖️', '教育学': '📚', '文学': '📖',
  '历史学': '📜', '理学': '🔢', '工学': '💻', '农学': '🌾', '医学': '🩺',
  '管理学': '🎨', '艺术学': '🎭', '交叉学科': '🔬',
};

async function main() {
  // Fetch current DB majors
  const majorsRes = await fetch(SUPABASE_URL + '/rest/v1/majors?select=id,code,name,category', { headers: H });
  const dbMajors = await majorsRes.json();
  const dbByCode = {};
  dbMajors.forEach(m => { dbByCode[m.code] = m; });

  console.log('MOE 2026: ' + moeData.length + ' entries');
  console.log('DB current: ' + dbMajors.length + ' entries\n');

  // Find missing entries (in MOE but not in DB)
  const missing = moeData.filter(m => !dbByCode[m.code]);
  console.log('Missing from DB: ' + missing.length);

  // Find extra entries (in DB but not in MOE 2026)
  const extra = dbMajors.filter(m => !moeByCode[m.code]);
  console.log('Extra in DB (not in MOE 2026): ' + extra.length);
  if (extra.length > 0) {
    extra.forEach(m => console.log('  ' + m.code + ': ' + m.name));
  }

  // Find name mismatches (code exists in both but name differs)
  const nameMismatches = [];
  dbMajors.forEach(m => {
    const moe = moeByCode[m.code];
    if (moe && moe.name !== m.name) {
      nameMismatches.push({ db: m, moe });
    }
  });
  console.log('Name mismatches: ' + nameMismatches.length);
  if (nameMismatches.length > 0) {
    nameMismatches.forEach(mm => {
      console.log('  ' + mm.db.code + ': DB="' + mm.db.name + '" vs MOE="' + mm.moe.name + '"');
    });
  }

  // Insert missing majors
  console.log('\nInserting ' + missing.length + ' missing majors...');
  let inserted = 0;
  let failed = 0;

  for (const m of missing) {
    const category = m.category + ' ' + m.subcategory;
    const icon = CATEGORY_ICONS[m.category] || '📖';

    const body = {
      code: m.code,
      name: m.name,
      category: m.category,
      category_icon: icon,
    };

    const res = await fetch(SUPABASE_URL + '/rest/v1/majors', {
      method: 'POST',
      headers: { ...H, 'Prefer': 'return=minimal' },
      body: JSON.stringify(body),
    });

    if (res.ok) {
      inserted++;
    } else {
      const err = await res.text();
      console.log('  FAIL ' + m.code + ' ' + m.name + ': ' + err.substring(0, 150));
      failed++;
    }

    if (inserted % 50 === 49) {
      console.log('  Inserted ' + (inserted) + '/' + missing.length + '...');
      await new Promise(r => setTimeout(r, 200));
    }
  }

  console.log('\nInserted: ' + inserted + ', Failed: ' + failed);

  // Final check
  const finalRes = await fetch(SUPABASE_URL + '/rest/v1/majors?select=code,name,category', { headers: H });
  const final = await finalRes.json();

  const byCat = {};
  final.forEach(m => {
    const cat = m.category.replace(/\s.*/, '');
    if (!byCat[cat]) byCat[cat] = 0;
    byCat[cat]++;
  });

  console.log('\n=== Final state ===');
  console.log('Total majors: ' + final.length);
  Object.entries(byCat).sort().forEach(([k,v]) => {
    console.log('  ' + k + ': ' + v);
  });

  // Verify no duplicates
  const byCode = {}, byName = {};
  final.forEach(m => {
    if (!byCode[m.code]) byCode[m.code] = [];
    byCode[m.code].push(m);
    if (!byName[m.name]) byName[m.name] = [];
    byName[m.name].push(m);
  });
  console.log('Duplicate codes: ' + Object.entries(byCode).filter(([_,v]) => v.length > 1).length);
  console.log('Duplicate names: ' + Object.entries(byName).filter(([_,v]) => v.length > 1).length);
}

main().catch(e => console.error(e));
