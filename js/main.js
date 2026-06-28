// BotForge — Main JavaScript
// Navigation, scroll effects, form handling

document.addEventListener('DOMContentLoaded', () => {
  initNav();
  initScrollEffects();
  initContactForm();
  setActiveNavLink();
});

// ── Mobile Navigation ──
function initNav() {
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (!toggle || !links) return;

  toggle.addEventListener('click', () => {
    const isOpen = links.classList.toggle('open');
    toggle.classList.toggle('open');
    toggle.setAttribute('aria-expanded', isOpen);
  });

  // Close on link click
  links.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      links.classList.remove('open');
      toggle.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
}

// ── Scroll Effects ──
function initScrollEffects() {
  // Animate elements on scroll
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

  document.querySelectorAll('.animate').forEach(el => observer.observe(el));

  // Nav background opacity on scroll
  const nav = document.querySelector('.nav');
  if (!nav) return;
  window.addEventListener('scroll', () => {
    if (window.scrollY > 10) {
      nav.style.background = 'rgba(8,8,10,0.95)';
    } else {
      nav.style.background = 'rgba(8,8,10,0.85)';
    }
  }, { passive: true });
}

// ── Active Nav Link ──
function setActiveNavLink() {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-links a');
  
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (!href) return;
    
    // Exact match or root
    if (href === currentPath || 
        (currentPath === '/' && href === '/') ||
        (currentPath !== '/' && href !== '/' && currentPath.includes(href))) {
      link.classList.add('active');
    }
  });
}

// ── Contact Form ──
function initContactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    const originalText = btn.textContent;
    
    btn.disabled = true;
    btn.textContent = 'Envoi en cours...';
    
    const formData = new FormData(form);
    
    try {
      // Formspree — replace FORMSPREE_ID with real endpoint
      const response = await fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: { 'Accept': 'application/json' }
      });
      
      if (response.ok) {
        form.innerHTML = `
          <div style="text-align:center;padding:40px 20px">
            <div style="font-size:48px;margin-bottom:16px">✅</div>
            <h3 style="font-size:20px;margin-bottom:8px">Message envoyé !</h3>
            <p style="color:var(--text2)">On vous répond dans la journée.</p>
          </div>
        `;
      } else {
        throw new Error('Form submission failed');
      }
    } catch (err) {
      btn.disabled = false;
      btn.textContent = originalText;
      alert('Erreur lors de l\'envoi. Réessayez ou contactez-nous par email : contact@botforge.fr');
    }
  });
}

// ── Smooth Scroll ──
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
