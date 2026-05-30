// Parse MOE 2026 official PDF text → structured JSON
// Handles: consecutive codes, multiline names, multiline degree notes, cross-discipline format
const fs = require('fs');

const text = fs.readFileSync(__dirname + '/moe-2026-fulltext.txt', 'utf8');

const CATEGORY_CANONICAL = {
  '01': '哲学', '02': '经济学', '03': '法学', '04': '教育学',
  '05': '文学', '06': '历史学', '07': '理学', '08': '工学',
  '09': '农学', '10': '医学', '12': '管理学', '13': '艺术学',
  '14': '交叉学科',
};

const lines = text.split('\n')
  .map(l => l.trim())
  .filter(l => l && !l.match(/^—\s*\d+\s*—$/) && !l.match(/^\d{1,2}$/));

// Phase 1: Build subcategory map
const subcatMap = {};
let curCatCode = null, curCatName = null;
for (let i = 0; i < lines.length; i++) {
  let m = lines[i].match(/^(\d{2})\s*学科门类[：:](.+)/);
  if (m) { curCatCode = m[1]; curCatName = m[2]; continue; }
  m = lines[i].match(/^(\d{4})\s*(.+类)\s*$/);
  if (m) { subcatMap[m[1]] = { code: m[1], name: m[2], cat_code: curCatCode, cat_name: curCatName }; }
}

// Phase 2: Pre-process lines - merge split notes
// If a line contains "（注：" but no closing "）", merge with next line
const merged = [];
for (let i = 0; i < lines.length; i++) {
  let line = lines[i];
  if (line.includes('（注：') && !line.includes('）') && i + 1 < lines.length) {
    line = line + lines[i + 1];
    i++; // Skip next line
  }
  // Also handle split across more lines (rare but possible)
  while (line.includes('（注：') && !line.includes('）') && i + 1 < lines.length) {
    line = line + lines[i + 1];
    i++;
  }
  merged.push(line);
}

// Phase 3: Parse majors from merged lines
const MAJORS = [];
const pendingCodes = [];

function addMajor(code, rawName) {
  let name = rawName.trim();
  if (!name) return;

  let degree = '';
  let note = '';

  const noteMatch = name.match(/[（(]注[：:](.+?)[）)]/);
  if (noteMatch) {
    note = noteMatch[1].trim().replace(/[。.]$/, '');
    name = name.replace(/[（(]注[：:].+?[）)]/, '').trim();

    const degMatch = note.match(/(?:授予|可授)(.+?)学士学位/);
    if (degMatch) degree = degMatch[1].trim();
  }

  name = name.replace(/[。.]$/, '').trim();
  if (!name) return;

  const remarkMatch = code.match(/(K|T|TK)$/);
  const remark = remarkMatch ? remarkMatch[1] : '';

  const subcatCode = code.substring(0, 4);
  const catCode = code.substring(0, 2);
  const sc = subcatMap[subcatCode];

  // 交叉学科 (14) doesn't have traditional subcategories in the PDF
  const subcatName = sc ? sc.name : (catCode === '14' ? '交叉学科类' : '');

  MAJORS.push({
    code, name,
    category_code: catCode,
    category_name: CATEGORY_CANONICAL[catCode] || '',
    subcategory_code: subcatCode,
    subcategory_name: subcatName,
    degree,
    remark,
    note: note || '',
  });
}

for (const line of merged) {
  // Skip category/subcategory headers
  if (line.match(/^(\d{2})\s*学科门类[：:]/)) continue;
  if (line.match(/^(\d{4})\s*(.+类)\s*$/)) continue;
  // Skip preamble text
  if (line.match(/^(附件|普通高等学校|教\s*育\s*部|说\s*明|一、|二、|三、|四、|五、|2026年)/)) continue;

  // Check for standalone code (6 or 7 digits + optional K/T/TK)
  const codeMatch = line.match(/^(\d{6,7}(?:K|T|TK)?)$/);
  if (codeMatch) {
    pendingCodes.push(codeMatch[1]);
    continue;
  }

  // Check for code + name on same line (6 or 7 digits + optional K/T/TK)
  const cnMatch = line.match(/^(\d{6,7}(?:K|T|TK)?)\s+(.+)$/);
  if (cnMatch) {
    addMajor(cnMatch[1], cnMatch[2]);
    continue;
  }

  // If pending codes exist, this line is a name for the first pending code
  if (pendingCodes.length > 0 && line.length > 1 && !line.match(/^\d/)) {
    const code = pendingCodes.shift();
    addMajor(code, line);
    continue;
  }
}

if (pendingCodes.length > 0) {
  console.log('WARNING: ' + pendingCodes.length + ' codes without names:');
  pendingCodes.forEach(c => console.log('  ' + c));
}

// Phase 4: Summary
MAJORS.forEach((m, i) => { m.seq = i + 1; });

console.log('=== PARSE RESULTS ===');
console.log('Total majors: ' + MAJORS.length);

const byCat = {};
MAJORS.forEach(m => {
  if (!byCat[m.category_code]) byCat[m.category_code] = { count: 0, name: m.category_name };
  byCat[m.category_code].count++;
});
Object.entries(byCat).sort().forEach(([k, v]) => {
  console.log('  ' + k + ' ' + v.name + ': ' + v.count);
});

const noSubcat = MAJORS.filter(m => !m.subcategory_name);
if (noSubcat.length > 0) {
  console.log('\nMissing subcategory:');
  noSubcat.forEach(m => console.log('  ' + m.code + ' ' + m.name));
}

const byRemark = {};
MAJORS.forEach(m => { const r = m.remark || '(none)'; byRemark[r] = (byRemark[r] || 0) + 1; });
console.log('\nRemarks:');
Object.entries(byRemark).sort().forEach(([k, v]) => console.log('  ' + k + ': ' + v));

// Compare with old directory
if (fs.existsSync(__dirname + '/moe-2026-directory.json')) {
  const old = JSON.parse(fs.readFileSync(__dirname + '/moe-2026-directory.json', 'utf8'));
  const refCodes = new Set(MAJORS.map(m => m.code));
  const missing = old.filter(m => !refCodes.has(m.code));
  console.log('\nStill missing from ' + old.length + ': ' + missing.length);
  if (missing.length > 0) {
    missing.forEach(m => console.log('  ' + m.code + ': ' + m.name));
  }
}

const outFile = __dirname + '/moe-2026-reference.json';
fs.writeFileSync(outFile, JSON.stringify(MAJORS, null, 2), 'utf8');
console.log('\nSaved: ' + outFile);
