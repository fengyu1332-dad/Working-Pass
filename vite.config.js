import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  root: '.',
  base: '/',
  publicDir: 'public',

  build: {
    outDir: 'dist',
    emptyOutDir: true,
    target: 'es2020',
    assetsInlineLimit: 4096,
    reportCompressedSize: false,
    modulePreload: { polyfill: true },
    minify: 'terser',
    cssMinify: true,
    sourcemap: false,
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        majors: resolve(__dirname, 'majors.html'),
        login: resolve(__dirname, 'login.html'),
        register: resolve(__dirname, 'register.html'),
        'reset-password': resolve(__dirname, 'reset-password.html'),
        'update-password': resolve(__dirname, 'update-password.html'),
        dashboard: resolve(__dirname, 'user/dashboard.html'),
        reports: resolve(__dirname, 'user/reports.html'),
        purchase: resolve(__dirname, 'user/purchase.html'),
        orders: resolve(__dirname, 'user/orders.html'),
        'admin/index': resolve(__dirname, 'admin/index.html'),
        'admin/users': resolve(__dirname, 'admin/users.html'),
        'admin/reports': resolve(__dirname, 'admin/reports.html'),
        'admin/majors': resolve(__dirname, 'admin/majors.html'),
        'admin/packages': resolve(__dirname, 'admin/packages.html'),
        'admin/orders': resolve(__dirname, 'admin/orders.html'),
      },
      output: {
        manualChunks(id) {
          if (id.includes('/js/utils.js')) return 'shared-utils';
          if (id.includes('/js/common.js')) return 'shared-ui';
          if (id.includes('/js/supabase-client.js')) return 'supabase-client';
          if (id.includes('/js/auth.js')) return 'auth';
          if (id.includes('/js/pages/admin-')) return 'admin';
        },
      },
    },
  },

  server: {
    port: 3456,
    open: '/',
  },

  css: {
    devSourcemap: false,
  },
});
