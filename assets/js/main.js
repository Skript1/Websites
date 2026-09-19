/* Spacetime Boxing — progressive enhancement only.
   Every page is complete and readable with this file absent. */
(() => {
  'use strict';

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  const canTilt = fine && !reduced;

  /* ── sticky nav ────────────────────────────────────────────────── */
  const nav = document.getElementById('nav');
  if (nav) {
    const onScroll = () => nav.classList.toggle('is-stuck', window.scrollY > 24);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ── mobile menu ───────────────────────────────────────────────── */
  const toggle = document.getElementById('navToggle');
  const menu = document.getElementById('mobileMenu');
  if (toggle && menu) {
    const setMenu = (open) => {
      toggle.setAttribute('aria-expanded', String(open));
      menu.hidden = !open;
      menu.classList.toggle('is-open', open);
      document.body.style.overflow = open ? 'hidden' : '';
    };
    toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
    menu.addEventListener('click', (e) => { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });
  }

  /* ── the round clock ───────────────────────────────────────────────
     A real 3:00 round and 1:00 rest, on a loop. It is the page's one
     honest piece of motion: the gym's whole subject is time. It ticks
     once a second, and only while the tab is visible and the clock is
     actually on screen — an off-screen timer is wasted battery.       */
  const clock = document.getElementById('roundClock');
  if (clock) {
    const face = clock.querySelector('[data-face]');
    const label = clock.querySelector('[data-phase]');
    const ROUND = 180, REST = 60;

    let left = ROUND;
    let resting = false;
    let timer = null;

    const paint = () => {
      const m = Math.floor(left / 60);
      const s = String(left % 60).padStart(2, '0');
      face.textContent = `${m}:${s}`;
      label.textContent = resting ? 'Rest' : 'Round';
      clock.classList.toggle('is-rest', resting);
    };

    const tick = () => {
      left -= 1;
      if (left < 0) { resting = !resting; left = resting ? REST : ROUND; }
      paint();
    };

    const start = () => { if (!timer && !reduced) timer = setInterval(tick, 1000); };
    const stop = () => { if (timer) { clearInterval(timer); timer = null; } };

    paint();

    if ('IntersectionObserver' in window) {
      new IntersectionObserver((entries) => {
        entries.forEach((e) => (e.isIntersecting && !document.hidden ? start() : stop()));
      }, { threshold: 0.1 }).observe(clock);
    } else {
      start();
    }
    document.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));
  }

  /* ── scroll reveal ─────────────────────────────────────────────── */
  const revealables = document.querySelectorAll('.reveal');
  if (reduced || !('IntersectionObserver' in window)) {
    revealables.forEach((el) => el.classList.add('is-in'));
  } else {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry, i) => {
        if (!entry.isIntersecting) return;
        setTimeout(() => entry.target.classList.add('is-in'), i * 65);
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.12 });
    revealables.forEach((el) => io.observe(el));
  }

  /* ── rail: mark the section you're in ──────────────────────────── */
  const railLinks = [...document.querySelectorAll('.rail a[href^="#"]')];
  if (railLinks.length && 'IntersectionObserver' in window) {
    const byId = new Map(railLinks.map((a) => [a.getAttribute('href').slice(1), a]));
    const seen = new Set();
    const mark = () => {
      const first = railLinks.find((a) => seen.has(a.getAttribute('href').slice(1)));
      railLinks.forEach((a) => a.classList.toggle('is-here', a === first));
    };
    const rio = new IntersectionObserver((entries) => {
      entries.forEach((e) => (e.isIntersecting ? seen.add(e.target.id) : seen.delete(e.target.id)));
      mark();
    }, { rootMargin: '-45% 0px -45% 0px' });
    byId.forEach((_, id) => { const s = document.getElementById(id); if (s) rio.observe(s); });
  }

  /* ── stat counters ─────────────────────────────────────────────── */
  const counters = document.querySelectorAll('[data-count]:not([data-plain])');
  const runCount = (el) => {
    const target = Number(el.dataset.count);
    if (!Number.isFinite(target)) return;
    if (reduced || document.hidden) { el.textContent = String(target); return; }
    const start = performance.now(), dur = 1000;
    /* rAF is throttled in background tabs; make sure the real number lands regardless. */
    setTimeout(() => { el.textContent = String(target); }, dur + 400);
    const step = (now) => {
      const t = Math.min((now - start) / dur, 1);
      el.textContent = String(Math.round(target * (1 - Math.pow(1 - t, 3))));
      if (t < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  if ('IntersectionObserver' in window) {
    const cio = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) { runCount(e.target); cio.unobserve(e.target); } });
    }, { threshold: 0.6 });
    counters.forEach((el) => cio.observe(el));
  } else {
    counters.forEach((el) => { el.textContent = el.dataset.count; });
  }

  /* ── hero pointer parallax ─────────────────────────────────────── */
  const hero = document.querySelector('.hero');
  const stage = document.querySelector('[data-stage]');
  if (hero && stage && canTilt) {
    stage.querySelectorAll('[data-depth]').forEach((el) => el.style.setProperty('--d', el.dataset.depth));
    let px = 0, py = 0, tx = 0, ty = 0, raf = null;
    const glide = () => {
      px += (tx - px) * 0.08;
      py += (ty - py) * 0.08;
      hero.style.setProperty('--px', px.toFixed(4));
      hero.style.setProperty('--py', py.toFixed(4));
      raf = (Math.abs(tx - px) > 0.001 || Math.abs(ty - py) > 0.001) ? requestAnimationFrame(glide) : null;
    };
    const kick = () => { if (raf === null) raf = requestAnimationFrame(glide); };
    hero.addEventListener('pointermove', (e) => {
      const r = hero.getBoundingClientRect();
      tx = (e.clientX - r.left) / r.width * 2 - 1;
      ty = (e.clientY - r.top) / r.height * 2 - 1;
      kick();
    }, { passive: true });
    hero.addEventListener('pointerleave', () => { tx = 0; ty = 0; kick(); });
  }

  /* ── tilt ──────────────────────────────────────────────────────── */
  if (canTilt) {
    const MAX = 8;
    document.querySelectorAll('[data-tilt]').forEach((el) => {
      let frame = null;
      const move = (e) => {
        if (frame) return;
        frame = requestAnimationFrame(() => {
          frame = null;
          const r = el.getBoundingClientRect();
          const x = (e.clientX - r.left) / r.width;
          const y = (e.clientY - r.top) / r.height;
          el.style.setProperty('--ry', ((x - 0.5) * 2 * MAX).toFixed(2) + 'deg');
          el.style.setProperty('--rx', ((0.5 - y) * 2 * MAX).toFixed(2) + 'deg');
          el.style.setProperty('--mx', (x * 100).toFixed(1) + '%');
          el.style.setProperty('--my', (y * 100).toFixed(1) + '%');
        });
      };
      const leave = () => {
        if (frame) { cancelAnimationFrame(frame); frame = null; }
        el.classList.remove('is-tilting');
        el.style.setProperty('--rx', '0deg');
        el.style.setProperty('--ry', '0deg');
      };
      el.addEventListener('pointerenter', () => el.classList.add('is-tilting'));
      el.addEventListener('pointermove', move, { passive: true });
      el.addEventListener('pointerleave', leave);
      el.addEventListener('blur', leave, true);
    });
  }

  /* ── booking form ──────────────────────────────────────────────── */
  const form = document.getElementById('bookForm');
  const status = document.getElementById('formStatus');
  if (form) {
    const showError = (input, message) => {
      const field = input.closest('.field');
      field.classList.toggle('is-error', Boolean(message));
      const slot = field.querySelector('.err');
      if (slot) slot.textContent = message;
      input.setAttribute('aria-invalid', message ? 'true' : 'false');
    };
    const validate = () => {
      let ok = true;
      const name = form.elements.name, contact = form.elements.contact;
      if (!name.value.trim()) { showError(name, 'Tell us what to call you.'); ok = false; }
      else showError(name, '');
      const v = contact.value.trim();
      const email = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
      const phone = /^[+()\d][\d\s().-]{6,}$/.test(v);
      if (!email && !phone) { showError(contact, 'Add a phone number or an email so we can reply.'); ok = false; }
      else showError(contact, '');
      return ok;
    };

    form.addEventListener('submit', async (e) => {
      if (!validate()) { e.preventDefault(); return; }
      if (form.action.includes('your-form-id')) {
        /* No form backend wired up yet: hand the enquiry to the visitor's mail client
           so the page still works end to end. Swap the Formspree id in contact.html
           to post it server-side instead. */
        e.preventDefault();
        const val = (n) => (form.elements[n] && form.elements[n].value.trim()) || '';
        const body = [
          'Name: ' + val('name'),
          'Contact: ' + val('contact'),
          'Experience: ' + val('level'),
          '',
          val('goal')
        ].join(String.fromCharCode(10));
        window.location.href = 'mailto:hello@spacetimeboxing.com'
          + '?subject=' + encodeURIComponent('Session enquiry — ' + (val('name') || 'website'))
          + '&body=' + encodeURIComponent(body);
        status.className = 'form__status is-ok';
        status.textContent = "Opening your email app — or just call (323) 206-2804.";
        return;
      }
      e.preventDefault();
      const btn = form.querySelector('button[type="submit"]');
      const original = btn.textContent;
      btn.disabled = true; btn.textContent = 'Sending…';
      status.className = 'form__status'; status.textContent = '';
      try {
        const res = await fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
        if (!res.ok) throw new Error('failed');
        form.reset();
        status.className = 'form__status is-ok';
        status.textContent = "Got it — we'll be in touch shortly.";
      } catch {
        status.className = 'form__status is-bad';
        status.textContent = "Couldn't send that. Call (323) 206-2804 and we'll sort it out.";
      } finally {
        btn.disabled = false; btn.textContent = original;
      }
    });

    form.querySelectorAll('input').forEach((input) => {
      input.addEventListener('input', () => {
        if (input.closest('.field').classList.contains('is-error')) validate();
      });
    });
  }

  /* ── year ──────────────────────────────────────────────────────── */
  document.querySelectorAll('[data-year]').forEach((el) => { el.textContent = String(new Date().getFullYear()); });
})();
