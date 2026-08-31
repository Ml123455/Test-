/* ============================================================
   NIDO — main.js : nav mobile, animations, FAQ, panier (localStorage)
   ============================================================ */

/* ---------- Produit & bundles ---------- */
const NIDO_PRODUCT = {
  id: 'organisateur-tiroir',
  name: 'Organisateur de Tiroirs Modulable Nido',
  image: 'img/product-main.jpg',
  bundles: {
    '1x': { qty: 1, label: '1 set', price: 29.90, old: 49.90 },
    '2x': { qty: 2, label: '2 sets', price: 49.90, old: 99.80 },
    '3x': { qty: 3, label: '3 sets', price: 64.90, old: 149.70 }
  }
};

const SHIPPING_THRESHOLD = 50;
const SHIPPING_FEE = 3.90;

/* ---------- Panier (localStorage) ---------- */
function getCart() {
  try { return JSON.parse(localStorage.getItem('nido-cart') || '[]'); }
  catch (e) { return []; }
}
function saveCart(cart) {
  localStorage.setItem('nido-cart', JSON.stringify(cart));
  updateCartCount();
}
function updateCartCount() {
  const cart = getCart();
  const total = cart.reduce((s, i) => s + i.qty, 0);
  document.querySelectorAll('.nav-cart-count').forEach(el => { el.textContent = total; });
}

function addToCart(bundleKey, silent) {
  const bundle = NIDO_PRODUCT.bundles[bundleKey];
  if (!bundle) return;
  let cart = getCart();
  // one-product store : un seul type de ligne, on remplace la quantité
  const existing = cart.find(i => i.bundle === bundleKey);
  if (existing) {
    existing.qty += 1;
  } else {
    cart = []; // single-product : on ne garde qu'une référence
    cart.push({
      id: NIDO_PRODUCT.id,
      name: NIDO_PRODUCT.name,
      image: NIDO_PRODUCT.image,
      bundle: bundleKey,
      unitLabel: bundle.label,
      qty: 1,
      unitPrice: bundle.price
    });
  }
  saveCart(cart);
  if (!silent) showToast('Ajouté au panier ✓');
}

function removeFromCart(index) {
  const cart = getCart();
  cart.splice(index, 1);
  saveCart(cart);
  renderCart();
}

function changeQty(index, delta) {
  const cart = getCart();
  if (!cart[index]) return;
  cart[index].qty += delta;
  if (cart[index].qty < 1) cart[index].qty = 1;
  saveCart(cart);
  renderCart();
}

function cartSubtotal() {
  return getCart().reduce((s, i) => s + (i.unitPrice * i.qty), 0);
}

function formatPrice(n) {
  return n.toFixed(2).replace('.', ',') + ' €';
}

function renderCart() {
  const wrap = document.getElementById('cart-root');
  if (!wrap) return;
  const cart = getCart();
  if (cart.length === 0) {
    wrap.innerHTML = `
      <div class="cart-empty">
        <div class="big">🛒</div>
        <h2>Votre panier est vide</h2>
        <p>Découvrez l'organisateur qui transforme vos tiroirs.</p>
        <a href="index.html" class="btn btn-primary btn-lg">Voir le produit</a>
      </div>`;
    return;
  }
  const subtotal = cartSubtotal();
  const shipping = subtotal >= SHIPPING_THRESHOLD ? 0 : SHIPPING_FEE;
  const total = subtotal + shipping;
  const missing = Math.max(0, SHIPPING_THRESHOLD - subtotal);

  let itemsHtml = '';
  cart.forEach((item, i) => {
    itemsHtml += `
      <div class="cart-item">
        <img src="${item.image}" alt="${item.name}">
        <div class="cart-item-info">
          <h4>${item.name}</h4>
          <div class="ci-price">${item.unitLabel} · ${formatPrice(item.unitPrice)} / set</div>
        </div>
        <div class="cart-item-qty">
          <button onclick="changeQty(${i}, -1)">−</button>
          <span>${item.qty}</span>
          <button onclick="changeQty(${i}, 1)">+</button>
        </div>
        <button class="cart-item-remove" onclick="removeFromCart(${i})">Retirer</button>
      </div>`;
  });

  const shipText = shipping === 0
    ? '<div class="free-ship">✓ Livraison offerte</div>'
    : `<div class="free-ship">Plus que ${formatPrice(missing)} pour la livraison offerte</div>`;

  wrap.innerHTML = `
    <div class="cart-grid">
      <div class="cart-items">${itemsHtml}</div>
      <div class="cart-summary">
        <h3>Récapitulatif</h3>
        <div class="cart-summary-row"><span>Sous-total</span><span>${formatPrice(subtotal)}</span></div>
        <div class="cart-summary-row"><span>Livraison</span><span>${shipping === 0 ? 'Offerte' : formatPrice(shipping)}</span></div>
        <div class="cart-summary-row total"><span>Total</span><span>${formatPrice(total)}</span></div>
        ${shipText}
        <button class="btn btn-primary btn-lg btn-block" onclick="checkout()">Payer maintenant</button>
        <p style="font-size:12px;color:var(--text3);margin-top:14px;text-align:center;">Paiement sécurisé · Stripe</p>
      </div>
    </div>`;
}

function checkout() {
  const total = cartSubtotal() + (cartSubtotal() >= SHIPPING_THRESHOLD ? 0 : SHIPPING_FEE);
  const cart = getCart();
  if (cart.length === 0) return;
  // STRIPE_PAYMENT_LINK à remplacer par le vrai lien Stripe Payment Link
  const stripeLink = (typeof STRIPE_PAYMENT_LINK !== 'undefined') ? STRIPE_PAYMENT_LINK : '';
  if (!stripeLink || stripeLink === '#') {
    showToast('Lien de paiement à configurer (Stripe)');
    return;
  }
  window.location.href = stripeLink;
}

/* ---------- Toast ---------- */
let toastTimer;
function showToast(msg) {
  let t = document.querySelector('.toast');
  if (!t) {
    t = document.createElement('div');
    t.className = 'toast';
    document.body.appendChild(t);
  }
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('show'), 2200);
}

/* ---------- Nav mobile ---------- */
function initNav() {
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => links.classList.toggle('open'));
    links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => links.classList.remove('open')));
  }
}

/* ---------- Animations au scroll ---------- */
function initAnimations() {
  const els = document.querySelectorAll('.fade-in');
  if (!('IntersectionObserver' in window)) {
    els.forEach(el => el.classList.add('visible'));
    return;
  }
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } });
  }, { threshold: 0.12 });
  els.forEach(el => io.observe(el));
}

/* ---------- FAQ ---------- */
function initFaq() {
  document.querySelectorAll('.faq-item').forEach(item => {
    const q = item.querySelector('.faq-q');
    if (q) q.addEventListener('click', () => item.classList.toggle('open'));
  });
}

/* ---------- Product page : bundle select + gallery ---------- */
function initProductPage() {
  document.querySelectorAll('.bundle-option').forEach(opt => {
    opt.addEventListener('click', () => {
      document.querySelectorAll('.bundle-option').forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
      opt.querySelector('input').checked = true;
    });
  });

  const mainImg = document.getElementById('main-product-img');
  document.querySelectorAll('.product-thumbs img').forEach(th => {
    th.addEventListener('click', () => {
      if (mainImg) mainImg.src = th.src;
      document.querySelectorAll('.product-thumbs img').forEach(x => x.classList.remove('active'));
      th.classList.add('active');
    });
  });
}

function selectedBundle() {
  const sel = document.querySelector('.bundle-option input:checked');
  return sel ? sel.value : '1x';
}
function addSelectedToCart() {
  addToCart(selectedBundle());
}

/* ---------- Init ---------- */
document.addEventListener('DOMContentLoaded', () => {
  initNav();
  initAnimations();
  initFaq();
  initProductPage();
  updateCartCount();
  renderCart();
});
