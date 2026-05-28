// ============================================================
// 专业星图 - Vue 3 模态框组件原型
// 可替换 index.html / majors.html 中重复的模态框 HTML + JS
// ============================================================

const MajorModal = {
  props: {
    major: { type: Object, default: null },
    visible: { type: Boolean, default: false },
  },

  emits: ['close'],

  data() {
    return { activeTab: 'overview' };
  },

  watch: {
    visible(val) {
      if (val) this.activeTab = 'overview';
    },
  },

  computed: {
    courses() {
      if (!this.major?.yearly_courses) return {};
      return typeof this.major.yearly_courses === 'string'
        ? JSON.parse(this.major.yearly_courses)
        : this.major.yearly_courses;
    },

    universities() {
      if (!this.major?.top_universities) return {};
      return typeof this.major.top_universities === 'string'
        ? JSON.parse(this.major.top_universities)
        : this.major.top_universities;
    },

    commentHtml() {
      const comment = this.major?.xuefeng_comment || '';
      if (!comment) return '';
      // 使用 window.formatXuefengComment（由 utils.js 全局导出）
      if (window.formatXuefengComment) return window.formatXuefengComment(comment);
      let html = comment;
      html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
      html = html.replace(/\n\n/g, '</p><p>');
      html = html.replace(/\n/g, '<br>');
      html = '<p>' + html + '</p>';
      return html;
    },
  },

  template: `
    <div class="modal" :class="{ show: visible }" @click.self="$emit('close')">
      <div class="modal-content" v-if="major">
        <div class="modal-header">
          <div class="modal-title">
            <div class="category-icon">{{ major.category_icon || '📚' }}</div>
            <div>
              <p class="modal-category">{{ major.category }}</p>
              <h2>{{ major.name }}</h2>
            </div>
          </div>
          <button class="modal-close" @click="$emit('close')">✕</button>
        </div>

        <div class="modal-body">
          <div class="tab-buttons">
            <button class="tab-btn" :class="{ active: activeTab === 'overview' }" @click="activeTab = 'overview'">专业概况</button>
            <button class="tab-btn" :class="{ active: activeTab === 'courses' }" @click="activeTab = 'courses'">课程安排</button>
            <button class="tab-btn" :class="{ active: activeTab === 'careers' }" @click="activeTab = 'careers'">就业前景</button>
            <button class="tab-btn" :class="{ active: activeTab === 'review' }" @click="activeTab = 'review'">⭐ 雪峰点评</button>
          </div>

          <div v-show="activeTab === 'overview'">
            <div class="info-grid">
              <div class="info-card">
                <p class="info-card-label">学科门类</p>
                <p class="info-card-value">{{ major.category }}</p>
              </div>
              <div class="info-card">
                <p class="info-card-label">专业代码</p>
                <p class="info-card-value">{{ major.code }}</p>
              </div>
              <div class="info-card">
                <p class="info-card-label">学习难度</p>
                <p class="info-card-value">{{ major.difficulty }}</p>
              </div>
              <div class="info-card">
                <p class="info-card-label">薪资范围</p>
                <p class="info-card-value">{{ major.salary_range }}</p>
              </div>
            </div>
            <div class="detail-section">
              <h3 class="detail-title">📋 专业概述</h3>
              <p class="detail-content">{{ major.overview || '暂无数据' }}</p>
            </div>
            <div class="detail-section">
              <h3 class="detail-title">📚 你将学到</h3>
              <p class="detail-content">{{ major.what_you_learn || '暂无数据' }}</p>
            </div>
            <div class="detail-section">
              <h3 class="detail-title">👤 适合人群</h3>
              <p class="detail-content">{{ major.suitable_for || '暂无数据' }}</p>
            </div>
          </div>

          <div v-show="activeTab === 'courses'">
            <div class="detail-section">
              <h3 class="detail-title">📅 四年课程安排</h3>
              <ul class="year-list">
                <li v-for="(items, year) in courses" :key="year">
                  <strong>{{ year }}：</strong>{{ Array.isArray(items) ? items.join('、') : items }}
                </li>
              </ul>
            </div>
            <div class="detail-section" v-if="universities.domestic">
              <h3 class="detail-title">🇨🇳 国内名校</h3>
              <div class="uni-tags">
                <span class="uni-tag chinese" v-for="u in universities.domestic" :key="u">{{ u }}</span>
              </div>
            </div>
            <div class="detail-section" v-if="universities.international">
              <h3 class="detail-title">🌍 国际名校</h3>
              <div class="uni-tags">
                <span class="uni-tag foreign" v-for="u in universities.international" :key="u">{{ u }}</span>
              </div>
            </div>
          </div>

          <div v-show="activeTab === 'careers'">
            <div class="detail-section">
              <h3 class="detail-title">🚀 前景展望</h3>
              <p class="detail-content">{{ major.career_outlook || '暂无数据' }}</p>
            </div>
            <div class="detail-section">
              <h3 class="detail-title">💰 薪资范畴</h3>
              <p class="detail-content">就业薪资范围：{{ major.salary_range || '暂无数据' }}</p>
            </div>
          </div>

          <div v-show="activeTab === 'review'">
            <div class="detail-section">
              <h3 class="detail-title">🔥 雪峰点评</h3>
              <p style="font-size:12px;color:#9e9e9e;margin-bottom:12px;">⚠️ 本栏目观点为模拟评论，仅供参考。</p>
              <div class="summary-box" style="background:linear-gradient(135deg,#fff3e0,#ffe0b2);border-left:4px solid #e65100;padding:24px;border-radius:16px;">
                <p class="detail-content" v-html="commentHtml" style="font-size:15px;line-height:1.9;color:#5d4037;"></p>
              </div>
            </div>
            <div class="cta-section">
              <button class="cta-button" @click="goToReports">🔥 获取深度分析报告</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,

  methods: {
    async goToReports() {
      const user = window.auth?.getCurrentUser ? await window.auth.getCurrentUser() : null;
      if (!user) {
        if (confirm('查看深度报告需要登录，是否前往登录？')) {
          window.location.href = 'login.html';
        }
        return;
      }
      window.location.href = 'user/reports.html';
    },
  },
};
