// ============================================================
// 专业星图 — 分享卡片生成器 (Canvas)
// 生成 600×800 的测评结果分享图
// ============================================================

const W = 600;
const H = 800;
const PADDING = 40;

// 温暖配色
const COLORS = {
  bg: '#FFF8F5',
  cardBg: '#FFFFFF',
  primary: '#E67E22',
  primaryDark: '#D35400',
  secondary: '#705A49',
  textMuted: '#8B7E74',
  accent: '#FAD7B2',
  white: '#FFFFFF',
  border: '#EBE0D6',
};

// 简单的 emoji→文字 映射（Canvas 不能可靠地渲染 emoji）
const EMOJI_MAP = {
  '🎓': '▶', '💰': '◎', '⚖️': '◈', '📚': '▣',
  '📖': '▤', '📜': '▥', '🔢': '◉', '💻': '◆',
  '🌾': '✦', '🩺': '❤', '📋': '◻', '🎭': '◇', '🔬': '○',
};

function roundRect(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(x + w - r, y);
  ctx.quadraticCurveTo(x + w, y, x + w, y + r);
  ctx.lineTo(x + w, y + h - r);
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  ctx.lineTo(x + r, y + h);
  ctx.quadraticCurveTo(x, y + h, x, y + h - r);
  ctx.lineTo(x, y + r);
  ctx.quadraticCurveTo(x, y, x + r, y);
  ctx.closePath();
}

function drawBackground(ctx) {
  // 渐变背景
  const grad = ctx.createLinearGradient(0, 0, W, H);
  grad.addColorStop(0, '#FFF8F5');
  grad.addColorStop(0.5, '#FFF3E8');
  grad.addColorStop(1, '#FFF8F5');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, W, H);

  // 装饰圆
  ctx.globalAlpha = 0.06;
  ctx.fillStyle = COLORS.primary;
  ctx.beginPath();
  ctx.arc(W - 60, 120, 180, 0, Math.PI * 2);
  ctx.fill();
  ctx.beginPath();
  ctx.arc(60, H - 180, 140, 0, Math.PI * 2);
  ctx.fill();
  ctx.globalAlpha = 1;
}

function drawHeader(ctx) {
  const centerX = W / 2;
  let y = 60;

  // Logo
  ctx.fillStyle = COLORS.secondary;
  ctx.font = 'bold 32px "Literata", "Georgia", serif';
  ctx.textAlign = 'center';
  ctx.fillText('专业星图', centerX, y + 32);

  // Subtitle
  y += 55;
  ctx.fillStyle = COLORS.primary;
  ctx.font = 'bold 20px "PingFang SC", "Microsoft YaHei", sans-serif';
  ctx.fillText('专业适配测评', centerX, y + 20);

  // Divider
  y += 40;
  ctx.strokeStyle = COLORS.border;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(PADDING + 40, y);
  ctx.lineTo(W - PADDING - 40, y);
  ctx.stroke();
}

function drawMajorCards(ctx, results) {
  let y = 210;
  const cardH = 120;
  const cardW = W - PADDING * 2;
  const gap = 16;

  for (let i = 0; i < Math.min(3, results.length); i++) {
    const r = results[i];
    const m = r.major || {};

    // 卡片背景
    ctx.fillStyle = (i === 0) ? '#FFF3E0' : COLORS.cardBg;
    ctx.strokeStyle = (i === 0) ? COLORS.primary : COLORS.border;
    ctx.lineWidth = (i === 0) ? 2 : 1;
    roundRect(ctx, PADDING, y, cardW, cardH, 14);
    ctx.fill();
    ctx.stroke();

    // 排名
    const cx = PADDING + 36;
    const cy = y + cardH / 2;
    if (i === 0) {
      // 👑 皇冠简笔画
      ctx.fillStyle = COLORS.primary;
      ctx.font = 'bold 24px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('#1', cx, cy - 6);
    } else {
      ctx.fillStyle = COLORS.textMuted;
      ctx.font = 'bold 20px "Literata", serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('#' + (i + 1), cx, cy - 6);
    }

    // 分隔线
    const sepX = PADDING + 68;
    ctx.strokeStyle = COLORS.border;
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(sepX, y + 20);
    ctx.lineTo(sepX, y + cardH - 20);
    ctx.stroke();

    // 专业名
    const nameX = sepX + 18;
    ctx.fillStyle = COLORS.secondary;
    ctx.font = 'bold 18px "PingFang SC", "Microsoft YaHei", sans-serif';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    ctx.fillText(m.name || r.name || '--', nameX, y + 36);

    // 门类
    ctx.fillStyle = COLORS.textMuted;
    ctx.font = '13px "PingFang SC", "Microsoft YaHei", sans-serif';
    ctx.fillText((m.category || r.category || ''), nameX, y + 60);

    // 薪资标签
    if (m.salary_range) {
      ctx.fillStyle = COLORS.secondary;
      ctx.font = '12px "PingFang SC", "Microsoft YaHei", sans-serif';
      const salaryW = ctx.measureText(m.salary_range).width + 20;
      roundRect(ctx, nameX, y + 72, salaryW + 4, 22, 11);
      ctx.fillStyle = '#F5EEE9';
      ctx.fill();
      ctx.fillStyle = COLORS.secondary;
      ctx.fillText(m.salary_range, nameX + 12, y + 83);
    }

    // 匹配度
    const scoreX = W - PADDING - 20;
    ctx.fillStyle = COLORS.primary;
    ctx.font = 'bold 30px "Literata", "Georgia", serif';
    ctx.textAlign = 'right';
    ctx.textBaseline = 'middle';
    ctx.fillText((r.percentage || 0) + '%', scoreX, cy - 8);

    ctx.fillStyle = COLORS.textMuted;
    ctx.font = '12px "PingFang SC", "Microsoft YaHei", sans-serif';
    ctx.fillText('匹配度', scoreX, cy + 22);

    y += cardH + gap;
  }
}

function drawTraits(ctx, traits) {
  if (!traits || traits.length === 0) return;

  let x = PADDING;
  let y = 615;
  const tagH = 30;
  const gap = 10;

  ctx.fillStyle = COLORS.secondary;
  ctx.font = 'bold 14px "PingFang SC", "Microsoft YaHei", sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText('你的特质', x, y - 10);
  y += 10;

  for (const trait of traits) {
    const text = '🧠 ' + trait;
    ctx.font = '13px "PingFang SC", "Microsoft YaHei", sans-serif';
    const tw = ctx.measureText(trait).width + 36;
    if (x + tw > W - PADDING) {
      x = PADDING;
      y += tagH + gap;
    }
    roundRect(ctx, x, y, tw, tagH, tagH / 2);
    ctx.fillStyle = '#FFF1E6';
    ctx.fill();
    ctx.strokeStyle = COLORS.accent;
    ctx.lineWidth = 1;
    ctx.stroke();
    ctx.fillStyle = COLORS.secondary;
    ctx.fillText(trait, x + 12, y + 20);
    x += tw + gap;
  }
}

function drawFooter(ctx) {
  const y = H - 70;

  ctx.fillStyle = COLORS.textMuted;
  ctx.font = '13px "PingFang SC", "Microsoft YaHei", sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('扫码或访问 专业星图 测测你的匹配专业', W / 2, y);

  ctx.fillStyle = COLORS.primary;
  ctx.font = '14px "PingFang SC", "Microsoft YaHei", sans-serif';
  ctx.fillText('working-pass.vercel.app', W / 2, y + 24);
}

/**
 * 生成测评分享卡片
 * @param {Array} results - 测评结果数组
 * @param {Array} traits - 用户特质标签
 * @returns {Promise<string>} dataURL (PNG)
 */
export async function generateShareCard(results, traits) {
  const canvas = document.createElement('canvas');
  canvas.width = W;
  canvas.height = H;
  const ctx = canvas.getContext('2d');

  drawBackground(ctx);
  drawHeader(ctx);
  drawMajorCards(ctx, results);
  drawTraits(ctx, traits);
  drawFooter(ctx);

  return canvas.toDataURL('image/png');
}

/**
 * 下载分享卡片为 PNG 文件
 */
export function downloadShareCard(dataURL) {
  const a = document.createElement('a');
  a.href = dataURL;
  a.download = '我的专业匹配测评.png';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

/**
 * 复制分享卡片到剪贴板（支持 PNG）
 */
// ---- 对比分享卡片 ----
function drawCompareHeader(ctx) {
  ctx.fillStyle = COLORS.secondary;
  ctx.font = 'bold 24px "Literata", "Georgia", serif';
  ctx.textAlign = 'center';
  ctx.fillText('专业星图 · 专业对比', W / 2, 60);

  // divider
  ctx.strokeStyle = COLORS.border;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(PADDING, 80);
  ctx.lineTo(W - PADDING, 80);
  ctx.stroke();
}

function drawCompareCards(ctx, majors) {
  const n = majors.length;
  const cardW = (W - PADDING * 2 - (n - 1) * 12) / n;
  const cardH = 160;
  const y = 100;

  majors.forEach((m, i) => {
    const x = PADDING + i * (cardW + 12);

    // card bg
    roundRect(ctx, x, y, cardW, cardH, 12);
    ctx.fillStyle = COLORS.cardBg;
    ctx.fill();
    ctx.strokeStyle = COLORS.border;
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // top accent bar
    roundRect(ctx, x, y, cardW, 4, 2);
    ctx.fillStyle = COLORS.primary;
    ctx.fill();

    // category badge
    const catIcon = (m.category_icon || '').replace(/[^一-龥]/g, '') || '◆';
    ctx.fillStyle = COLORS.accent;
    ctx.font = '11px "PingFang SC", "Microsoft YaHei", sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(catIcon + ' ' + (m.category || '').substring(0, 6), x + 10, y + 24);

    // major name
    ctx.fillStyle = COLORS.secondary;
    ctx.font = 'bold 15px "Literata", "Georgia", serif';
    const name = m.name.length > 6 ? m.name.substring(0, 6) + '…' : m.name;
    ctx.fillText(name, x + 10, y + 50);

    // stats
    const statsY = y + 80;
    ctx.fillStyle = COLORS.textMuted;
    ctx.font = '12px "PingFang SC", "Microsoft YaHei", sans-serif';
    ctx.fillText('薪资 ' + (m.salary_range || 'N/A'), x + 10, statsY);
    ctx.fillText('难度 ' + (m.difficulty || 'N/A'), x + 10, statsY + 22);
    ctx.fillText('学制 ' + (m.duration || 'N/A') + '年', x + 10, statsY + 44);
    ctx.fillText('学位 ' + (m.degree || 'N/A'), x + 10, statsY + 66);
  });
}

function drawCompareFooter(ctx) {
  const y = 310;
  ctx.strokeStyle = COLORS.border;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(PADDING, y);
  ctx.lineTo(W - PADDING, y);
  ctx.stroke();

  ctx.fillStyle = COLORS.textMuted;
  ctx.font = '13px "PingFang SC", "Microsoft YaHei", sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('来自 专业星图 — 温暖、专业的大学专业选择指南', W / 2, y + 30);

  ctx.fillStyle = COLORS.primary;
  ctx.font = '14px "PingFang SC", "Microsoft YaHei", sans-serif';
  ctx.fillText('working-pass.vercel.app', W / 2, y + 54);
}

/**
 * 生成专业对比分享卡片
 * @param {Array} majors - 对比的专业数组 (2-4 items)
 * @returns {Promise<string>} dataURL (PNG)
 */
export async function generateCompareShareCard(majors) {
  const canvas = document.createElement('canvas');
  canvas.width = W;
  canvas.height = 400;
  const ctx = canvas.getContext('2d');

  // bg
  ctx.fillStyle = COLORS.bg;
  ctx.fillRect(0, 0, W, 400);

  drawCompareHeader(ctx);
  drawCompareCards(ctx, majors.slice(0, 4));
  drawCompareFooter(ctx);

  return canvas.toDataURL('image/png');
}

export async function copyShareCardToClipboard(dataURL) {
  const res = await fetch(dataURL);
  const blob = await res.blob();
  await navigator.clipboard.write([
    new ClipboardItem({ 'image/png': blob }),
  ]);
}
