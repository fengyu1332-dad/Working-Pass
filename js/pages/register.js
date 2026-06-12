// ============================================================
// 专业星图 - 注册页
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

  const registerForm = document.getElementById('registerForm');
  const registerBtn = document.getElementById('registerBtn');
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

  const googleBtn = document.getElementById('googleRegisterBtn');
  if (googleBtn) {
    googleBtn.addEventListener('click', async () => {
      clearMessages();
      googleBtn.disabled = true;
      googleBtn.textContent = t('google_redirect', '跳转至 Google...');
      try {
        await window.auth.signInWithGoogle();
      } catch (error) {
        console.error('Google register error:', error);
        showError(error.message || t('google_register_fail', 'Google 注册失败，请重试'));
        googleBtn.disabled = false;
        googleBtn.innerHTML = '<svg class="google-icon" viewBox="0 0 24 24" width="18" height="18"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>' + t('google_register_btn', '使用 Google 账号注册');
      }
    });
  }

  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearMessages();

    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const termsChecked = document.getElementById('terms').checked;

    if (!email || !password || !confirmPassword) {
      showError(t('fill_required_fields', '请填写所有必填项'));
      return;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      showError(t('invalid_email', '请输入有效的邮箱地址'));
      return;
    }

    if (password !== confirmPassword) {
      showError(t('password_mismatch', '两次输入的密码不一致'));
      return;
    }

    if (password.length < 6) {
      showError(t('password_too_short', '密码长度至少为6位'));
      return;
    }

    if (!termsChecked) {
      showError(t('agree_terms', '请同意用户协议和隐私政策'));
      return;
    }

    registerBtn.disabled = true;
    registerBtn.textContent = t('registering', '注册中...');

    try {
      await window.auth.registerWithEmail(email, password, phone);
      showSuccess(t('register_success', '注册成功！请检查邮箱并点击确认链接，然后即可登录。即将跳转到登录页...'));

      setTimeout(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get('code');
        const redirect = urlParams.get('redirect');
        const loginParams = new URLSearchParams();
        if (code) loginParams.set('code', code);
        if (redirect) loginParams.set('redirect', redirect);
        const qs = loginParams.toString();
        window.location.href = 'login.html' + (qs ? '?' + qs : '');
      }, 3000);
    } catch (error) {
      console.error('Registration error:', error);
      let msg = error.message || t('register_fail', '注册失败，请稍后重试');
      if (msg.includes('already registered') || msg.includes('already exists')) {
        msg = t('email_already_registered', '该邮箱已被注册，请直接登录或使用其他邮箱');
      }
      showError(msg);
    } finally {
      registerBtn.disabled = false;
      registerBtn.textContent = t('register_submit', '注册');
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
