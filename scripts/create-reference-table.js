// Create moe_2026_reference table and insert all 883 entries
// This is the SINGLE SOURCE OF TRUTH for all major data
const fs = require('fs');

const SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co';
const KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4';
const H = { 'apikey': KEY, 'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json' };

const data = JSON.parse(fs.readFileSync(__dirname + '/moe-2026-reference.json', 'utf8'));

async function main() {
  // Step 1: Create table via REST (Supabase auto-creates schema on first insert)
  // But we need proper columns, so let's use the SQL API or create via individual inserts
  // Actually, the REST API can't create tables. We need to use the Management API or SQL.

  // Let's first try to see if we can query the existing majors table to understand available patterns
  console.log('Fetching current DB schema info...');

  // Check if moe_2026_reference table exists
  const checkRes = await fetch(SUPABASE_URL + '/rest/v1/moe_2026_reference?limit=1', { headers: H });
  if (checkRes.ok) {
    console.log('moe_2026_reference table already exists');
    // Check count
    const countRes = await fetch(SUPABASE_URL + '/rest/v1/moe_2026_reference?select=count', { headers: { ...H, 'Prefer': 'count=exact' } });
    const count = parseInt(countRes.headers.get('content-range')?.split('/')[1] || '0');
    console.log('Existing rows: ' + count);
  } else {
    console.log('Table does not exist yet: ' + checkRes.status + ' - will create via insert');
  }

  // Step 2: Try bulk insert via REST
  // Supabase REST API allows creating a table implicitly via first insert
  console.log('\nInserting ' + data.length + ' entries...');

  const batchSize = 50;
  let inserted = 0;
  let failed = 0;
  const errors = [];

  for (let i = 0; i < data.length; i += batchSize) {
    const batch = data.slice(i, i + batchSize).map(m => ({
      seq: m.seq,
      code: m.code,
      name: m.name,
      category_code: m.category_code,
      category_name: m.category_name,
      subcategory_code: m.subcategory_code,
      subcategory_name: m.subcategory_name,
      degree: m.degree || null,
      remark: m.remark || null,
      note: m.note || null,
    }));

    const res = await fetch(SUPABASE_URL + '/rest/v1/moe_2026_reference', {
      method: 'POST',
      headers: { ...H, 'Prefer': 'return=minimal' },
      body: JSON.stringify(batch),
    });

    if (res.ok) {
      inserted += batch.length;
    } else {
      const errText = await res.text();
      console.log('Batch ' + (i / batchSize + 1) + ' FAILED: ' + errText.substring(0, 200));

      // Try inserting one by one for this batch
      for (const item of batch) {
        const singleRes = await fetch(SUPABASE_URL + '/rest/v1/moe_2026_reference', {
          method: 'POST',
          headers: { ...H, 'Prefer': 'return=minimal' },
          body: JSON.stringify(item),
        });
        if (singleRes.ok) {
          inserted++;
        } else {
          const err = await singleRes.text();
          errors.push(item.code + ': ' + err.substring(0, 100));
          failed++;
        }
      }
    }

    if (i % 200 === 0 && i > 0) {
      console.log('  Progress: ' + i + '/' + data.length + ' (inserted: ' + inserted + ', failed: ' + failed + ')');
    }
    await new Promise(r => setTimeout(r, 100));
  }

  console.log('\n=== RESULT ===');
  console.log('Inserted: ' + inserted);
  console.log('Failed: ' + failed);
  if (errors.length > 0) {
    console.log('Errors:');
    errors.forEach(e => console.log('  ' + e));
  }

  // Step 3: Verify
  const finalRes = await fetch(SUPABASE_URL + '/rest/v1/moe_2026_reference?select=count', { headers: { ...H, 'Prefer': 'count=exact' } });
  const finalCount = parseInt(finalRes.headers.get('content-range')?.split('/')[1] || '0');
  console.log('\nFinal table count: ' + finalCount);

  // Step 4: Show category distribution
  const catRes = await fetch(SUPABASE_URL + '/rest/v1/moe_2026_reference?select=category_code,category_name', { headers: H });
  const all = await catRes.json();
  const byCat = {};
  all.forEach(m => {
    if (!byCat[m.category_code]) byCat[m.category_code] = { count: 0, name: m.category_name };
    byCat[m.category_code].count++;
  });
  console.log('\nCategory distribution:');
  Object.entries(byCat).sort().forEach(([k, v]) => console.log('  ' + k + ' ' + v.name + ': ' + v.count));
}

main().catch(e => console.error('FATAL:', e));
