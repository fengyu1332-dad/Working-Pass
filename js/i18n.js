// ============================================================
// 专业星图 - 中英文双语模块
// ============================================================

const LANG_KEY = 'starmap_lang';
const LANG_EVENT = 'starmap_lang_change';

const ZH = {
  // 全局
  site_name: '专业星图',
  site_tagline: '温暖的大学专业选择指南',
  site_subtitle: '探索中国大学全部专业，了解就业前景、薪资范围、学习难度，找到最适合你的专业方向',
  data_source: '数据来源：专业星图数据库 · 请结合自身情况选择',
  back_home: '← 返回首页',
  skip_to_main: '跳到主要内容',
  search_placeholder: '搜专业 / 拼音 / 首字母 / 缩写（如 CS、AI）...',
  search_btn: '搜索',
  clear_search: '清除搜索',
  no_results: '未找到匹配结果',
  try_other: '请尝试其他关键词',
  no_data: '暂无数据',
  load_error: '加载失败，请刷新重试',
  retry: '重试',
  unknown_error: '未知错误',
  logout_fail: '退出失败',

  // 导航
  nav_home: '首页',
  nav_majors: '专业浏览',
  nav_dashboard: '个人中心',
  nav_purchase: '购买点数',
  nav_orders: '历史记录',
  nav_logout: '退出',
  nav_login: '登录',
  nav_register: '注册',
  browse_reports_nav: '浏览报告',

  // 首页
  hero_title: '专业星图',
  hero_desc: '温暖的大学专业选择指南',
  hero_cta: '探索全部专业 →',
  featured_title: '热门推荐专业',
  featured_subtitle: '基于专业热度与就业前景精选',
  view_all: '查看全部',
  major_count_unit: '个专业',
  category_count_unit: '个专业',
  search_tab: '搜索',
  category_tab: '分类浏览',
  recent_searches: '最近搜索',
  clear_recent: '清除',
  no_recent: '暂无搜索记录',
  popular_searches: '热门搜索',
  search_history: '搜索历史',
  all_majors: '全部专业',
  suggest_title: '建议搜索',
  suggest_desc: '试试搜索"计算机"、"金融"、"医学"等关键词',
  did_you_mean: '你要找的是不是',
  did_you_mean_prefix: '你要找的是不是：',
  no_results_tip: '试试输入专业名称、拼音首字母或学科门类',
  view_all_results: '查看全部搜索结果',
  result_count_unit: '个结果',
  graph_loading: '正在构建关系图谱...',
  graph_loading_sub: '连接专业与职业路径',
  graph_hint: '拖拽节点 | 滚轮缩放 | 点击查看详情',
  legend_category: '学科门类',
  legend_major: '专业节点',
  footer_tagline: '用数据照亮你的大学选择',
  modal_cta: '查看深度分析报告 →',

  // 专业详情弹窗标签
  tab_overview: '专业概况',
  tab_courses: '学习内容',
  tab_careers: '就业前景',
  tab_review: '雪峰点评',
  detail_salary_range: '就业薪资范围',
  xuefeng_disclaimer: '以上点评仅代表个人观点，仅供参考',

  // 专业浏览页
  majors_title: '大学专业浏览',
  majors_subtitle: '按学科分类浏览全部专业',
  filter_title: '筛选条件',
  filter_category: '学科分类',
  filter_all: '全部学科',
  filter_difficulty: '学习难度',
  filter_salary: '薪资水平',
  salary_all: '全部薪资',
  salary_below_10k: '10k以下',
  salary_10k_20k: '10k-20k',
  salary_20k_30k: '20k-30k',
  salary_above_30k: '30k以上',
  reset_filters: '重置筛选',
  sidebar_filter: '筛选条件',
  sort_label: '排序',
  sort_name: '按名称',
  sort_difficulty: '按难度',
  sort_salary: '按薪资',
  major_count: '个专业',
  major_count_short: '个',
  major_count_unit_short: '个专业',
  view_list: '列表视图',
  view_grid: '关系图谱',
  major_detail: '专业详情',
  major_code: '专业代码',
  major_category: '学科门类',
  major_degree: '学位',
  major_duration: '学制',
  major_duration_unit: '年',
  major_difficulty: '学习难度',
  major_salary: '薪资范围',
  major_overview: '专业概述',
  major_courses: '学习内容',
  major_suitable: '适合人群',
  major_career: '就业前景',
  major_comment: '雪峰点评',
  major_universities: '推荐院校',
  major_directions: '就业方向',
  domestic_unis: '国内院校',
  international_unis: '国际院校',
  yearly_courses: '分年级课程',
  career_outlook: '职业前景',
  no_matching_majors: '未找到匹配的专业',
  no_results_prefix: '没有找到与',
  no_results_suffix: '" 匹配的专业',
  category_hint: '点击任意专业查看详情',
  select_category_prompt: '请选择一个学科分类',
  loading_majors: '正在加载专业数据...',
  pagination_info: '共',
  pagination_pages: '页',
  pagination_prev: '上一页',
  pagination_next: '下一页',
  salary_detail_prefix: '就业薪资范围：',
  salary_negotiable: '薪资面议',

  // 登录/注册
  login_title: '登录',
  login_submit: '登录',
  login_forgot: '忘记密码？',
  register_title: '注册',
  register_submit: '注册',
  no_account: '还没有账号？',
  has_account: '已有账号？',
  go_register: '去注册',
  go_login: '去登录',
  email_label: '邮箱',
  email_placeholder: '请输入邮箱地址',
  password_label: '密码',
  password_placeholder: '请输入密码',
  register_password_placeholder: '请设置密码（至少6位）',
  confirm_password_label: '确认密码',
  confirm_password_placeholder: '请再次输入密码',
  username_label: '用户名',
  username_placeholder: '请输入用户名',
  confirm_password: '确认密码',
  terms_agree: '我已阅读并同意《用户协议》和《隐私政策》',
  fill_email_password: '请填写邮箱和密码',
  logging_in: '登录中...',
  login_success: '登录成功！即将跳转...',
  login_fail: '登录失败，请检查邮箱和密码',
  login_bad_credentials: '邮箱或密码错误，请重试',
  login_email_not_confirmed: '邮箱尚未验证，请先点击邮件中的确认链接',
  google_redirect: '跳转至 Google...',
  google_register_fail: 'Google 注册失败，请重试',
  google_register_btn: '使用 Google 账号注册',
  fill_required_fields: '请填写所有必填项',
  invalid_email: '请输入有效的邮箱地址',
  password_mismatch: '两次输入的密码不一致',
  password_too_short: '密码长度至少为6位',
  agree_terms: '请同意用户协议和隐私政策',
  registering: '注册中...',
  register_success: '注册成功！请检查邮箱并点击确认链接，然后即可登录。即将跳转到登录页...',
  email_already_registered: '该邮箱已被注册，请直接登录或使用其他邮箱',
  register_fail: '注册失败，请稍后重试',

  // 密码重置
  reset_password_title: '🔑 重置密码',
  reset_password_subtitle: '请输入注册时使用的邮箱，我们将发送密码重置链接',
  send_reset_link: '发送重置链接',
  reset_sending: '发送中...',
  reset_sent: '已发送',
  reset_email_sent: '✓ 重置链接已发送，请检查邮箱（含垃圾邮件箱）',
  reset_fail: '发送失败，请稍后重试',
  back_to_login: '← 返回登录',
  update_password_title: '🔒 设置新密码',
  update_password_subtitle: '请输入至少 6 位的新密码',
  update_password_btn: '更新密码',
  updating: '更新中...',
  password_updated: '✓ 密码已更新！3 秒后跳转登录页...',
  password_update_fail: '更新失败，链接可能已过期，请重新申请',
  new_password_placeholder: '输入新密码',
  confirm_new_password_placeholder: '确认新密码',
  min_6_chars: '至少 6 位字符',

  // 个人中心/订单/购买
  unknown_user: '未知用户',
  no_orders: '暂无订单记录',
  points_recharge: '点数充值',
  load_failed: '加载失败',
  major_report: '专业报告',
  load_error_retry: '加载失败，请稍后重试',
  no_downloads: '暂无下载记录',
  order_paid: '已支付',
  order_pending: '待支付',
  order_cancelled: '已取消',
  order_expired: '已过期',
  load_packages_fail: '加载套餐失败：',
  no_packages: '暂无可用套餐，请联系管理员',
  no_packages_short: '暂无可用套餐',
  recommended: '推荐',
  unlock_report_desc: '解锁专业深度报告',
  creating_order: '创建订单...',
  create_order_fail: '创建订单失败，请重试',

  // 报告页
  reports_title: '专业深度报告',
  reports_subtitle: '解锁完整深度分析报告，获取专业选择的全面指南',
  points_balance: '当前点数余额',
  unlocked_only: '仅显示已解锁',
  sort_downloads: '按解锁量',
  sort_recent: '按时间',
  report_unlocked: '已解锁',
  report_locked: '未解锁',
  report_preview: '免费预览',
  report_unlock: '消耗 1 点解锁',
  report_unlock_btn: '解锁完整深度分析报告',
  report_buy_points: '充值获取点数',
  report_share: '分享报告',
  report_copied: '已复制',
  report_loading: '加载中...',
  report_no_content: '暂无报告内容',
  report_load_error: '加载失败',
  report_unlock_success: '解锁成功！',
  report_unlock_fail: '解锁失败',
  report_downloads: '次解锁',
  report_cost: '消耗 1 点',
  back_dashboard: '← 返回个人中心',
  report_flow_title: '深度分析报告',
  login_required_report: '请先登录后再查看深度分析报告',
  search_report_placeholder: '搜索专业名称或代码...',
  filter_category_label: '学科分类：',
  report_search_empty: '没有找到匹配的报告',
  report_search_empty_suffix: '',
  report_no_data: '暂无报告数据',
  report_unnamed: '未命名报告',
  your_points: '你的点数余额',

  // 阅读器
  font_small: '小号字体',
  font_medium: '中号字体',
  font_large: '大号字体',
  fullscreen_on: '全屏阅读',
  fullscreen_off: '退出全屏',

  // 个人中心
  dashboard_title: '个人中心',
  profile_section: '个人信息',
  role_label: '角色',
  my_reports: '我的报告',
  no_unlocked: '暂无已解锁报告',
  browse_reports: '浏览全部报告 →',

  // 购买
  purchase_title: '购买点数',
  purchase_desc: '选择适合你的点数套餐',
  purchase_btn: '立即购买',
  points_unit: '点',
  current_balance: '当前余额',

  // 订单
  orders_title: '历史记录',
  orders_empty: '暂无记录',
  order_id: '订单号',
  order_date: '日期',
  order_amount: '金额',
  order_status: '状态',

  // 预热弹窗
  preheat_title: '专业星图 - 即将上线',
  preheat_desc: '深度专业报告、个性化推荐、职业路径规划',
  preheat_feature_1: '883个大学专业全覆盖',
  preheat_feature_2: 'AI 驱动的深度分析报告',
  preheat_feature_3: '个性化专业推荐',
  preheat_feature_4: '实时就业市场数据',
  preheat_feature_5: '张雪峰风格犀利点评',
  preheat_cta: '抢先体验 →',

  // 专业对比
  compare_title: '横向对比',
  compare_subtitle: '并排比较，一目了然',
  compare_dimension: '对比维度',
  compare_select_hint: '选择专业，开始对比',
  compare_start_btn: '开始对比',
  compare_clear: '清空',
  compare_collapse: '收起',
  compare_add_empty: '+ 添加专业',
  compare_need_one_more: '再选 1 个即可对比',
  compare_remove: '移除',
  compare_max_hint: '最多对比 4 个专业',
  compare_already_in: '该专业已在对比列表中',
  compare_add_btn: '加入对比',
  compare_share: '📋 复制对比链接',
  compare_section_basic: '基础信息',
  compare_section_salary: '薪资与就业',
  compare_section_study: '学习内容',
  compare_section_fit: '适合人群',
  compare_section_schools: '推荐院校',
  compare_section_comment: '雪峰点评',
  compare_empty_title: '请选择要对比的专业',
  compare_empty_desc: '从专业列表中选择 2-4 个专业，即可开始并排对比',
  compare_browse_btn: '浏览全部专业 →',
  share_success: '对比链接已复制到剪贴板',

  // 错误/通用
  error_occurred: '发生错误',
  try_later: '请稍后再试',
  loading: '加载中...',
  save: '保存',
  cancel: '取消',
  confirm: '确认',
  delete: '删除',
  edit: '编辑',
  close: '关闭',
  back: '返回',

  // 站点统计
  site_visits: '累计访问',
  site_time: '用户累计停留',
  visits_unit: '次',
  hours_unit: '小时',
  minutes_unit: '分钟',

  // 决策工具
  decision_title: '🧭 三步找到最适合你的专业',
  decision_subtitle: '用科学方法，从883个专业中做出明智选择',
  decision_browse_name: '专业浏览',
  decision_browse_desc: '883个专业，按门类筛选',
  decision_browse_btn: '去看看 →',
  decision_compare_name: '横向对比',
  decision_compare_desc: '并排比较，一目了然',
  decision_compare_btn: '去对比 →',
  decision_assessment_name: '适配测评',
  decision_assessment_desc: '8道题，科学匹配专业',
  decision_assessment_btn: '开始测评 →',

  // 适配测评
  nav_assessment: '适配测评',
  assessment_title: '专业适配测评',
  assessment_subtitle: '8道题 · 约3分钟 · 科学匹配你的专业方向',
  assessment_step1_title: '学科兴趣',
  assessment_step1_subtitle: '了解你喜欢什么、擅长什么',
  assessment_step2_title: '职业偏好',
  assessment_step2_subtitle: '了解你想要的职业是什么样的',
  assessment_step3_title: '自我评估',
  assessment_step3_subtitle: '客观评估你的能力和基础',
  btn_prev: '← 上一步',
  btn_next: '下一步 →',
  view_results: '查看结果',
  fill_all_required: '请完成当前步骤的所有问题后再继续',
  data_not_loaded: '专业数据尚未加载完成，请稍候',
  results_title: '你的最佳匹配专业',
  results_subtitle_prefix: '基于你的',
  results_subtitle_suffix: '个特质维度，从883个专业中匹配出最佳选择',
  retake: '🔄 重新测评',
  browse_all: '📚 浏览全部专业',
  result_detail: '📋 详情',
  result_compare_add: '+ 对比',
  result_compare_added: '✓ 已加入',
  match_score: '匹配度',
  loading_majors_data: '正在加载专业数据...',
  load_data_error: '数据加载失败',
  login_save_prompt: '登录后可保存测评结果',
  save_results: '💾 保存结果',
  saved: '✓ 已保存',
  save_success: '结果已保存！下次访问可直接查看',
  save_fail: '保存失败，请重试',
  login_required_save: '请先登录后再保存结果',
  saved_results_title: '📋 你的上次测评结果',
  load_saved_fail: '加载历史结果失败',
  share_results: '📤 分享结果',
  share_generating: '生成中...',
  share_copy_success: '分享图片已复制到剪贴板，可直接粘贴发送！',
  share_download_success: '分享图片已下载，可直接发送给朋友！',
  share_fail: '生成分享卡片失败，请重试',
  q_subjects: '你最喜欢的高中学科（最多选3个）',
  q_subjects_hint: '选择你学得最轻松、最有成就感的学科',
  q_learningStyle: '你的学习风格偏好是？',
  q_learningStyle_hint: '选择最符合你日常学习习惯的描述',
  q_interests: '对以下活动的兴趣程度',
  q_interests_hint: '1 = 完全不想碰，5 = 非常喜欢',
  q_careerValues: '你最看重的职业要素（按重要性选3项）',
  q_careerValues_hint: '点击选项按顺序选择，第1个最重要',
  q_careerValues_hint2: '点击选项选定，再次点击已选中的可取消，按顺序排列优先级',
  q_workEnv: '你理想的未来工作环境是？',
  q_workEnv_hint: '选择最符合你愿景的工作场所',
  q_attitudes: '对以下说法的同意程度',
  q_attitudes_hint: '1 = 完全不同意，5 = 完全同意',
  q_abilities: '能力自评',
  q_abilities_hint: '1 = 较弱，5 = 很强。请客观评价自己当前的能力水平',
  q_grades: '学科成绩水平',
  q_grades_hint: '1 = 不及格/较差，5 = 年级前列。评估各学科的掌握程度',

  // 收藏
  fav_add: '收藏',
  fav_remove: '已收藏',
  fav_login_required: '请先登录后再收藏',
  fav_title: '我的收藏',
  fav_empty: '还没有收藏任何专业',
  fav_empty_hint: '浏览专业时点击 ♡ 即可收藏',
  fav_browse: '去浏览专业',
  fav_view_all: '查看全部收藏',
  fav_count: '收藏专业',
  // 图表
  chart_radar_title: '你的能力画像',
  chart_bar_title: '专业匹配度',
  // 仪表盘
  dash_favorites: '我的收藏',
  dash_assessment: '我的测评',
  dash_no_assessment: '还没有完成测评',
  dash_go_assessment: '去测评',
  dash_view_result: '查看完整结果',
  dash_retake: '重新测评',
  dash_assessment_date: '测评时间',
};

const EN = {
  // Global
  site_name: 'StarMap',
  site_tagline: 'Your Warm Guide to Choosing a University Major',
  site_subtitle: 'Explore all Chinese university majors — career prospects, salary ranges, difficulty levels — find your best fit.',
  data_source: 'Data: StarMap Database · Choose based on your own situation',
  back_home: '← Back to Home',
  skip_to_main: 'Skip to main content',
  search_placeholder: 'Search majors / pinyin / initials / abbreviations (e.g. CS, AI)...',
  search_btn: 'Search',
  clear_search: 'Clear Search',
  no_results: 'No matching results',
  try_other: 'Please try different keywords',
  no_data: 'No data available',
  load_error: 'Failed to load, please refresh',
  retry: 'Retry',
  unknown_error: 'Unknown error',
  logout_fail: 'Logout failed',

  // Nav
  nav_home: 'Home',
  nav_majors: 'Majors',
  nav_dashboard: 'Dashboard',
  nav_purchase: 'Buy Points',
  nav_orders: 'History',
  nav_logout: 'Logout',
  nav_login: 'Login',
  nav_register: 'Register',
  browse_reports_nav: 'Browse Reports',

  // Home
  hero_title: 'StarMap',
  hero_desc: 'Your Warm Guide to Choosing a University Major',
  hero_cta: 'Explore All Majors →',
  featured_title: 'Featured Majors',
  featured_subtitle: 'Curated by popularity and career prospects',
  view_all: 'View All',
  major_count_unit: 'majors',
  category_count_unit: 'majors',
  search_tab: 'Search',
  category_tab: 'Categories',
  recent_searches: 'Recent',
  clear_recent: 'Clear',
  no_recent: 'No recent searches',
  popular_searches: 'Popular',
  search_history: 'Search History',
  all_majors: 'All Majors',
  suggest_title: 'Suggestions',
  suggest_desc: 'Try searching "computer", "finance", "medicine" etc.',
  did_you_mean: 'Did you mean',
  did_you_mean_prefix: 'Did you mean: ',
  no_results_tip: 'Try entering a major name, pinyin initials, or category',
  view_all_results: 'View all results',
  result_count_unit: 'results',
  graph_loading: 'Building relationship graph...',
  graph_loading_sub: 'Connecting majors to career paths',
  graph_hint: 'Drag nodes | Scroll to zoom | Click for details',
  legend_category: 'Category',
  legend_major: 'Major node',
  footer_tagline: 'Data-driven guidance for your university choices',
  modal_cta: 'View In-Depth Report →',

  // Major detail modal tabs
  tab_overview: 'Overview',
  tab_courses: 'Courses',
  tab_careers: 'Careers',
  tab_review: 'Review',
  detail_salary_range: 'Salary Range',
  xuefeng_disclaimer: 'The above review is personal opinion, for reference only',

  // Majors page
  majors_title: 'University Majors',
  majors_subtitle: 'Browse all majors by academic category',
  filter_title: 'Filters',
  filter_category: 'Category',
  filter_all: 'All Categories',
  filter_difficulty: 'Difficulty',
  filter_salary: 'Salary',
  salary_all: 'All',
  salary_below_10k: 'Below 10k',
  salary_10k_20k: '10k-20k',
  salary_20k_30k: '20k-30k',
  salary_above_30k: 'Above 30k',
  reset_filters: 'Reset Filters',
  sidebar_filter: 'Filters',
  sort_label: 'Sort',
  sort_name: 'By Name',
  sort_difficulty: 'By Difficulty',
  sort_salary: 'By Salary',
  major_count: 'majors',
  major_count_short: '',
  major_count_unit_short: 'majors',
  view_list: 'List View',
  view_grid: 'Graph View',
  major_detail: 'Major Details',
  major_code: 'Code',
  major_category: 'Category',
  major_degree: 'Degree',
  major_duration: 'Duration',
  major_duration_unit: 'years',
  major_difficulty: 'Difficulty',
  major_salary: 'Salary Range',
  major_overview: 'Overview',
  major_courses: 'What You Will Learn',
  major_suitable: 'Who Should Apply',
  major_career: 'Career Prospects',
  major_comment: 'Expert Commentary',
  major_universities: 'Top Universities',
  major_directions: 'Career Directions',
  domestic_unis: 'Domestic',
  international_unis: 'International',
  yearly_courses: 'Yearly Courses',
  career_outlook: 'Career Outlook',
  no_matching_majors: 'No matching majors found',
  no_results_prefix: 'No results for "',
  no_results_suffix: '"',
  category_hint: 'Click any major for details',
  select_category_prompt: 'Select a category',
  loading_majors: 'Loading majors...',
  pagination_info: '',
  pagination_pages: 'pages',
  pagination_prev: 'Previous',
  pagination_next: 'Next',
  salary_detail_prefix: 'Salary range: ',
  salary_negotiable: 'Negotiable',

  // Login / Register
  login_title: 'Login',
  login_submit: 'Login',
  login_forgot: 'Forgot password?',
  register_title: 'Register',
  register_submit: 'Register',
  no_account: "Don't have an account?",
  has_account: 'Already have an account?',
  go_register: 'Register',
  go_login: 'Login',
  email_label: 'Email',
  email_placeholder: 'Enter your email address',
  password_label: 'Password',
  password_placeholder: 'Enter your password',
  register_password_placeholder: 'Set a password (min. 6 characters)',
  confirm_password_label: 'Confirm Password',
  confirm_password_placeholder: 'Re-enter your password',
  username_label: 'Username',
  username_placeholder: 'Enter your username',
  confirm_password: 'Confirm password',
  terms_agree: 'I have read and agree to the Terms of Service and Privacy Policy',
  fill_email_password: 'Please enter your email and password',
  logging_in: 'Logging in...',
  login_success: 'Login successful! Redirecting...',
  login_fail: 'Login failed, please check your email and password',
  login_bad_credentials: 'Invalid email or password, please try again',
  login_email_not_confirmed: 'Email not confirmed. Please click the confirmation link in your email first',
  google_redirect: 'Redirecting to Google...',
  google_register_fail: 'Google registration failed, please try again',
  google_register_btn: 'Sign up with Google',
  fill_required_fields: 'Please fill in all required fields',
  invalid_email: 'Please enter a valid email address',
  password_mismatch: 'Passwords do not match',
  password_too_short: 'Password must be at least 6 characters',
  agree_terms: 'Please agree to the Terms of Service and Privacy Policy',
  registering: 'Registering...',
  register_success: 'Registration successful! Please check your email and click the confirmation link. Redirecting to login...',
  email_already_registered: 'This email is already registered. Please log in or use another email',
  register_fail: 'Registration failed, please try again later',

  // Password reset
  reset_password_title: '🔑 Reset Password',
  reset_password_subtitle: 'Enter the email you used to register, we will send a password reset link',
  send_reset_link: 'Send Reset Link',
  reset_sending: 'Sending...',
  reset_sent: 'Sent',
  reset_email_sent: '✓ Reset link sent! Please check your email (including spam folder)',
  reset_fail: 'Failed to send, please try again later',
  back_to_login: '← Back to Login',
  update_password_title: '🔒 Set New Password',
  update_password_subtitle: 'Please enter a new password (min. 6 characters)',
  update_password_btn: 'Update Password',
  updating: 'Updating...',
  password_updated: '✓ Password updated! Redirecting to login in 3s...',
  password_update_fail: 'Update failed, link may have expired. Please request a new link.',
  new_password_placeholder: 'Enter new password',
  confirm_new_password_placeholder: 'Confirm new password',
  min_6_chars: 'At least 6 characters',

  // Dashboard / Orders / Purchase
  unknown_user: 'Unknown User',
  no_orders: 'No orders yet',
  points_recharge: 'Points Recharge',
  load_failed: 'Failed to load',
  major_report: 'Major Report',
  load_error_retry: 'Failed to load, please try again later',
  no_downloads: 'No downloads yet',
  order_paid: 'Paid',
  order_pending: 'Pending',
  order_cancelled: 'Cancelled',
  order_expired: 'Expired',
  load_packages_fail: 'Failed to load packages: ',
  no_packages: 'No packages available, please contact admin',
  no_packages_short: 'No packages available',
  recommended: 'Recommended',
  unlock_report_desc: 'Unlock in-depth major reports',
  creating_order: 'Creating order...',
  create_order_fail: 'Failed to create order, please try again',

  // Reports
  reports_title: 'In-Depth Major Reports',
  reports_subtitle: 'Unlock comprehensive analysis reports for informed major decisions',
  points_balance: 'Points Balance',
  unlocked_only: 'Unlocked Only',
  sort_downloads: 'By Unlocks',
  sort_recent: 'By Time',
  report_unlocked: 'Unlocked',
  report_locked: 'Locked',
  report_preview: 'Free Preview',
  report_unlock: 'Spend 1 Point to Unlock',
  report_unlock_btn: 'Unlock Full Report',
  report_buy_points: 'Buy Points',
  report_share: 'Share Report',
  report_copied: 'Copied',
  report_loading: 'Loading...',
  report_no_content: 'No content available',
  report_load_error: 'Failed to load',
  report_unlock_success: 'Unlocked!',
  report_unlock_fail: 'Unlock failed',
  report_downloads: 'unlocks',
  report_cost: 'Costs 1 point',
  back_dashboard: '← Back to Dashboard',
  report_flow_title: 'In-Depth Analysis Report',
  login_required_report: 'Please log in to view the in-depth report',
  search_report_placeholder: 'Search major name or code...',
  filter_category_label: 'Category:',
  report_search_empty: 'No matching reports',
  report_search_empty_suffix: '',
  report_no_data: 'No report data available',
  report_unnamed: 'Unnamed report',
  your_points: 'Your points balance',

  // Reader
  font_small: 'Small',
  font_medium: 'Medium',
  font_large: 'Large',
  fullscreen_on: 'Fullscreen',
  fullscreen_off: 'Exit Fullscreen',

  // Dashboard
  dashboard_title: 'Dashboard',
  profile_section: 'Profile',
  role_label: 'Role',
  my_reports: 'My Reports',
  no_unlocked: 'No unlocked reports yet',
  browse_reports: 'Browse All Reports →',

  // Purchase
  purchase_title: 'Buy Points',
  purchase_desc: 'Choose a points package',
  purchase_btn: 'Buy Now',
  points_unit: 'pts',
  current_balance: 'Current Balance',

  // Orders
  orders_title: 'Order History',
  orders_empty: 'No records',
  order_id: 'Order ID',
  order_date: 'Date',
  order_amount: 'Amount',
  order_status: 'Status',

  // Preheat modal
  preheat_title: 'StarMap — Coming Soon',
  preheat_desc: 'In-depth reports, personalized recommendations, career path planning',
  preheat_feature_1: 'Covering all 883 university majors',
  preheat_feature_2: 'AI-powered in-depth analysis reports',
  preheat_feature_3: 'Personalized major recommendations',
  preheat_feature_4: 'Real-time job market data',
  preheat_feature_5: 'Frank, no-nonsense expert reviews',
  preheat_cta: 'Get Early Access →',

  // Errors / Common
  // Compare
  compare_title: 'Compare',
  compare_subtitle: 'Side-by-side comparison at a glance',
  compare_dimension: 'Dimension',
  compare_select_hint: 'Select majors to compare',
  compare_start_btn: 'Compare',
  compare_clear: 'Clear',
  compare_collapse: 'Collapse',
  compare_add_empty: '+ Add major',
  compare_need_one_more: 'Add 1 more to compare',
  compare_remove: 'Remove',
  compare_max_hint: 'Maximum 4 majors',
  compare_already_in: 'Already in comparison list',
  compare_add_btn: 'Add to Compare',
  compare_share: '📋 Copy Comparison Link',
  compare_section_basic: 'Basic Info',
  compare_section_salary: 'Salary & Career',
  compare_section_study: 'What You Study',
  compare_section_fit: 'Who It Fits',
  compare_section_schools: 'Top Universities',
  compare_section_comment: 'Expert Review',
  compare_empty_title: 'Select majors to compare',
  compare_empty_desc: 'Choose 2-4 majors from the list to start side-by-side comparison',
  compare_browse_btn: 'Browse All Majors →',
  share_success: 'Comparison link copied to clipboard',

  error_occurred: 'An error occurred',
  try_later: 'Please try again later',
  loading: 'Loading...',
  save: 'Save',
  cancel: 'Cancel',
  confirm: 'Confirm',
  delete: 'Delete',
  edit: 'Edit',
  close: 'Close',
  back: 'Back',

  // Site stats
  site_visits: 'Total Visits',
  site_time: 'Total Time Spent',
  visits_unit: 'visits',
  hours_unit: 'hours',
  minutes_unit: 'minutes',

  // Decision Tools
  decision_title: '🧭 Find Your Best Major in 3 Steps',
  decision_subtitle: 'A scientific approach to choose from 883 majors',
  decision_browse_name: 'Browse Majors',
  decision_browse_desc: '883 majors, filter by category',
  decision_browse_btn: 'Explore →',
  decision_compare_name: 'Compare',
  decision_compare_desc: 'Side by side comparison',
  decision_compare_btn: 'Compare →',
  decision_assessment_name: 'Assessment',
  decision_assessment_desc: '8 questions, science-based match',
  decision_assessment_btn: 'Start Quiz →',

  // Assessment
  nav_assessment: 'Assessment',
  assessment_title: 'Major Fit Assessment',
  assessment_subtitle: '8 Questions · ~3 Minutes · Find Your Best Major Match',
  assessment_step1_title: 'Academic Interests',
  assessment_step1_subtitle: 'What you enjoy learning',
  assessment_step2_title: 'Career Preferences',
  assessment_step2_subtitle: 'What kind of career you want',
  assessment_step3_title: 'Self-Evaluation',
  assessment_step3_subtitle: 'Honestly evaluate your abilities',
  btn_prev: '← Previous',
  btn_next: 'Next →',
  view_results: 'View Results',
  fill_all_required: 'Please complete all questions in this step before continuing',
  data_not_loaded: 'Major data not yet loaded, please wait',
  results_title: 'Your Best Matching Majors',
  results_subtitle_prefix: 'Based on your',
  results_subtitle_suffix: 'trait dimensions, matched from 883 majors',
  retake: '🔄 Retake Quiz',
  browse_all: '📚 Browse All Majors',
  result_detail: '📋 Details',
  result_compare_add: '+ Compare',
  result_compare_added: '✓ Added',
  match_score: 'Match',
  loading_majors_data: 'Loading major data...',
  load_data_error: 'Failed to load data',
  login_save_prompt: 'Log in to save your results',
  save_results: '💾 Save Results',
  saved: '✓ Saved',
  save_success: 'Results saved! You can view them next time',
  save_fail: 'Save failed, please retry',
  login_required_save: 'Please log in first to save results',
  saved_results_title: '📋 Your Previous Assessment Results',
  load_saved_fail: 'Failed to load saved results',
  share_results: '📤 Share Results',
  share_generating: 'Generating...',
  share_copy_success: 'Share card copied to clipboard! Paste to share',
  share_download_success: 'Share card downloaded! Send it to your friends',
  share_fail: 'Failed to generate share card, please retry',
  q_subjects: 'Your favorite high school subjects (up to 3)',
  q_subjects_hint: 'Select the subjects you find easiest and most rewarding',
  q_learningStyle: 'What is your preferred learning style?',
  q_learningStyle_hint: 'Choose the description that best matches your habits',
  q_interests: 'Interest level in these activities',
  q_interests_hint: '1 = Not interested at all, 5 = Very interested',
  q_careerValues: 'What do you value most in a career? (Pick & rank 3)',
  q_careerValues_hint: 'Click to select in order of priority',
  q_careerValues_hint2: 'Click to select, click again to deselect, arranged by priority',
  q_workEnv: 'What is your ideal work environment?',
  q_workEnv_hint: 'Choose the setting that matches your vision',
  q_attitudes: 'How much do you agree with these statements?',
  q_attitudes_hint: '1 = Strongly disagree, 5 = Strongly agree',
  q_abilities: 'Self-assessed abilities',
  q_abilities_hint: '1 = Weak, 5 = Strong. Be honest about your current level',
  q_grades: 'Academic performance level',
  q_grades_hint: '1 = Below average, 5 = Top of class. Evaluate your mastery',

  // Favorites
  fav_add: 'Save',
  fav_remove: 'Saved',
  fav_login_required: 'Please login to save favorites',
  fav_title: 'My Favorites',
  fav_empty: 'No saved majors yet',
  fav_empty_hint: 'Click ♡ while browsing majors to save them',
  fav_browse: 'Browse Majors',
  fav_view_all: 'View All Favorites',
  fav_count: 'Saved Majors',
  // Charts
  chart_radar_title: 'Your Ability Profile',
  chart_bar_title: 'Match Score',
  // Dashboard
  dash_favorites: 'My Favorites',
  dash_assessment: 'My Assessment',
  dash_no_assessment: 'No assessment completed yet',
  dash_go_assessment: 'Take Assessment',
  dash_view_result: 'View Full Results',
  dash_retake: 'Retake',
  dash_assessment_date: 'Assessment Date',
};

const translations = { 'zh-CN': ZH, 'en': EN };

function getLang() {
  try {
    const stored = localStorage.getItem(LANG_KEY);
    if (stored === 'en') return 'en';
  } catch {}
  return 'zh-CN';
}

let currentLang = getLang();

export function t(key, fallback) {
  return translations[currentLang]?.[key] || translations['zh-CN'][key] || fallback || key;
}

export function setLanguage(lang) {
  if (lang === currentLang) return;
  currentLang = lang;
  try { localStorage.setItem(LANG_KEY, lang); } catch {}
  applyTranslations();
  window.dispatchEvent(new CustomEvent(LANG_EVENT, { detail: lang }));
}

export function getLanguage() {
  return currentLang;
}

export function onLanguageChange(fn) {
  window.addEventListener(LANG_EVENT, fn);
}

// 将 data-i18n 属性的元素翻译
export function applyTranslations(root = document) {
  // textContent 替换
  root.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (!key) return;
    const text = t(key);
    if (text) el.textContent = text;
  });

  // placeholder 替换
  root.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (!key) return;
    const text = t(key);
    if (text) el.placeholder = text;
  });

  // title 替换
  root.querySelectorAll('[data-i18n-title]').forEach(el => {
    const key = el.getAttribute('data-i18n-title');
    if (!key) return;
    const text = t(key);
    if (text) el.title = text;
  });

  // meta description
  const metaDesc = document.querySelector('meta[name="description"]');
  if (metaDesc && metaDesc.hasAttribute('data-i18n-content')) {
    metaDesc.content = t(metaDesc.getAttribute('data-i18n-content'));
  }
}

// 创建语言切换按钮HTML
export function createLangSwitcher() {
  const div = document.createElement('div');
  div.className = 'lang-switcher';
  div.innerHTML = `
    <button class="lang-btn${currentLang === 'zh-CN' ? ' active' : ''}" data-lang="zh-CN" aria-label="切换到中文">中</button>
    <span class="lang-sep">|</span>
    <button class="lang-btn${currentLang === 'en' ? ' active' : ''}" data-lang="en" aria-label="Switch to English">EN</button>
  `;
  div.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const lang = btn.dataset.lang;
      if (lang === currentLang) return;
      setLanguage(lang);
      div.querySelectorAll('.lang-btn').forEach(b => {
        b.classList.toggle('active', b.dataset.lang === lang);
      });
    });
  });
  return div;
}

// 页面加载时自动应用
if (typeof document !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => {
    applyTranslations();
  });
}
