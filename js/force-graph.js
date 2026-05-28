// ============================================================
// 专业星图 - 力导向关系图模块
// 22 学科门类 + 611 专业节点 · Canvas 渲染 · D3 物理引擎
// ============================================================

const CATEGORY_RADIUS = 20;
const MAJOR_RADIUS = 5;
const LINK_COLOR = '#DED0C6';
const LINK_DIM_COLOR = '#f0ece8';
const BG_COLOR = '#FFF8F5';
const ANIM_SPEED = 0.12;

const CATEGORY_PALETTE = [
  '#E67E22', '#27AE60', '#2980B9', '#8E44AD', '#C0392B',
  '#16A085', '#D35400', '#2C3E50', '#F39C12', '#7F8C8D',
  '#1ABC9C', '#E74C3C', '#3498DB', '#9B59B6', '#2ECC71',
  '#E91E63', '#00BCD4', '#FF5722', '#607D8B', '#795548',
  '#4CAF50', '#FF9800',
];

export class ForceGraph {
  constructor(container, options = {}) {
    this.container = container;
    this.options = options;
    this.width = container.clientWidth;
    this.height = container.clientHeight;

    this.nodes = [];
    this.links = [];
    this.categoryMap = {};
    this.simulation = null;
    this.hoveredNode = null;
    this.highlightedCatId = null;
    this._touchStartNode = null;

    this.canvas = document.createElement('canvas');
    this.ctx = this.canvas.getContext('2d');
    this.canvas.style.display = 'block';
    this.container.appendChild(this.canvas);

    this._dpr = Math.min(window.devicePixelRatio || 1, 2);
    this._resize();

    this._bindEvents();
    this._setupSimulation();
  }

  // --- Public API ---

  setData(majorsData) {
    this._buildGraph(majorsData);
    this._restartSimulation();
    this._startRender();
  }

  highlightCategory(categoryName) {
    this.highlightedCatId = categoryName;
    this._updateAllTargets();
  }

  clearHighlight() {
    this.highlightedCatId = null;
    this._updateAllTargets();
  }

  resize() {
    this.width = this.container.clientWidth;
    this.height = this.container.clientHeight;
    this._resize();
    if (this.simulation) {
      this.simulation.force('center', d3.forceCenter(this.width / 2, this.height / 2));
      this.simulation.alpha(0.3).restart();
    }
  }

  destroy() {
    cancelAnimationFrame(this._animFrame);
    if (this.simulation) this.simulation.stop();
    this.canvas.remove();
  }

  // --- Private: Setup ---

  _resize() {
    this.canvas.width = this.width * this._dpr;
    this.canvas.height = this.height * this._dpr;
    this.canvas.style.width = this.width + 'px';
    this.canvas.style.height = this.height + 'px';
    this.ctx.setTransform(this._dpr, 0, 0, this._dpr, 0, 0);
  }

  _bindEvents() {
    this.canvas.addEventListener('mousemove', (e) => this._onMouseMove(e));
    this.canvas.addEventListener('click', (e) => this._onClick(e));
    this.canvas.addEventListener('mouseleave', () => this._onMouseLeave());
    this.canvas.addEventListener('touchstart', (e) => this._onTouchStart(e), { passive: false });
    this.canvas.addEventListener('touchmove', (e) => this._onTouchMove(e), { passive: false });
    this.canvas.addEventListener('touchend', (e) => this._onTouchEnd(e));
    window.addEventListener('resize', () => this.resize());
  }

  _setupSimulation() {
    this.simulation = d3.forceSimulation()
      .force('center', d3.forceCenter(this.width / 2, this.height / 2))
      .force('charge', d3.forceManyBody().strength(-80))
      .force('collide', d3.forceCollide().radius(d => (d.type === 'category' ? CATEGORY_RADIUS + 4 : MAJOR_RADIUS + 2)))
      .force('link', d3.forceLink().id(d => d.id).distance(d => d.type === 'cat-cat' ? 180 : 90))
      .alphaDecay(0.02)
      .on('tick', () => { /* render handled by rAF */ });
  }

  // --- Private: Build Graph ---

  _buildGraph(majorsData) {
    this.nodes = [];
    this.links = [];
    this.categoryMap = {};
    const seenCat = new Set();

    majorsData.forEach((m) => {
      const cat = m.category || '其他';
      if (!seenCat.has(cat)) {
        seenCat.add(cat);
        const colorIdx = Object.keys(this.categoryMap).length % CATEGORY_PALETTE.length;
        this.categoryMap[cat] = {
          id: `cat-${cat}`,
          name: cat,
          type: 'category',
          color: CATEGORY_PALETTE[colorIdx],
          fx: null, fy: null,
        };
      }
    });

    // Category nodes
    const catNodes = Object.values(this.categoryMap);
    this.nodes.push(...catNodes);

    // Major nodes
    majorsData.forEach((m) => {
      const cat = m.category || '其他';
      this.nodes.push({
        id: `major-${m.id || m.code}`,
        name: m.name,
        code: m.code,
        type: 'major',
        category: cat,
        color: this.categoryMap[cat].color,
        majorData: m,
      });
    });

    // Category↔Category links (mesh)
    for (let i = 0; i < catNodes.length; i++) {
      for (let j = i + 1; j < catNodes.length; j++) {
        this.links.push({
          source: catNodes[i].id,
          target: catNodes[j].id,
          type: 'cat-cat',
        });
      }
    }

    // Major→Category links
    this.nodes.filter(n => n.type === 'major').forEach((major) => {
      this.links.push({
        source: major.id,
        target: `cat-${major.category}`,
        type: 'major-cat',
      });
    });

    // Initialize visual state
    this.nodes.forEach((n) => {
      const baseR = n.type === 'category' ? CATEGORY_RADIUS : MAJOR_RADIUS;
      n.currentR = baseR;
      n.targetR = baseR;
      n.currentOpacity = 1;
      n.targetOpacity = 1;
      n.currentLabelOpacity = n.type === 'category' ? 1 : 0;
      n.targetLabelOpacity = n.type === 'category' ? 1 : 0;
      n.zIndex = n.type === 'category' ? 2 : 1;
      n.targetZIndex = n.zIndex;
    });

    this.links.forEach((l) => {
      l.currentOpacity = 1;
      l.targetOpacity = 1;
    });
  }

  _restartSimulation() {
    this.simulation.nodes(this.nodes);
    this.simulation.force('link').links(this.links);
    this.simulation.alpha(1).restart();

    // Pre-warm: run 200 ticks silently
    for (let i = 0; i < 200; i++) this.simulation.tick();
    this.simulation.alpha(0.1).alphaDecay(0.01);
  }

  // --- Private: Render Loop ---

  _startRender() {
    const render = () => {
      this._animFrame = requestAnimationFrame(render);
      this._animate();
      this._draw();
    };
    this._animFrame = requestAnimationFrame(render);
  }

  _animate() {
    const factor = ANIM_SPEED;
    this.nodes.forEach((n) => {
      n.currentR += (n.targetR - n.currentR) * factor;
      n.currentOpacity += (n.targetOpacity - n.currentOpacity) * factor;
      n.currentLabelOpacity += (n.targetLabelOpacity - n.currentLabelOpacity) * factor;
      n.zIndex = n.targetZIndex;
    });
    this.links.forEach((l) => {
      l.currentOpacity += (l.targetOpacity - l.currentOpacity) * factor;
    });
  }

  _draw() {
    const ctx = this.ctx;
    ctx.clearRect(0, 0, this.width, this.height);

    // Background
    ctx.fillStyle = BG_COLOR;
    ctx.fillRect(0, 0, this.width, this.height);

    // Draw links
    this.links.forEach((l) => {
      if (l.currentOpacity < 0.02) return;
      const sx = l.source.x, sy = l.source.y;
      const tx = l.target.x, ty = l.target.y;
      ctx.beginPath();
      ctx.moveTo(sx, sy);
      ctx.lineTo(tx, ty);
      ctx.strokeStyle = l.type === 'cat-cat' ? LINK_DIM_COLOR : LINK_COLOR;
      ctx.globalAlpha = l.currentOpacity * 0.5;
      ctx.lineWidth = l.type === 'cat-cat' ? 0.6 : 0.4;
      ctx.stroke();
      ctx.globalAlpha = 1;
    });

    // Sort nodes by zIndex for correct overlap
    const sorted = [...this.nodes].sort((a, b) => a.zIndex - b.zIndex);

    // Draw nodes
    sorted.forEach((n) => {
      if (n.currentOpacity < 0.03) return;
      const x = n.x, y = n.y, r = n.currentR;

      // Glow for highlighted category's children
      if (this.highlightedCatId && n.type === 'major' && n.category === this.highlightedCatId) {
        ctx.beginPath();
        ctx.arc(x, y, r + 3, 0, Math.PI * 2);
        ctx.fillStyle = n.color;
        ctx.globalAlpha = 0.25 * n.currentOpacity;
        ctx.fill();
        ctx.globalAlpha = 1;
      }

      // Node circle
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fillStyle = n.color;
      ctx.globalAlpha = n.currentOpacity;
      ctx.fill();

      // Border for category nodes
      if (n.type === 'category') {
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 2;
        ctx.globalAlpha = n.currentOpacity;
        ctx.stroke();
      }
      ctx.globalAlpha = 1;

      // Label
      if (n.currentLabelOpacity > 0.01) {
        const fontSize = n.type === 'category' ? 12 : 10;
        ctx.font = `${fontSize}px "PingFang SC", "Microsoft YaHei", sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = n.type === 'category' ? '#2C2621' : '#8B7E74';

        // Measure and draw background pill for category labels
        if (n.type === 'category') {
          const metrics = ctx.measureText(n.name);
          const tw = metrics.width;
          const th = fontSize + 2;
          ctx.fillStyle = 'rgba(255,255,255,0.85)';
          ctx.globalAlpha = n.currentLabelOpacity;
          ctx.fillRect(x - tw / 2 - 6, y + r + 4, tw + 12, th + 4);
          ctx.fillStyle = '#2C2621';
        }

        ctx.globalAlpha = n.currentLabelOpacity;
        ctx.fillText(n.name, x, y + r + (n.type === 'category' ? fontSize / 2 + 6 : 12));
        ctx.globalAlpha = 1;
      }
    });
  }

  // --- Private: Interaction ---

  _findNodeAt(mx, my) {
    const sorted = [...this.nodes].sort((a, b) => b.zIndex - a.zIndex);
    for (const n of sorted) {
      if (n.currentOpacity < 0.05) continue;
      const dx = mx - n.x, dy = my - n.y;
      const r = Math.max(n.currentR, n.type === 'category' ? CATEGORY_RADIUS : MAJOR_RADIUS) + 4;
      if (dx * dx + dy * dy <= r * r) return n;
    }
    return null;
  }

  _isConnected(n1, n2) {
    if (n1.type === 'category' && n2.type === 'major' && n2.category === n1.name) return true;
    if (n2.type === 'category' && n1.type === 'major' && n1.category === n2.name) return true;
    if (n1.type === 'category' && n2.type === 'category') return true;
    return false;
  }

  _updateAllTargets() {
    const hovered = this.hoveredNode;
    const highlightedCat = this.highlightedCatId;

    // Determine which nodes to "show"
    const highlightedMajors = new Set();
    if (highlightedCat && !hovered) {
      this.nodes.forEach((n) => {
        if (n.type === 'major' && n.category === highlightedCat) highlightedMajors.add(n.id);
      });
    }

    const connectedIds = new Set();
    if (hovered) {
      connectedIds.add(hovered.id);
      this.nodes.forEach((n) => {
        if (n.id !== hovered.id && this._isConnected(hovered, n)) connectedIds.add(n.id);
      });
    }

    this.nodes.forEach((n) => {
      const baseR = n.type === 'category' ? CATEGORY_RADIUS : MAJOR_RADIUS;

      if (!hovered && !highlightedCat) {
        // Default: all normal
        n.targetR = baseR;
        n.targetOpacity = 1;
        n.targetLabelOpacity = n.type === 'category' ? 1 : 0;
        n.targetZIndex = n.type === 'category' ? 2 : 1;
      } else if (hovered) {
        if (n.id === hovered.id) {
          n.targetR = baseR * (n.type === 'category' ? 1.6 : 2.5);
          n.targetOpacity = 1;
          n.targetLabelOpacity = 1;
          n.targetZIndex = 10;
        } else if (connectedIds.has(n.id)) {
          n.targetR = baseR * 1.3;
          n.targetOpacity = 0.85;
          n.targetLabelOpacity = n.type === 'category' ? 0.9 : 0.6;
          n.targetZIndex = 8;
        } else {
          n.targetR = baseR * 0.4;
          n.targetOpacity = 0.08;
          n.targetLabelOpacity = 0;
          n.targetZIndex = 0;
        }
      } else if (highlightedCat) {
        // Category highlight mode (click on category)
        if (n.type === 'category' && n.name === highlightedCat) {
          n.targetR = baseR * 1.5;
          n.targetOpacity = 1;
          n.targetLabelOpacity = 1;
          n.targetZIndex = 10;
        } else if (highlightedMajors.has(n.id)) {
          n.targetR = baseR * 1.8;
          n.targetOpacity = 1;
          n.targetLabelOpacity = 0.7;
          n.targetZIndex = 8;
        } else if (n.type === 'category') {
          n.targetR = baseR * 0.7;
          n.targetOpacity = 0.3;
          n.targetLabelOpacity = 0.3;
          n.targetZIndex = 0;
        } else {
          n.targetR = baseR * 0.3;
          n.targetOpacity = 0.04;
          n.targetLabelOpacity = 0;
          n.targetZIndex = 0;
        }
      }
    });

    this.links.forEach((l) => {
      const srcId = typeof l.source === 'object' ? l.source.id : l.source;
      const tgtId = typeof l.target === 'object' ? l.target.id : l.target;
      if (!hovered && !highlightedCat) {
        l.targetOpacity = 1;
      } else if (hovered) {
        l.targetOpacity = (connectedIds.has(srcId) || connectedIds.has(tgtId)) ? 1 : 0.03;
      } else if (highlightedCat) {
        const isHighlightedLink = highlightedMajors.has(srcId) || highlightedMajors.has(tgtId)
          || srcId === `cat-${highlightedCat}` || tgtId === `cat-${highlightedCat}`;
        l.targetOpacity = isHighlightedLink ? 1 : 0.03;
      }
    });
  }

  _onMouseMove(e) {
    const rect = this.canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left, my = e.clientY - rect.top;
    const node = this._findNodeAt(mx, my);

    if (node !== this.hoveredNode) {
      this.hoveredNode = node;
      if (node) this.canvas.style.cursor = 'pointer';
      else this.canvas.style.cursor = 'grab';
      this._updateAllTargets();
    }
  }

  _onMouseLeave() {
    this.hoveredNode = null;
    this.canvas.style.cursor = 'default';
    this._updateAllTargets();
  }

  _onTouchStart(e) {
    e.preventDefault();
    if (e.touches.length === 1) {
      const rect = this.canvas.getBoundingClientRect();
      const mx = e.touches[0].clientX - rect.left;
      const my = e.touches[0].clientY - rect.top;
      this._touchStartNode = this._findNodeAt(mx, my);
      this.hoveredNode = this._touchStartNode;
      if (this.hoveredNode) this.canvas.style.cursor = 'pointer';
      this._updateAllTargets();
    }
  }

  _onTouchMove(e) {
    e.preventDefault();
    if (e.touches.length === 1) {
      const rect = this.canvas.getBoundingClientRect();
      const mx = e.touches[0].clientX - rect.left;
      const my = e.touches[0].clientY - rect.top;
      const node = this._findNodeAt(mx, my);
      if (node !== this.hoveredNode) {
        this.hoveredNode = node;
        this._updateAllTargets();
      }
    }
  }

  _onTouchEnd() {
    if (this._touchStartNode && this._touchStartNode === this.hoveredNode) {
      // Tap on same node → treat as click
      if (this._touchStartNode.type === 'category') {
        if (this.highlightedCatId === this._touchStartNode.name) {
          this.clearHighlight();
        } else {
          this.highlightCategory(this._touchStartNode.name);
        }
        if (this.options.onCategoryClick) this.options.onCategoryClick(this._touchStartNode.name);
      } else if (this._touchStartNode.type === 'major') {
        if (this.options.onMajorClick) {
          this.options.onMajorClick(this._touchStartNode.majorData);
        }
      }
    }
    // Clear hover on touch end
    setTimeout(() => {
      if (!this._touchStartNode || this._touchStartNode === this.hoveredNode) {
        this.hoveredNode = null;
        this._updateAllTargets();
      }
    }, 300);
    this._touchStartNode = null;
  }

  _onClick(e) {
    const rect = this.canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left, my = e.clientY - rect.top;
    const node = this._findNodeAt(mx, my);
    if (!node) return;

    if (node.type === 'category') {
      // Toggle highlight
      if (this.highlightedCatId === node.name) {
        this.clearHighlight();
      } else {
        this.highlightCategory(node.name);
      }
      if (this.options.onCategoryClick) this.options.onCategoryClick(node.name);
    } else if (node.type === 'major') {
      if (this.options.onMajorClick) {
        this.options.onMajorClick(node.majorData);
      } else if (node.code) {
        window.openModalByCode
          ? window.openModalByCode(node.code)
          : window.open(`majors.html?code=${node.code}`, '_self');
      }
    }
  }
}
