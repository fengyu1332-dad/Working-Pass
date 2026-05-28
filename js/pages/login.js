// ============================================================
// 专业星图 - 登录页
// ============================================================

import '../supabase-client.js';
import '../auth.js';
import '../error-report.js';

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('loginForm');
  const loginBtn = document.getElementById('loginBtn');
  const errorMessage = document.getElementById('errorMessage');
  const successMessage = document.getElementById('successMessage');

  function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.add('show');
    successMessage.classList.remove('show');
  }

  function showSuccess(message) {
    successMessage.textContent = message;
    successMessage.classList.add('show');
    errorMessage.classList.remove('show');
  }

  function clearMessages() {
    errorMessage.classList.remove('show');
    successMessage.classList.remove('show');
  }

  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearMessages();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    if (!email || !password) {
      showError('请填写邮箱和密码');
      return;
    }

    loginBtn.disabled = true;
    loginBtn.textContent = '登录中...';

    try {
      await window.auth.loginWithEmail(email, password);
      showSuccess('登录成功！即将跳转...');
      setTimeout(() => {
        window.location.href = 'index.html';
      }, 1000);
    } catch (error) {
      console.error('Login error:', error);
      let msg = error.message || '登录失败，请检查邮箱和密码';
      if (msg.includes('Invalid login credentials') || msg.includes('Invalid Login')) {
        msg = '邮箱或密码错误，请重试';
      } else if (msg.includes('Email not confirmed')) {
        msg = '邮箱尚未验证，请先点击邮件中的确认链接';
      }
      showError(msg);
    } finally {
      loginBtn.disabled = false;
      loginBtn.textContent = '登录';
    }
  });

  window.auth.initSupabase();
  window.auth.checkAuthState(async (session) => {
    if (session) {
      window.location.href = 'index.html';
    }
  });
});
