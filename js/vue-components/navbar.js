// ============================================================
// 专业星图 - Vue 3 导航栏组件原型
// 可统一替换各页面中的 top-nav / nav 区域
// ============================================================

const SiteNavbar = {
  props: {
    user: { type: Object, default: null },
    currentPage: { type: String, default: 'home' },
  },

  emits: ['logout'],

  computed: {
    displayName() {
      if (!this.user) return '';
      const phone = this.user.phone || this.user.email || '用户';
      return phone.length > 11 ? phone.slice(0, 11) : phone;
    },

    navLinks() {
      const links = [];
      if (this.currentPage !== 'home') links.push({ href: '/', label: '首页' });
      if (this.user) {
        links.push({ href: '/user/dashboard.html', label: '个人中心' });
        links.push({ href: '/user/reports.html', label: '浏览报告' });
        links.push({ href: '/user/orders.html', label: '历史记录' });
      }
      return links;
    },
  },

  template: `
    <div class="top-nav">
      <a href="/" class="nav-logo">专业星图</a>
      <div class="nav-links">
        <a v-for="link in navLinks" :key="link.href" :href="link.href" class="nav-link">{{ link.label }}</a>

        <template v-if="user">
          <div class="user-info">
            <div class="user-avatar">👤</div>
            <span class="user-name">{{ displayName }}</span>
            <button class="btn-sm btn-primary-sm" @click="$emit('logout')">退出</button>
          </div>
        </template>

        <template v-else>
          <a href="/login.html" class="nav-link">登录</a>
          <a href="/register.html" class="btn-sm btn-primary-sm" style="text-decoration:none;">注册</a>
        </template>
      </div>
    </div>
  `,

  methods: {
    async refreshUser() {
      if (window.auth?.getCurrentUser) {
        const u = await window.auth.getCurrentUser();
        this.$emit('update:user', u);
      }
    },
  },

  mounted() {
    this.refreshUser();
  },
};
