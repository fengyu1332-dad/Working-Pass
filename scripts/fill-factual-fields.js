// Phase 1: Fill degree, duration, career_directions for all 883 majors
// Data source: moe_2026_reference + category conventions
const fs = require('fs');

const SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co';
const KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4';
const H = { 'apikey': KEY, 'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json' };

// Category → default degree mapping
const CAT_DEGREE = {
  '01': '哲学学士', '02': '经济学学士', '03': '法学学士', '04': '教育学学士',
  '05': '文学学士', '06': '历史学学士', '07': '理学学士', '08': '工学学士',
  '09': '农学学士', '10': '医学学士', '12': '管理学学士', '13': '艺术学学士',
  '14': '工学学士', // 交叉学科 default
};

// Degree abbreviation → full name
function expandDegree(abbr) {
  const map = {
    '哲学': '哲学学士', '经济学': '经济学学士', '法学': '法学学士', '教育学': '教育学学士',
    '文学': '文学学士', '历史学': '历史学学士', '理学': '理学学士', '工学': '工学学士',
    '农学': '农学学士', '医学': '医学学士', '管理学': '管理学学士', '艺术学': '艺术学学士',
  };
  // Handle compound: "工学或理学" → "工学或理学学士"
  return abbr.split('或').map(s => map[s.trim()] || s.trim()).join('或');
}

// 5-year duration majors (code patterns)
function isFiveYear(code) {
  const fiveYearPatterns = [
    '082801', // 建筑学
    '082802', // 城乡规划
    '082803', // 风景园林
    '100201K', // 临床医学
    '100202TK', // 麻醉学
    '100203TK', // 医学影像学
    '100204TK', // 眼视光医学
    '100205TK', // 精神医学
    '100206TK', // 放射医学
    '100207TK', // 儿科学
    '100301K', // 口腔医学
    '100401K', // 预防医学
    '100403TK', // 妇幼保健医学
    '100404TK', // 卫生监督
    '100405TK', // 全球健康学
    '100501K', // 中医学
    '100502K', // 针灸推拿学
    '100503K', // 藏医学
    '100504K', // 蒙医学
    '100505K', // 维医学
    '100506K', // 壮医学
    '100507K', // 哈医学
    '100508TK', // 傣医学
    '100509TK', // 回医学
    '100510TK', // 中医康复学
    '100511TK', // 中医养生学
    '100512TK', // 中医儿科学
    '100513TK', // 中医骨伤科学
    '100601K', // 中西医临床医学
    '100901K', // 法医学
    '090401', // 动物医学
  ];
  return fiveYearPatterns.some(p => code.startsWith(p) || code === p);
}

// Career directions by category
const CAT_CAREERS = {
  '01': ['高校/科研机构', '公务员/事业单位', '中学政治教师', '出版社/媒体', '企业行政/管理培训生'],
  '02': ['银行/证券/保险', '投行/基金/信托', '四大会计师事务所', '政府经济部门', '企业战略/财务', '咨询公司'],
  '03': ['公检法/律师/法务', '公务员/事业单位', '国际组织/NGO', '企业法务/合规', '公证处/仲裁机构'],
  '04': ['中小学/幼儿园教师', '教育科技公司', '教育行政部门', '特殊教育机构', '教育培训机构', '教育研究'],
  '05': ['新闻/出版/传媒', '翻译/国际交流', '公务员/事业单位', '广告/公关/营销', '教育/培训机构', '互联网内容运营'],
  '06': ['高校/科研机构', '博物馆/档案馆', '文化遗产保护', '公务员/事业单位', '文化旅游/文创', '出版/传媒'],
  '07': ['科研院所/高校', 'IT/互联网/数据分析', '中学教师', '金融/保险/精算', '制药/化工/环保', '继续深造(硕博)'],
  '08': ['IT/互联网/通信', '制造业/工程设计', '建筑/土木/交通', '能源/电力/石油', '汽车/航空航天', '科研院所'],
  '09': ['农业企业/种植基地', '农业行政部门', '农业科研院所', '种业/肥料/农药公司', '畜牧/水产/兽医', '生态/环保/NGO'],
  '10': ['各级医院/诊所', '疾控中心/卫健委', '医药企业/器械公司', '科研院所/高校', '社区卫生服务', '医疗保险机构'],
  '12': ['企业管理/咨询', '银行/金融/投行', '互联网/电商运营', '政府/事业单位', '房地产/物业', '物流/供应链'],
  '13': ['设计院/设计公司', '影视/动画/游戏', '演艺/剧团/乐团', '学校/培训机构', '博物馆/美术馆', '自由职业/独立艺术家'],
  '14': ['高科技企业', '科研院所', '智能制造/机器人', '集成电路/半导体', '新能源/碳中和', '继续深造'],
};

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
  console.log('Fetching data...');
  const ref = await fetchAll('moe_2026_reference', 'code,degree,category_code');
  const majors = await fetchAll('majors', 'id,code,name,category');

  const refByCode = {};
  ref.forEach(r => { refByCode[r.code] = r; });

  console.log('Reference entries: ' + ref.length);
  console.log('Major entries: ' + majors.length);

  let updated = 0;
  let failed = 0;
  const degreeStats = {};
  const durStats = {};

  for (const m of majors) {
    const refEntry = refByCode[m.code];
    const catCode = m.code.substring(0, 2);

    // Determine degree
    let degree = null;
    if (refEntry && refEntry.degree) {
      degree = expandDegree(refEntry.degree);
    } else {
      degree = CAT_DEGREE[catCode] || '学士';
    }

    // Determine duration (integer: 4 or 5)
    let duration = isFiveYear(m.code) ? 5 : 4;

    // Determine career directions
    let careerDirections = CAT_CAREERS[catCode] || CAT_CAREERS['08'];
    // For cross-discipline, use specific directions based on subcategory
    if (catCode === '14') {
      careerDirections = CAT_CAREERS['14'];
    }

    const durLabel = duration + '年';
    degreeStats[degree] = (degreeStats[degree] || 0) + 1;
    durStats[durLabel] = (durStats[durLabel] || 0) + 1;

    const body = {
      degree: degree,
      duration: duration,
      career_directions: careerDirections,
    };

    const res = await fetch(SUPABASE_URL + '/rest/v1/majors?id=eq.' + m.id, {
      method: 'PATCH',
      headers: { ...H, 'Prefer': 'return=minimal' },
      body: JSON.stringify(body),
    });

    if (res.ok) {
      updated++;
    } else {
      const err = await res.text();
      console.log('FAIL ' + m.code + ' ' + m.name + ': ' + err.substring(0, 100));
      failed++;
    }

    if (updated % 100 === 0) {
      console.log('  Updated: ' + updated + '/' + majors.length);
      await new Promise(r => setTimeout(r, 50));
    }
  }

  console.log('\n=== Phase 1 Complete ===');
  console.log('Updated: ' + updated + ', Failed: ' + failed);

  console.log('\nDegree distribution:');
  Object.entries(degreeStats).sort().forEach(([k, v]) => {
    console.log('  ' + k + ': ' + v);
  });

  console.log('\nDuration distribution:');
  Object.entries(durStats).sort().forEach(([k, v]) => {
    console.log('  ' + k + ': ' + v);
  });
}

main().catch(e => console.error('FATAL:', e));
