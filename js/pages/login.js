// ============================================================
// 专业星图 - 登录页
// ============================================================

import '../supabase-client.js';
import '../auth.js';
import '../error-report.js';
import { t, createLangSwitcher } from '../i18n.js';

document.addEventListener('DOMContentLoaded', () => {
  const langContainer = document.getElementById('langSwitcherContainer');
  if (langContainer) {
    langContainer.appendChild(createLangSwitcher());
  }
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

  const googleBtn = document.getElementById('googleLoginBtn');
  if (googleBtn) {
    googleBtn.addEventListener('click', async () => {
      clearMessages();
      googleBtn.disabled = true;
      googleBtn.textContent = '跳转至 Google...';
      try {
        await window.auth.signInWithGoogle();
      } catch (error) {
        console.error('Google login error:', error);
        showError(error.message || 'Google 登录失败，请重试');
        googleBtn.disabled = false;
        googleBtn.innerHTML = '<svg class="google-icon" viewBox="0 0 24 24" width="18" height="18"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>使用 Google 账号登录';
      }
    });
  }

  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearMessages();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    if (!email || !password) {
      showError(t('fill_email_password', '请填写邮箱和密码'));
      return;
    }

    loginBtn.disabled = true;
    loginBtn.textContent = t('logging_in', '登录中...');

    try {
      const { data } = await window.auth.loginWithEmail(email, password);
      showSuccess(t('login_success', '登录成功！即将跳转...'));
      setTimeout(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get('code');
        const redirect = urlParams.get('redirect') || 'index.html';
        if (code) {
          window.location.href = `${redirect}?code=${encodeURIComponent(code)}`;
        } else {
          window.location.href = 'index.html';
        }
      }, 1000);
    } catch (error) {
      console.error('Login error:', error);
      let msg = error.message || t('login_fail', '登录失败，请检查邮箱和密码');
      if (msg.includes('Invalid login credentials') || msg.includes('Invalid Login')) {
        msg = t('login_bad_credentials', '邮箱或密码错误，请重试');
      } else if (msg.includes('Email not confirmed')) {
        msg = t('login_email_not_confirmed', '邮箱尚未验证，请先点击邮件中的确认链接');
      }
      showError(msg);
    } finally {
      loginBtn.disabled = false;
      loginBtn.textContent = t('login_submit', '登录');
    }
  });

  window.auth.initSupabase();
  window.auth.checkAuthState(async (session) => {
    if (session) {
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get('code');
      const redirect = urlParams.get('redirect') || 'index.html';
      if (code) {
        window.location.href = `${redirect}?code=${encodeURIComponent(code)}`;
      } else {
        window.location.href = 'index.html';
      }
    }
  });
});
