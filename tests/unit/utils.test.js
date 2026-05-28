import { describe, it, expect, vi } from 'vitest';
import {
  escapeHtml,
  getJsonArray,
  formatXuefengComment,
  debounce,
  renderErrorState,
  renderLoadingState,
} from '../../js/utils.js';

describe('escapeHtml', () => {
  it('转义 & 符号', () => {
    expect(escapeHtml('a & b')).toBe('a &amp; b');
  });

  it('转义 < 和 >', () => {
    expect(escapeHtml('<script>')).toBe('&lt;script&gt;');
  });

  it('转义引号', () => {
    expect(escapeHtml('"hello"')).toBe('&quot;hello&quot;');
    expect(escapeHtml("it's")).toBe('it&#39;s');
  });

  it('处理空值和空字符串', () => {
    expect(escapeHtml('')).toBe('');
    expect(escapeHtml(null)).toBe('');
    expect(escapeHtml(undefined)).toBe('');
  });

  it('数字转字符串', () => {
    expect(escapeHtml(123)).toBe('123');
  });

  it('不改变普通文本', () => {
    expect(escapeHtml('计算机科学与技术')).toBe('计算机科学与技术');
  });
});

describe('getJsonArray', () => {
  it('解析 JSON 字符串数组', () => {
    expect(getJsonArray({ a: '["x","y"]' }, 'a')).toEqual(['x', 'y']);
  });

  it('返回已有的数组', () => {
    expect(getJsonArray({ a: ['x', 'y'] }, 'a')).toEqual(['x', 'y']);
  });

  it('key 不存在时返回空数组', () => {
    expect(getJsonArray({}, 'a')).toEqual([]);
    expect(getJsonArray(null, 'a')).toEqual([]);
    expect(getJsonArray(undefined, 'a')).toEqual([]);
  });

  it('key 值为 null/undefined 时返回空数组', () => {
    expect(getJsonArray({ a: null }, 'a')).toEqual([]);
    expect(getJsonArray({ a: undefined }, 'a')).toEqual([]);
  });

  it('非数组 JSON 时返回空数组', () => {
    expect(getJsonArray({ a: '"not array"' }, 'a')).toEqual([]);
    expect(getJsonArray({ a: '{"x":1}' }, 'a')).toEqual([]);
  });

  it('畸形 JSON 时返回空数组', () => {
    expect(getJsonArray({ a: 'not json' }, 'a')).toEqual([]);
  });
});

describe('formatXuefengComment', () => {
  it('空/空字符串时返回空', () => {
    expect(formatXuefengComment('')).toBe('');
    expect(formatXuefengComment(null)).toBe('');
    expect(formatXuefengComment(undefined)).toBe('');
  });

  it('将 **text** 转为 <strong>', () => {
    const result = formatXuefengComment('这是**重点**内容');
    expect(result).toContain('<strong>重点</strong>');
  });

  it('换行转 <br>', () => {
    const result = formatXuefengComment('第一行\n第二行');
    expect(result).toContain('<br>');
  });

  it('双换行转段落', () => {
    const result = formatXuefengComment('段落1\n\n段落2');
    expect(result).toContain('</p><p>');
  });

  it('对 HTML 特殊字符进行转义', () => {
    const result = formatXuefengComment('<script>alert("xss")</script>');
    expect(result).not.toContain('<script>');
    expect(result).toContain('&lt;script&gt;');
  });

  it('列表项格式处理', () => {
    const result = formatXuefengComment('- 项目一\n- 项目二');
    expect(result).toContain('•');
  });

  it('包含在 <p> 标签中', () => {
    const result = formatXuefengComment('测试内容');
    expect(result).toMatch(/^<p>/);
    expect(result).toMatch(/<\/p>$/);
  });
});

describe('debounce', () => {
  beforeEach(() => { vi.useFakeTimers(); });
  afterEach(() => { vi.useRealTimers(); });

  it('延迟执行函数', () => {
    const fn = vi.fn();
    const debounced = debounce(fn, 300);

    debounced();
    expect(fn).not.toHaveBeenCalled();

    vi.advanceTimersByTime(300);
    expect(fn).toHaveBeenCalledTimes(1);
  });

  it('快速多次调用只执行最后一次', () => {
    const fn = vi.fn();
    const debounced = debounce(fn, 300);

    debounced();
    debounced();
    debounced();

    vi.advanceTimersByTime(300);
    expect(fn).toHaveBeenCalledTimes(1);
  });

  it('传递参数', () => {
    const fn = vi.fn();
    const debounced = debounce(fn, 300);

    debounced('a', 1);
    vi.advanceTimersByTime(300);

    expect(fn).toHaveBeenCalledWith('a', 1);
  });

  it('定时器重置', () => {
    const fn = vi.fn();
    const debounced = debounce(fn, 300);

    debounced();
    vi.advanceTimersByTime(200);
    debounced();
    vi.advanceTimersByTime(200);
    expect(fn).not.toHaveBeenCalled();

    vi.advanceTimersByTime(100);
    expect(fn).toHaveBeenCalledTimes(1);
  });
});

describe('renderErrorState', () => {
  it('渲染错误消息和重试按钮', () => {
    const container = document.createElement('div');
    renderErrorState(container, '加载失败', () => {});
    expect(container.innerHTML).toContain('加载失败');
    expect(container.innerHTML).toContain('重试');
  });

  it('不提供回调时不渲染重试按钮', () => {
    const container = document.createElement('div');
    renderErrorState(container, '加载失败');
    expect(container.innerHTML).not.toContain('重试');
  });

  it('对错误消息进行 HTML 转义', () => {
    const container = document.createElement('div');
    renderErrorState(container, '<script>alert(1)</script>');
    expect(container.innerHTML).not.toContain('<script>');
    expect(container.innerHTML).toContain('&lt;script&gt;');
  });

  it('点击重试按钮触发回调', () => {
    const container = document.createElement('div');
    const retryFn = vi.fn();
    renderErrorState(container, '错误', retryFn);

    const retryBtn = container.querySelector('#retryBtn');
    retryBtn.click();
    expect(retryFn).toHaveBeenCalledTimes(1);
  });
});

describe('renderLoadingState', () => {
  it('渲染加载提示', () => {
    const container = document.createElement('div');
    renderLoadingState(container);
    expect(container.innerHTML).toContain('加载中');
  });

  it('自定义加载文案', () => {
    const container = document.createElement('div');
    renderLoadingState(container, '正在获取数据...');
    expect(container.innerHTML).toContain('正在获取数据...');
  });

  it('对消息进行 HTML 转义', () => {
    const container = document.createElement('div');
    renderLoadingState(container, '<b>loading</b>');
    expect(container.innerHTML).not.toContain('<b>');
  });
});
