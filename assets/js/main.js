/* ============================================
   SAKSHAM ENGLISH SCHOOL — SHARED MAIN.JS
   Place in: assets/js/main.js

   In index.html add before </body>:
   <script src="assets/js/main.js"></script>

   In all other pages add before </body>:
   <script src="../assets/js/main.js"></script>
   ============================================ */

(function () {

  /* ── 1. PAGE LOADER ── */
  var loader = document.createElement('div');
  loader.id = 'pageLoader';
  loader.innerHTML = '<div class="loader-ring"></div>';
  document.body.prepend(loader);

  window.addEventListener('load', function () {
    setTimeout(function () {
      loader.classList.add('hidden');
      setTimeout(function () {
        if (loader.parentNode) loader.parentNode.removeChild(loader);
      }, 400);
    }, 350);
  });


  /* ── 2. SCROLL TO TOP BUTTON ── */
  var scrollBtn = document.createElement('button');
  scrollBtn.id = 'scrollTop';
  scrollBtn.title = 'Back to top';
  scrollBtn.setAttribute('aria-label', 'Scroll to top');
  scrollBtn.innerHTML =
    '<svg viewBox="0 0 24 24"><polyline points="18 15 12 9 6 15"/></svg>';
  document.body.appendChild(scrollBtn);

  scrollBtn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  window.addEventListener('scroll', function () {
    if (window.scrollY > 320) {
      scrollBtn.classList.add('visible');
    } else {
      scrollBtn.classList.remove('visible');
    }
  }, { passive: true });


  /* ── 3. NAVBAR SHRINK ON SCROLL ── */
  var navbar = document.getElementById('navbar');
  if (navbar) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 60) {
        navbar.style.height = '56px';
        navbar.style.boxShadow = '0 2px 16px rgba(0,0,0,0.13)';
      } else {
        navbar.style.height = '70px';
        navbar.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
      }
    }, { passive: true });
  }


  /* ── 4. SCROLL REVEAL (Intersection Observer) ── */
  var revealEls = document.querySelectorAll(
    '.why-card, .staff-card, .campus-card, .vision-block, ' +
    '.info-card, .unique-list li, .reason-item, .policy-block, ' +
    '.why-section, .unique-section, .about-section, ' +
    '.mgmt-heading, .staff-section, .principal-section, ' +
    '.campus-section, .contact-main, .gallery-welcome'
  );

  revealEls.forEach(function (el) {
    el.classList.add('reveal');
  });

  /* Left/right reveals for two-column sections */
  var leftEls = document.querySelectorAll(
    '.why-left, .event-text, .about-photo, .principal-text, .whyus-left, .policy-text'
  );
  leftEls.forEach(function (el) {
    el.classList.add('reveal-left');
  });

  var rightEls = document.querySelectorAll(
    '.why-right, .event-photo, .about-text, .principal-photo, .whyus-right, .admission-card'
  );
  rightEls.forEach(function (el) {
    el.classList.add('reveal-right');
  });

  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });

    document.querySelectorAll('.reveal, .reveal-left, .reveal-right')
      .forEach(function (el) {
        observer.observe(el);
      });
  } else {
    /* Fallback for older browsers */
    document.querySelectorAll('.reveal, .reveal-left, .reveal-right')
      .forEach(function (el) {
        el.classList.add('revealed');
      });
  }


  /* ── 5. LAZY IMAGE FADE IN ── */
  var lazyImgs = document.querySelectorAll('img[loading="lazy"]');
  lazyImgs.forEach(function (img) {
    img.addEventListener('load', function () {
      img.classList.add('loaded-lazy');
    });
    if (img.complete) {
      img.classList.add('loaded-lazy');
    }
  });


  /* ── 6. SMOOTH ACTIVE NAV HIGHLIGHT ── */
  var currentPath = window.location.pathname;
  var navLinks = document.querySelectorAll('.nav-links a, .mobile-menu a');
  navLinks.forEach(function (link) {
    var href = link.getAttribute('href');
    if (href && currentPath === href) {
      link.classList.add('active');
    } else if (href && href !== '/' && currentPath.startsWith(href)) {
      link.classList.add('active');
    }
  });


  /* ── 7. COUNTER ANIMATION (for stats numbers on Home page) ── */
  function animateCounter(el, target, duration) {
    var start = 0;
    var startTime = null;
    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      var eased = progress < 0.5
        ? 2 * progress * progress
        : -1 + (4 - 2 * progress) * progress;
      var current = Math.floor(eased * target);
      el.textContent = current + (el.dataset.suffix || '');
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = target + (el.dataset.suffix || '');
      }
    }
    requestAnimationFrame(step);
  }

  /* Usage: add data-count="259" data-suffix="+" to any element */
  var counters = document.querySelectorAll('[data-count]');
  if (counters.length && 'IntersectionObserver' in window) {
    var counterObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var el = entry.target;
          var target = parseInt(el.dataset.count, 10);
          animateCounter(el, target, 1400);
          counterObs.unobserve(el);
        }
      });
    }, { threshold: 0.5 });
    counters.forEach(function (el) { counterObs.observe(el); });
  }


  /* ── 8. MOBILE MENU CLOSE ON OUTSIDE CLICK ── */
  document.addEventListener('click', function (e) {
    var menu = document.getElementById('mobileMenu');
    var ham = document.getElementById('hamburger');
    if (menu && ham && !ham.contains(e.target) && !menu.contains(e.target)) {
      menu.classList.remove('open');
      ham.classList.remove('open');
    }
  });


  /* ── 9. SMOOTH SCROLL FOR ANCHOR LINKS ── */
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });


  /* ── 10. FORM RIPPLE EFFECT ON SUBMIT BUTTONS ── */
  var submitBtns = document.querySelectorAll(
    '.btn-red, .send-btn, .wform-submit, .cform-submit, .footer-form .send-row button'
  );
  submitBtns.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      var ripple = document.createElement('span');
      var rect = btn.getBoundingClientRect();
      var size = Math.max(rect.width, rect.height);
      ripple.style.cssText =
        'position:absolute;border-radius:50%;' +
        'width:' + size + 'px;height:' + size + 'px;' +
        'left:' + (e.clientX - rect.left - size / 2) + 'px;' +
        'top:' + (e.clientY - rect.top - size / 2) + 'px;' +
        'background:rgba(255,255,255,0.25);' +
        'transform:scale(0);animation:rippleAnim 0.5s linear;' +
        'pointer-events:none;';
      if (getComputedStyle(btn).position === 'static') {
        btn.style.position = 'relative';
      }
      btn.style.overflow = 'hidden';
      btn.appendChild(ripple);
      setTimeout(function () {
        if (ripple.parentNode) ripple.parentNode.removeChild(ripple);
      }, 500);
    });
  });

  /* Ripple keyframe */
  if (!document.getElementById('rippleStyle')) {
    var style = document.createElement('style');
    style.id = 'rippleStyle';
    style.textContent =
      '@keyframes rippleAnim{to{transform:scale(2.5);opacity:0;}}';
    document.head.appendChild(style);
  }

})();