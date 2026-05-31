import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { mockSupabase, mockQueryChain } from './helpers.js';

let mockSB;
let profileChain;

beforeEach(async () => {
  mockSB = mockSupabase();
  profileChain = mockQueryChain();

  // Different tables get different chains
  mockSB.from.mockImplementation((table) => {
    if (table === 'user_profiles') return profileChain;
    return mockQueryChain();
  });

  // Auth.js imports getSupabase from supabase-client.js which calls supabase.createClient
  // Must be set BEFORE vi.resetModules() triggers re-import
  globalThis.supabase = { createClient: vi.fn().mockReturnValue(mockSB) };
  window.supabaseClient = {
    init: vi.fn().mockReturnValue(mockSB),
    get: vi.fn().mockReturnValue(mockSB),
    url: 'https://test.supabase.co',
    key: 'anon-key',
  };
  window.location = { href: '', origin: 'http://localhost:3456' };

  vi.resetModules();
});

afterEach(() => {
  vi.clearAllMocks();
});

async function loadAuth() {
  return import('../../js/auth.js');
}

describe('auth — loginWithEmail', () => {
  it('登录成功返回 user 和 session', async () => {
    mockSB.auth.signInWithPassword.mockResolvedValue({
      data: { user: { id: 'u1', email: 'test@test.com' }, session: { access_token: 'at-123' } },
      error: null,
    });
    const auth = await loadAuth();
    const result = await auth.loginWithEmail('test@test.com', 'pass123');
    expect(result.user.email).toBe('test@test.com');
    expect(result.session.access_token).toBe('at-123');
  });

  it('密码错误抛出异常', async () => {
    mockSB.auth.signInWithPassword.mockResolvedValue({
      data: {},
      error: { message: 'Invalid login credentials' },
    });
    const auth = await loadAuth();
    await expect(auth.loginWithEmail('a@b.com', 'wrong')).rejects.toThrow('Invalid login credentials');
  });
});

describe('auth — registerWithEmail', () => {
  it('注册成功后创建 user_profiles', async () => {
    mockSB.auth.signUp.mockResolvedValue({
      data: { user: { id: 'new-user', email: 'new@test.com' } },
      error: null,
    });
    profileChain._setResponse({ data: { id: 'new-user' }, error: null });

    const auth = await loadAuth();
    const result = await auth.registerWithEmail('new@test.com', 'Pass123!');
    expect(result.user.email).toBe('new@test.com');
    expect(mockSB.from).toHaveBeenCalledWith('user_profiles');
  });

  it('注册失败抛出异常', async () => {
    mockSB.auth.signUp.mockResolvedValue({
      data: {},
      error: { message: 'User already registered' },
    });
    const auth = await loadAuth();
    await expect(auth.registerWithEmail('dup@test.com', 'Pass123!')).rejects.toThrow('User already registered');
  });
});

describe('auth — getCurrentUser', () => {
  it('获取当前登录用户', async () => {
    mockSB.auth.getUser.mockResolvedValue({
      data: { user: { id: 'u1', email: 'me@test.com' } },
      error: null,
    });
    const auth = await loadAuth();
    const user = await auth.getCurrentUser();
    expect(user.email).toBe('me@test.com');
  });

  it('未登录返回 null', async () => {
    mockSB.auth.getUser.mockRejectedValue(new Error('no session'));
    const auth = await loadAuth();
    const user = await auth.getCurrentUser();
    expect(user).toBeNull();
  });

  it('auth error 返回 null', async () => {
    mockSB.auth.getUser.mockResolvedValue({ data: { user: null }, error: { message: 'no auth' } });
    const auth = await loadAuth();
    const user = await auth.getCurrentUser();
    expect(user).toBeNull();
  });
});

describe('auth — getUserProfile', () => {
  it('profile 存在直接返回', async () => {
    mockSB.auth.getUser.mockResolvedValue({ data: { user: { id: 'u1' } }, error: null });
    profileChain._setResponse({ data: { id: 'u1', role: 'user', points_balance: 5 }, error: null });

    const auth = await loadAuth();
    const profile = await auth.getUserProfile();
    expect(profile.role).toBe('user');
    expect(profile.points_balance).toBe(5);
  });

  it('profile 不存在时自动创建 (PGRST116)', async () => {
    mockSB.auth.getUser.mockResolvedValue({ data: { user: { id: 'u2' } }, error: null });
    // First call: profile not found
    profileChain.single
      .mockResolvedValueOnce({ data: null, error: { code: 'PGRST116' } })
      .mockResolvedValueOnce({ data: { id: 'u2', role: 'user', points_balance: 1 }, error: null });

    const auth = await loadAuth();
    const profile = await auth.getUserProfile();
    expect(profile.role).toBe('user');
    expect(profile.points_balance).toBe(1);
  });

  it('未登录返回 null', async () => {
    mockSB.auth.getUser.mockResolvedValue({ data: { user: null }, error: null });
    const auth = await loadAuth();
    const profile = await auth.getUserProfile();
    expect(profile).toBeNull();
  });
});

describe('auth — logout', () => {
  it('登出成功跳转到登录页', async () => {
    mockSB.auth.signOut.mockResolvedValue({ error: null });
    const auth = await loadAuth();
    await auth.logout();
    expect(mockSB.auth.signOut).toHaveBeenCalled();
    expect(window.location.href).toBe('/login.html');
  });
});

describe('auth — isAdmin', () => {
  it('管理员返回 true', async () => {
    mockSB.auth.getUser.mockResolvedValue({ data: { user: { id: 'admin-1' } }, error: null });
    profileChain._setResponse({ data: { id: 'admin-1', role: 'admin' }, error: null });
    const auth = await loadAuth();
    expect(await auth.isAdmin()).toBe(true);
  });

  it('普通用户返回 false', async () => {
    mockSB.auth.getUser.mockResolvedValue({ data: { user: { id: 'u1' } }, error: null });
    profileChain._setResponse({ data: { id: 'u1', role: 'user' }, error: null });
    const auth = await loadAuth();
    expect(await auth.isAdmin()).toBe(false);
  });
});

describe('auth — checkAuthAndRedirect', () => {
  it('未登录跳转到登录页', async () => {
    mockSB.auth.getUser.mockResolvedValue({ data: { user: null }, error: null });
    const auth = await loadAuth();
    const result = await auth.checkAuthAndRedirect();
    expect(result).toBe(false);
    expect(window.location.href).toBe('/login.html');
  });

  it('已登录返回 true', async () => {
    mockSB.auth.getUser.mockResolvedValue({ data: { user: { id: 'u1' } }, error: null });
    const auth = await loadAuth();
    const result = await auth.checkAuthAndRedirect('/custom.html');
    expect(result).toBe(true);
  });
});

describe('auth — sendPasswordResetEmail', () => {
  it('发送重置密码邮件', async () => {
    mockSB.auth.resetPasswordForEmail.mockResolvedValue({ data: {}, error: null });
    const auth = await loadAuth();
    const result = await auth.sendPasswordResetEmail('user@test.com');
    expect(result).toBeDefined();
    expect(mockSB.auth.resetPasswordForEmail).toHaveBeenCalledWith('user@test.com', {
      redirectTo: 'http://localhost:3456/update-password.html',
    });
  });
});

describe('auth — signInWithGoogle', () => {
  it('跳转 Google OAuth', async () => {
    mockSB.auth.signInWithOAuth.mockResolvedValue({
      data: { url: 'https://accounts.google.com/o/oauth2/...' },
      error: null,
    });
    const auth = await loadAuth();
    const result = await auth.signInWithGoogle();
    expect(result.url).toContain('google');
  });
});

describe('auth — showToast', () => {
  it('创建 toast 容器并显示消息', async () => {
    const auth = await loadAuth();
    auth.showToast('操作成功', 'success');

    const container = document.querySelector('.toast-container');
    expect(container).not.toBeNull();
    expect(container.getAttribute('aria-live')).toBe('polite');
    expect(container.querySelector('.toast-success').textContent).toBe('操作成功');
  });

  it('重复使用已有容器', async () => {
    const auth = await loadAuth();
    auth.showToast('msg1');
    auth.showToast('msg2');
    expect(document.querySelectorAll('.toast-container').length).toBe(1);
  });
});
