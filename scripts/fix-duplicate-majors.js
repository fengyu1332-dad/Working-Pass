// ============================================================
// 专业星图 - 修复重复专业名称 & 生成数据库约束 SQL
// 对照 MOE 2024 官方目录
// ============================================================

const fs = require('fs');

const SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4';

const moeData = JSON.parse(fs.readFileSync(__dirname + '/moe-2024-directory.json', 'utf8'));
const moeByCode = {};
const moeByName = {};
moeData.forEach(m => {
  moeByCode[m.code] = m.name;
  if (!moeByName[m.name]) moeByName[m.name] = [];
  moeByName[m.name].push(m.code);
});

// 人工审核映射: DB中名称与MOE名称略有差异但明确指向同一专业的条目
const MANUAL_OVERRIDES = [
  { dbName: '航空服务艺术管理', correctCode: '130208TK', correctName: '航空服务艺术与管理' },
  { dbName: '草学', correctCode: '090701', correctName: '草业科学' },
  { dbName: '戏曲表演', correctCode: '130301', correctName: '表演' },
  { dbName: '戏曲导演', correctCode: '130306', correctName: '戏剧影视导演' },
];
const manualByName = {};
MANUAL_OVERRIDES.forEach(ov => { manualByName[ov.dbName] = ov; });

async function fetchTable(table) {
  const all = [];
  let offset = 0;
  const limit = 1000;
  while (true) {
    const url = SUPABASE_URL + '/rest/v1/' + table + '?select=*&limit=' + limit + '&offset=' + offset;
    const res = await fetch(url, {
      headers: { 'apikey': SUPABASE_ANON_KEY, 'Authorization': 'Bearer ' + SUPABASE_ANON_KEY },
    });
    if (!res.ok) throw new Error('HTTP ' + res.status + ': ' + await res.text());
    const data = await res.json();
    if (data.length === 0) break;
    all.push(...data);
    offset += limit;
  }
  return all;
}

function esc(s) {
  return s.replace(/'/g, "''");
}

function buildAllFixes(dbMajors, reports) {
  const sql = [];
  let fixCount = 0;
  const fixLog = [];

  const reportsByCode = {};
  reports.forEach(r => {
    if (!reportsByCode[r.major_code]) reportsByCode[r.major_code] = [];
    reportsByCode[r.major_code].push(r);
  });

  // Step 1: Fix each major entry
  const fixedEntries = [];

  for (const m of dbMajors) {
    const moeNameForCode = moeByCode[m.code];
    const moeCodesForName = moeByName[m.name];
    const manualOv = manualByName[m.name];

    if (moeNameForCode && moeNameForCode === m.name) {
      fixedEntries.push({ id: m.id, code: m.code, name: m.name, action: 'KEEP', oldCode: m.code });
    } else if (moeNameForCode && moeNameForCode !== m.name) {
      sql.push('-- RENAME: code ' + m.code + ' MOE="' + moeNameForCode + '" DB="' + m.name + '"');
      sql.push("UPDATE majors SET name = '" + esc(moeNameForCode) + "' WHERE id = " + m.id + ";");
      fixedEntries.push({ id: m.id, code: m.code, name: moeNameForCode, action: 'RENAME', oldCode: m.code });
      fixLog.push({ id: m.id, code: m.code, oldName: m.name, newName: moeNameForCode, action: 'RENAME' });
      fixCount++;
    } else if (!moeNameForCode && moeCodesForName && moeCodesForName.length > 0) {
      const oldCode = m.code;
      const newCode = moeCodesForName[0];
      sql.push('-- FIX_CODE: "' + m.name + '" ' + oldCode + ' -> ' + newCode);
      sql.push("UPDATE majors SET code = '" + esc(newCode) + "' WHERE id = " + m.id + ";");
      if (reportsByCode[oldCode]) {
        sql.push("UPDATE reports SET major_code = '" + esc(newCode) + "' WHERE major_code = '" + esc(oldCode) + "';");
      }
      fixedEntries.push({ id: m.id, code: newCode, name: m.name, action: 'FIX_CODE', oldCode });
      fixLog.push({ id: m.id, oldCode, newCode, name: m.name, action: 'FIX_CODE' });
      fixCount++;
    } else if (manualOv) {
      const oldCode = m.code;
      sql.push('-- MANUAL_FIX: "' + m.name + '" -> "' + manualOv.correctName + '" (' + manualOv.correctCode + ')');
      sql.push("UPDATE majors SET code = '" + esc(manualOv.correctCode) + "', name = '" + esc(manualOv.correctName) + "' WHERE id = " + m.id + ";");
      if (reportsByCode[oldCode]) {
        sql.push("UPDATE reports SET major_code = '" + esc(manualOv.correctCode) + "' WHERE major_code = '" + esc(oldCode) + "';");
      }
      fixedEntries.push({ id: m.id, code: manualOv.correctCode, name: manualOv.correctName, action: 'MANUAL_FIX', oldCode });
      fixLog.push({ id: m.id, oldCode, newCode: manualOv.correctCode, oldName: m.name, newName: manualOv.correctName, action: 'MANUAL_FIX' });
      fixCount++;
    } else {
      sql.push('-- DELETE: "' + m.name + '" (' + m.code + ') not in MOE 2024');
      sql.push('DELETE FROM majors WHERE id = ' + m.id + ';');
      sql.push("DELETE FROM reports WHERE major_code = '" + esc(m.code) + "';");
      fixedEntries.push(null);
      fixLog.push({ id: m.id, code: m.code, name: m.name, action: 'DELETE' });
      fixCount++;
    }
  }

  sql.push('');
  sql.push('-- ============================================================');
  sql.push('-- Step 2: Dedup (remove duplicates after fixes)');
  sql.push('-- ============================================================');

  const activeEntries = fixedEntries.filter(e => e !== null);
  const byCode = {};
  const byName = {};

  for (const e of activeEntries) {
    if (!byCode[e.code]) byCode[e.code] = [];
    byCode[e.code].push(e);
    if (!byName[e.name]) byName[e.name] = [];
    byName[e.name].push(e);
  }

  const deletedIds = new Set();

  for (const [code, entries] of Object.entries(byCode)) {
    if (entries.length > 1) {
      entries.sort((a, b) => a.id - b.id);
      const keeper = entries[0];
      for (let i = 1; i < entries.length; i++) {
        if (deletedIds.has(entries[i].id)) continue;
        const td = entries[i];
        sql.push('-- DEDUP_CODE: code ' + code + ' dup, delete "' + td.name + '" (id=' + td.id + '), keep id=' + keeper.id);
        sql.push('DELETE FROM majors WHERE id = ' + td.id + ';');
        if (td.oldCode && td.oldCode !== code) {
          sql.push("UPDATE reports SET major_code = '" + esc(code) + "' WHERE major_code = '" + esc(td.oldCode) + "';");
        }
        deletedIds.add(td.id);
        fixLog.push({ id: td.id, code, name: td.name, action: 'DEDUP_CODE', keeperId: keeper.id });
        fixCount++;
      }
    }
  }

  for (const [name, entries] of Object.entries(byName)) {
    if (entries.length > 1) {
      entries.sort((a, b) => a.id - b.id);
      const stillActive = entries.filter(e => !deletedIds.has(e.id));
      if (stillActive.length > 1) {
        const keeper = stillActive[0];
        for (let i = 1; i < stillActive.length; i++) {
          if (deletedIds.has(stillActive[i].id)) continue;
          const td = stillActive[i];
          sql.push('-- DEDUP_NAME: "' + name + '" dup, delete code=' + td.code + ' (id=' + td.id + '), keep code=' + keeper.code + ' (id=' + keeper.id + ')');
          sql.push('DELETE FROM majors WHERE id = ' + td.id + ';');
          if (td.code !== keeper.code) {
            sql.push("UPDATE reports SET major_code = '" + esc(keeper.code) + "' WHERE major_code = '" + esc(td.code) + "';");
          }
          deletedIds.add(td.id);
          fixLog.push({ id: td.id, code: td.code, name, action: 'DEDUP_NAME', keeperId: keeper.id });
          fixCount++;
        }
      }
    }
  }

  return { sql, fixCount, fixLog, activeEntries };
}

async function main() {
  console.log('Fetching data from Supabase...');
  const dbMajors = await fetchTable('majors');
  const reports = await fetchTable('reports');
  console.log('DB: ' + dbMajors.length + ' majors, ' + reports.length + ' reports');
  console.log('MOE 2024: ' + moeData.length + ' majors\n');

  const { sql, fixCount, fixLog } = buildAllFixes(dbMajors, reports);

  const countByAction = {};
  fixLog.forEach(l => {
    countByAction[l.action] = (countByAction[l.action] || 0) + 1;
  });

  console.log('='.repeat(60));
  console.log('Fix summary:');
  Object.entries(countByAction).forEach(([k, v]) => {
    console.log('  ' + k + ': ' + v);
  });
  console.log('  Total: ' + fixCount);
  console.log('='.repeat(60));

  const deletes = fixLog.filter(l => l.action === 'DELETE');
  console.log('\nEntries to DELETE (not in MOE 2024):');
  deletes.forEach(d => {
    const hasReport = reports.some(r => r.major_code === d.code);
    console.log('  ' + d.code + ': "' + d.name + '" (id=' + d.id + ')' + (hasReport ? ' [has report]' : ''));
  });

  const manualFixes = fixLog.filter(l => l.action === 'MANUAL_FIX');
  if (manualFixes.length > 0) {
    console.log('\nManual overrides applied:');
    manualFixes.forEach(f => {
      console.log('  "' + f.oldName + '" -> "' + f.newName + '" (' + f.oldCode + ' -> ' + f.newCode + ')');
    });
  }

  // Add UNIQUE constraints
  sql.push('');
  sql.push('-- ============================================================');
  sql.push('-- Step 3: Add UNIQUE constraints');
  sql.push('-- ============================================================');
  sql.push('');
  sql.push("DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'majors_code_unique') THEN");
  sql.push('  ALTER TABLE majors ADD CONSTRAINT majors_code_unique UNIQUE (code);');
  sql.push('END IF; END $$;');
  sql.push('');
  sql.push("DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'majors_name_unique') THEN");
  sql.push('  ALTER TABLE majors ADD CONSTRAINT majors_name_unique UNIQUE (name);');
  sql.push('END IF; END $$;');

  const sqlFile = __dirname + '/fix-duplicates.sql';
  fs.writeFileSync(sqlFile, sql.join('\n'), 'utf8');
  console.log('\nSQL saved to: ' + sqlFile);
  console.log('Total ' + sql.length + ' lines (includes reports sync)');

  fs.writeFileSync(__dirname + '/fix-log.json', JSON.stringify(fixLog, null, 2), 'utf8');
}

main().catch(err => { console.error('Error:', err); process.exit(1); });
