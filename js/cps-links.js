// ============================================================
// 教育类 CPS/CPA 推广链接数据
// 替换 URL 中的 PLACEHOLDER 为你的真实推广链接
// ============================================================

const CPS_LINKS = {
  // ── 通用（所有专业都显示）──
  common: [
    {
      name: '高考志愿填报一对一',
      desc: '专家一对一，精准匹配专业和院校',
      url: 'https://PLACEHOLDER_REPLACE_ME/gaokao',
      icon: '🎓',
      tag: '热门',
    },
    {
      name: '考研公共课全程班',
      desc: '英语+政治+数学，一站式系统备考',
      url: 'https://PLACEHOLDER_REPLACE_ME/kaoyan',
      icon: '📝',
      tag: '推荐',
    },
  ],

  // ── 按学科门类 ──
  '工学': [
    {
      name: 'IT 编程就业班',
      desc: 'Java/Python/前端，零基础到高薪就业',
      url: 'https://PLACEHOLDER_REPLACE_ME/it-train',
      icon: '💻',
    },
    {
      name: '计算机等级考试培训',
      desc: 'NCRE 二/三/四级系统辅导',
      url: 'https://PLACEHOLDER_REPLACE_ME/ncre',
      icon: '🖥️',
    },
    {
      name: '工程类注册考试',
      desc: '一建/二建/注册工程师备考课程',
      url: 'https://PLACEHOLDER_REPLACE_ME/engineer',
      icon: '🏗️',
    },
  ],
  '理学': [
    {
      name: '数学建模竞赛辅导',
      desc: '国赛/美赛系统培训，获奖率提升',
      url: 'https://PLACEHOLDER_REPLACE_ME/math-model',
      icon: '📐',
    },
    {
      name: '数据分析师认证课',
      desc: 'Python+SQL+统计学，拿证就业',
      url: 'https://PLACEHOLDER_REPLACE_ME/data-analyst',
      icon: '📊',
    },
  ],
  '医学': [
    {
      name: '执业医师资格考试',
      desc: '临床/口腔/中医，系统精讲+真题',
      url: 'https://PLACEHOLDER_REPLACE_ME/doctor-exam',
      icon: '🩺',
    },
    {
      name: '医学考研专业课',
      desc: '西医综合/中医综合全程班',
      url: 'https://PLACEHOLDER_REPLACE_ME/med-kaoyan',
      icon: '💊',
    },
    {
      name: '护理资格证培训',
      desc: '护士/护师职称考试辅导',
      url: 'https://PLACEHOLDER_REPLACE_ME/nurse',
      icon: '🏥',
    },
  ],
  '经济学': [
    {
      name: 'CFA/FRM 金融证书培训',
      desc: '特许金融分析师/风险管理师备考',
      url: 'https://PLACEHOLDER_REPLACE_ME/cfa',
      icon: '📈',
    },
    {
      name: 'CPA 注册会计师课程',
      desc: '专业阶段+综合阶段系统辅导',
      url: 'https://PLACEHOLDER_REPLACE_ME/cpa',
      icon: '💰',
    },
    {
      name: '证券/基金从业资格',
      desc: '一个月拿证，金融行业敲门砖',
      url: 'https://PLACEHOLDER_REPLACE_ME/securities',
      icon: '📋',
    },
  ],
  '管理学': [
    {
      name: 'MBA/MPA 联考辅导',
      desc: '管理类联考系统备考方案',
      url: 'https://PLACEHOLDER_REPLACE_ME/mba',
      icon: '🎯',
    },
    {
      name: 'PMP 项目管理认证',
      desc: '国际项目管理师认证培训',
      url: 'https://PLACEHOLDER_REPLACE_ME/pmp',
      icon: '📋',
    },
    {
      name: '人力资源/会计实操',
      desc: 'HR+财务实操技能速成',
      url: 'https://PLACEHOLDER_REPLACE_ME/hr-accounting',
      icon: '💼',
    },
  ],
  '法学': [
    {
      name: '法考全程班（客观+主观）',
      desc: '名师系统精讲，通过率有保障',
      url: 'https://PLACEHOLDER_REPLACE_ME/law-exam',
      icon: '⚖️',
    },
    {
      name: '公务员/事业编考试',
      desc: '行测+申论+公基，三科一体',
      url: 'https://PLACEHOLDER_REPLACE_ME/gongkao',
      icon: '🏛️',
    },
  ],
  '教育学': [
    {
      name: '教师资格证全程班',
      desc: '笔试+面试一站式，多学科可选',
      url: 'https://PLACEHOLDER_REPLACE_ME/teacher-cert',
      icon: '📚',
    },
    {
      name: '教师招聘考试辅导',
      desc: '教综+学科专业知识系统课',
      url: 'https://PLACEHOLDER_REPLACE_ME/teacher-recruit',
      icon: '🏫',
    },
  ],
  '文学': [
    {
      name: '翻译资格证（CATTI）',
      desc: '口译+笔译系统培训',
      url: 'https://PLACEHOLDER_REPLACE_ME/catti',
      icon: '🌐',
    },
    {
      name: '新媒体运营实战课',
      desc: '文案+短视频+账号运营',
      url: 'https://PLACEHOLDER_REPLACE_ME/new-media',
      icon: '✍️',
    },
  ],
  '农学': [
    {
      name: '农业硕士考研辅导',
      desc: '农管/农村发展方向专业课',
      url: 'https://PLACEHOLDER_REPLACE_ME/agriculture',
      icon: '🌾',
    },
    {
      name: '执业兽医资格考试',
      desc: '基础+临床+预防综合辅导',
      url: 'https://PLACEHOLDER_REPLACE_ME/veterinary',
      icon: '🐾',
    },
  ],
  '哲学': [
    {
      name: '考研政治高分突破',
      desc: '马原理+毛中特+思修系统精讲',
      url: 'https://PLACEHOLDER_REPLACE_ME/politics-kaoyan',
      icon: '📖',
    },
  ],
  '历史学': [
    {
      name: '历史学考研专业课',
      desc: '中国史+世界史系统辅导',
      url: 'https://PLACEHOLDER_REPLACE_ME/history-kaoyan',
      icon: '🏺',
    },
  ],
  '艺术学': [
    {
      name: '艺术类考研专业课',
      desc: '中外美术史+艺术概论精讲',
      url: 'https://PLACEHOLDER_REPLACE_ME/art-kaoyan',
      icon: '🎨',
    },
    {
      name: '设计软件系统课',
      desc: 'PS+AI+AE+Sketch 职场技能',
      url: 'https://PLACEHOLDER_REPLACE_ME/design-tools',
      icon: '🖌️',
    },
  ],
  '交叉学科': [
    {
      name: 'AI/数据科学就业班',
      desc: '机器学习+深度学习+项目实战',
      url: 'https://PLACEHOLDER_REPLACE_ME/ai-ml',
      icon: '🤖',
    },
  ],
};

// ── 获取某门类的推荐链接（含通用链接）──
function getCPSLinks(category) {
  const categoryLinks = CPS_LINKS[category] || [];
  const commonLinks = CPS_LINKS.common || [];
  // 通用链接在前，门类链接在后，最多 4 条
  return [...commonLinks, ...categoryLinks].slice(0, 4);
}

// ── 渲染为 HTML ──
function renderCPSWidget(category) {
  const links = getCPSLinks(category);
  if (!links.length) return '';

  const items = links.map((l) => `
    <a href="${l.url}" target="_blank" rel="nofollow sponsored noopener" class="cps-card"
       onclick="window.reportCPSClick &amp;&amp; window.reportCPSClick('${l.name}', '${category}')">
      <span class="cps-card-icon">${l.icon || '📌'}</span>
      <div class="cps-card-body">
        <div class="cps-card-name">
          ${l.name}
          ${l.tag ? `<span class="cps-card-tag">${l.tag}</span>` : ''}
        </div>
        <div class="cps-card-desc">${l.desc}</div>
      </div>
      <span class="cps-card-arrow">→</span>
    </a>
  `).join('');

  return `
    <div class="cps-widget">
      <div class="cps-widget-header">
        <span>📌 推荐资源</span>
        <span class="cps-widget-disclaimer">广告</span>
      </div>
      <div class="cps-card-list">
        ${items}
      </div>
    </div>`;
}

export { CPS_LINKS, getCPSLinks, renderCPSWidget };
