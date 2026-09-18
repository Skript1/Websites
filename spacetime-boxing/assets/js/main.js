/* Spacetime Boxing — progressive enhancement only.
   Everything on the page works without this file. */
(() => {
  'use strict';

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── sticky nav shadow ─────────────────────────────────────────── */
  const nav = document.getElementById('nav');
  const onScroll = () => nav.classList.toggle('is-stuck', window.scrollY > 24);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ── mobile menu ───────────────────────────────────────────────── */
  const toggle = document.getElementById('navToggle');
  const menu = document.getElementById('mobileMenu');

  const setMenu = (open) => {
    toggle.setAttribute('aria-expanded', String(open));
    menu.hidden = !open;
    menu.classList.toggle('is-open', open);
    document.body.style.overflow = open ? 'hidden' : '';
  };

  toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
  menu.addEventListener('click', (e) => { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });

  /* ── scroll reveal ─────────────────────────────────────────────── */
  const revealables = document.querySelectorAll('.reveal');

  if (reduced || !('IntersectionObserver' in window)) {
    revealables.forEach((el) => el.classList.add('is-in'));
  } else {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry, i) => {
        if (!entry.isIntersecting) return;
        // small stagger for siblings coming into view together
        setTimeout(() => entry.target.classList.add('is-in'), i * 70);
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.12 });

    revealables.forEach((el) => io.observe(el));
  }

  /* ── stat counters ─────────────────────────────────────────────── */
  const counters = document.querySelectorAll('[data-count]:not([data-plain])');

  const runCount = (el) => {
    const target = Number(el.dataset.count);
    if (!Number.isFinite(target)) return;
    if (reduced) { el.textContent = String(target); return; }

    const start = performance.now();
    const dur = 1100;
    const step = (now) => {
      const t = Math.min((now - start) / dur, 1);
      const eased = 1 - Math.pow(1 - t, 3);
      el.textContent = String(Math.round(target * eased));
      if (t < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  if ('IntersectionObserver' in window) {
    const cio = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        runCount(entry.target);
        cio.unobserve(entry.target);
      });
    }, { threshold: 0.6 });
    counters.forEach((el) => cio.observe(el));
  } else {
    counters.forEach((el) => { el.textContent = el.dataset.count; });
  }

  /* ── booking form ──────────────────────────────────────────────── */
  const form = document.getElementById('bookForm');
  const status = document.getElementById('formStatus');

  const showError = (input, message) => {
    const field = input.closest('.field');
    field.classList.toggle('is-error', Boolean(message));
    const slot = field.querySelector('.err');
    if (slot) slot.textContent = message;
    input.setAttribute('aria-invalid', message ? 'true' : 'false');
  };

  const validate = () => {
    let ok = true;
    const name = form.elements.name;
    const contact = form.elements.contact;

    if (!name.value.trim()) { showError(name, 'Tell us what to call you.'); ok = false; }
    else showError(name, '');

    const v = contact.value.trim();
    const looksLikeEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
    const looksLikePhone = /^[+()\d][\d\s().-]{6,}$/.test(v);
    if (!looksLikeEmail && !looksLikePhone) {
      showError(contact, 'Add a phone number or an email so we can reply.');
      ok = false;
    } else showError(contact, '');

    return ok;
  };

  if (form) {
    form.addEventListener('submit', async (e) => {
      if (!validate()) { e.preventDefault(); return; }

      // If the endpoint hasn't been configured, fall back to a mailto/phone prompt
      // rather than silently posting into the void.
      if (form.action.includes('your-form-id')) {
        e.preventDefault();
        status.className = 'form__status is-bad';
        status.textContent = 'Form endpoint not configured yet — please call (323) 206-2804.';
        return;
      }

      e.preventDefault();
      const btn = form.querySelector('button[type="submit"]');
      const original = btn.textContent;
      btn.disabled = true;
      btn.textContent = 'Sending…';
      status.className = 'form__status';
      status.textContent = '';

      try {
        const res = await fetch(form.action, {
          method: 'POST',
          body: new FormData(form),
          headers: { Accept: 'application/json' }
        });
        if (!res.ok) throw new Error('Request failed');
        form.reset();
        status.className = 'form__status is-ok';
        status.textContent = "Got it — we'll be in touch shortly.";
      } catch {
        status.className = 'form__status is-bad';
        status.textContent = "Couldn't send that. Call (323) 206-2804 and we'll sort it out.";
      } finally {
        btn.disabled = false;
        btn.textContent = original;
      }
    });

    form.querySelectorAll('input').forEach((input) => {
      input.addEventListener('input', () => {
        if (input.closest('.field').classList.contains('is-error')) validate();
      });
    });
  }


  /* ── 3D: hero pointer parallax ─────────────────────────────────── */
  const fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  const canTilt = fine && !reduced;

  const hero = document.querySelector('.hero');
  const stage = document.querySelector('[data-stage]');

  if (hero && stage && canTilt) {
    // each depth layer declares how far it drifts
    stage.querySelectorAll('[data-depth]').forEach((el) => {
      el.style.setProperty('--d', el.dataset.depth);
    });

    let px = 0, py = 0, tx = 0, ty = 0, raf = null;

    const glide = () => {
      // ease toward the pointer instead of snapping to it
      px += (tx - px) * 0.08;
      py += (ty - py) * 0.08;
      hero.style.setProperty('--px', px.toFixed(4));
      hero.style.setProperty('--py', py.toFixed(4));

      if (Math.abs(tx - px) > 0.001 || Math.abs(ty - py) > 0.001) {
        raf = requestAnimationFrame(glide);
      } else {
        raf = null;
      }
    };

    const kick = () => { if (raf === null) raf = requestAnimationFrame(glide); };

    hero.addEventListener('pointermove', (e) => {
      const r = hero.getBoundingClientRect();
      tx = (e.clientX - r.left) / r.width * 2 - 1;   // -1 … 1
      ty = (e.clientY - r.top) / r.height * 2 - 1;
      kick();
    }, { passive: true });

    hero.addEventListener('pointerleave', () => { tx = 0; ty = 0; kick(); });
  }

  /* ── 3D: card / tile tilt ──────────────────────────────────────── */
  if (canTilt) {
    const MAX = 9; // degrees

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
      // a card can be focused by keyboard — never leave it skewed
      el.addEventListener('blur', leave, true);
    });
  }

  /* ── year ──────────────────────────────────────────────────────── */
  const year = document.getElementById('year');
  if (year) year.textContent = String(new Date().getFullYear());
})();
