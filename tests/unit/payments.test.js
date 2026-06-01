import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { mockSupabase, mockQueryChain } from './helpers.js';

let mockSB;
let ordersChain;
let packagesChain;
let downloadChain;

beforeEach(async () => {
  mockSB = mockSupabase();
  ordersChain = mockQueryChain();
  packagesChain = mockQueryChain();
  downloadChain = mockQueryChain();

  mockSB.from.mockImplementation((table) => {
    if (table === 'orders') return ordersChain;
    if (table === 'point_packages') return packagesChain;
    if (table === 'download_records') return downloadChain;
    return mockQueryChain();
  });

  // Direct import path: getSupabase() must work
  globalThis.supabase = { createClient: vi.fn().mockReturnValue(mockSB) };

  // Direct import path: getCurrentUser() calls sb.auth.getUser()
  mockSB.auth.getUser.mockResolvedValue({
    data: { user: { id: 'user-1', email: 'test@test.com' } },
    error: null,
  });

  // createAlipayOrder uses sb.auth.getSession()
  mockSB.auth.getSession.mockResolvedValue({
    data: { session: { access_token: 'jwt-token-123' } },
    error: null,
  });

  // Backward compat for window-pattern consumers
  window.supabaseClient = {
    init: vi.fn().mockReturnValue(mockSB),
    get: vi.fn().mockReturnValue(mockSB),
    url: 'https://test.supabase.co',
    key: 'anon-key',
  };
  window.auth = {
    getCurrentUser: vi.fn().mockResolvedValue({ id: 'user-1', email: 'test@test.com' }),
    getSupabase: vi.fn().mockReturnValue(mockSB),
    getUserProfile: vi.fn(),
  };
  window.location = { href: '', origin: 'http://localhost:3456' };

  vi.resetModules();
});

afterEach(() => {
  vi.clearAllMocks();
});

async function loadPayments() {
  return import('../../js/payments.js');
}

describe('payments — getPointPackages', () => {
  it('返回激活套餐按价格升序', async () => {
    packagesChain._setResponse({
      data: [{ id: 1, name: '体验套餐', points: 10, price: 0.99, is_active: true }],
      error: null,
    });
    const pm = await loadPayments();
    const result = await pm.getPointPackages();
    expect(result.length).toBe(1);
    expect(result[0].name).toBe('体验套餐');
  });

  it('Supabase 未初始化抛出异常', async () => {
    // Remove global supabase so initSupabase() fails
    const oldSupabase = globalThis.supabase;
    delete globalThis.supabase;
    try {
      const pm = await loadPayments();
      await expect(pm.getPointPackages()).rejects.toThrow('Supabase not initialized');
    } finally {
      globalThis.supabase = oldSupabase;
    }
  });
});

describe('payments — createAlipayOrder', () => {
  it('调用 Edge Function 创建支付宝订单', async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({
        success: true,
        payment_url: 'https://openapi.alipaydev.com/gateway.do?sign=...',
        order: { id: 'order-uuid', amount: 9.90, points: 50, status: 'pending' },
      }),
    });

    const pm = await loadPayments();
    const result = await pm.createAlipayOrder(2);
    expect(result.success).toBe(true);
    expect(result.payment_url).toContain('alipay');
    const [url, init] = fetch.mock.calls[0];
    expect(init.headers.Authorization).toBe('Bearer jwt-token-123');
  });

  it('未登录抛出异常（中文提示）', async () => {
    mockSB.auth.getSession.mockResolvedValue({ data: { session: null }, error: null });
    const pm = await loadPayments();
    await expect(pm.createAlipayOrder(1)).rejects.toThrow('请先登录');
  });
});

describe('payments — queryOrderStatus', () => {
  it('返回订单状态', async () => {
    ordersChain._setResponse({ data: { status: 'paid', points: 50 }, error: null });
    const pm = await loadPayments();
    const result = await pm.queryOrderStatus('order-1');
    expect(result.status).toBe('paid');
  });
});

describe('payments — getOrders', () => {
  it('返回用户订单含套餐名', async () => {
    ordersChain._setResponse({
      data: [{ id: 'o1', status: 'paid', point_packages: { name: '推荐套餐' } }],
      error: null,
    });
    const pm = await loadPayments();
    const orders = await pm.getOrders();
    expect(orders.length).toBe(1);
    expect(orders[0].point_packages.name).toBe('推荐套餐');
  });
});

describe('payments — getDownloadRecords', () => {
  it('返回用户下载记录含报告信息', async () => {
    downloadChain._setResponse({
      data: [{ id: 'dr1', report_id: 'r1', reports: { major_name: '计算机科学' } }],
      error: null,
    });
    const pm = await loadPayments();
    const records = await pm.getDownloadRecords();
    expect(records.length).toBe(1);
    expect(records[0].reports.major_name).toBe('计算机科学');
  });
});
