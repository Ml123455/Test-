// ═══════════════════════════════════════════
// TEMPLATE ARTISAN — JavaScript
// Mobile nav, scroll animations, form handling
// ═══════════════════════════════════════════

(function() {
  'use strict';

  // Mobile nav toggle
  const toggle = document.getElementById('nav-toggle');
  const links = document.getElementById('nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function() {
      links.classList.toggle('active');
    });
    // Close on link click
    links.querySelectorAll('a').forEach(function(a) {
      a.addEventListener('click', function() {
        links.classList.remove('active');
      });
    });
  }

  // Shrink nav on scroll
  const nav = document.getElementById('nav');
  if (nav) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 60) {
        nav.classList.add('nav-scrolled');
      } else {
        nav.classList.remove('nav-scrolled');
      }
    });
  }

  // Fade-in animations on scroll
  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.service-card, .gallery-item, .highlight').forEach(function(el) {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
  });

  // Pré-remplir le formulaire de commande depuis la démo
  function prefillFromDemo() {
    try {
      var raw = localStorage.getItem('sitegen-v3');
      if (!raw) return;
      var d = JSON.parse(raw);
      if (document.getElementById('gen-name') || !document.querySelector('form.contact-form')) return; // on est sur la démo, pas la landing

      var nameEl = document.querySelector('input[name="name"]');
      var jobEl = document.querySelector('input[name="job"]');
      if (nameEl && d['gen-name']) nameEl.value = d['gen-name'];
      if (jobEl && d['gen-job']) jobEl.value = d['gen-job'];
    } catch(e) {}
  }
  prefillFromDemo();

})();
