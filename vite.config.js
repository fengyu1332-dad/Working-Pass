import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  root: '.',
  base: '/',
  publicDir: 'public',

  build: {
    outDir: 'dist',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        majors: resolve(__dirname, 'majors.html'),
        login: resolve(__dirname, 'login.html'),
        register: resolve(__dirname, 'register.html'),
        dashboard: resolve(__dirname, 'user/dashboard.html'),
        reports: resolve(__dirname, 'user/reports.html'),
        purchase: resolve(__dirname, 'user/purchase.html'),
        orders: resolve(__dirname, 'user/orders.html'),
        'admin/index': resolve(__dirname, 'admin/index.html'),
        'admin/users': resolve(__dirname, 'admin/users.html'),
        'admin/reports': resolve(__dirname, 'admin/reports.html'),
        'admin/majors': resolve(__dirname, 'admin/majors.html'),
        'admin/packages': resolve(__dirname, 'admin/packages.html'),
      },
    },
    minify: 'terser',
    cssMinify: true,
    sourcemap: false,
  },

  server: {
    port: 3456,
    open: '/',
  },

  css: {
    devSourcemap: false,
  },
});
