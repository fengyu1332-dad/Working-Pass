// ============================================================
// 专业星图 - HTML 内容清洗（防止 AI 生成内容中的 XSS）
// ============================================================

const KNOWN_SAFE_TAGS = new Set([
  'h1','h2','h3','h4','h5','h6',
  'p','div','span','br','hr',
  'ul','ol','li','dl','dt','dd',
  'table','thead','tbody','tr','th','td','caption','colgroup','col',
  'strong','b','em','i','u','s','del','ins','mark','sub','sup','small','code','kbd',
  'a','img',
  'blockquote','pre','figure','figcaption',
  'section','article','header','footer','nav','main','aside',
]);

const ALLOWED_ATTRS = new Set([
  'href','title','target','rel',
  'src','alt','width','height','loading',
  'class','id','style','lang','dir',
  'colspan','rowspan','scope',
  'start','type',
]);

const DANGEROUS_EVENTS = /^on\w+/i;
const JS_URL = /^\s*javascript:/i;

export function sanitizeHTML(html) {
  if (!html || typeof html !== 'string') return '';

  const template = document.createElement('template');
  template.innerHTML = html;

  walkAndClean(template.content);

  return template.innerHTML;
}

function walkAndClean(node) {
  // Text nodes are safe
  if (node.nodeType === 3) return;

  if (node.nodeType !== 1) {
    // Remove non-text, non-element nodes (comments, etc.)
    node.parentNode?.removeChild(node);
    return;
  }

  const tag = node.tagName?.toLowerCase();

  // Remove dangerous elements
  if (['script','iframe','object','embed','form','input','link','meta','base','applet','area','audio','video','source','track','canvas','svg','math'].includes(tag)) {
    node.parentNode?.removeChild(node);
    return;
  }

  // Remove unknown elements (not in safe list)
  if (!KNOWN_SAFE_TAGS.has(tag)) {
    // Replace with its children to preserve text content
    while (node.firstChild) {
      node.parentNode?.insertBefore(node.firstChild, node);
    }
    node.parentNode?.removeChild(node);
    return;
  }

  // Clean attributes
  if (node.attributes && node.attributes.length > 0) {
    const toRemove = [];
    for (const attr of node.attributes) {
      const name = attr.name?.toLowerCase();
      if (DANGEROUS_EVENTS.test(name) || !ALLOWED_ATTRS.has(name)) {
        toRemove.push(name);
      }
      // Check for javascript: URLs in href/src
      if ((name === 'href' || name === 'src') && JS_URL.test(attr.value)) {
        toRemove.push(name);
      }
    }
    for (const name of toRemove) {
      node.removeAttribute(name);
    }
  }

  // For <a> tags, add rel="noopener noreferrer" for safety
  if (tag === 'a' && node.getAttribute('target') === '_blank') {
    node.setAttribute('rel', 'noopener noreferrer');
  }

  // Recurse into children (use a copy since child list may change)
  const children = Array.from(node.childNodes);
  for (const child of children) {
    walkAndClean(child);
  }
}

// 挂载到全局 window 方便各处使用
if (typeof window !== 'undefined') {
  window.__starmap_sanitizeHTML = sanitizeHTML;
}
