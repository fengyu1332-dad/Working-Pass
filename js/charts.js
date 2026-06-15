// ============================================================
// 专业星图 — D3 图表模块
// 雷达图 + 柱状图，纯函数，不依赖全局状态
// ============================================================

/**
 * 绘制雷达图（6轴能力画像）
 * @param {HTMLElement} container - 容器 DOM 元素
 * @param {{math_logic:number, verbal:number, hands_on:number, memory:number, spatial:number, stress:number}} data - 能力值 1-5
 */
export function drawRadarChart(container, data) {
  if (typeof d3 === 'undefined') return;
  container.innerHTML = '';

  const width = 300;
  const height = 300;
  const margin = 40;
  const radius = Math.min(width, height) / 2 - margin;

  const axes = [
    { key: 'math_logic', label: '数理逻辑' },
    { key: 'verbal', label: '语言表达' },
    { key: 'hands_on', label: '动手操作' },
    { key: 'memory', label: '记忆背诵' },
    { key: 'spatial', label: '空间想象' },
    { key: 'stress', label: '抗压能力' },
  ];

  const svg = d3.select(container)
    .append('svg')
    .attr('viewBox', `0 0 ${width} ${height}`)
    .attr('width', width)
    .attr('height', height)
    .append('g')
    .attr('transform', `translate(${width / 2},${height / 2})`);

  const levels = 5;
  const angleSlice = (Math.PI * 2) / axes.length;

  // 背景网格
  for (let lvl = 1; lvl <= levels; lvl++) {
    const r = (radius / levels) * lvl;
    const points = axes.map((_, i) => {
      const angle = angleSlice * i - Math.PI / 2;
      return [r * Math.cos(angle), r * Math.sin(angle)];
    });
    svg.append('polygon')
      .attr('points', points.map(p => p.join(',')).join(' '))
      .attr('fill', 'none')
      .attr('stroke', lvl === levels ? '#D4C5B9' : '#E8DDD4')
      .attr('stroke-width', lvl === levels ? 1.5 : 0.8);
  }

  // 轴线
  axes.forEach((_, i) => {
    const angle = angleSlice * i - Math.PI / 2;
    svg.append('line')
      .attr('x1', 0).attr('y1', 0)
      .attr('x2', radius * Math.cos(angle))
      .attr('y2', radius * Math.sin(angle))
      .attr('stroke', '#D4C5B9')
      .attr('stroke-width', 1);
  });

  // 数据多边形
  const dataPoints = axes.map((a, i) => {
    const val = (data[a.key] || 3) / 5; // 归一化到 0-1
    const angle = angleSlice * i - Math.PI / 2;
    return [radius * val * Math.cos(angle), radius * val * Math.sin(angle)];
  });

  svg.append('polygon')
    .attr('points', dataPoints.map(p => p.join(',')).join(' '))
    .attr('fill', 'rgba(230, 126, 34, 0.2)')
    .attr('stroke', '#E67E22')
    .attr('stroke-width', 2);

  // 数据点
  svg.selectAll('.dot')
    .data(dataPoints)
    .enter()
    .append('circle')
    .attr('cx', d => d[0])
    .attr('cy', d => d[1])
    .attr('r', 4)
    .attr('fill', '#E67E22');

  // 轴标签
  axes.forEach((a, i) => {
    const angle = angleSlice * i - Math.PI / 2;
    const labelR = radius + 20;
    const x = labelR * Math.cos(angle);
    const y = labelR * Math.sin(angle);
    svg.append('text')
      .attr('x', x)
      .attr('y', y)
      .attr('text-anchor', 'middle')
      .attr('dominant-baseline', 'middle')
      .attr('font-size', '11')
      .attr('fill', '#705A49')
      .attr('font-family', 'sans-serif')
      .text(a.label);
  });
}

/**
 * 绘制横向柱状图（Top 3 匹配度）
 * @param {HTMLElement} container - 容器 DOM 元素
 * @param {Array<{name:string, percentage:number}>} results - Top 3 结果
 */
export function drawMatchBarChart(container, results) {
  if (typeof d3 === 'undefined') return;
  container.innerHTML = '';

  const top3 = results.slice(0, 3);
  const width = 400;
  const barHeight = 36;
  const height = top3.length * (barHeight + 12) + 20;
  const margin = { left: 120, right: 60, top: 10, bottom: 10 };
  const chartWidth = width - margin.left - margin.right;

  const svg = d3.select(container)
    .append('svg')
    .attr('viewBox', `0 0 ${width} ${height}`)
    .attr('width', '100%')
    .attr('height', height);

  const g = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`);

  const colors = ['#E67E22', '#E8963E', '#EDB05A'];
  const maxPct = 100;

  top3.forEach((item, i) => {
    const y = i * (barHeight + 12);
    const barWidth = (item.percentage / maxPct) * chartWidth;

    // 专业名标签
    g.append('text')
      .attr('x', -8)
      .attr('y', y + barHeight / 2)
      .attr('text-anchor', 'end')
      .attr('dominant-baseline', 'middle')
      .attr('font-size', '12')
      .attr('font-weight', '600')
      .attr('fill', '#705A49')
      .attr('font-family', 'sans-serif')
      .text(item.name.length > 8 ? item.name.substring(0, 8) + '…' : item.name);

    // 背景条
    g.append('rect')
      .attr('x', 0)
      .attr('y', y)
      .attr('width', chartWidth)
      .attr('height', barHeight)
      .attr('rx', 6)
      .attr('fill', '#F5EEE9');

    // 数据条
    g.append('rect')
      .attr('x', 0)
      .attr('y', y)
      .attr('width', barWidth)
      .attr('height', barHeight)
      .attr('rx', 6)
      .attr('fill', colors[i]);

    // 百分比标签
    g.append('text')
      .attr('x', barWidth + 8)
      .attr('y', y + barHeight / 2)
      .attr('dominant-baseline', 'middle')
      .attr('font-size', '14')
      .attr('font-weight', '700')
      .attr('fill', i === 0 ? '#E67E22' : '#705A49')
      .attr('font-family', 'sans-serif')
      .text(item.percentage + '%');
  });
}
