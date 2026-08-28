/* Bouncy Castle Man, shared behaviour. Loaded on every page.
   Every block guards its own targets, so a missing element never throws. */

/* REVEAL (defined before first use) */
const io = new IntersectionObserver(es => {
  es.forEach(en => {
    if (en.isIntersecting) {
      en.target.style.opacity = '1';
      en.target.style.transform = 'none';
      io.unobserve(en.target);
    }
  });
}, { threshold: .08, rootMargin: '0px 0px -40px' });
document.querySelectorAll('[data-reveal]').forEach((el, i) => {
  el.style.transitionDelay = (i % 4 * 55) + 'ms';
  io.observe(el);
});

/* RAIL: top bar plus drawer below 1100px */
const burger = document.getElementById('burger'), rail = document.getElementById('rail');
if (burger && rail) {
  burger.addEventListener('click', () => {
    const open = rail.classList.toggle('open');
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  rail.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
    rail.classList.remove('open');
    burger.setAttribute('aria-expanded', 'false');
  }));
}

/* SHELVES: the arrows are an enhancement. The track scrolls by touch, wheel
   and keyboard on its own, so if this never runs nothing is lost. */
document.querySelectorAll('[data-shelf]').forEach(shelf => {
  const track = shelf.querySelector('.track');
  const prev = shelf.querySelector('[data-dir="prev"]');
  const next = shelf.querySelector('[data-dir="next"]');
  if (!track || !prev || !next) return;

  const step = () => {
    const card = track.firstElementChild;
    if (!card) return track.clientWidth;
    const gap = parseFloat(getComputedStyle(track).columnGap) || 16;
    return (card.getBoundingClientRect().width + gap) * Math.max(1,
      Math.floor(track.clientWidth / (card.getBoundingClientRect().width + gap)) - 1);
  };
  const sync = () => {
    const max = track.scrollWidth - track.clientWidth - 2;
    prev.disabled = track.scrollLeft <= 2;
    next.disabled = track.scrollLeft >= max;
  };
  prev.addEventListener('click', () => track.scrollBy({ left: -step(), behavior: 'smooth' }));
  next.addEventListener('click', () => track.scrollBy({ left: step(), behavior: 'smooth' }));
  track.addEventListener('scroll', sync, { passive: true });
  window.addEventListener('resize', sync);
  sync();
});

/* AREA CHECKER */
/* HERO SLIDESHOW. Crossfade, pause on hover, stop entirely for anyone who has
   asked for reduced motion. The first slide is already visible from the markup,
   so none of this is load bearing. */
const slidesEl = document.getElementById('heroSlides');
if (slidesEl) {
  const slides = [...slidesEl.querySelectorAll('.slide')];
  const dots = [...document.querySelectorAll('#heroDots .dot')];
  const cap = document.querySelector('.mast-tag');
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let i = 0, timer = null;

  function show(n) {
    i = (n + slides.length) % slides.length;
    slides.forEach((s, k) => s.classList.toggle('on', k === i));
    dots.forEach((d, k) => d.classList.toggle('on', k === i));
    if (cap) cap.textContent = slides[i].dataset.cap;
  }
  function start() { if (!still && !timer) timer = setInterval(() => show(i + 1), 5000); }
  function stop() { clearInterval(timer); timer = null; }

  dots.forEach((d, k) => d.addEventListener('click', () => { show(k); stop(); }));
  slidesEl.addEventListener('mouseenter', stop);
  slidesEl.addEventListener('mouseleave', start);
  /* Nothing animates while the hero is off screen. */
  new IntersectionObserver(es => es[0].isIntersecting ? start() : stop(),
                           { threshold: 0.2 }).observe(slidesEl);
}

/* DATE PICKER (hero) and the date it hands to the contact form.
   Not an availability calendar: no day is ever marked free or booked, because
   there is no booking data behind this site. It picks a date, puts it in the
   link to the contact page, and the contact page fills the field. */
const dpGrid = document.getElementById('dpGrid');
if (dpGrid) {
  const MONTHS = ['January','February','March','April','May','June','July',
                  'August','September','October','November','December'];
  const monthEl = document.getElementById('dpMonth');
  const goEl = document.getElementById('dpGo');
  const prevEl = document.getElementById('dpPrev');
  const nextEl = document.getElementById('dpNext');
  const today = new Date(); today.setHours(0, 0, 0, 0);
  let view = new Date(today.getFullYear(), today.getMonth(), 1);
  let picked = null;

  const iso = d => d.getFullYear() + '-' +
    String(d.getMonth() + 1).padStart(2, '0') + '-' +
    String(d.getDate()).padStart(2, '0');

  function render() {
    monthEl.textContent = MONTHS[view.getMonth()] + ' ' + view.getFullYear();
    prevEl.disabled = view.getFullYear() === today.getFullYear() &&
                      view.getMonth() === today.getMonth();
    dpGrid.textContent = '';
    /* Monday first: getDay() is 0 for Sunday, so shift it. */
    const lead = (new Date(view.getFullYear(), view.getMonth(), 1).getDay() + 6) % 7;
    for (let i = 0; i < lead; i++) dpGrid.appendChild(document.createElement('span'));
    const days = new Date(view.getFullYear(), view.getMonth() + 1, 0).getDate();
    for (let d = 1; d <= days; d++) {
      const date = new Date(view.getFullYear(), view.getMonth(), d);
      const b = document.createElement('button');
      b.type = 'button'; b.textContent = d;
      if (date < today) { b.disabled = true; }
      if (date.getTime() === today.getTime()) b.classList.add('today');
      if (picked && date.getTime() === picked.getTime()) {
        b.classList.add('on'); b.setAttribute('aria-pressed', 'true');
      }
      b.addEventListener('click', () => { picked = date; render(); });
      dpGrid.appendChild(b);
    }
    goEl.href = picked ? '/contact/?d=' + iso(picked) : '/contact/';
    goEl.textContent = picked
      ? 'Get a price for ' + picked.getDate() + ' ' + MONTHS[picked.getMonth()].slice(0, 3)
      : 'Get a price';
  }
  prevEl.addEventListener('click', () => {
    view = new Date(view.getFullYear(), view.getMonth() - 1, 1); render();
  });
  nextEl.addEventListener('click', () => {
    view = new Date(view.getFullYear(), view.getMonth() + 1, 1); render();
  });
  render();
}

/* The contact form picks the date up out of the URL. */
const dField = document.getElementById('d');
if (dField) {
  const q = new URLSearchParams(location.search).get('d');
  if (q && /^\d{4}-\d{2}-\d{2}$/.test(q)) {
    dField.value = q;
    dField.closest('form').scrollIntoView({ block: 'center' });
  }
}

const areaBtn = document.getElementById('areaBtn');
if (areaBtn) {
  areaBtn.addEventListener('click', () => {
    const v = document.getElementById('areaSel').value, r = document.getElementById('areaOut');
    if (!v) { r.textContent = 'Pick your area first.'; return; }
    if (v === '__other__') {
      r.innerHTML = 'Not listed? <a href="tel:0879005391" style="text-decoration:underline">Give us a call</a>, we may still reach you.';
    } else {
      r.textContent = 'Yes, we deliver to ' + v + '. Send us your date for a price.';
    }
  });
}

/* FAQ */
document.querySelectorAll('.faq-q').forEach(q => q.addEventListener('click', () => {
  const item = q.parentElement, a = item.querySelector('.faq-a'),
        open = item.classList.contains('open');
  document.querySelectorAll('.faq-item').forEach(i => {
    i.classList.remove('open');
    i.querySelector('.faq-a').style.maxHeight = null;
    i.querySelector('.faq-q').setAttribute('aria-expanded', 'false');
  });
  if (!open) {
    item.classList.add('open');
    a.style.maxHeight = a.scrollHeight + 'px';
    q.setAttribute('aria-expanded', 'true');
  }
}));

/* INIT */
const yr = document.getElementById('yr');
if (yr) yr.textContent = new Date().getFullYear();
