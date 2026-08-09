/* === FLOPPY FISH — PRODUCT PAGE LOGIC ================================
   Driven entirely by three globals the page defines BEFORE this loads:
     PRODUCT  – pricing, payhip keys, feature lists
     MEDIA    – carousel entries  { type:"image", src } | { type:"video", id }
     SCRIPTS  – script vault      { name, kind, location, file }
   This file contains no product content. Add a product by adding a page.
   ==================================================================== */
(function () {
  'use strict';

  var P = window.PRODUCT || {};
  var MEDIA_IN = window.MEDIA || [];
  var SCRIPTS_IN = window.SCRIPTS || [];

  var PAYHIP = 'https://payhip.com/buy?link=';

  /* ---------- helpers ---------- */
  function $(id) { return document.getElementById(id); }
  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function reduced() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  }

  var ICON = {
    check: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',
    spark: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 18h20l-1.5-9-4.5 4-4-6-4 6-4.5-4z"/></svg>',
    down: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 15V3"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/></svg>',
    copy: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="14" height="14" x="8" y="8" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>',
    file: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 12.5 8 15l2 2.5"/><path d="m14 12.5 2 2.5-2 2.5"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z"/></svg>',
    play: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="6 3 20 12 6 21 6 3"/></svg>',
    doc: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 13h4"/><path d="M10 17h4"/></svg>',
    eye: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.06 12.35a1 1 0 0 1 0-.7 10.75 10.75 0 0 1 19.88 0 1 1 0 0 1 0 .7 10.75 10.75 0 0 1-19.88 0"/><circle cx="12" cy="12" r="3"/></svg>'
  };

  /* =================================================================
     1. MEDIA CAROUSEL
     ================================================================= */
  var MEDIA = MEDIA_IN.filter(function (m) {
    if (!m) return false;
    if (m.type === 'video') return /^[A-Za-z0-9_-]{11}$/.test(m.id || '');
    return !!m.src;
  });

  var carIdx = 0, carTimer = null;

  function carSlide(m, i) {
    if (m.type === 'video') {
      return '<div class="ffcar-slide"><iframe src="https://www.youtube.com/embed/' + esc(m.id) +
        '" title="Tutorial video" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>';
    }
    return '<div class="ffcar-slide" data-i="' + i + '"><img src="' + esc(m.src) +
      '" alt="' + esc(P.name || '') + ' preview" loading="lazy" decoding="async"></div>';
  }

  function carUpdate() {
    var track = $('ffcarTrack');
    if (!track) return;
    track.style.transform = 'translateX(-' + (carIdx * 100) + '%)';
    var dots = document.querySelectorAll('.ffcar-dot');
    for (var i = 0; i < dots.length; i++) dots[i].classList.toggle('act', i === carIdx);
  }
  function carGo(i) { carIdx = ((i % MEDIA.length) + MEDIA.length) % MEDIA.length; carUpdate(); carAuto(); }
  function carAuto() {
    if (MEDIA.length <= 1 || reduced()) return;
    clearTimeout(carTimer);
    var dwell = (MEDIA[carIdx] && MEDIA[carIdx].type === 'video') ? 14000 : 5000;
    carTimer = setTimeout(function () { carGo(carIdx + 1); }, dwell);
  }

  function carRender() {
    var wrap = $('ffmedia'), car = $('ffcar'), track = $('ffcarTrack'), dots = $('ffcarDots');
    if (!wrap || !car || !track) return;
    if (!MEDIA.length) { wrap.style.display = 'none'; return; }

    track.innerHTML = MEDIA.map(carSlide).join('');
    dots.innerHTML = MEDIA.map(function (m, i) {
      return '<button class="ffcar-dot' + (i === 0 ? ' act' : '') + '" data-i="' + i +
        '" aria-label="' + (m.type === 'video' ? 'Video' : 'Image ' + (i + 1)) + '"></button>';
    }).join('');

    // an image that 404s removes itself rather than showing a broken box
    Array.prototype.forEach.call(track.querySelectorAll('img'), function (img) {
      img.addEventListener('error', function () {
        var slide = img.closest('.ffcar-slide');
        var i = parseInt(slide.getAttribute('data-i'), 10);
        MEDIA.splice(i, 1);
        carIdx = 0;
        if (!MEDIA.length) { wrap.style.display = 'none'; return; }
        carRender();
      });
    });

    if (MEDIA.length <= 1) { car.classList.add('ffcar-single'); }
    else { car.classList.remove('ffcar-single'); carAuto(); }

    dots.onclick = function (e) {
      var b = e.target.closest('.ffcar-dot');
      if (b) carGo(parseInt(b.getAttribute('data-i'), 10));
    };
    var prev = car.querySelector('.ffcar-btn.prev');
    var next = car.querySelector('.ffcar-btn.next');
    if (prev) prev.onclick = function () { carGo(carIdx - 1); };
    if (next) next.onclick = function () { carGo(carIdx + 1); };
    carUpdate();
  }

  /* =================================================================
     2. BUY PANEL  — defaults to FREE
     ================================================================= */
  function featRow(text, prem) {
    return '<div class="ff-buy-fi' + (prem ? ' pm' : '') + '">' +
      (prem ? ICON.spark : ICON.check) + '<span>' + esc(text) + '</span></div>';
  }

  function isPlaceholder(k) { return !k || /^(TODO|REPLACE|XXXX)/i.test(k); }

  function payBtn(key, cls, inner) {
    if (isPlaceholder(key)) {
      return '<span class="ffbtn ' + cls + ' is-soon" aria-disabled="true">' + inner + '</span>';
    }
    return '<a class="ffbtn ' + cls + '" href="' + PAYHIP + esc(key) +
      '" target="_blank" rel="noopener">' + inner + '</a>';
  }

  function setTab(mode) {
    var tf = $('fftbf'), tp = $('fftbp'), bc = $('ffbc'), bf = $('ffbf');
    if (!bc || !bf) return;
    if (tf) { tf.classList.toggle('act', mode === 'free'); tf.setAttribute('aria-selected', mode === 'free'); }
    if (tp) { tp.classList.toggle('act', mode === 'prem'); tp.setAttribute('aria-selected', mode === 'prem'); }

    var freeBtn = payBtn(P.freeKey, 'ffbtn-ghost', ICON.down + P.freeLabel);
    var premBtn = payBtn(P.premKey, 'ffbtn-prem',
      ICON.spark + 'Get ' + esc(P.paidName) + ' · ' + esc(P.premPrice));

    if (P.singleTier) {
      var showOrig1 = P.premOriginal && P.premOriginal !== P.premPrice;
      bc.innerHTML =
        '<div class="ff-pr-row"><span class="ff-pr">' + esc(P.premPrice) + '</span>' +
        (showOrig1 ? '<span class="ff-pr-orig">' + esc(P.premOriginal) + '</span>' : '') + '</div>' +
        '<div class="ff-pr-note">' + esc(P.priceNote || 'One-time purchase · Instant download') + '</div>' +
        premBtn +
        (P.extraBtns || []).map(function (b) {
          return '<a class="ffbtn ffbtn-ghost" href="' + esc(b.href) + '" target="_blank" rel="noopener">' +
            (ICON[b.icon] || '') + esc(b.label) + '</a>';
        }).join('');
      bf.innerHTML = '<div class="ff-buy-fl">' + esc(P.featsLabel || 'Includes') + '</div>' +
        (P.premFeatures || []).map(function (f) { return featRow(f, true); }).join('') +
        (P.buyFoot ? '<div class="ff-buy-foot">' + esc(P.buyFoot) + '</div>' : '');
      return;
    }

    if (mode === 'free') {
      bc.innerHTML =
        '<div class="ff-pr-row"><span class="ff-pr-free">Free</span></div>' +
        '<div class="ff-pr-note">No account tricks, no email wall · Instant download</div>' +
        freeBtn + premBtn;
      bf.innerHTML = '<div class="ff-buy-fl">What\'s in the free download</div>' +
        (P.freeFeatures || []).map(function (f) { return featRow(f, false); }).join('') +
        '<div class="ff-buy-foot">The scripts are on this page too — copy them straight from the vault below.</div>';
    } else {
      var showOrig = P.premOriginal && P.premOriginal !== P.premPrice;
      bc.innerHTML =
        '<div class="ff-pr-row"><span class="ff-pr">' + esc(P.premPrice) + '</span>' +
        (showOrig ? '<span class="ff-pr-orig">' + esc(P.premOriginal) + '</span>' : '') + '</div>' +
        '<div class="ff-pr-note">One-time purchase · Instant download · Yours forever</div>' +
        premBtn + freeBtn;
      bf.innerHTML = '<div class="ff-buy-fl">' + esc(P.paidName) + ' adds</div>' +
        (P.premFeatures || []).map(function (f) { return featRow(f, true); }).join('') +
        '<div class="ff-buy-foot">Buying is optional. It saves you the setup, nothing more.</div>';
    }
  }

  /* =================================================================
     3. SCRIPT VAULT
        Files are prefetched on load and cached, so the copy handler is
        SYNCHRONOUS. Awaiting a fetch inside a click handler breaks
        clipboard writes in iOS Safari — don't reintroduce that.
     ================================================================= */
  var cache = Object.create(null);   // file -> source string
  var failed = Object.create(null);

  function prefetch() {
    return Promise.all(SCRIPTS_IN.map(function (s) {
      return fetch(s.file, { cache: 'no-cache' })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
        .then(function (t) {
          t = t.replace(/^\uFEFF/, '').replace(/\s+$/, '');
          if (!t) throw new Error('empty');
          cache[s.file] = t;
        })
        .catch(function () { failed[s.file] = true; });
    }));
  }

  /* Legacy textarea + execCommand path. Still the only thing that works in a
     lot of in-app webviews (Instagram, TikTok, the YouTube app browser), which
     is exactly where a link from a video description gets opened. */
  function copyLegacy(text) {
    return new Promise(function (res, rej) {
      try {
        var ta = document.createElement('textarea');
        ta.value = text;
        ta.setAttribute('readonly', '');
        ta.contentEditable = 'true';
        ta.style.cssText = 'position:fixed;top:0;left:0;width:1px;height:1px;padding:0;border:none;outline:none;opacity:0;font-size:16px;';
        document.body.appendChild(ta);

        // iOS refuses .select() on a readonly field — use a range instead.
        var ios = /ipad|iphone|ipod/i.test(navigator.userAgent);
        if (ios) {
          var range = document.createRange();
          range.selectNodeContents(ta);
          var sel = window.getSelection();
          sel.removeAllRanges();
          sel.addRange(range);
          ta.setSelectionRange(0, 999999);
        } else {
          ta.select();
          ta.setSelectionRange(0, text.length);
        }

        var ok = document.execCommand('copy');
        document.body.removeChild(ta);
        ok ? res() : rej(new Error('execCommand refused'));
      } catch (e) { rej(e); }
    });
  }

  function copySync(text) {
    if (navigator.clipboard && navigator.clipboard.writeText && window.isSecureContext) {
      // The async API can exist and still reject: permissions policy inside an
      // iframe, a locked-down webview, Firefox with asyncClipboard off. Falling
      // back only when the API is *absent* leaves those users stuck, so chain
      // the legacy path onto the rejection too.
      return navigator.clipboard.writeText(text).catch(function () {
        return copyLegacy(text);
      });
    }
    return copyLegacy(text);
  }

  function codeBlock(src) {
    var lines = src.split('\n');
    return '<div class="ffcode-bar"><span class="n">' + lines.length + ' lines · Lua</span></div>' +
      '<pre>' + lines.map(function (l) {
        return '<span class="cl">' + (esc(l) || ' ') + '</span>';
      }).join('') + '</pre>';
  }

  function renderVault() {
    var wrap = $('ffdlRows');
    if (!wrap) return;
    var live = SCRIPTS_IN.filter(function (s) { return !!cache[s.file]; });

    if (!SCRIPTS_IN.length || !live.length) {
      wrap.innerHTML = '<div class="ffdl-empty">The scripts for this system aren\'t up yet — ' +
        'they\'re in the video description in the meantime.</div>';
      return;
    }

    wrap.innerHTML = SCRIPTS_IN.map(function (s, i) {
      var bad = !cache[s.file];
      return '<div class="ffdl-row">' +
        '<div class="ffdl-top">' +
        '<span class="ffdl-row-ic">' + ICON.file + '</span>' +
        '<span class="ffdl-meta">' +
        '<span class="ffdl-name">' + esc(s.name) + '.lua</span>' +
        '<span class="ffdl-pills">' +
        '<span class="ffdl-pill">' + esc(s.kind) + '</span>' +
        '</span></span>' +
        '<span class="ffdl-acts">' +
        '<button class="ffdl-btn view" data-i="' + i + '" type="button"' + (bad ? ' disabled' : '') +
        ' aria-expanded="false">' + ICON.eye + '<span class="l">View</span></button>' +
        '<button class="ffdl-btn copy" data-i="' + i + '" type="button"' + (bad ? ' disabled' : '') +
        '>' + ICON.copy + '<span class="l">' + (bad ? 'Unavailable' : 'Copy') + '</span></button>' +
        '</span></div>' +
        '<div class="ffcode" id="ffcode' + i + '"></div>' +
        '</div>';
    }).join('');

    wrap.addEventListener('click', function (e) {
      var btn = e.target.closest('.ffdl-btn');
      if (!btn || btn.disabled) return;
      var i = parseInt(btn.getAttribute('data-i'), 10);
      var s = SCRIPTS_IN[i];
      var src = cache[s.file];
      if (!src) return;

      /* --- view / hide --- */
      if (btn.classList.contains('view')) {
        var box = $('ffcode' + i);
        var open = box.classList.contains('open');
        if (!open && !box.innerHTML) box.innerHTML = codeBlock(src);
        box.classList.toggle('open', !open);
        btn.setAttribute('aria-expanded', String(!open));
        btn.querySelector('.l').textContent = open ? 'View' : 'Hide';
        return;
      }

      /* --- copy (synchronous, cached) --- */
      if (btn.classList.contains('done')) return;
      var label = btn.querySelector('.l');
      copySync(src).then(function () {
        btn.classList.add('done');
        btn.querySelector('svg').outerHTML = ICON.check;
        label.textContent = 'Copied';
        setTimeout(function () {
          btn.classList.remove('done');
          btn.querySelector('svg').outerHTML = ICON.copy;
          label.textContent = 'Copy';
        }, 1700);
      }).catch(function () {
        var box = $('ffcode' + i);
        if (!box.innerHTML) box.innerHTML = codeBlock(src);
        box.classList.add('open');
        btn.classList.add('fail');
        label.textContent = 'Select it and press Ctrl+C';
        setTimeout(function () {
          btn.classList.remove('fail');
          label.textContent = 'Copy';
        }, 3200);
      });
    });
  }

  /* =================================================================
     4. ACCORDION (open by default) + hero jump
     ================================================================= */
  function initVaultShell() {
    var acc = $('ffdl'), head = $('ffdlHead');
    if (!acc || !head) return;
    head.addEventListener('click', function () {
      var open = acc.classList.toggle('open');
      head.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    var jump = $('ffJumpScripts');
    if (jump) {
      jump.addEventListener('click', function (e) {
        e.preventDefault();
        if (!acc.classList.contains('open')) {
          acc.classList.add('open');
          head.setAttribute('aria-expanded', 'true');
        }
        acc.scrollIntoView({ behavior: reduced() ? 'auto' : 'smooth', block: 'start' });
      });
    }
  }

  /* =================================================================
     5. MOBILE STICKY BAR
     ================================================================= */
  function initBar() {
    if (isPlaceholder(P.premKey)) return;
    var bar = document.createElement('div');
    bar.className = 'ffbar';
    bar.innerHTML =
      '<span class="ffbar-pr"><span class="a">' + esc(P.paidName) + '</span><span class="b">' + esc(P.premPrice) + '</span></span>' +
      (P.singleTier || isPlaceholder(P.freeKey) ? '' :
        '<a class="ffbtn ffbtn-ghost" href="' + PAYHIP + esc(P.freeKey) + '" target="_blank" rel="noopener">Free</a>') +
      '<a class="ffbtn ffbtn-prem" href="' + PAYHIP + esc(P.premKey) + '" target="_blank" rel="noopener">Get ' + esc(P.paidName) + '</a>';
    document.body.appendChild(bar);

    var panel = document.querySelector('.ff-buy');
    var head = document.querySelector('.ffdtl-head');
    var panelVisible = false, pastHero = false;

    function sync() { bar.classList.toggle('show', pastHero && !panelVisible); }

    if ('IntersectionObserver' in window) {
      if (panel) {
        new IntersectionObserver(function (es) {
          panelVisible = es[0].isIntersecting; sync();
        }, { threshold: 0.15 }).observe(panel);
      }
      if (head) {
        new IntersectionObserver(function (es) {
          pastHero = !es[0].isIntersecting; sync();
        }, { threshold: 0 }).observe(head);
      }
    } else {
      pastHero = true; sync();
    }
  }

  /* =================================================================
     BOOT
     ================================================================= */
  document.addEventListener('DOMContentLoaded', function () {
    P.freeLabel = P.freeLabel || 'Download the free files';
    P.paidName = P.paidName || 'Drop-in';
    carRender();

    var tabs = document.querySelector('.ff-buy-tabs');
    if (P.singleTier) {
      if (tabs) tabs.style.display = 'none';
      setTab('prem');
    } else {
      var tf = $('fftbf'), tp = $('fftbp');
      if (tf) tf.addEventListener('click', function () { setTab('free'); });
      if (tp) tp.addEventListener('click', function () { setTab('prem'); });
      setTab('free');   // free is the default. Deliberately.
    }

    initVaultShell();
    initBar();

    prefetch().then(renderVault);
  });
})();
