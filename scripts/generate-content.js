// Phase 2: Generate A-level content for empty majors using knowledge base
// Fields: overview, what_you_learn, suitable_for, career_outlook, xuefeng_comment,
//         yearly_courses, top_universities, difficulty, salary_range
const KB = require('./data/knowledge-base.js');

const SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co';
const KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4';
const H = { 'apikey': KEY, 'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json' };

// Course database per subcategory for more accurate course names
const SUBCAT_COURSES = {
  '0101': { '大一': ['哲学导论', '中国哲学史(上)', '西方哲学史(上)', '逻辑学导论'], '大二': ['中国哲学史(下)', '西方哲学史(下)', '伦理学', '马克思主义哲学'], '大三': ['科学哲学', '宗教学', '政治哲学', '现代西方哲学'], '大四': ['毕业论文', '专业实习', '中国哲学原著', '西方哲学原著'] },
  '0201': { '大一': ['高等数学(上)', '政治经济学', '微观经济学', '管理学'], '大二': ['高等数学(下)', '宏观经济学', '会计学', '财政学'], '大三': ['计量经济学', '国际经济学', '金融学', '产业经济学'], '大四': ['毕业论文', '专业实习', '发展经济学', '经济思想史'] },
  '0202': { '大一': ['高等数学(上)', '微观经济学', '财政学导论', '会计学'], '大二': ['宏观经济学', '税收学', '政府预算', '统计学'], '大三': ['中国税制', '国际税收', '税务管理', '公共支出管理'], '大四': ['毕业论文', '税务实习', '税收筹划', '财政政策分析'] },
  '0203': { '大一': ['高等数学(上)', '微观经济学', '金融学导论', '会计学'], '大二': ['宏观经济学', '货币银行学', '公司金融', '投资学'], '大三': ['证券投资学', '国际金融', '金融工程', '风险管理'], '大四': ['毕业论文', '金融机构实习', '金融科技', '固定收益证券'] },
  '0204': { '大一': ['高等数学(上)', '微观经济学', '国际贸易导论', '管理学'], '大二': ['宏观经济学', '国际贸易实务', '国际商法', '统计学'], '大三': ['国际金融', '世界经济', '国际商务谈判', '跨境电商'], '大四': ['毕业论文', '外贸实习', '国际市场营销', '贸易政策分析'] },
  '0301': { '大一': ['法理学', '宪法学', '中国法制史', '民法总论'], '大二': ['刑法总论', '行政法学', '民事诉讼法学', '商法学'], '大三': ['经济法学', '国际法学', '知识产权法', '环境资源法'], '大四': ['毕业实习', '毕业论文', '法律职业伦理', '模拟法庭'] },
  '0302': { '大一': ['政治学原理', '宪法学', '比较政治学', '西方政治思想史'], '大二': ['国际政治学', '公共行政学', '中国政治制度', '政治学研究方法'], '大三': ['国际关系理论', '外交学', '地缘政治学', '公共政策分析'], '大四': ['毕业论文', '政府/国际组织实习', '全球治理', '当代中国政治'] },
  '0303': { '大一': ['社会学概论', '社会研究方法', '社会统计学', '西方社会学理论'], '大二': ['中国社会思想史', '社会心理学', '社会工作导论', '人类学基础'], '大三': ['城市社会学', '经济社会学', '质性研究方法', '社会分层'], '大四': ['毕业论文', '社会调查实习', '社会政策分析', '社区研究'] },
  '0304': { '大一': ['民族学概论', '人类学导论', '中国民族志', '社会学基础'], '大二': ['民族理论与政策', '田野调查方法', '世界民族', '宗教人类学'], '大三': ['民族经济学', '语言人类学', '民族文化遗产', '跨境民族研究'], '大四': ['毕业论文', '田野调查实习', '民族文化保护', '边疆研究'] },
  '0305': { '大一': ['马克思主义哲学原理', '政治经济学', '科学社会主义', '政治学原理'], '大二': ['中共党史', '马克思主义发展史', '思想政治教育学原理', '法学概论'], '大三': ['马克思主义经典著作选读', '思想政治教育方法论', '西方马克思主义', '当代社会思潮'], '大四': ['毕业论文', '思政课教学实习', '比较思想政治教育', '网络思想政治教育'] },
  '0306': { '大一': ['法理学', '宪法学', '刑法学', '公安学基础'], '大二': ['刑事诉讼法学', '行政法学', '治安管理学', '侦查学原理'], '大三': ['刑事科学技术', '犯罪学', '公安情报学', '警察战术'], '大四': ['毕业实习(公安一线)', '毕业论文', '警务实战', '公安管理'] },
  '0401': { '大一': ['教育学原理', '普通心理学', '中国教育史', '教育心理学'], '大二': ['外国教育史', '课程与教学论', '教育统计学', '发展心理学'], '大三': ['教育社会学', '教育管理学', '比较教育学', '教育研究方法'], '大四': ['教育实习', '毕业论文', '教育政策分析', '现代教育技术'] },
  '0402': { '大一': ['运动解剖学', '运动生理学', '体育概论', '田径基础'], '大二': ['运动训练学', '体育心理学', '运动生物力学', '专项训练1'], '大三': ['学校体育学', '体育管理学', '运动营养学', '专项训练2'], '大四': ['教育实习(体育教学)', '毕业论文', '运动康复', '体育产业概论'] },
  '0501': { '大一': ['现代汉语', '古代汉语', '中国现代文学', '文学概论'], '大二': ['中国古代文学(上)', '外国文学(上)', '语言学概论', '基础写作'], '大三': ['中国古代文学(下)', '外国文学(下)', '比较文学', '美学概论'], '大四': ['毕业论文', '毕业实习', '文学批评', '文化研究'] },
  '0502': { '大一': ['基础外语1', '外语语音', '外语语法', '对象国概况'], '大二': ['基础外语2', '外语听力', '外语口语', '外语写作'], '大三': ['高级外语', '外语翻译(笔译)', '外语翻译(口译)', '对象国文学'], '大四': ['毕业论文', '专业实习', '商务外语', '跨文化交际'] },
  '0503': { '大一': ['新闻学概论', '传播学概论', '中国新闻史', '新闻采访'], '大二': ['新闻写作', '新闻编辑', '新闻评论', '广播电视概论'], '大三': ['媒介伦理与法规', '数据新闻', '新媒体概论', '深度报道'], '大四': ['毕业实习(媒体)', '毕业论文/设计', '媒体经营管理', '融合新闻'] },
};

// Function to get best-fit courses for a subcategory
function getCourses(code, defaultCourses) {
  const subKey = code.substring(0, 4);
  if (SUBCAT_COURSES[subKey]) return SUBCAT_COURSES[subKey];
  // For codes not in our detailed list, use category defaults
  return defaultCourses;
}

// Generate what_you_learn based on courses
function generateWhatYouLearn(code, courses) {
  const courseList = [];
  Object.entries(courses).forEach(([year, list]) => {
    courseList.push(...list);
  });
  // Take sample courses and categorize
  const theory = courseList.filter(c => c.match(/原理|概论|导论|基础|史|理论/)).slice(0, 4);
  const methods = courseList.filter(c => c.match(/方法|统计|分析|研究|实验|调查|测量/)).slice(0, 3);
  const applied = courseList.filter(c => !theory.includes(c) && !methods.includes(c) && !c.includes('毕业') && !c.includes('实习')).slice(0, 4);

  let result = '';
  if (theory.length > 0) result += '1）理论基础：' + theory.join('、') + '；';
  if (methods.length > 0) result += '2）分析方法：' + methods.join('、') + '；';
  if (applied.length > 0) result += '3）应用领域：' + applied.join('、') + '；';

  // Core competencies
  const catCode = code.substring(0, 2);
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
  const comps = competences[catCode] || ['专业实践能力', '综合分析能力', '创新思维', '团队协作能力'];
  result += '核心能力：' + comps.join('、') + '。';

  return result;
}

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

function genDifficulty(catCode, majorName, code) {
  // 5-year medical and advanced engineering are harder
  if (['082801', '082802', '080911TK', '080918TK', '080717T'].some(p => code.startsWith(p))) return 5;
  if (catCode === '10') return 5; // Medical
  if (catCode === '14') return 5; // Cross-discipline
  const kb = KB[catCode];
  if (kb) return kb.difficulty || 4;
  return 4;
}

function genSalary(catCode, majorName, code) {
  if (catCode === '08' && KB['08'].isIT({name: majorName})) return KB['08'].salary_IT;
  const kb = KB[catCode];
  if (kb) return kb.salary || '¥6k-18k';
  return '¥6k-18k';
}

function isITMajor(code, name) {
  if (code.substring(0, 2) !== '08') return false;
  return KB['08'].isIT({ name });
}

async function main() {
  console.log('Fetching majors...');
  const majors = await fetchAll('majors', 'id,code,name,category,overview,what_you_learn');

  // Find empty majors (no overview)
  const empty = majors.filter(m => !m.overview);
  // Find majors missing what_you_learn
  const missingWYL = majors.filter(m => m.overview && !m.what_you_learn);

  console.log('Total majors: ' + majors.length);
  console.log('Empty (no content): ' + empty.length);
  console.log('Missing what_you_learn only: ' + missingWYL.length);

  // Process empty majors
  console.log('\n=== Generating content for ' + empty.length + ' empty majors ===');
  let updated = 0, failed = 0;

  for (let i = 0; i < empty.length; i++) {
    const m = empty[i];
    const catCode = m.code.substring(0, 2);
    const kb = KB[catCode];
    if (!kb) {
      console.log('SKIP: ' + m.code + ' ' + m.name + ' (unknown category ' + catCode + ')');
      continue;
    }

    const isIT = (catCode === '08' && KB['08'].isIT(m));
    const courses = getCourses(m.code, kb.courses);
    const difficulty = genDifficulty(catCode, m.name, m.code);
    const salary = genSalary(catCode, m.name, m.code);
    const overviewFn = (isIT && KB['08'].overview_IT) ? KB['08'].overview_IT : kb.overview;
    const xuefengFn = (isIT && KB['08'].xuefeng_IT) ? KB['08'].xuefeng_IT : kb.xuefeng;

    const body = {
      overview: overviewFn(m).substring(0, 500),
      what_you_learn: generateWhatYouLearn(m.code, courses).substring(0, 500),
      suitable_for: kb.suitable(m).substring(0, 500),
      career_outlook: kb.careers.tiers.substring(0, 600),
      xuefeng_comment: xuefengFn(m).substring(0, 800),
      yearly_courses: courses,
      top_universities: kb.unis,
      difficulty: '⭐'.repeat(difficulty),
      salary_range: salary,
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
      console.log('FAIL ' + m.code + ' ' + m.name + ': ' + err.substring(0, 120));
      failed++;
    }

    if (updated % 50 === 0) {
      console.log('  Progress: ' + (i + 1) + '/' + empty.length + ' (updated: ' + updated + ', failed: ' + failed + ')');
      await new Promise(r => setTimeout(r, 100));
    }
  }

  console.log('\nEmpty majors: updated=' + updated + ', failed=' + failed);

  // Process missing what_you_learn
  console.log('\n=== Backfilling what_you_learn for ' + missingWYL.length + ' majors ===');
  let wylUpdated = 0, wylFailed = 0;

  for (const m of missingWYL) {
    const catCode = m.code.substring(0, 2);
    const kb = KB[catCode];
    if (!kb) continue;

    const courses = getCourses(m.code, kb.courses);
    const wyl = generateWhatYouLearn(m.code, courses).substring(0, 500);

    const res = await fetch(SUPABASE_URL + '/rest/v1/majors?id=eq.' + m.id, {
      method: 'PATCH',
      headers: { ...H, 'Prefer': 'return=minimal' },
      body: JSON.stringify({ what_you_learn: wyl }),
    });

    if (res.ok) wylUpdated++;
    else wylFailed++;
  }
  console.log('what_you_learn: updated=' + wylUpdated + ', failed=' + wylFailed);

  console.log('\n=== Phase 2 Complete ===');
  console.log('Total updated: ' + (updated + wylUpdated));
  console.log('Total failed: ' + (failed + wylFailed));
}

main().catch(e => console.error('FATAL:', e));
