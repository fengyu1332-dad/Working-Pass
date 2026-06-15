// ============================================================
// 专业星图 - 单元测试：分享卡片生成器
// ============================================================
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// ---- Canvas Mock ----
// 必须在导入 share-card 前安装，因为 generateShareCard 内联创建 canvas

function makeMockContext() {
  return {
    fillStyle: '',
    strokeStyle: '',
    font: '',
    textAlign: '',
    textBaseline: '',
    lineWidth: 1,
    globalAlpha: 1,
    beginPath: vi.fn(),
    closePath: vi.fn(),
    moveTo: vi.fn(),
    lineTo: vi.fn(),
    quadraticCurveTo: vi.fn(),
    arc: vi.fn(),
    fill: vi.fn(),
    stroke: vi.fn(),
    fillRect: vi.fn(),
    fillText: vi.fn(),
    strokeText: vi.fn(),
    save: vi.fn(),
    restore: vi.fn(),
    translate: vi.fn(),
    scale: vi.fn(),
    rotate: vi.fn(),
    createLinearGradient: vi.fn(() => ({ addColorStop: vi.fn() })),
    measureText: vi.fn((text) => ({ width: String(text).length * 10 })),
  };
}

function makeMockCanvasElement() {
  const ctx = makeMockContext();
  return {
    width: 600,
    height: 800,
    getContext: vi.fn(() => ctx),
    toDataURL: vi.fn(() => 'data:image/png;base64,mockCanvasData'),
  };
}

// 拦截 document.createElement
const realCreateElement = document.createElement.bind(document);
vi.spyOn(document, 'createElement').mockImplementation((tagName, ...args) => {
  if (tagName.toLowerCase() === 'canvas') {
    return makeMockCanvasElement();
  }
  return realCreateElement(tagName, ...args);
});

// ---- 现在安全导入被测模块 ----
import { generateShareCard, downloadShareCard, copyShareCardToClipboard } from '../../js/share-card.js';

// ---- 测试数据 ----
const mockResults = [
  {
    major: { name: '计算机科学与技术', category: '08 工学', salary_range: '¥10k-35k' },
    percentage: 92,
    rank: 1,
  },
  {
    major: { name: '软件工程', category: '08 工学', salary_range: '¥10k-32k' },
    percentage: 88,
    rank: 2,
  },
  {
    major: { name: '数据科学与大数据技术', category: '08 工学', salary_range: '¥12k-38k' },
    percentage: 85,
    rank: 3,
  },
];

const mockTraits = ['逻辑思维强', '动手能力好', '喜欢钻研'];

// ---- 测试 ----
describe('generateShareCard', () => {
  it('返回有效的 PNG dataURL', async () => {
    const dataURL = await generateShareCard(mockResults, mockTraits);
    expect(dataURL).toMatch(/^data:image\/png;base64,/);
  });

  it('使用 document.createElement(\'canvas\') 创建画布', async () => {
    await generateShareCard(mockResults, mockTraits);
    const calls = document.createElement.mock.calls.filter(c => c[0] === 'canvas');
    expect(calls.length).toBeGreaterThanOrEqual(1);
  });

  it('只显示前3个结果（传入超过3个不报错）', async () => {
    const extraResults = [...mockResults, {
      major: { name: '第四专业', category: '07 理学', salary_range: '¥8k-20k' },
      percentage: 70, rank: 4,
    }];
    const dataURL = await generateShareCard(extraResults, mockTraits);
    expect(dataURL).toMatch(/^data:image\/png;base64,/);
  });

  it('空特质数组不报错', async () => {
    const dataURL = await generateShareCard(mockResults, []);
    expect(dataURL).toMatch(/^data:image\/png;base64,/);
  });

  it('null traits 不报错', async () => {
    const dataURL = await generateShareCard(mockResults, null);
    expect(dataURL).toMatch(/^data:image\/png;base64,/);
  });

  it('缺少 major 对象时使用 name/category fallback', async () => {
    const partial = [{ major: null, name: '未知', category: '未知', percentage: 50, rank: 1 }];
    const dataURL = await generateShareCard(partial, mockTraits);
    expect(dataURL).toMatch(/^data:image\/png;base64,/);
  });

  it('空结果数组不报错', async () => {
    const dataURL = await generateShareCard([], []);
    expect(dataURL).toMatch(/^data:image\/png;base64,/);
  });

  it('无 percentage 字段时使用 0%', async () => {
    const results = [{ major: { name: '测试', category: '01 哲学', salary_range: '¥6k-18k' }, rank: 1 }];
    const dataURL = await generateShareCard(results, mockTraits);
    expect(dataURL).toMatch(/^data:image\/png;base64,/);
  });
});

describe('downloadShareCard', () => {
  let clickSpy, mockAnchor;
  let bodyAppendSpy, bodyRemoveSpy;

  beforeEach(() => {
    clickSpy = vi.fn();
    mockAnchor = { href: '', download: '', click: clickSpy };
    // 修改 createElement mock：对 'a' 返回 mockAnchor
    document.createElement.mockImplementation((tagName) => {
      if (tagName === 'a') return mockAnchor;
      if (tagName === 'canvas') return makeMockCanvasElement();
      return realCreateElement(tagName);
    });
    bodyAppendSpy = vi.spyOn(document.body, 'appendChild').mockImplementation(() => {});
    bodyRemoveSpy = vi.spyOn(document.body, 'removeChild').mockImplementation(() => {});
  });

  afterEach(() => {
    // 仅恢复 body spy，保留 createElement 的顶层 mock
    bodyAppendSpy.mockRestore();
    bodyRemoveSpy.mockRestore();
  });

  it('创建链接并触发点击下载', () => {
    downloadShareCard('data:image/png;base64,test');
    expect(clickSpy).toHaveBeenCalled();
  });

  it('文件名设置为中文', () => {
    downloadShareCard('data:image/png;base64,abc');
    expect(mockAnchor.download).toBe('我的专业匹配测评.png');
  });

  it('href 设置为传入的 dataURL', () => {
    const url = 'data:image/png;base64,hello';
    downloadShareCard(url);
    expect(mockAnchor.href).toBe(url);
  });
});

describe('copyShareCardToClipboard', () => {
  let mockClipboard;

  beforeEach(() => {
    mockClipboard = { write: vi.fn().mockResolvedValue(undefined) };
    Object.defineProperty(navigator, 'clipboard', {
      value: mockClipboard, writable: true, configurable: true,
    });
    global.ClipboardItem = class {
      constructor(items) { this.items = items; }
    };
    global.fetch = vi.fn().mockResolvedValue({
      blob: () => Promise.resolve(new Blob(['x'], { type: 'image/png' })),
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
    // 恢复顶层 createElement spy
    vi.spyOn(document, 'createElement').mockImplementation((tagName, ...args) => {
      if (tagName.toLowerCase() === 'canvas') return makeMockCanvasElement();
      return realCreateElement(tagName, ...args);
    });
  });

  it('fetch dataURL 并获取 blob', async () => {
    await copyShareCardToClipboard('data:image/png;base64,test');
    expect(global.fetch).toHaveBeenCalledWith('data:image/png;base64,test');
  });

  it('将 PNG blob 封装为 ClipboardItem 写入剪贴板', async () => {
    await copyShareCardToClipboard('data:image/png;base64,test');
    expect(mockClipboard.write).toHaveBeenCalledTimes(1);
    expect(mockClipboard.write.mock.calls[0][0][0]).toBeInstanceOf(ClipboardItem);
  });
});
