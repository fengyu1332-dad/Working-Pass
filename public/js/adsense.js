// ============================================================
// Google AdSense 广告管理
// 使用前将 PUBLISHER_ID 替换为你的 AdSense 发布商 ID
// ============================================================

(function () {
  // TODO: 替换为你的 AdSense 发布商 ID（格式：ca-pub-XXXXXXXXXXXX）
  var PUBLISHER_ID = 'ca-pub-XXXXXXXXXXXXXXXX';

  function init() {
    if (document.querySelector('script[src*="adsbygoogle"]')) return;

    var containers = document.querySelectorAll('.ad-container:not(.ad-loaded)');
    if (containers.length === 0) return;

    var script = document.createElement('script');
    script.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + PUBLISHER_ID;
    script.async = true;
    script.crossOrigin = 'anonymous';
    script.onload = function () {
      containers.forEach(function (el) {
        el.classList.add('ad-loaded');
        var ins = document.createElement('ins');
        ins.className = 'adsbygoogle';
        ins.style.display = 'block';
        ins.setAttribute('data-ad-client', PUBLISHER_ID);
        ins.setAttribute('data-ad-format', 'auto');
        ins.setAttribute('data-full-width-responsive', 'true');
        el.appendChild(ins);
        try {
          (window.adsbygoogle = window.adsbygoogle || []).push({});
        } catch (e) { /* ignore */ }
      });
    };
    document.head.appendChild(script);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
