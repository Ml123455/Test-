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

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    const originalText = btn.textContent;

    // Build email from form data
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const plan = document.getElementById('plan').value;
    const members = document.getElementById('members').value;
    const discord = document.getElementById('discord').value.trim();
    const message = document.getElementById('message').value.trim();

    const subject = encodeURIComponent('[BotForge] Demande essai gratuit — ' + name);
    let body = `Nom: ${name}\nEmail: ${email}\nPlan: ${plan}\nMembres: ${members}`;
    if (discord) body += `\nDiscord: ${discord}`;
    if (message) body += `\n\nMessage:\n${message}`;
    body += `\n\n---\nEnvoyé depuis botarmory.com`;

    // Open email client
    window.location.href = `mailto:contact@botforge.fr?subject=${subject}&body=${encodeURIComponent(body)}`;

    // Show success
    form.innerHTML = `
      <div style="text-align:center;padding:40px 20px">
        <div style="font-size:48px;margin-bottom:16px">📨</div>
        <h3 style="font-size:20px;margin-bottom:8px">Ouvrez votre email !</h3>
        <p style="color:var(--text2);margin-bottom:16px">Votre client email devrait s'ouvrir. Envoyez le message et on vous répond dans la journée.</p>
        <p style="font-size:13px;color:var(--text3)">
          Si rien ne s'ouvre, écrivez-nous à<br>
          <a href="mailto:contact@botforge.fr">contact@botforge.fr</a>
        </p>
      </div>
    `;
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
