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
