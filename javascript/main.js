/* main.js — progressive enhancement only.
   Every page already contains its full content as plain HTML; this file
   turns lists into interactive widgets. Vanilla JavaScript, except the
   poster track on the projects page, which uses GSAP + ScrollTrigger
   loaded from the CDN (see build.py). */
(function () {
  'use strict';
  var doc = document, root = doc.documentElement;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $(s, c) { return (c || doc).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function svgIcon(name) {
    var s = doc.createElementNS('http://www.w3.org/2000/svg', 'svg');
    s.setAttribute('class', 'ico'); s.setAttribute('aria-hidden', 'true');
    var u = doc.createElementNS('http://www.w3.org/2000/svg', 'use');
    u.setAttribute('href', '#i-' + name); s.appendChild(u); return s;
  }
  function el(tag, cls, text) { var e = doc.createElement(tag); if (cls) e.className = cls; if (text) e.textContent = text; return e; }
  function toast(msg) {
    var t = $('.toast') || doc.body.appendChild(el('div', 'toast'));
    t.setAttribute('role', 'status'); t.textContent = msg; t.classList.add('show');
    clearTimeout(t._h); t._h = setTimeout(function () { t.classList.remove('show'); }, 3200);
  }

  /* ---------- theme ---------- */
  var themeBtn = $('.theme-btn');
  function currentTheme() {
    var t = root.getAttribute('data-theme');
    if (t) return t;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  if (themeBtn) themeBtn.addEventListener('click', function () {
    var next = currentTheme() === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next); store('otep2_theme', next);
    themeBtn.setAttribute('aria-label', next === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
  });

  /* ---------- mobile menu ---------- */
  var menuBtn = $('.menu-btn'), drawer = $('#drawer');
  if (menuBtn && drawer) {
    function setMenu(open) { drawer.classList.toggle('open', open); menuBtn.setAttribute('aria-expanded', String(open)); menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu'); }
    menuBtn.addEventListener('click', function () { setMenu(menuBtn.getAttribute('aria-expanded') !== 'true'); });
    doc.addEventListener('keydown', function (e) { if (e.key === 'Escape' && drawer.classList.contains('open')) { setMenu(false); menuBtn.focus(); } });
    window.addEventListener('resize', function () { if (window.innerWidth >= 980) setMenu(false); });
  }

  /* ---------- Manila clock ---------- */
  var clock = $('#clock');
  if (clock) {
    var fmt;
    try { fmt = new Intl.DateTimeFormat('en-PH', { timeZone: 'Asia/Manila', hour: 'numeric', minute: '2-digit', hour12: true }); } catch (e) { fmt = null; }
    var tick = function () { clock.textContent = (fmt ? fmt.format(new Date()) : new Date().toLocaleTimeString()) + ' in Manila'; };
    tick(); setInterval(tick, 15000);
  }

  /* ---------- plain / technical toggle (shared by every page) ---------- */
  var techBtns = $$('[data-tech]');
  function setTech(on) {
    root.classList.toggle('show-tech', on);
    techBtns.forEach(function (b) { b.setAttribute('aria-pressed', String((b.getAttribute('data-tech') === 'on') === on)); });
    $$('details.more').forEach(function (d) { d.open = on; });
    store('otep2_tech', on ? '1' : '0');
  }
  techBtns.forEach(function (b) { b.addEventListener('click', function () { setTech(b.getAttribute('data-tech') === 'on'); }); });
  setTech(store('otep2_tech') === '1');

  /* ---------- Follow the Packet ---------- */
  $$('[data-packet]').forEach(function (box) {
    var scns = $$('.packet-scn', box); if (!scns.length) return;
    var tabs = $('.tabs', box), card = $('.step-card', box);
    var prev = $('[data-prev]', box), next = $('[data-next]', box), play = $('[data-play]', box), bar = $('.bar i', box);
    var si = 0, st = 0, timer = null, steps = [];
    function readSteps(s) {
      return $$('.steps-list li', s).map(function (li) {
        return { title: $('strong', li).textContent, plain: $('.plain', li).textContent, tech: $('.tech', li).textContent };
      });
    }
    scns.forEach(function (s, i) {
      var b = el('button'); b.type = 'button'; b.setAttribute('role', 'tab');
      b.appendChild(svgIcon(s.getAttribute('data-icon'))); b.appendChild(doc.createTextNode(s.getAttribute('data-label')));
      b.style.setProperty('--tab', 'var(--c-' + s.getAttribute('data-color') + ')');
      b.addEventListener('click', function () { stop(); show(i, 0); });
      tabs.appendChild(b);
      var route = $('.route', s); if (route) route.appendChild(el('span', 'packet-dot'));
    });
    function show(i, n) {
      si = i; st = n; var s = scns[i]; steps = readSteps(s);
      scns.forEach(function (x, k) { x.classList.toggle('active', k === i); });
      $$('button', tabs).forEach(function (b, k) { b.setAttribute('aria-selected', String(k === i)); });
      box.style.setProperty('--line', 'var(--c-' + s.getAttribute('data-color') + ')');
      var stations = $$('.station', s), route = $('.route', s);
      route.style.setProperty('--n', stations.length); route.style.setProperty('--i', n); route.style.setProperty('--line', 'var(--c-' + s.getAttribute('data-color') + ')');
      stations.forEach(function (x, k) { x.classList.toggle('done', k < n); x.classList.toggle('now', k === n); });
      var d = steps[n];
      $('.step-count', card).textContent = 'Step ' + (n + 1) + ' of ' + steps.length;
      $('.step-route', card).textContent = s.getAttribute('data-route');
      $('h4', card).textContent = d.title; $('.plain', card).textContent = d.plain; $('.tech', card).textContent = 'Technical: ' + d.tech;
      card.style.setProperty('--line', 'var(--c-' + s.getAttribute('data-color') + ')');
      bar.style.width = ((n + 1) / steps.length * 100) + '%';
      prev.disabled = n === 0; next.disabled = n === steps.length - 1;
    }
    function setPlaying(on) {
      play.setAttribute('aria-pressed', String(on));
      play.firstElementChild.replaceWith(svgIcon(on ? 'pause' : 'play'));
      $('span', play).textContent = on ? 'Pause' : 'Play journey';
      card.setAttribute('aria-live', on ? 'off' : 'polite');
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; setPlaying(false); } }
    function start(ms) {
      if (timer) return; setPlaying(true);
      if (st >= steps.length - 1) show(si, 0);
      timer = setInterval(function () { if (st < steps.length - 1) show(si, st + 1); else stop(); }, ms || 4200);
    }
    prev.addEventListener('click', function () { stop(); show(si, Math.max(0, st - 1)); });
    next.addEventListener('click', function () { stop(); show(si, Math.min(steps.length - 1, st + 1)); });
    play.addEventListener('click', function () { timer ? stop() : start(4200); });
    box.addEventListener('keydown', function (e) {
      if (e.target.closest('input,textarea')) return;
      if (e.key === 'ArrowRight') { next.click(); } else if (e.key === 'ArrowLeft') { prev.click(); }
    });
    show(0, 0);
    /* one orchestrated moment: on the home page the packet makes a single run */
    if (box.hasAttribute('data-autorun') && !reduce) {
      var started = false, run = function () { if (!started && !timer && st === 0) { started = true; start(1900); } };
      if ('IntersectionObserver' in window) {
        var io = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { io.disconnect(); setTimeout(run, 700); } }, { threshold: .5 });
        io.observe(box);
      }
    }
  });

  /* ---------- Everyday journeys ---------- */
  $$('[data-journeys]').forEach(function (wrap) {
    var list = $$('.journey', wrap), picks = $$('.pick', wrap);
    if (!list.length) return;
    var state = {};
    function build(j) {
      var steps = $$('.jstep', j), n = steps.length, i = 0;
      var count = $('.j-count', j), seg = $('.segbar', j), back = $('[data-back]', j), fwd = $('[data-fwd]', j);
      seg.textContent = '';
      steps.forEach(function (s, k) {
        var b = el('button'); b.type = 'button'; b.setAttribute('aria-label', 'Go to step ' + (k + 1) + ': ' + s.getAttribute('data-name'));
        b.addEventListener('click', function () { go(k); }); seg.appendChild(b);
      });
      function go(k, noScroll) {
        i = Math.max(0, Math.min(n - 1, k));
        steps.forEach(function (s, x) { s.classList.toggle('on', x === i); });
        $$('button', seg).forEach(function (b, x) { b.classList.toggle('on', x <= i); if (x === i) b.setAttribute('aria-current', 'step'); else b.removeAttribute('aria-current'); });
        count.textContent = 'Step ' + (i + 1) + ' of ' + n;
        back.disabled = i === 0;
        var last = i === n - 1;
        $('span', fwd).textContent = last ? 'Try another journey' : 'Next: ' + steps[i + 1].getAttribute('data-name');
        fwd.lastElementChild.replaceWith(svgIcon(last ? 'refresh' : 'arrow-right'));
        if (!noScroll) { var r = j.getBoundingClientRect(); if (r.top < 70) j.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' }); }
      }
      back.addEventListener('click', function () { go(i - 1); });
      fwd.addEventListener('click', function () {
        if (i < n - 1) { go(i + 1); return; }
        var idx = list.indexOf(j); select((idx + 1) % list.length, true);
      });
      state[j.id] = go; go(0, true);
    }
    list.forEach(build);
    function select(k, scroll) {
      list.forEach(function (j, x) { j.classList.toggle('active', x === k); });
      picks.forEach(function (p, x) { p.setAttribute('aria-selected', String(x === k)); });
      state[list[k].id](0, true);
      if (scroll) list[k].scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
      try { history.replaceState(null, '', '#' + list[k].id); } catch (e) { /* file:// */ }
    }
    picks.forEach(function (p, k) { p.addEventListener('click', function (e) { e.preventDefault(); select(k, true); }); });
    var h = (location.hash || '').slice(1), start = list.map(function (j) { return j.id; }).indexOf(h);
    if (start < 0) { start = 0; var firstLoad = true; }
    list.forEach(function (j, x) { j.classList.toggle('active', x === start); });
    picks.forEach(function (p, x) { p.setAttribute('aria-selected', String(x === start)); });
    if (start >= 0 && h) setTimeout(function () { list[start].scrollIntoView({ block: 'start' }); }, 60);
  });

  /* ---------- Learn one thing ---------- */
  $$('[data-tips]').forEach(function (box) {
    var items = $$('.tip-list > li', box); if (!items.length) return;
    var data = items.map(function (li) { return { t: $('h3', li).textContent, w: $('.why', li).textContent, a: $('.act', li).textContent }; });
    var day = Math.floor(Date.now() / 864e5);
    var i = day % data.length;
    var ui = el('div', 'tip-ui');
    var tag = el('p', 'small-label', ''), h = el('h2'), p = el('p'), act = el('div', 'tip-action'), nav = el('div', 'tip-nav');
    var ab = el('div'), aLab = el('b', '', 'Try this today'), aTxt = el('span'); ab.append(aLab, aTxt); act.append(svgIcon('bulb'), ab);
    var bp = el('button', 'icon-btn'); bp.type = 'button'; bp.setAttribute('aria-label', 'Previous tip'); bp.appendChild(svgIcon('arrow-left'));
    var bn = el('button', 'icon-btn'); bn.type = 'button'; bn.setAttribute('aria-label', 'Next tip'); bn.appendChild(svgIcon('arrow-right'));
    var where = el('span', 'where'); nav.append(bp, bn, where);
    ui.append(tag, h, p, act, nav);
    box.querySelector('.tip-panel').appendChild(ui);
    function r() { var d = data[i]; tag.textContent = 'Learn one thing'; h.textContent = d.t; p.textContent = d.w; aTxt.textContent = d.a; where.textContent = 'Tip ' + (i + 1) + ' of ' + data.length; }
    bp.addEventListener('click', function () { i = (i - 1 + data.length) % data.length; r(); });
    bn.addEventListener('click', function () { i = (i + 1) % data.length; r(); });
    r();
  });
  var checks = $$('[data-checklist] input[type=checkbox]');
  if (checks.length) {
    var saved = {}; try { saved = JSON.parse(store('otep2_done') || '{}'); } catch (e) { saved = {}; }
    var note = $('[data-progress]');
    var upd = function () { var n = checks.filter(function (c) { return c.checked; }).length; if (note) note.textContent = n === checks.length ? 'All ' + n + ' done. Your devices are in better shape than most.' : n + ' of ' + checks.length + ' done'; };
    checks.forEach(function (c) {
      c.checked = !!saved[c.value];
      c.addEventListener('change', function () { saved[c.value] = c.checked; store('otep2_done', JSON.stringify(saved)); upd(); });
    });
    upd();
  }

  /* ---------- project filter ---------- */
  $$('[data-filter-wrap]').forEach(function (wrap) {
    var chips = $$('.chip', wrap), cards = $$('.poster', wrap), out = $('[data-count]', wrap);
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        var f = c.getAttribute('data-filter'), n = 0;
        chips.forEach(function (x) { x.setAttribute('aria-pressed', String(x === c)); });
        cards.forEach(function (k) { var ok = f === 'all' || (' ' + k.getAttribute('data-tags') + ' ').indexOf(' ' + f + ' ') > -1; k.hidden = !ok; if (ok) n++; });
        if (out) out.textContent = 'Showing ' + n + ' of ' + cards.length + ' projects';
        if (window.ScrollTrigger) window.ScrollTrigger.refresh(); /* track got shorter/longer */
      });
    });
  });

  /* ---------- poster track: GSAP horizontal pin (projects page only) ----------
     GSAP + ScrollTrigger load from the CDN in build.py (projects page only).
     If they fail to load, or the visitor prefers reduced motion, or the
     screen is a phone, the track stays a plain swipeable strip / stack. */
  (function () {
    var section = $('#posters');
    if (!section) return;
    var track = $('.posters-track', section);
    if (!track) return;
    if (reduce) return;
    if (!window.gsap || !window.ScrollTrigger) return;
    gsap.registerPlugin(ScrollTrigger);
    var mm = gsap.matchMedia();
    mm.add('(min-width: 769px)', function () {
      section.classList.add('posters--pinned');
      var skewSetter = gsap.quickSetter('.poster-img', 'skewX', 'deg');
      var clampSkew = gsap.utils.clamp(-5, 5);
      var proxy = { skew: 0 };
      var getDist = function () {
        return Math.max(0, track.scrollWidth - document.documentElement.clientWidth);
      };
      gsap.to(track, {
        x: function () { return -getDist(); },
        ease: 'none',
        scrollTrigger: {
          trigger: section,
          start: 'top top',
          end: function () { return '+=' + getDist(); },
          pin: true,
          scrub: 1,
          anticipatePin: 1,
          invalidateOnRefresh: true,
          onUpdate: function (self) {
            var skew = clampSkew(self.getVelocity() / -250);
            if (Math.abs(skew) > Math.abs(proxy.skew)) {
              proxy.skew = skew;
              gsap.to(proxy, { skew: 0, duration: 0.8, ease: 'power3', overwrite: true, onUpdate: function () { skewSetter(proxy.skew); } });
            }
          }
        }
      });
      return function () { section.classList.remove('posters--pinned'); };
    });
  })();

  /* ---------- contact form ---------- */
  var form = $('[data-contact]');
  if (form) {
    var EMAIL = form.getAttribute('data-email');
    function field(id) { return doc.getElementById(id); }
    function mark(f, bad) { f.closest('.field').classList.toggle('bad', bad); f.setAttribute('aria-invalid', String(bad)); return !bad; }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = field('c-name'), mail = field('c-email'), msg = field('c-msg');
      var ok = mark(name, !name.value.trim());
      ok = mark(mail, !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(mail.value.trim())) && ok;
      ok = mark(msg, msg.value.trim().length < 10) && ok;
      if (!ok) { var first = form.querySelector('.bad input, .bad textarea'); if (first) first.focus(); return; }
      var kind = form.querySelector('input[name=kind]:checked'); kind = kind ? kind.value : 'Hello';
      var body = msg.value.trim() + '\n\nFrom: ' + name.value.trim() + ' (' + mail.value.trim() + ')';
      location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(kind + ' — from ' + name.value.trim()) + '&body=' + encodeURIComponent(body);
      toast('Opening your email app. Nothing happened? Copy my address instead.');
    });
    $$('input,textarea', form).forEach(function (f) { f.addEventListener('input', function () { if (f.closest('.bad')) f.closest('.field').classList.remove('bad'); }); });
  }
  $$('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var v = b.getAttribute('data-copy');
      if (navigator.clipboard) navigator.clipboard.writeText(v).then(function () { toast('Email address copied'); }, function () { toast(v); });
      else toast(v);
    });
  });
})();
