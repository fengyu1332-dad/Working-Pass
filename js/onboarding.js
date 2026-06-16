// ============================================================
// 专业星图 - 新用户引导
// ============================================================

import { t } from './i18n.js';

// Inject onboarding styles once
const OBO_STYLES = `
#onboardingOverlay{position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity 0.4s;pointer-events:none;}
#onboardingOverlay.obo-visible{opacity:1;pointer-events:auto;}
.obo-backdrop{position:absolute;inset:0;background:rgba(44,38,33,0.6);backdrop-filter:blur(4px);}
.obo-dialog{position:relative;background:var(--surface-container,#fff);border-radius:24px;padding:40px 36px 32px;max-width:420px;width:90%;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,0.2);animation:obo-pop-in 0.4s cubic-bezier(0.34,1.56,0.64,1);}
#onboardingOverlay.obo-exit .obo-dialog{animation:obo-pop-out 0.3s ease forwards;}
@keyframes obo-pop-in{from{transform:scale(0.9) translateY(20px);opacity:0;}to{transform:scale(1) translateY(0);opacity:1;}}
@keyframes obo-pop-out{to{transform:scale(0.9) translateY(20px);opacity:0;}}
.obo-steps{display:flex;justify-content:center;gap:8px;margin-bottom:20px;}
.obo-dot{width:8px;height:8px;border-radius:50%;background:var(--outline,#ded0c6);transition:all 0.3s;}
.obo-dot.active{background:var(--primary,#e67e22);width:28px;border-radius:4px;}
.obo-dot.done{background:var(--primary-container,#fad7b2);}
.obo-icon{font-size:48px;margin-bottom:12px;}
.obo-title{font-family:"Literata",serif;font-size:22px;font-weight:700;color:var(--secondary,#705a49);margin-bottom:8px;}
.obo-desc{font-size:15px;color:var(--on-surface-variant,#8b7e74);line-height:1.7;margin-bottom:28px;}
.obo-actions{display:flex;gap:12px;justify-content:center;}
.obo-btn{padding:12px 28px;border-radius:14px;font-size:15px;font-weight:600;cursor:pointer;font-family:inherit;transition:all 0.2s;border:none;}
.obo-skip{background:transparent;color:var(--on-surface-variant,#8b7e74);}
.obo-skip:hover{color:var(--primary,#e67e22);}
.obo-next{background:linear-gradient(135deg,#E67E22,#D35400);color:#fff;}
.obo-next:hover{transform:translateY(-1px);box-shadow:0 4px 16px rgba(230,126,34,0.4);}
.obo-done-btn{background:linear-gradient(135deg,#E67E22,#D35400);}
`;
const styleEl = document.createElement('style');
styleEl.textContent = OBO_STYLES;
document.head.appendChild(styleEl);

const ONBOARDING_KEY = 'starmap_onboarding_done';
const STEPS = [
  {
    icon: '🌟',
    titleKey: 'onboarding_welcome_title',
    descKey: 'onboarding_welcome_desc',
  },
  {
    icon: '🔍',
    titleKey: 'onboarding_search_title',
    descKey: 'onboarding_search_desc',
  },
  {
    icon: '🧭',
    titleKey: 'onboarding_tools_title',
    descKey: 'onboarding_tools_desc',
  },
  {
    icon: '📊',
    titleKey: 'onboarding_report_title',
    descKey: 'onboarding_report_desc',
  },
];

export function isOnboardingDone() {
  try { return localStorage.getItem(ONBOARDING_KEY) === '1'; } catch { return false; }
}

export function resetOnboarding() {
  try { localStorage.removeItem(ONBOARDING_KEY); } catch { /* */ }
}

function buildOverlay() {
  const overlay = document.createElement('div');
  overlay.id = 'onboardingOverlay';
  overlay.innerHTML = `
    <div class="obo-backdrop"></div>
    <div class="obo-dialog">
      <div class="obo-steps">
        ${STEPS.map((_, i) => `<span class="obo-dot" data-step="${i}"></span>`).join('')}
      </div>
      <div class="obo-icon" id="oboIcon"></div>
      <h2 class="obo-title" id="oboTitle"></h2>
      <p class="obo-desc" id="oboDesc"></p>
      <div class="obo-actions">
        <button class="obo-btn obo-skip" id="oboSkip">${t('onboarding_skip', '跳过')}</button>
        <button class="obo-btn obo-next" id="oboNext">${t('onboarding_next', '下一步')}</button>
      </div>
    </div>
  `;
  return overlay;
}

let _currentStep = 0;
let _overlay = null;

function renderStep(step) {
  const s = STEPS[step];
  document.getElementById('oboIcon').textContent = s.icon;
  document.getElementById('oboTitle').textContent = t(s.titleKey);
  document.getElementById('oboDesc').textContent = t(s.descKey);

  document.querySelectorAll('.obo-dot').forEach((d, i) => {
    d.classList.toggle('active', i === step);
    d.classList.toggle('done', i < step);
  });

  const nextBtn = document.getElementById('oboNext');
  const skipBtn = document.getElementById('oboSkip');

  if (step === STEPS.length - 1) {
    nextBtn.textContent = t('onboarding_done', '开始探索');
    nextBtn.classList.add('obo-done-btn');
    skipBtn.style.display = 'none';
  } else {
    nextBtn.textContent = t('onboarding_next', '下一步');
    nextBtn.classList.remove('obo-done-btn');
    skipBtn.style.display = '';
  }
}

function finish() {
  try { localStorage.setItem(ONBOARDING_KEY, '1'); } catch { /* */ }
  if (_overlay) {
    _overlay.classList.add('obo-exit');
    setTimeout(() => {
      if (_overlay && _overlay.parentNode) _overlay.parentNode.removeChild(_overlay);
      _overlay = null;
    }, 400);
  }
}

function nextStep() {
  if (_currentStep >= STEPS.length - 1) {
    finish();
    return;
  }
  _currentStep++;
  renderStep(_currentStep);
}

export function startOnboarding() {
  if (isOnboardingDone()) return;
  if (document.getElementById('onboardingOverlay')) return;

  _currentStep = 0;
  _overlay = buildOverlay();
  document.body.appendChild(_overlay);

  // Bind events
  document.getElementById('oboSkip').addEventListener('click', finish);
  document.getElementById('oboNext').addEventListener('click', nextStep);

  // Keyboard nav
  const keyHandler = (e) => {
    if (e.key === 'Escape') finish();
    if (e.key === 'ArrowRight' || e.key === 'Enter') nextStep();
  };
  document.addEventListener('keydown', keyHandler, { once: false });
  const origFinish = finish;
  finish = () => {
    document.removeEventListener('keydown', keyHandler);
    origFinish();
  };

  renderStep(0);
  requestAnimationFrame(() => _overlay.classList.add('obo-visible'));
}
