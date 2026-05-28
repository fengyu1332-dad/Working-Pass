// ============================================================
// 专业星图 - 注册页
// ============================================================

import '../supabase-client.js';
import '../auth.js';
import '../error-report.js';

document.addEventListener('DOMContentLoaded', () => {
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

  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearMessages();

    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const termsChecked = document.getElementById('terms').checked;

    if (!email || !password || !confirmPassword) {
      showError('请填写所有必填项');
      return;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      showError('请输入有效的邮箱地址');
      return;
    }

    if (password !== confirmPassword) {
      showError('两次输入的密码不一致');
      return;
    }

    if (password.length < 6) {
      showError('密码长度至少为6位');
      return;
    }

    if (!termsChecked) {
      showError('请同意用户协议和隐私政策');
      return;
    }

    registerBtn.disabled = true;
    registerBtn.textContent = '注册中...';

    try {
      await window.auth.registerWithEmail(email, password, phone);
      showSuccess('注册成功！请检查邮箱并点击确认链接，然后即可登录。即将跳转到登录页...');

      setTimeout(() => {
        window.location.href = 'login.html';
      }, 3000);
    } catch (error) {
      console.error('Registration error:', error);
      let msg = error.message || '注册失败，请稍后重试';
      if (msg.includes('already registered') || msg.includes('already exists')) {
        msg = '该邮箱已被注册，请直接登录或使用其他邮箱';
      }
      showError(msg);
    } finally {
      registerBtn.disabled = false;
      registerBtn.textContent = '注册';
    }
  });

  window.auth.initSupabase();
  window.auth.checkAuthState(async (session) => {
    if (session) {
      window.location.href = 'index.html';
    }
  });
});
