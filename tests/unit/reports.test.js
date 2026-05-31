import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { mockSupabase, mockQueryChain } from './helpers.js';

let mockSB;
let reportsChain;
let downloadChain;

const SAMPLE_REPORT = {
  id: 'rpt-uuid-1',
  major_code: '080901',
  major_name: '计算机科学与技术',
  category: '工学',
  preview_content: '<h2>一、专业概述</h2>',
  full_content: '<h1>深度报告</h1><p>完整内容...</p>',
  download_count: 42,
  status: 'published',
};

beforeEach(async () => {
  mockSB = mockSupabase();
  reportsChain = mockQueryChain();
  downloadChain = mockQueryChain();

  mockSB.from.mockImplementation((table) => {
    if (table === 'reports') return reportsChain;
    if (table === 'download_records') return downloadChain;
    return mockQueryChain();
  });

  globalThis.supabase = { createClient: vi.fn().mockReturnValue(mockSB) };
  window.supabaseClient = {
    init: vi.fn().mockReturnValue(mockSB),
    get: vi.fn().mockReturnValue(mockSB),
    url: 'https://test.supabase.co',
    key: 'anon-key',
  };
  window.auth = {
    getCurrentUser: vi.fn().mockResolvedValue({ id: 'user-1', email: 'u@test.com' }),
    getSupabase: vi.fn().mockReturnValue(mockSB),
  };
  window.location = { href: '' };

  vi.resetModules();
});

afterEach(() => {
  vi.clearAllMocks();
});

async function loadReports() {
  return import('../../js/reports.js');
}

describe('reports — getReports', () => {
  it('获取已发布报告列表', async () => {
    reportsChain._setResponse({ data: [SAMPLE_REPORT], error: null });
    const rpt = await loadReports();
    const result = await rpt.getReports();
    expect(result.length).toBe(1);
    expect(result[0].major_name).toBe('计算机科学与技术');
  });

  it('按类别筛选', async () => {
    reportsChain._setResponse({ data: [SAMPLE_REPORT], error: null });
    const rpt = await loadReports();
    await rpt.getReports('工学');
    expect(reportsChain.eq).toHaveBeenCalledWith('category', '工学');
  });

  it('搜索匹配名称/代码/类别', async () => {
    reportsChain._setResponse({ data: [SAMPLE_REPORT], error: null });
    const rpt = await loadReports();
    await rpt.getReports(null, '计算机');
    expect(reportsChain.or).toHaveBeenCalledWith(
      expect.stringContaining('major_name.ilike.%计算机%')
    );
  });
});

describe('reports — getReportByMajorCode', () => {
  it('找到已发布报告', async () => {
    reportsChain.maybeSingle.mockResolvedValue({ data: SAMPLE_REPORT, error: null });
    const rpt = await loadReports();
    const result = await rpt.getReportByMajorCode('080901');
    expect(result.major_name).toBe('计算机科学与技术');
  });

  it('未找到返回 null', async () => {
    reportsChain.maybeSingle.mockResolvedValue({ data: null, error: null });
    const rpt = await loadReports();
    const result = await rpt.getReportByMajorCode('999999');
    expect(result).toBeNull();
  });
});

describe('reports — getReport', () => {
  it('通过 ID 获取报告', async () => {
    reportsChain._setResponse({ data: SAMPLE_REPORT, error: null });
    const rpt = await loadReports();
    const result = await rpt.getReport('rpt-uuid-1');
    expect(result.major_code).toBe('080901');
  });
});

describe('reports — unlockReport', () => {
  it('已解锁直接返回内容', async () => {
    // checkUnlocked: returns true
    downloadChain.maybeSingle.mockResolvedValue({ data: { id: 'dr-1' }, error: null });
    // get report content after already-unlocked check
    reportsChain.single.mockResolvedValue({ data: SAMPLE_REPORT, error: null });

    const rpt = await loadReports();
    const result = await rpt.unlockReport('rpt-uuid-1');
    expect(result.alreadyUnlocked).toBe(true);
    expect(result.content).toBe(SAMPLE_REPORT.full_content);
    expect(mockSB.rpc).not.toHaveBeenCalled();
  });

  it('首次解锁调用 spend_points RPC', async () => {
    // checkUnlocked: returns false
    downloadChain.maybeSingle.mockResolvedValue({ data: null, error: null });
    // RPC success
    mockSB.rpc.mockResolvedValue({ data: { success: true, new_balance: 4 }, error: null });
    // get report content
    reportsChain.single.mockResolvedValue({ data: SAMPLE_REPORT, error: null });

    const rpt = await loadReports();
    const result = await rpt.unlockReport('rpt-uuid-1');
    expect(result.alreadyUnlocked).toBe(false);
    expect(mockSB.rpc).toHaveBeenCalledWith('spend_points', { p_report_id: 'rpt-uuid-1' });
  });

  it('点数不足抛出异常', async () => {
    downloadChain.maybeSingle.mockResolvedValue({ data: null, error: null });
    mockSB.rpc.mockResolvedValue({ data: { success: false, error: '点数不足，请先充值' }, error: null });

    const rpt = await loadReports();
    await expect(rpt.unlockReport('rpt-uuid-1')).rejects.toThrow('点数不足，请先充值');
  });

  it('RPC 调用失败抛出异常', async () => {
    downloadChain.maybeSingle.mockResolvedValue({ data: null, error: null });
    mockSB.rpc.mockResolvedValue({ data: null, error: new Error('DB offline') });

    const rpt = await loadReports();
    await expect(rpt.unlockReport('rpt-uuid-1')).rejects.toThrow('DB offline');
  });
});

describe('reports — getUnlockedReportIds', () => {
  it('返回已解锁报告 ID 列表', async () => {
    downloadChain._setResponse({
      data: [{ report_id: 'rpt-1' }, { report_id: 'rpt-2' }],
      error: null,
    });
    const rpt = await loadReports();
    const ids = await rpt.getUnlockedReportIds();
    expect(ids).toEqual(['rpt-1', 'rpt-2']);
  });

  it('未登录返回空数组', async () => {
    window.auth.getCurrentUser.mockResolvedValue(null);
    const rpt = await loadReports();
    const ids = await rpt.getUnlockedReportIds();
    expect(ids).toEqual([]);
  });
});

describe('reports — checkUnlocked', () => {
  it('已解锁返回 true', async () => {
    downloadChain.maybeSingle.mockResolvedValue({ data: { id: 'dr-1' }, error: null });
    const rpt = await loadReports();
    expect(await rpt.checkUnlocked('rpt-1')).toBe(true);
  });

  it('未解锁返回 false', async () => {
    downloadChain.maybeSingle.mockResolvedValue({ data: null, error: null });
    const rpt = await loadReports();
    expect(await rpt.checkUnlocked('rpt-1')).toBe(false);
  });
});
