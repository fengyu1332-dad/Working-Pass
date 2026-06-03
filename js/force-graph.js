// ============================================================
// 专业星图 - 力导向关系图模块
// 22 学科门类 + 611 专业节点 · Canvas 渲染 · D3 物理引擎
// ============================================================

const CATEGORY_RADIUS = 34;
const MAJOR_RADIUS = 9;
const LINK_COLOR = '#DED0C6';
const LINK_DIM_COLOR = '#f0ece8';
const BG_COLOR = '#FFFFFF';
const CURSOR_DEFAULT = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32'%3E%3Cpolygon points='4,4 14,28 18,19 28,15' fill='%23000' stroke='%23fff' stroke-width='1.5'/%3E%3C/svg%3E\") 4 4, auto";
const CURSOR_POINTER = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32'%3E%3Cpath d='M12 2C10 2 8 4 8 6v14l-3-5-4 1 5 12 3 1 9-3V6c0-2-2-4-4-4z' fill='%23000' stroke='%23fff' stroke-width='1.2'/%3E%3C/svg%3E\") 8 2, pointer";
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
    this.focusedNode = null;
    this.highlightedCatId = null;
    this._focusedCat = null;
    this._touchStartNode = null;
    this._transform = { x: 0, y: 0, k: 1 };

    this.canvas = document.createElement('canvas');
    this.ctx = this.canvas.getContext('2d');
    this.canvas.style.display = 'block';
    this.canvas.style.cursor = CURSOR_DEFAULT;
    this.canvas.setAttribute('role', 'application');
    this.canvas.setAttribute('aria-label', '专业关系图谱。使用 Tab 键聚焦后，可用方向键在节点间导航，按 Enter 键选择节点。');
    this.canvas.tabIndex = 0;
    this.container.appendChild(this.canvas);

    // Live region for screen reader announcements
    this._liveRegion = document.createElement('div');
    this._liveRegion.setAttribute('aria-live', 'polite');
    this._liveRegion.setAttribute('aria-atomic', 'true');
    this._liveRegion.className = 'sr-only';
    this._liveRegion.style.cssText = 'position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;';
    this.container.appendChild(this._liveRegion);

    this._dpr = Math.min(window.devicePixelRatio || 1, 2);
    this._resize();

    this._setupZoom();
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
    if (this._focusedCat) {
      this._focusedCat = null;
      this._animateTransformTo({ x: 0, y: 0, k: 1 });
      setTimeout(() => this.fitView(), 650);
    }
    this._updateAllTargets();
  }

  resize() {
    this.width = this.container.clientWidth;
    this.height = this.container.clientHeight;
    this._resize();
    if (this.simulation) {
      this.simulation.force('x', d3.forceX(this.width / 2).strength(0.006));
      this.simulation.force('y', d3.forceY(this.height / 2).strength(0.006));
      this.simulation.alpha(0.3).restart();
      clearTimeout(this._fitViewTimer);
      this._fitViewTimer = setTimeout(() => this.fitView(), 250);
    }
  }

  /** 自动缩放使节点填满整个可视区域 */
  fitView(padding = 10) {
    if (!this.nodes.length) return;
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    this.nodes.forEach(n => {
      if (n.x < minX) minX = n.x;
      if (n.y < minY) minY = n.y;
      if (n.x > maxX) maxX = n.x;
      if (n.y > maxY) maxY = n.y;
    });
    const graphW = maxX - minX + padding * 2;
    const graphH = maxY - minY + padding * 2;
    if (graphW <= 0 || graphH <= 0) return;
    // 计算填满视口的缩放比，上限 3.0 避免过度放大
    const scale = Math.min(this.width / graphW, this.height / graphH, 3.0);
    const tx = (this.width - (minX + maxX) * scale) / 2;
    const ty = (this.height - (minY + maxY) * scale) / 2;
    this._transform = { x: tx, y: ty, k: scale };
    d3.select(this.canvas).call(this._zoom.transform, d3.zoomIdentity.translate(tx, ty).scale(scale));
  }

  _animateTransformTo(target) {
    const start = { ...this._transform };
    const duration = 600;
    const startTime = performance.now();
    const self = this;

    function step(now) {
      const elapsed = now - startTime;
      const t = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - t, 3); // ease-out cubic
      self._transform = {
        x: start.x + (target.x - start.x) * eased,
        y: start.y + (target.y - start.y) * eased,
        k: start.k + (target.k - start.k) * eased,
      };
      if (t < 1) {
        requestAnimationFrame(step);
      }
    }
    requestAnimationFrame(step);
  }

  _focusCategoryView(categoryName) {
    const catNode = this.nodes.find((n) => n.type === 'category' && n.name === categoryName);
    if (!catNode) return;

    const scale = 2;
    const cx = catNode.x;
    const cy = catNode.y;
    const tx = this.width / 2 - cx * scale;
    const ty = this.height / 2 - cy * scale;
    this._animateTransformTo({ x: tx, y: ty, k: scale });
  }

  destroy() {
    clearTimeout(this._fitViewTimer);
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
    this.canvas.addEventListener('keydown', (e) => this._onKeyDown(e));
    this.canvas.addEventListener('focus', () => this._onCanvasFocus());
    this.canvas.addEventListener('blur', () => this._onCanvasBlur());
    window.addEventListener('resize', () => this.resize());
  }

  _setupZoom() {
    this._zoom = d3.zoom()
      .filter(() => false)
      .on('zoom', (e) => {
        this._transform = e.transform;
      });
    d3.select(this.canvas).call(this._zoom);
  }

  _setupSimulation() {
    const self = this;
    this.simulation = d3.forceSimulation()
      .force('x', d3.forceX(this.width / 2).strength(0.006))
      .force('y', d3.forceY(this.height / 2).strength(0.006))
      .force('charge', d3.forceManyBody().strength(d => d.type === 'category' ? -450 : -130))
      .force('collide', d3.forceCollide().radius(d => (d.type === 'category' ? CATEGORY_RADIUS + 8 : MAJOR_RADIUS + 4)))
      .force('link', d3.forceLink().id(d => d.id).distance(d => d.type === 'cat-cat' ? 350 : 150))
      .force('bounds', () => {
        const margin = 30;
        for (const n of self.nodes) {
          const r = n.type === 'category' ? CATEGORY_RADIUS : MAJOR_RADIUS;
          if (n.x < margin + r) n.vx += (margin + r - n.x) * 0.025;
          if (n.x > self.width - margin - r) n.vx -= (n.x - self.width + margin + r) * 0.025;
          if (n.y < margin + r) n.vy += (margin + r - n.y) * 0.025;
          if (n.y > self.height - margin - r) n.vy -= (n.y - self.height + margin + r) * 0.025;
        }
      })
      .alphaDecay(0.012)
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

    // Pre-warm: run more ticks for even spread with weak center
    for (let i = 0; i < 350; i++) this.simulation.tick();
    this.simulation.alpha(0.08).alphaDecay(0.008);

    // Auto-fit view to show all nodes
    setTimeout(() => this.fitView(), 150);
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
    const t = this._transform;
    ctx.clearRect(0, 0, this.width, this.height);

    // Background
    ctx.fillStyle = BG_COLOR;
    ctx.fillRect(0, 0, this.width, this.height);

    // Apply zoom/pan transform
    ctx.save();
    ctx.translate(t.x, t.y);
    ctx.scale(t.k, t.k);

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
        const isHovered = n === this.hoveredNode;
        const fontSize = n.type === 'category' ? 32 : (isHovered ? 52 : 26);
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

    ctx.restore();
  }

  // --- Private: Interaction ---

  _findNodeAt(mx, my) {
    // Convert screen coords to graph coords (inverse zoom transform)
    const t = this._transform;
    const gx = (mx - t.x) / t.k;
    const gy = (my - t.y) / t.k;
    const sorted = [...this.nodes].sort((a, b) => b.zIndex - a.zIndex);
    for (const n of sorted) {
      if (n.currentOpacity < 0.05) continue;
      const dx = gx - n.x, dy = gy - n.y;
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
        } else if (hovered.type === 'category' && n.type === 'category') {
          // Hovering a category: other categories stay fully visible
          n.targetR = baseR;
          n.targetOpacity = 1;
          n.targetLabelOpacity = 1;
          n.targetZIndex = 2;
        } else if (connectedIds.has(n.id)) {
          n.targetR = baseR * 1.3;
          n.targetOpacity = 0.85;
          n.targetLabelOpacity = 0;
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
          n.targetLabelOpacity = 0;
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
        const isCatCat = l.type === 'cat-cat';
        l.targetOpacity = (isCatCat || connectedIds.has(srcId) || connectedIds.has(tgtId)) ? 1 : 0.03;
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
      if (node) this.canvas.style.cursor = CURSOR_POINTER;
      else this.canvas.style.cursor = CURSOR_DEFAULT;
      this._updateAllTargets();
    }
  }

  _onMouseLeave() {
    this.hoveredNode = null;
    this.canvas.style.cursor = CURSOR_DEFAULT;
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
      if (this.hoveredNode) this.canvas.style.cursor = CURSOR_POINTER;
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
          this._focusedCat = this._touchStartNode.name;
          this._focusCategoryView(this._touchStartNode.name);
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
        this._focusedCat = node.name;
        this._focusCategoryView(node.name);
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

  // --- Private: Keyboard Navigation ---

  _onKeyDown(e) {
    const visible = this.nodes.filter(n => n.currentOpacity > 0.1);
    if (!visible.length) return;

    if (e.key === 'ArrowUp' || e.key === 'ArrowDown' || e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
      e.preventDefault();
      const next = this._findNodeInDirection(e.key);
      if (next) {
        this.focusedNode = next;
        this.hoveredNode = next;
        this._updateAllTargets();
        this._announceNode(next);
        this._scrollToNode(next);
      }
    } else if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      if (this.focusedNode) {
        this._activateNode(this.focusedNode);
      }
    } else if (e.key === 'Escape') {
      if (this.highlightedCatId) {
        this.clearHighlight();
        this._liveRegion.textContent = '已取消门类高亮';
      }
    }
  }

  _onCanvasFocus() {
    if (!this.focusedNode && this.nodes.length > 0) {
      // Default to the first category node
      const firstCat = this.nodes.find(n => n.type === 'category' && n.currentOpacity > 0.1);
      if (firstCat) {
        this.focusedNode = firstCat;
        this.hoveredNode = firstCat;
        this._updateAllTargets();
        this._announceNode(firstCat);
      }
    }
    this.canvas.style.outline = '2px solid #E67E22';
    this.canvas.style.outlineOffset = '2px';
  }

  _onCanvasBlur() {
    this.canvas.style.outline = '';
  }

  _findNodeInDirection(key) {
    const current = this.focusedNode;
    const visible = this.nodes.filter(n => n.currentOpacity > 0.1);
    if (!visible.length) return null;

    if (!current) return visible[0];

    const cx = current.x, cy = current.y;
    let best = null;
    let bestScore = Infinity;

    visible.forEach(n => {
      if (n === current) return;
      const dx = n.x - cx, dy = n.y - cy;
      let score;
      switch (key) {
        case 'ArrowUp':    score = dy >= 0 ? Infinity : Math.abs(dx) * 1.5 - dy; break;
        case 'ArrowDown':  score = dy <= 0 ? Infinity : Math.abs(dx) * 1.5 + dy; break;
        case 'ArrowLeft':  score = dx >= 0 ? Infinity : Math.abs(dy) * 1.5 - dx; break;
        case 'ArrowRight': score = dx <= 0 ? Infinity : Math.abs(dy) * 1.5 + dx; break;
        default: score = Math.abs(dx) + Math.abs(dy);
      }
      if (score < bestScore) {
        bestScore = score;
        best = n;
      }
    });

    return best;
  }

  _activateNode(node) {
    if (node.type === 'category') {
      if (this.highlightedCatId === node.name) {
        this.clearHighlight();
        this._liveRegion.textContent = '已取消门类 ' + node.name + ' 的高亮';
      } else {
        this.highlightCategory(node.name);
        this._liveRegion.textContent = '已高亮门类 ' + node.name + '，包含 ' +
          this.nodes.filter(n => n.type === 'major' && n.category === node.name).length + ' 个专业';
      }
      if (this.options.onCategoryClick) this.options.onCategoryClick(node.name);
    } else if (node.type === 'major') {
      this._liveRegion.textContent = '已选择专业 ' + node.name;
      if (this.options.onMajorClick) {
        this.options.onMajorClick(node.majorData);
      } else if (node.code) {
        window.openModalByCode
          ? window.openModalByCode(node.code)
          : window.open(`majors.html?code=${node.code}`, '_self');
      }
    }
  }

  _announceNode(node) {
    const type = node.type === 'category' ? '门类' : '专业';
    this._liveRegion.textContent = type + ' ' + node.name;
  }

  _scrollToNode(node) {
    const t = this._transform;
    const sx = node.x * t.k + t.x;
    const sy = node.y * t.k + t.y;
    const margin = 100;
    if (sx < margin || sx > this.width - margin || sy < margin || sy > this.height - margin) {
      const targetX = this.width / 2 - node.x * t.k;
      const targetY = this.height / 2 - node.y * t.k;
      const transform = d3.zoomIdentity.translate(targetX, targetY).scale(t.k);
      d3.select(this.canvas).transition().duration(200).call(this._zoom.transform, transform);
    }
  }
}
