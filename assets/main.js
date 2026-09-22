/* Purple Key Title & Escrow - light interaction layer.
   Keeps to what the spec allows: no carousels, no counters, no autoplay.
   Everything here respects prefers-reduced-motion. */
(function () {
  'use strict';

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- mobile menu ---- */
  var burger = document.querySelector('.burger');
  var sheet = document.querySelector('.mobile');
  if (burger && sheet) {
    burger.addEventListener('click', function () {
      var open = burger.getAttribute('aria-expanded') === 'true';
      burger.setAttribute('aria-expanded', String(!open));
      burger.setAttribute('aria-label', open ? 'Open menu' : 'Close menu');
      sheet.hidden = open;
      document.body.style.overflow = open ? '' : 'hidden';
    });
    sheet.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        burger.setAttribute('aria-expanded', 'false');
        burger.setAttribute('aria-label', 'Open menu');
        sheet.hidden = true;
        document.body.style.overflow = '';
      }
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 920 && !sheet.hidden) {
        burger.setAttribute('aria-expanded', 'false');
        sheet.hidden = true;
        document.body.style.overflow = '';
      }
    });
  }

  /* ---- services dropdown: hover on pointer devices, click/keys everywhere ---- */
  var dd = document.querySelector('.has-dd');
  if (dd) {
    var btn = dd.querySelector('.dd-btn');
    var close = function () {
      dd.classList.remove('show');
      btn.setAttribute('aria-expanded', 'false');
    };
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = dd.classList.toggle('show');
      btn.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('click', function (e) {
      if (!dd.contains(e.target)) close();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });
    dd.addEventListener('focusout', function (e) {
      if (!dd.contains(e.relatedTarget)) close();
    });
  }

  /* ---- reveal on scroll ---- */
  var targets = document.querySelectorAll('.reveal, .cov-map');
  if (reduce || !('IntersectionObserver' in window)) {
    Array.prototype.forEach.call(targets, function (el) { el.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var el = entry.target;
      var sibs = el.parentNode ? el.parentNode.children : [];
      var i = Array.prototype.indexOf.call(sibs, el);
      el.style.transitionDelay = Math.min(i, 5) * 70 + 'ms';
      el.classList.add('in');
      io.unobserve(el);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  Array.prototype.forEach.call(targets, function (el) { io.observe(el); });
})();
