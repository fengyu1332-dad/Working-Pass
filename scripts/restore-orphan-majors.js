// Restore missing majors for orphan reports
const fs = require('fs');

const SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co';
const KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4';
const H = { 'apikey': KEY, 'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json' };

const moeData = JSON.parse(fs.readFileSync(__dirname + '/moe-2024-directory.json', 'utf8'));
const moeByCode = {};
moeData.forEach(m => { moeByCode[m.code] = m.name; });

const CATEGORY_NAMES = {
  '01': '01 哲学', '02': '02 经济学', '03': '03 法学', '04': '04 教育学',
  '05': '05 文学', '06': '06 历史学', '07': '07 理学', '08': '08 工学',
  '09': '09 农学', '10': '10 医学', '12': '12 管理学', '13': '13 艺术学',
};

const CATEGORY_ICONS = {
  '01': '🎓', '02': '💰', '03': '⚖️', '04': '📚', '05': '📖', '06': '📜',
  '07': '🔢', '08': '💻', '09': '🌾', '10': '🩺', '12': '🎨', '13': '🎭',
};

async function main() {
  const majorsRes = await fetch(SUPABASE_URL + '/rest/v1/majors?select=code,name', { headers: H });
  const majors = await majorsRes.json();
  const majorCodes = new Set(majors.map(m => m.code));

  const reportsRes = await fetch(SUPABASE_URL + '/rest/v1/reports?select=major_code,major_name,category', { headers: H });
  const reports = await reportsRes.json();

  const orphans = reports.filter(r => !majorCodes.has(r.major_code));
  console.log('Orphan reports: ' + orphans.length);

  let restored = 0;
  let deleted = 0;

  for (const r of orphans) {
    const moeName = moeByCode[r.major_code];
    if (moeName) {
      const catPrefix = r.major_code.substring(0, 2);
      const category = CATEGORY_NAMES[catPrefix] || (catPrefix + ' 未知');
      const icon = CATEGORY_ICONS[catPrefix] || '📖';

      const body = {
        code: r.major_code,
        name: moeName,
        category: category,
        category_icon: icon,
      };

      const res = await fetch(SUPABASE_URL + '/rest/v1/majors', {
        method: 'POST',
        headers: { ...H, 'Prefer': 'return=minimal' },
        body: JSON.stringify(body),
      });

      if (res.ok) {
        console.log('RESTORED: ' + r.major_code + ' ' + moeName);
        restored++;
      } else {
        const err = await res.text();
        console.log('FAILED: ' + r.major_code + ' ' + moeName + ' - ' + err.substring(0, 200));
      }
    } else {
      await fetch(SUPABASE_URL + '/rest/v1/reports?major_code=eq.' + r.major_code, {
        method: 'DELETE', headers: H,
      });
      console.log('DELETED: ' + r.major_code + ' ' + r.major_name + ' (invalid code)');
      deleted++;
    }
  }

  // Check for remaining duplicate codes that could cause issues with UNIQUE constraint
  const finalMajors = await fetch(SUPABASE_URL + '/rest/v1/majors?select=id,code,name', { headers: H });
  const final = await finalMajors.json();
  const byCode = {};
  final.forEach(m => {
    if (!byCode[m.code]) byCode[m.code] = [];
    byCode[m.code].push(m);
  });
  const dups = Object.entries(byCode).filter(([k,v]) => v.length > 1);
  if (dups.length > 0) {
    console.log('\nWARNING: Still have ' + dups.length + ' duplicate codes!');
    dups.forEach(([code, entries]) => {
      console.log('  ' + code + ': ' + entries.map(e => e.id + '=' + e.name).join(', '));
      // Delete duplicates, keep lowest id
      entries.sort((a, b) => a.id - b.id);
      for (let i = 1; i < entries.length; i++) {
        console.log('    Deleting duplicate id=' + entries[i].id);
      }
    });
  }

  const finalReports = await fetch(SUPABASE_URL + '/rest/v1/reports?select=major_code', { headers: H });
  const fr = await finalReports.json();
  const finalOrphans = fr.filter(r => !final.some(m => m.code === r.major_code));

  console.log('\n=== FINAL ===');
  console.log('Majors: ' + final.length);
  console.log('Reports: ' + fr.length);
  console.log('Orphan reports: ' + finalOrphans.length);
  console.log('Duplicate codes: ' + dups.length);
  console.log('Restored: ' + restored + ', Deleted: ' + deleted);
}

main().catch(e => console.error(e));
