// ============================================================
// 专业星图 - 专业适配测评
// 3步问卷 → 匹配883个专业 → 排序推荐
// ============================================================

import '../supabase-client.js';
import '../auth.js';
import '../common.js';
import { escapeHtml, getJsonArray } from '../utils.js';
import { t, createLangSwitcher, onLanguageChange } from '../i18n.js';
import { generateShareCard, downloadShareCard, copyShareCardToClipboard } from '../share-card.js';
import { drawRadarChart, drawMatchBarChart } from '../charts.js';

// ---- 状态 ----
let majorsData = [];
let currentStep = 1;
const answers = {
  subjects: [],           // 学科兴趣（多选）
  learningStyle: null,   // 学习风格（单选）
  interests: {},          // 兴趣程度（5级量表）
  careerValues: [],       // 职业要素排序
  workEnv: null,          // 理想工作环境（单选）
  attitudes: {},          // 态度量表（5级）
  abilities: {},          // 能力自评（5级）
  grades: {},             // 学科成绩（5级）
};
let resultsCache = null;
let lastTraits = [];

const TOTAL_STEPS = 3;

// ---- 常量 ----
const CATEGORY_MAP = {
  '01': '🎓', '02': '💰', '03': '⚖️', '04': '📚',
  '05': '📖', '06': '📜', '07': '🔢', '08': '💻',
  '09': '🌾', '10': '🩺', '12': '📋', '13': '🎭', '14': '🔬',
};

// 学科→门类映射
const SUBJECT_CATEGORY_MAP = {
  '数学': ['07', '08', '02'],
  '物理': ['08', '07'],
  '化学': ['07', '08', '10', '09'],
  '生物': ['10', '09', '07'],
  '计算机': ['08'],
  '语文': ['05', '01', '03'],
  '英语': ['05', '02'],
  '历史': ['06', '01', '03'],
  '政治': ['03', '01', '12'],
  '地理': ['07', '09'],
  '美术': ['13'],
  '音乐': ['13'],
  '体育': ['04'],
};

// IT子类检测关键词
const IT_KEYWORDS = ['计算机', '软件', '网络', '信息安全', '物联网', '数字媒体', '智能科学', '数据科学', '大数据', '网络空间', '新媒体', '虚拟现实', '区块链', '密码', '工业软件', '人工智能', '电影制作', '保密技术', '服务科学', '空间信息'];

// 职业要素映射到匹配逻辑
const CAREER_VALUE_MATCHERS = {
  '高薪资': (major) => {
    const salary = parseFloat(major.salary_range?.replace(/[^0-9.]/g, '')) || 8;
    if (salary >= 30) return 20;
    if (salary >= 20) return 15;
    if (salary >= 10) return 10;
    return 5;
  },
  '工作稳定': (major) => {
    const dirs = getJsonArray(major, 'career_directions');
    const stableKeywords = ['政府', '事业编', '公务员', '国企', '教师', '教育', '医疗', '卫生'];
    const text = dirs.join(' ');
    return stableKeywords.some(k => text.includes(k)) ? 20 : 5;
  },
  '社会贡献': (major) => {
    const contribCats = ['10', '04', '09'];
    const catCode = (major.category || '').split(' ')[0];
    return contribCats.includes(catCode) ? 20 : 8;
  },
  '创造力': (major) => {
    const creativeCats = ['13', '05', '08'];
    const catCode = (major.category || '').split(' ')[0];
    if (creativeCats.includes(catCode)) return 20;
    const dirs = getJsonArray(major, 'career_directions');
    const creativeKeywords = ['设计', '创意', '创作', '艺术', '策划', '研发'];
    const text = dirs.join(' ');
    return creativeKeywords.some(k => text.includes(k)) ? 15 : 8;
  },
  '人际关系': (major) => {
    const socialCats = ['03', '04', '12', '05'];
    const catCode = (major.category || '').split(' ')[0];
    if (socialCats.includes(catCode)) return 20;
    const dirs = getJsonArray(major, 'career_directions');
    const socialKeywords = ['管理', '咨询', '教育', '培训', '销售', '市场', '公关', '人力资源'];
    const text = dirs.join(' ');
    return socialKeywords.some(k => text.includes(k)) ? 15 : 8;
  },
  '自主性': (major) => {
    const dirs = getJsonArray(major, 'career_directions');
    const autoKeywords = ['创业', '自由', '独立', '咨询', '设计'];
    const text = dirs.join(' ');
    return autoKeywords.some(k => text.includes(k)) ? 18 : 8;
  },
};

// 特质关键词（用于 suitable_for 匹配）
const TRAIT_POSITIVE = {
  '逻辑型': ['逻辑思维', '逻辑分析', '推理能力', '逻辑推理', '逻辑思维缜密', '逻辑思维强', '逻辑思维清晰', '数学基础扎实', '数理基础扎实', '善于分析因果', '抽象推理'],
  '数理型': ['数学基础', '数理基础', '数学和计算', '理科学得', '数理能力', '计算能力', '微积分', '概率论', '数量分析', '数字敏感'],
  '研究型': ['钻研精神', '探究', '研究', '好奇心', '探索', '实验', '科研', '耐得住', '深造', '读研', '读博', '博士'],
  '动手型': ['动手能力', '实践能力', '动手操作', '工程技术', '实验', '操作能力', '手巧', '实操', '实践动手'],
  '记忆型': ['记忆力好', '记忆', '背诵', '记忆力强', '能应对大量法条', '掌握大量'],
  '表达型': ['语言表达', '表达能力', '写作', '文笔', '口头辩论', '沟通表达', '文字功底', '文字表达', '善于书面'],
  '创造型': ['创造力', '创新', '创意', '想象力', '设计能力', '空间想象', '审美能力', '艺术'],
  '社交型': ['沟通', '团队', '组织', '领导', '管理', '协调', '帮助他人', '社会责任感', '正义感', '人际交往'],
  '抗压型': ['抗压能力', '能吃苦', '高强度', '心理素质', '抗压能力强', '耐得住寂寞'],
  '细致型': ['细心', '有耐心', '耐心', '细致', '严谨', '细致入微', '一丝不苟'],
};

const TRAIT_NEGATIVE = {
  '逻辑型': ['逻辑思维混乱', '数学偏科', '逻辑不清'],
  '数理型': ['数学严重偏科', '数学偏科', '对数字不敏感'],
  '动手型': ['不喜欢动手', '动手能力差', '拒绝体力劳动'],
  '记忆型': ['不喜欢背书', '记忆力差'],
  '表达型': ['文字功底差', '表达能力差', '对文字工作无兴趣', '不喜欢读书写作', '不喜欢写作'],
  '社交型': ['不喜欢沟通', '性格内向'],
  '抗压型': ['抗压能力弱', '不能吃苦'],
  '创造型': ['缺乏创意'],
};

// 问卷定义
const QUESTIONNAIRE = {
  step1: {
    title: '学科兴趣',
    subtitle: '了解你喜欢什么、擅长什么',
    questions: [
      {
        id: 'subjects',
        type: 'multi',
        label: '你最喜欢的高中学科（最多选3个）',
        hint: '选择你学得最轻松、最有成就感的学科',
        options: [
          { value: '数学', emoji: '📐' },
          { value: '物理', emoji: '⚡' },
          { value: '化学', emoji: '🧪' },
          { value: '生物', emoji: '🧬' },
          { value: '计算机', emoji: '💻' },
          { value: '语文', emoji: '📝' },
          { value: '英语', emoji: '🌍' },
          { value: '历史', emoji: '📜' },
          { value: '政治', emoji: '⚖️' },
          { value: '地理', emoji: '🌏' },
          { value: '美术', emoji: '🎨' },
          { value: '音乐', emoji: '🎵' },
          { value: '体育', emoji: '🏃' },
        ],
        maxSelect: 3,
      },
      {
        id: 'learningStyle',
        type: 'single-card',
        label: '你的学习风格偏好是？',
        hint: '选择最符合你日常学习习惯的描述',
        options: [
          { value: 'theoretical', emoji: '📖', label: '理论学习型', desc: '喜欢阅读、推理、推导公式' },
          { value: 'practical', emoji: '🔧', label: '实践动手型', desc: '喜欢做实验、操作、制作' },
          { value: 'exploratory', emoji: '🔍', label: '研究探索型', desc: '喜欢深入钻研、发现问题' },
          { value: 'creative', emoji: '✨', label: '创作表达型', desc: '喜欢写作、设计、艺术创作' },
        ],
      },
      {
        id: 'interests',
        type: 'likert',
        label: '对以下活动的兴趣程度',
        hint: '1 = 完全不想碰，5 = 非常喜欢',
        items: [
          { id: 'experiment', label: '做实验、收集数据、观察现象' },
          { id: 'writing', label: '写文章、分析文本、阅读经典' },
          { id: 'coding', label: '编程、使用工具解决问题' },
          { id: 'social', label: '与人沟通、帮助他人、组织活动' },
        ],
      },
    ],
  },
  step2: {
    title: '职业偏好',
    subtitle: '了解你想要的职业是什么样的',
    questions: [
      {
        id: 'careerValues',
        type: 'rank',
        label: '你最看重的职业要素（按重要性选3项）',
        hint: '点击选项按顺序选择，第1个最重要',
        options: [
          { value: '高薪资', emoji: '💰' },
          { value: '工作稳定', emoji: '🛡️' },
          { value: '社会贡献', emoji: '🌟' },
          { value: '创造力', emoji: '💡' },
          { value: '自主性', emoji: '🚀' },
          { value: '人际关系', emoji: '🤝' },
        ],
        maxSelect: 3,
      },
      {
        id: 'workEnv',
        type: 'single-card',
        label: '你理想的未来工作环境是？',
        hint: '选择最符合你愿景的工作场所',
        options: [
          { value: 'corporate', emoji: '🏢', label: '大公司/机构', desc: '知名企业，体系完善，晋升清晰' },
          { value: 'sme', emoji: '🏭', label: '中小企业', desc: '多元角色，成长快，贴近业务' },
          { value: 'startup', emoji: '🚀', label: '自由职业/创业', desc: '时间自由，自我驱动，高风险高回报' },
          { value: 'academic', emoji: '🎓', label: '高校/科研院所', desc: '学术氛围，深耕领域，稳定' },
          { value: 'gov', emoji: '🏛️', label: '政府/事业单位', desc: '稳定，服务公众，规范' },
        ],
      },
      {
        id: 'attitudes',
        type: 'likert',
        label: '对以下说法的同意程度',
        hint: '1 = 完全不同意，5 = 完全同意',
        items: [
          { id: 'keep_studying', label: '我愿意持续学习到硕士/博士' },
          { id: 'overtime_ok', label: '我不介意为了事业经常加班' },
          { id: 'small_city_ok', label: '我愿意去小城市或基层工作' },
          { id: 'change_world', label: '我要做能直接改变世界的事情' },
        ],
      },
    ],
  },
  step3: {
    title: '自我评估',
    subtitle: '客观评估你的能力和基础',
    questions: [
      {
        id: 'abilities',
        type: 'likert',
        label: '能力自评',
        hint: '1 = 较弱，5 = 很强。请客观评价自己当前的能力水平',
        items: [
          { id: 'math_logic', label: '数学逻辑能力 — 推导、计算、分析' },
          { id: 'verbal', label: '语言表达能力 — 写作、演讲、沟通' },
          { id: 'hands_on', label: '动手操作能力 — 实验、制作、工具使用' },
          { id: 'memory', label: '记忆背诵能力 — 记忆、复述、积累' },
          { id: 'spatial', label: '空间想象能力 — 三维空间、图形、设计' },
          { id: 'stress', label: '抗压能力 — 高强度、多任务、紧迫时限' },
        ],
      },
      {
        id: 'grades',
        type: 'likert',
        label: '学科成绩水平',
        hint: '1 = 不及格/较差，5 = 年级前列。评估各学科的掌握程度',
        items: [
          { id: 'math', label: '数学 — 函数、几何、概率等' },
          { id: 'physics', label: '物理 — 力学、电磁学等' },
          { id: 'chemistry', label: '化学 — 反应、结构、实验等' },
          { id: 'chinese', label: '语文 — 阅读、写作、文言文等' },
          { id: 'english', label: '英语 — 听说读写综合' },
          { id: 'cs', label: '信息技术 — 编程基础、计算机操作' },
        ],
      },
    ],
  },
};

// ---- DOM 工具 ----
function $(sel) { return document.querySelector(sel); }
function $$(sel) { return document.querySelectorAll(sel); }

// ---- 渲染步骤 ----
function renderStep(stepNum) {
  const stepDef = QUESTIONNAIRE[`step${stepNum}`];
  const quizCard = $('#quizCard');
  const progressFill = $('#progressFill');
  const progressSteps = $$('.progress-step');

  // 更新进度条
  const pct = ((stepNum - 1) / TOTAL_STEPS) * 100;
  progressFill.style.width = pct + '%';
  progressSteps.forEach((s, i) => {
    s.classList.remove('active', 'done');
    if (i + 1 < stepNum) s.classList.add('done');
    if (i + 1 === stepNum) s.classList.add('active');
  });

  // 渲染问题
  let html = '';
  stepDef.questions.forEach((q, qi) => {
    html += `<div class="quiz-question-group">`;
    html += `<div class="quiz-question-label"><span class="q-num">${qi + 1}</span>${t(`q_${q.id}`, q.label)}</div>`;
    if (q.hint) html += `<div class="quiz-question-hint">${t(`q_${q.id}_hint`, q.hint)}</div>`;

    if (q.type === 'multi') {
      html += `<div class="option-grid" data-q="${q.id}">`;
      q.options.forEach((opt) => {
        const sel = (answers[q.id] || []).includes(opt.value) ? ' selected' : '';
        html += `<button class="option-btn${sel}" data-value="${opt.value}"><span class="option-emoji">${opt.emoji}</span>${opt.value}</button>`;
      });
      html += `</div>`;
    } else if (q.type === 'single-card') {
      html += `<div class="option-cards" data-q="${q.id}">`;
      q.options.forEach((opt) => {
        const sel = answers[q.id] === opt.value ? ' selected' : '';
        html += `<div class="option-card${sel}" data-value="${opt.value}">
          <span class="card-emoji">${opt.emoji}</span>
          <span class="card-label">${opt.label}</span>
          <span class="card-desc">${opt.desc}</span>
        </div>`;
      });
      html += `</div>`;
    } else if (q.type === 'rank') {
      html += `<div class="rank-options" data-q="${q.id}">`;
      const rankedValues = (answers[q.id] || []);
      q.options.forEach((opt) => {
        const idx = rankedValues.indexOf(opt.value);
        const isRanked = idx !== -1;
        html += `<button class="rank-option${isRanked ? ' ranked' : ''}" data-value="${opt.value}">
          <span class="rank-num${isRanked ? '' : ' empty'}">${isRanked ? idx + 1 : '?'}</span>
          <span>${opt.emoji}</span> ${opt.value}
        </button>`;
      });
      html += `</div>`;
      html += `<div class="rank-hint">${t('q_careerValues_hint2', '点击选项选定，再次点击已选中的可取消，按顺序排列优先级')}</div>`;
    } else if (q.type === 'likert') {
      html += `<div data-q="${q.id}">`;
      q.items.forEach((item) => {
        const currentVal = (answers[q.id] || {})[item.id] || 0;
        html += `<div class="likert-row" data-item="${item.id}">
          <span class="likert-label">${item.label}</span>
          <div class="likert-options">`;
        for (let v = 1; v <= 5; v++) {
          html += `<button class="likert-btn${v === currentVal ? ' selected' : ''}" data-v="${v}">${v}</button>`;
        }
        html += `</div></div>`;
      });
      html += `</div>`;
    }
    html += `</div>`;
  });

  quizCard.innerHTML = html;
  bindCardEvents(stepDef);

  // 更新按钮
  const btnPrev = $('#btnPrev');
  const btnNext = $('#btnNext');
  const btnSubmit = $('#btnSubmit');

  btnPrev.style.display = stepNum > 1 ? '' : 'none';
  btnNext.style.display = stepNum < TOTAL_STEPS ? '' : 'none';
  btnSubmit.style.display = stepNum === TOTAL_STEPS ? '' : 'none';

  if (stepNum === TOTAL_STEPS) {
    btnSubmit.textContent = t('view_results', '查看结果');
  }

  // 翻译按钮文字
  btnPrev.textContent = t('btn_prev', '← 上一步');
  btnNext.textContent = t('btn_next', '下一步 →');
}

function bindCardEvents(stepDef) {
  stepDef.questions.forEach((q) => {
    const container = $(`[data-q="${q.id}"]`);
    if (!container) return;

    if (q.type === 'multi') {
      container.querySelectorAll('.option-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          const val = btn.dataset.value;
          let selected = answers[q.id] || [];
          if (selected.includes(val)) {
            selected = selected.filter(v => v !== val);
          } else if (selected.length < (q.maxSelect || 99)) {
            selected = [...selected, val];
          }
          answers[q.id] = selected;
          renderStep(currentStep);
        });
      });
    } else if (q.type === 'single-card') {
      container.querySelectorAll('.option-card').forEach(card => {
        card.addEventListener('click', () => {
          const val = card.dataset.value;
          answers[q.id] = answers[q.id] === val ? null : val;
          renderStep(currentStep);
        });
      });
    } else if (q.type === 'rank') {
      container.querySelectorAll('.rank-option').forEach(btn => {
        btn.addEventListener('click', () => {
          const val = btn.dataset.value;
          let ranked = answers[q.id] || [];
          if (ranked.includes(val)) {
            ranked = ranked.filter(v => v !== val);
          } else if (ranked.length < (q.maxSelect || 99)) {
            ranked = [...ranked, val];
          }
          answers[q.id] = ranked;
          renderStep(currentStep);
        });
      });
    } else if (q.type === 'likert') {
      container.querySelectorAll('.likert-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          const v = parseInt(btn.dataset.v);
          const row = btn.closest('.likert-row');
          const itemId = row.dataset.item;
          if (!answers[q.id]) answers[q.id] = {};
          answers[q.id][itemId] = answers[q.id][itemId] === v ? 0 : v;
          renderStep(currentStep);
        });
      });
    }
  });
}

// ---- 步骤验证 ----
function canProceed(stepNum) {
  const stepDef = QUESTIONNAIRE[`step${stepNum}`];
  for (const q of stepDef.questions) {
    const ans = answers[q.id];
    if (q.type === 'multi' || q.type === 'rank') {
      if (!ans || ans.length === 0) return false;
    } else if (q.type === 'single-card') {
      if (!ans) return false;
    } else if (q.type === 'likert') {
      if (!ans || Object.keys(ans).length === 0) return false;
      for (const item of q.items) {
        if (!ans[item.id]) return false;
      }
    }
  }
  return true;
}

// ---- 匹配引擎 ----
function getTraitProfile() {
  const traits = [];
  // 从量表推断特质
  const interests = answers.interests || {};
  const abilities = answers.abilities || {};
  const grades = answers.grades || {};

  // 理科倾向
  const stemScore = (interests.experiment || 0) + (interests.coding || 0) +
    (abilities.math_logic || 0) + (grades.math || 0) + (grades.physics || 0);
  if (stemScore >= 15) traits.push('数理型');
  if ((interests.coding || 0) + (abilities.math_logic || 0) >= 7) traits.push('逻辑型');

  // 研究倾向
  if (answers.learningStyle === 'exploratory' || answers.learningStyle === 'theoretical') traits.push('研究型');
  if ((answers.attitudes || {}).keep_studying >= 4) traits.push('研究型');

  // 实践动手
  if (answers.learningStyle === 'practical') traits.push('动手型');
  if ((abilities.hands_on || 0) >= 4) traits.push('动手型');

  // 记忆型
  if ((abilities.memory || 0) >= 4) traits.push('记忆型');

  // 表达型
  const verbalScore = (interests.writing || 0) + (abilities.verbal || 0) + (grades.chinese || 0) + (grades.english || 0);
  if (verbalScore >= 13) traits.push('表达型');

  // 创造型
  if (answers.learningStyle === 'creative') traits.push('创造型');
  if ((abilities.spatial || 0) >= 4 && answers.learningStyle === 'creative') traits.push('创造型');

  // 社交型
  if ((interests.social || 0) >= 4) traits.push('社交型');

  // 抗压型
  if ((abilities.stress || 0) >= 4) traits.push('抗压型');
  if ((answers.attitudes || {}).overtime_ok >= 4) traits.push('抗压型');

  // 细致型
  if ((abilities.memory || 0) >= 3 && (grades.chemistry || 0) >= 4) traits.push('细致型');

  // 去重
  return [...new Set(traits)];
}

function getAbilityLevel() {
  const ab = answers.abilities || {};
  const scores = Object.values(ab).filter(v => typeof v === 'number');
  if (scores.length === 0) return 3;
  const avg = scores.reduce((a, b) => a + b, 0) / scores.length;
  return Math.round(avg);
}

function matchCategory(major) {
  const catCode = (major.category || '').split(' ')[0];
  const subjects = answers.subjects || [];
  if (!subjects.length) return 20; // 未选学科，不偏不倚

  let maxScore = 0;
  for (const subj of subjects) {
    const cats = SUBJECT_CATEGORY_MAP[subj] || [];
    if (cats.includes(catCode)) {
      // 检查是否是IT类
      if (catCode === '08' && subj === '计算机') {
        const isIT = IT_KEYWORDS.some(k => (major.name || '').includes(k));
        if (isIT) maxScore = Math.max(maxScore, 40);
        else maxScore = Math.max(maxScore, 30);
      } else {
        maxScore = Math.max(maxScore, 40);
      }
    }
  }

  // 部分匹配：学习风格暗示的领域
  if (maxScore === 0) {
    const style = answers.learningStyle;
    if (style === 'theoretical' && ['01', '02', '07'].includes(catCode)) maxScore = 20;
    if (style === 'practical' && ['08', '10', '09'].includes(catCode)) maxScore = 20;
    if (style === 'exploratory' && ['07', '10', '14'].includes(catCode)) maxScore = 20;
    if (style === 'creative' && ['05', '13', '08'].includes(catCode)) maxScore = 20;
  }

  return maxScore;
}

function matchSuitableFor(major, traits) {
  const text = major.suitable_for || '';
  let matches = 0;
  let penalty = 0;

  for (const trait of traits) {
    const keywords = TRAIT_POSITIVE[trait] || [];
    if (keywords.some(k => text.includes(k))) {
      matches++;
    }
  }

  // 检查慎报关键词
  for (const trait of traits) {
    const negKeywords = TRAIT_NEGATIVE[trait] || [];
    if (negKeywords.some(k => text.includes(k))) {
      penalty = 10;
    }
  }

  if (matches >= 3) return 25 - penalty;
  if (matches === 2) return 18 - penalty;
  if (matches === 1) return 10 - penalty;
  return Math.max(0, 5 - penalty);
}

function matchCareerPreference(major) {
  const values = answers.careerValues || [];
  if (!values.length) return 12;

  // 取优先级最高的要素权重
  let maxScore = 0;
  const weights = [1.0, 0.7, 0.5]; // 第1选100%权重，第2选70%，第3选50%
  for (let i = 0; i < values.length; i++) {
    const matcher = CAREER_VALUE_MATCHERS[values[i]];
    if (matcher) {
      const raw = matcher(major);
      maxScore = Math.max(maxScore, Math.round(raw * weights[i]));
    }
  }
  return maxScore;
}

function matchAbility(major) {
  const difficultyStr = major.difficulty || '⭐⭐⭐';
  const difficulty = (difficultyStr.match(/⭐/g) || []).length;
  const abilityLevel = getAbilityLevel();

  const diff = abilityLevel - difficulty;
  if (diff >= 0) return 15;
  if (diff === -1) return 10;
  if (diff === -2) return 5;
  return 0;
}

function matchWorkEnv(major) {
  const env = answers.workEnv;
  const dirs = getJsonArray(major, 'career_directions');
  const text = dirs.join(' ').toLowerCase();

  const envMap = {
    'corporate': ['企业', '公司', '银行', '证券', '基金', '咨询', '事务所', 'it'],
    'sme': ['中小企业', '创业', '公司'],
    'startup': ['创业', '互联网', '新媒体', '自由', '设计'],
    'academic': ['高校', '科研', '研究院', '教育', '学术'],
    'gov': ['政府', '事业编', '公务员', '体制', '机关', '行政'],
  };

  const keywords = envMap[env] || [];
  if (keywords.some(k => text.includes(k) || dirs.some(d => d.includes(k)))) {
    return 5; // 额外加分
  }
  return 0;
}

function matchAttitudes(major) {
  const att = answers.attitudes || {};
  let bonus = 0;
  const catCode = (major.category || '').split(' ')[0];

  // 愿意深造 → 适合需要读研的专业（理学、医学）
  if (att.keep_studying >= 4 && ['07', '10', '01'].includes(catCode)) bonus += 3;

  // 愿意加班 → 适合高强度专业（医学、IT）
  if (att.overtime_ok >= 4 && ['10', '08'].includes(catCode)) bonus += 2;

  // 愿意去小城市 → 农学、教育、医学
  if (att.small_city_ok >= 4 && ['09', '04', '10'].includes(catCode)) bonus += 3;

  // 改变世界 → 工科、医学、交叉学科
  if (att.change_world >= 4 && ['08', '10', '14'].includes(catCode)) bonus += 2;

  return bonus;
}

function calculateScore(major) {
  const traits = getTraitProfile();
  const catScore = matchCategory(major);
  const traitScore = matchSuitableFor(major, traits);
  const careerScore = matchCareerPreference(major);
  const abilityScore = matchAbility(major);
  const envBonus = matchWorkEnv(major);
  const attBonus = matchAttitudes(major);

  const total = catScore + traitScore + careerScore + abilityScore + envBonus + attBonus;

  return {
    total,
    catScore,
    traitScore,
    careerScore,
    abilityScore,
    envBonus,
    attBonus,
  };
}

function computeResults() {
  const scored = majorsData.map(major => {
    const scores = calculateScore(major);
    return { major, ...scores };
  });

  scored.sort((a, b) => b.total - a.total);

  // 归一化到百分制
  const maxScore = scored.length > 0 ? scored[0].total : 100;
  return scored.slice(0, 50).map((item, idx) => ({
    ...item,
    rank: idx + 1,
    percentage: Math.round((item.total / Math.max(maxScore, 1)) * 100),
  }));
}

// ---- 结果渲染 ----
function renderResults(results) {
  const section = $('#resultsSection');
  const quizSection = $('#quizSection');
  const progressWrap = $('#progressBarWrap');

  quizSection.style.display = 'none';
  progressWrap.style.display = 'none';
  section.style.display = '';

  // 副标题
  const traits = getTraitProfile();
  lastTraits = traits;
  const topCats = getTopCategories(results);
  $('#resultsSubtitle').textContent = `基于你的 ${traits.length} 个特质维度，从 ${majorsData.length} 个专业中匹配出最佳选择`;

  // 摘要标签
  const summaryDiv = $('#resultsSummary');
  summaryDiv.innerHTML = [
    ...traits.map(t => `<span class="summary-tag">🧠 ${t}</span>`),
    ...topCats.map(c => `<span class="summary-tag">📚 ${c}</span>`),
  ].join('');

  // 结果列表
  const list = $('#resultsList');
  list.innerHTML = results.slice(0, 20).map(r => renderResultCard(r)).join('');

  bindResultEvents(results);

  // 绘制图表
  const radarContainer = document.getElementById('radarChart');
  if (radarContainer) {
    drawRadarChart(radarContainer, answers.abilities || {});
  }
  const barContainer = document.getElementById('barChart');
  if (barContainer) {
    drawMatchBarChart(barContainer, results.slice(0, 3).map(r => ({
      name: r.major.name,
      percentage: r.percentage,
    })));
  }

  // 更新结果底部按钮区域
  updateResultsFooter(results);

  // 检查是否有历史保存结果
  checkSavedState();
}

function renderResultCard(item) {
  const m = item.major;
  const catIcon = CATEGORY_MAP[(m.category || '').split(' ')[0]] || '📚';
  const difficulty = m.difficulty || '⭐⭐⭐';
  const inCompare = (window.__compareList || []).some(c => c.code === m.code);
  const isTop1 = item.rank === 1;

  return `
    <div class="result-card" data-code="${escapeHtml(m.code)}" data-major='${JSON.stringify(m).replace(/'/g, "&#39;")}'>
      <div class="result-rank${isTop1 ? ' top1' : ''}">${isTop1 ? '👑' : '#' + item.rank}</div>
      <div class="result-icon">${catIcon}</div>
      <div class="result-info">
        <div class="result-name">${escapeHtml(m.name)}</div>
        <div class="result-category">${escapeHtml(m.category)} · ${escapeHtml(m.degree || '')}</div>
        <div class="result-meta">
          <span class="result-meta-tag">${escapeHtml(difficulty)}</span>
          <span class="result-meta-tag">${escapeHtml(m.salary_range || '')}</span>
        </div>
      </div>
      <div class="result-score-col">
        <div class="result-score">${item.percentage}%</div>
        <div class="result-score-label">匹配度</div>
      </div>
      <div class="result-actions-col">
        <button class="btn-result-action btn-result-detail" data-action="detail" data-code="${escapeHtml(m.code)}">📋 详情</button>
        <button class="btn-result-action ${inCompare ? 'btn-result-compare remove' : 'btn-result-compare'}" data-action="compare" data-code="${escapeHtml(m.code)}">
          ${inCompare ? '✓ 已加入' : '+ 对比'}
        </button>
        <button class="btn-result-action btn-result-fav" data-action="fav" data-code="${escapeHtml(m.code)}">♡</button>
      </div>
    </div>
  `;
}

async function updateResultsFooter(results) {
  const footer = document.getElementById('resultsFooterArea');
  if (!footer) return;

  const shareBtnHTML = `<button class="btn btn-outline" id="btnShare" style="padding:14px 28px;border-radius:14px;font-size:15px;font-weight:600;cursor:pointer;font-family:inherit;background:transparent;border:2px solid var(--outline);color:var(--on-surface-variant);transition:all .3s;">${t('share_results', '📤 分享结果')}</button>`;

  const userId = await getCurrentUserId();
  if (userId) {
    footer.innerHTML = `
      <button class="btn btn-primary" id="btnSave" style="padding:14px 28px;border-radius:14px;font-size:15px;font-weight:600;cursor:pointer;font-family:inherit;background:var(--primary);color:#fff;border:none;transition:all .3s;">${t('save_results', '💾 保存结果')}</button>
      ${shareBtnHTML}
      <button class="btn btn-outline" id="btnRetake" style="padding:14px 28px;border-radius:14px;font-size:15px;font-weight:600;cursor:pointer;font-family:inherit;background:transparent;border:2px solid var(--outline);color:var(--on-surface-variant);transition:all .3s;">${t('retake', '🔄 重新测评')}</button>
      <a href="majors.html" class="btn btn-outline" style="padding:14px 28px;border-radius:14px;font-size:15px;font-weight:600;cursor:pointer;font-family:inherit;background:transparent;border:2px solid var(--outline);color:var(--on-surface-variant);text-decoration:none;transition:all .3s;">${t('browse_all', '📚 浏览全部专业')}</a>
    `;

    const btnSave = document.getElementById('btnSave');
    if (btnSave) {
      btnSave.addEventListener('click', saveResults);
    }
    bindShareAndRetake();
  } else {
    footer.innerHTML = `
      <div style="text-align:center;margin-bottom:16px;">
        <div class="login-prompt">${t('login_save_prompt', '登录后可保存测评结果')}<br>
          <a href="login.html?redirect=assessment.html" style="color:var(--primary);font-weight:600;text-decoration:none;">${t('nav_login', '登录')}</a>
          &nbsp;·&nbsp;
          <a href="register.html?redirect=assessment.html" style="color:var(--primary);font-weight:600;text-decoration:none;">${t('nav_register', '注册')}</a>
        </div>
      </div>
      ${shareBtnHTML}
      <button class="btn btn-outline" id="btnRetake" style="padding:14px 28px;border-radius:14px;font-size:15px;font-weight:600;cursor:pointer;font-family:inherit;background:transparent;border:2px solid var(--outline);color:var(--on-surface-variant);transition:all .3s;">${t('retake', '🔄 重新测评')}</button>
      <a href="majors.html" class="btn btn-outline" style="padding:14px 28px;border-radius:14px;font-size:15px;font-weight:600;cursor:pointer;font-family:inherit;background:transparent;border:2px solid var(--outline);color:var(--on-surface-variant);text-decoration:none;transition:all .3s;">${t('browse_all', '📚 浏览全部专业')}</a>
    `;

    bindShareAndRetake();
  }
}

function bindShareAndRetake() {
  const btnRetake = document.getElementById('btnRetake');
  if (btnRetake) {
    btnRetake.addEventListener('click', resetQuiz);
  }

  const btnShare = document.getElementById('btnShare');
  if (btnShare) {
    btnShare.addEventListener('click', handleShare);
  }
}

async function handleShare() {
  if (!resultsCache || !resultsCache.length) return;

  const btnShare = document.getElementById('btnShare');
  if (btnShare) {
    btnShare.textContent = t('share_generating', '生成中...');
    btnShare.disabled = true;
  }

  try {
    const dataURL = await generateShareCard(resultsCache, lastTraits);

    // 尝试复制到剪贴板，失败则下载
    try {
      await copyShareCardToClipboard(dataURL);
      showToast(t('share_copy_success', '分享图片已复制到剪贴板，可直接粘贴发送！'), 'success');
    } catch {
      // 降级：触发下载
      downloadShareCard(dataURL);
      showToast(t('share_download_success', '分享图片已下载，可直接发送给朋友！'), 'success');
    }
  } catch (err) {
    console.error('Share card generation failed:', err);
    showToast(t('share_fail', '生成分享卡片失败，请重试'), 'error');
  } finally {
    if (btnShare) {
      btnShare.textContent = t('share_results', '📤 分享结果');
      btnShare.disabled = false;
    }
  }
}

async function checkSavedState() {
  const userId = await getCurrentUserId();
  if (!userId) return;
  try {
    const sb = window.supabaseClient?.getSupabase ? window.supabaseClient.getSupabase() : null;
    if (!sb) return;
    const { data } = await sb.from('assessment_results')
      .select('user_id')
      .eq('user_id', userId)
      .maybeSingle();
    if (data) {
      updateSaveButtonState(true);
    }
  } catch (e) { /* ignore */ }
}

function bindResultEvents(results) {
  const list = $('#resultsList');

  list.querySelectorAll('[data-action="detail"]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const code = btn.dataset.code;
      const item = results.find(r => r.major.code === code);
      if (item && window.openModal) {
        window.openModal(item.major);
      }
    });
  });

  list.querySelectorAll('[data-action="compare"]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const code = btn.dataset.code;
      const item = results.find(r => r.major.code === code);
      if (!item) return;
      if (window.addToCompare) {
        window.addToCompare(item.major);
      }
      // 重新渲染结果以更新按钮状态
      setTimeout(() => renderResults(results), 100);
    });
  });

  // 收藏按钮
  list.querySelectorAll('[data-action="fav"]').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.stopPropagation();
      const code = btn.dataset.code;
      if (!window.toggleFavorite) return;
      const result = await window.toggleFavorite(code);
      if (result !== null) {
        updateResultFavButtonUI(btn, code);
      }
    });
  });

  // 初始化收藏按钮状态
  list.querySelectorAll('[data-action="fav"]').forEach(btn => {
    updateResultFavButtonUI(btn, btn.dataset.code);
  });

  // 点击整个卡片查看详情
  list.querySelectorAll('.result-card').forEach(card => {
    card.addEventListener('click', () => {
      const code = card.dataset.code;
      const item = results.find(r => r.major.code === code);
      if (item && window.openModal) {
        window.openModal(item.major);
      }
    });
  });
}

function getTopCategories(results) {
  const catCount = {};
  results.slice(0, 20).forEach(r => {
    const cat = r.major.category || '';
    catCount[cat] = (catCount[cat] || 0) + 1;
  });
  return Object.entries(catCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3)
    .map(([cat]) => cat);
}

// ---- 状态管理 ----
function goToStep(step) {
  if (step < 1 || step > TOTAL_STEPS) return;
  if (step > currentStep && !canProceed(currentStep)) {
    showToast(t('fill_all_required', '请完成当前步骤的所有问题后再继续'));
    return;
  }
  currentStep = step;
  renderStep(step);
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function submitQuiz() {
  if (!canProceed(TOTAL_STEPS)) {
    showToast(t('fill_all_required', '请完成所有问题后再查看结果'));
    return;
  }
  if (!majorsData.length) {
    showToast(t('data_not_loaded', '专业数据尚未加载完成，请稍候'));
    return;
  }

  // 更新进度条到100%
  const progressFill = $('#progressFill');
  progressFill.style.width = '100%';
  $$('.progress-step').forEach((s, i) => {
    s.classList.remove('active');
    s.classList.add('done');
  });

  // 计算并渲染结果
  resultsCache = computeResults();
  renderResults(resultsCache);

  // 重置保存按钮状态
  updateSaveButtonState(false);
}

function resetQuiz() {
  answers.subjects = [];
  answers.learningStyle = null;
  answers.interests = {};
  answers.careerValues = [];
  answers.workEnv = null;
  answers.attitudes = {};
  answers.abilities = {};
  answers.grades = {};
  resultsCache = null;
  currentStep = 1;

  $('#quizSection').style.display = '';
  $('#resultsSection').style.display = 'none';
  $('#progressBarWrap').style.display = '';
  $('#progressFill').style.width = '0%';
  $$('.progress-step').forEach(s => s.classList.remove('active', 'done'));

  renderStep(1);
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function updateResultFavButtonUI(btn, code) {
  if (!btn) return;
  const isFav = window.__userFavorites && window.__userFavorites.has(code);
  btn.textContent = isFav ? '❤' : '♡';
  btn.classList.toggle('favorited', isFav);
}

function showToast(msg, type) {
  if (window.auth && window.auth.showToast) {
    window.auth.showToast(msg, type || 'error');
    return;
  }
  const container = $('#toastContainer');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = 'toast ' + (type === 'success' ? 'toast-success' : 'toast-error');
  toast.textContent = msg;
  container.appendChild(toast);
  setTimeout(() => { toast.remove(); }, 3000);
}

// ---- 保存/加载逻辑 ----
async function getCurrentUserId() {
  try {
    if (window.auth && window.auth.getCurrentUser) {
      const user = await window.auth.getCurrentUser();
      return user ? user.id : null;
    }
  } catch (e) { /* not logged in */ }
  return null;
}

async function saveResults() {
  if (!resultsCache || !resultsCache.length) return;
  const userId = await getCurrentUserId();
  if (!userId) {
    showToast(t('login_required_save', '请先登录后再保存结果'), 'error');
    return;
  }

  try {
    const sb = window.supabaseClient?.getSupabase ? window.supabaseClient.getSupabase() : null;
    if (!sb) throw new Error('Supabase not available');

    const saveData = {
      user_id: userId,
      answers,
      results: resultsCache.slice(0, 20).map(r => ({
        code: r.major.code,
        name: r.major.name,
        category: r.major.category,
        percentage: r.percentage,
        rank: r.rank,
      })),
    };

    const { error } = await sb.from('assessment_results').upsert(saveData, { onConflict: 'user_id' });
    if (error) throw error;

    showToast(t('save_success', '结果已保存！下次访问可直接查看'), 'success');
    updateSaveButtonState(true);
  } catch (err) {
    console.error('Save assessment results failed:', err);
    showToast(t('save_fail', '保存失败，请重试'), 'error');
  }
}

async function loadSavedResults() {
  const userId = await getCurrentUserId();
  if (!userId) return null;

  try {
    const sb = window.supabaseClient?.getSupabase ? window.supabaseClient.getSupabase() : null;
    if (!sb) return null;

    const { data, error } = await sb.from('assessment_results')
      .select('*')
      .eq('user_id', userId)
      .maybeSingle();

    if (error || !data) return null;

    // 恢复 answers
    if (data.answers) {
      Object.assign(answers, data.answers);
    }

    // 重建 resultsCache 用于渲染
    if (data.results && data.results.length) {
      return data.results.map(r => {
        const major = majorsData.find(m => m.code === r.code);
        return {
          major: major || { code: r.code, name: r.name, category: r.category, difficulty: '--', salary_range: '--' },
          rank: r.rank,
          percentage: r.percentage,
        };
      });
    }
    return null;
  } catch (e) {
    console.error('Load assessment results failed:', e);
    return null;
  }
}

function updateSaveButtonState(saved) {
  const btn = $('#btnSave');
  if (!btn) return;
  if (saved) {
    btn.textContent = t('saved', '✓ 已保存');
    btn.disabled = true;
    btn.style.opacity = '0.6';
  } else {
    btn.textContent = t('save_results', '💾 保存结果');
    btn.disabled = false;
    btn.style.opacity = '1';
  }
}

// ---- 数据加载 ----
async function loadMajorsData() {
  const loadingEl = $('#loadingState');
  const errorEl = $('#errorState');
  const quizEl = $('#quizSection');

  loadingEl.style.display = '';
  quizEl.style.display = 'none';

  // 检查 sessionStorage 缓存
  const cached = sessionStorage.getItem('assessment_majors_data');
  if (cached) {
    try {
      majorsData = JSON.parse(cached);
      loadingEl.style.display = 'none';
      quizEl.style.display = '';
      renderStep(1);
      return;
    } catch (e) { /* 缓存已损坏，重新加载 */ }
  }

  try {
    if (!window.supabaseClient) {
      throw new Error('Supabase client not ready');
    }
    const { url, key } = window.supabaseClient;
    const fields = 'code,name,category,category_icon,salary_range,difficulty,overview,career_outlook,what_you_learn,suitable_for,xuefeng_comment,career_directions,degree,duration';
    let allData = [];
    let offset = 0;
    const limit = 1000;

    while (true) {
      const response = await fetch(
        `${url}/rest/v1/majors?select=${fields}&limit=${limit}&offset=${offset}`,
        { headers: { apikey: key, Authorization: `Bearer ${key}` } }
      );
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const rows = await response.json();
      if (!rows || rows.length === 0) break;
      allData = allData.concat(rows);
      offset += limit;
      if (rows.length < limit) break;
    }

    majorsData = allData;
    // 缓存到 sessionStorage
    try {
      sessionStorage.setItem('assessment_majors_data', JSON.stringify(allData));
    } catch (e) { /* 数据太大无法缓存 */ }

    loadingEl.style.display = 'none';
    quizEl.style.display = '';
    renderStep(1);
  } catch (err) {
    console.error('Failed to load majors data:', err);
    loadingEl.style.display = 'none';
    errorEl.style.display = '';
  }
}

// ---- 事件绑定 ----
function bindGlobalEvents() {
  $('#btnNext').addEventListener('click', () => goToStep(currentStep + 1));
  $('#btnPrev').addEventListener('click', () => goToStep(currentStep - 1));
  $('#btnSubmit').addEventListener('click', submitQuiz);
  // #btnRetake 在 updateResultsFooter() 中动态绑定

  // 语言切换时重新渲染
  onLanguageChange(() => {
    if (resultsCache) {
      renderResults(resultsCache);
    } else {
      renderStep(currentStep);
    }
  });
}

// ---- 初始化 ----
async function init() {
  // 创建语言切换器
  createLangSwitcher($('#langSwitcherContainer'));

  bindGlobalEvents();

  // 初始化 common.js 的对比栏
  if (window.initCompareBar) {
    window.initCompareBar();
  }

  // 加载数据
  await loadMajorsData();

  // 加载收藏状态
  if (typeof window.loadUserFavorites === 'function') window.loadUserFavorites();

  // 尝试加载已保存的结果
  const savedResults = await loadSavedResults();
  if (savedResults && savedResults.length) {
    resultsCache = savedResults;
    renderResults(savedResults);
    // 更新标题显示为"上次测评结果"
    const resultsTitle = document.querySelector('.results-title');
    if (resultsTitle) {
      resultsTitle.textContent = t('saved_results_title', '📋 你的上次测评结果');
    }
  }

  // 监听对比列表变化
  window.addEventListener('compareListChanged', () => {
    if (resultsCache) {
      renderResults(resultsCache);
    }
  });
}

init().catch(err => {
  console.error('Assessment init error:', err);
  const errorEl = $('#errorState');
  const loadingEl = $('#loadingState');
  if (loadingEl) loadingEl.style.display = 'none';
  if (errorEl) errorEl.style.display = '';
});
