/* Jiya Digital — shop logic (vanilla JS, no dependencies) */

// ---------- State ----------
let state = {
  category: "All",
  search: "",
  sort: "featured",
  favOnly: false,
  cart: loadJSON("jiya_cart", {}),      // { productId: qty }
  favs: loadJSON("jiya_favs", []),      // [productId]
};

function loadJSON(key, fallback) {
  try {
    const v = JSON.parse(localStorage.getItem(key));
    return v ?? fallback;
  } catch {
    return fallback;
  }
}
function save() {
  localStorage.setItem("jiya_cart", JSON.stringify(state.cart));
  localStorage.setItem("jiya_favs", JSON.stringify(state.favs));
}

// ---------- Helpers ----------
const $ = (sel) => document.querySelector(sel);
const fmt = (n) => "$" + n.toFixed(2);
const byId = (id) => PRODUCTS.find((p) => p.id === id);

function thumbHTML(p, large = false) {
  return `
    <div class="thumb ${large ? "thumb-lg" : ""}" style="background:linear-gradient(135deg, ${p.art.from}, ${p.art.to})">
      <span class="thumb-emoji">${p.art.emoji}</span>
      <span class="thumb-shine"></span>
    </div>`;
}

function starsHTML(rating) {
  const full = Math.round(rating);
  return `<span class="stars">${"★".repeat(full)}${"☆".repeat(5 - full)}</span>`;
}

// ---------- Rendering: categories ----------
function renderChips() {
  $("#categoryChips").innerHTML = CATEGORIES.map((c) => {
    const count = c === "All" ? PRODUCTS.length : PRODUCTS.filter((p) => p.category === c).length;
    return `<button class="chip ${state.category === c ? "active" : ""}" data-cat="${c}">${c} <small>${count}</small></button>`;
  }).join("");
}

// ---------- Rendering: product grid ----------
function filteredProducts() {
  let list = PRODUCTS.slice();
  if (state.favOnly) list = list.filter((p) => state.favs.includes(p.id));
  if (state.category !== "All") list = list.filter((p) => p.category === state.category);
  if (state.search) {
    const q = state.search.toLowerCase();
    list = list.filter((p) => (p.name + " " + p.category + " " + p.desc).toLowerCase().includes(q));
  }
  switch (state.sort) {
    case "price-asc": list.sort((a, b) => a.price - b.price); break;
    case "price-desc": list.sort((a, b) => b.price - a.price); break;
    case "rating": list.sort((a, b) => b.rating - a.rating); break;
    default: list.sort((a, b) => (b.bestseller ? 1 : 0) - (a.bestseller ? 1 : 0));
  }
  return list;
}

function renderGrid() {
  const list = filteredProducts();
  $("#emptyMsg").hidden = list.length > 0;
  $("#productGrid").innerHTML = list.map((p) => {
    const off = p.oldPrice ? Math.round((1 - p.price / p.oldPrice) * 100) : 0;
    const faved = state.favs.includes(p.id);
    return `
    <article class="card" data-open="${p.id}">
      ${thumbHTML(p)}
      ${p.bestseller ? `<span class="tag tag-best">Bestseller</span>` : ""}
      ${off ? `<span class="tag tag-sale">-${off}%</span>` : ""}
      <button class="fav ${faved ? "faved" : ""}" data-fav="${p.id}" title="Favorite">${faved ? "♥" : "♡"}</button>
      <div class="card-body">
        <p class="card-cat">${p.category}</p>
        <h3 class="card-name">${p.name}</h3>
        <p class="card-rating">${starsHTML(p.rating)} <span>${p.rating} (${p.reviews})</span></p>
        <div class="card-foot">
          <p class="price">${fmt(p.price)} ${p.oldPrice ? `<s>${fmt(p.oldPrice)}</s>` : ""}</p>
          <button class="btn btn-small" data-add="${p.id}">Add to bag</button>
        </div>
      </div>
    </article>`;
  }).join("");
}

// ---------- Product modal ----------
function openProduct(id) {
  const p = byId(id);
  if (!p) return;
  $("#productModalBody").innerHTML = `
    <div class="pm-grid">
      ${thumbHTML(p, true)}
      <div class="pm-info">
        <p class="card-cat">${p.category} · Digital download</p>
        <h2>${p.name}</h2>
        <p class="card-rating">${starsHTML(p.rating)} <span>${p.rating} · ${p.reviews} reviews</span></p>
        <p class="pm-price">${fmt(p.price)} ${p.oldPrice ? `<s>${fmt(p.oldPrice)}</s>` : ""}</p>
        <p class="pm-desc">${p.desc}</p>
        <h4>What's included</h4>
        <ul class="pm-includes">${p.includes.map((i) => `<li>✨ ${i}</li>`).join("")}</ul>
        <button class="btn btn-primary btn-wide" data-add="${p.id}">Add to bag — ${fmt(p.price)}</button>
        <p class="pm-note">📥 Instant download · No physical item will be shipped</p>
      </div>
    </div>`;
  showOverlay("#productOverlay");
}

// ---------- Cart ----------
function cartEntries() {
  return Object.entries(state.cart).map(([id, qty]) => ({ p: byId(id), qty })).filter((e) => e.p);
}
function cartTotal() {
  return cartEntries().reduce((s, e) => s + e.p.price * e.qty, 0);
}
function cartCount() {
  return cartEntries().reduce((s, e) => s + e.qty, 0);
}

function addToCart(id) {
  state.cart[id] = (state.cart[id] || 0) + 1;
  save();
  renderCartBadge();
  toast(`Added to your bag 🛍️`);
}

function setQty(id, qty) {
  if (qty <= 0) delete state.cart[id];
  else state.cart[id] = qty;
  save();
  renderCartBadge();
  renderCart();
}

function renderCartBadge() {
  const n = cartCount();
  $("#cartCount").hidden = n === 0;
  $("#cartCount").textContent = n;
  const f = state.favs.length;
  $("#favCount").hidden = f === 0;
  $("#favCount").textContent = f;
}

function renderCart() {
  const entries = cartEntries();
  if (entries.length === 0) {
    $("#cartItems").innerHTML = `<p class="cart-empty">Your bag is empty 🌙<br/><small>Add something dreamy from the shop!</small></p>`;
    $("#cartFoot").innerHTML = "";
    return;
  }
  $("#cartItems").innerHTML = entries.map(({ p, qty }) => `
    <div class="cart-row">
      ${thumbHTML(p)}
      <div class="cart-info">
        <p class="cart-name">${p.name}</p>
        <p class="cart-price">${fmt(p.price)}</p>
        <div class="qty">
          <button data-qty="${p.id}" data-d="-1">−</button>
          <span>${qty}</span>
          <button data-qty="${p.id}" data-d="1">+</button>
          <button class="remove" data-qty="${p.id}" data-d="-999">Remove</button>
        </div>
      </div>
      <p class="cart-line">${fmt(p.price * qty)}</p>
    </div>`).join("");
  $("#cartFoot").innerHTML = `
    <div class="total-row"><span>Total</span><strong>${fmt(cartTotal())}</strong></div>
    <p class="muted small">Digital products — delivered instantly by email 💌</p>
    <button class="btn btn-primary btn-wide" id="checkoutBtn">Checkout →</button>`;
}

// ---------- Checkout ----------
function openCheckout() {
  hideOverlays();
  const entries = cartEntries();
  if (entries.length === 0) return;
  $("#checkoutBody").innerHTML = `
    <h2>Checkout 💳</h2>
    <div class="co-summary">
      ${entries.map(({ p, qty }) => `<div class="co-line"><span>${p.name} × ${qty}</span><span>${fmt(p.price * qty)}</span></div>`).join("")}
      <div class="co-line co-total"><span>Total</span><span>${fmt(cartTotal())}</span></div>
    </div>
    <form id="checkoutForm" class="co-form">
      <label>Full name<input required name="name" placeholder="Jiya Irfan" /></label>
      <label>Email (downloads sent here)<input required type="email" name="email" placeholder="you@example.com" /></label>
      <label>Card number (demo — don't use a real card)<input required name="card" inputmode="numeric" placeholder="4242 4242 4242 4242" /></label>
      <div class="co-row">
        <label>Expiry<input required name="exp" placeholder="12/28" /></label>
        <label>CVC<input required name="cvc" inputmode="numeric" placeholder="123" /></label>
      </div>
      <button class="btn btn-primary btn-wide" type="submit">Pay ${fmt(cartTotal())}</button>
      <p class="pm-note">🔒 Demo checkout — no real payment is processed.</p>
    </form>`;
  showOverlay("#checkoutOverlay");
  $("#checkoutForm").addEventListener("submit", (e) => {
    e.preventDefault();
    const email = new FormData(e.target).get("email");
    completeOrder(email);
  });
}

function completeOrder(email) {
  const orderNo = "JD-" + Math.random().toString(36).slice(2, 8).toUpperCase();
  state.cart = {};
  save();
  renderCartBadge();
  $("#checkoutBody").innerHTML = `
    <div class="success">
      <div class="success-icon">🎉</div>
      <h2>Order confirmed!</h2>
      <p>Order <strong>${orderNo}</strong></p>
      <p class="muted">Your download links have been sent to<br/><strong>${email}</strong></p>
      <button class="btn btn-primary" data-close>Continue shopping ✨</button>
    </div>`;
}

// ---------- Favorites ----------
function toggleFav(id) {
  const i = state.favs.indexOf(id);
  if (i >= 0) state.favs.splice(i, 1);
  else state.favs.push(id);
  save();
  renderCartBadge();
  renderGrid();
}

// ---------- Overlays & toast ----------
function showOverlay(sel) {
  hideOverlays();
  $(sel).hidden = false;
  document.body.style.overflow = "hidden";
}
function hideOverlays() {
  document.querySelectorAll(".overlay").forEach((o) => (o.hidden = true));
  document.body.style.overflow = "";
}

let toastTimer;
function toast(msg) {
  const t = $("#toast");
  t.textContent = msg;
  t.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => (t.hidden = true), 2200);
}

// ---------- Events ----------
document.addEventListener("click", (e) => {
  const t = e.target.closest("[data-add],[data-fav],[data-open],[data-cat],[data-qty],[data-close]");
  if (!t) {
    if (e.target.classList.contains("overlay")) hideOverlays();
    return;
  }
  if (t.dataset.add) { e.stopPropagation(); addToCart(t.dataset.add); return; }
  if (t.dataset.fav) { e.stopPropagation(); toggleFav(t.dataset.fav); return; }
  if (t.dataset.qty) { setQty(t.dataset.qty, (state.cart[t.dataset.qty] || 0) + Number(t.dataset.d)); return; }
  if (t.dataset.cat) { state.category = t.dataset.cat; renderChips(); renderGrid(); return; }
  if (t.hasAttribute("data-close")) { hideOverlays(); return; }
  if (t.dataset.open) { openProduct(t.dataset.open); return; }
});

document.addEventListener("click", (e) => {
  if (e.target.id === "checkoutBtn") openCheckout();
});

$("#cartBtn").addEventListener("click", () => { renderCart(); showOverlay("#cartOverlay"); });
$("#favBtn").addEventListener("click", () => {
  if (!state.favOnly && state.favs.length === 0) {
    toast("No favorites yet — tap ♡ on a product!");
    return;
  }
  state.favOnly = !state.favOnly;
  state.category = "All";
  state.search = "";
  $("#searchInput").value = "";
  $("#favBtn").classList.toggle("active", state.favOnly);
  renderChips();
  renderGrid();
  document.getElementById("shop").scrollIntoView({ behavior: "smooth" });
  toast(state.favOnly ? "Showing your favorites ♥" : "Showing all products");
});

$("#searchInput").addEventListener("input", (e) => {
  state.search = e.target.value.trim();
  renderGrid();
});

$("#sortSelect").addEventListener("change", (e) => {
  state.sort = e.target.value;
  renderGrid();
});

$("#logoLink").addEventListener("click", (e) => {
  e.preventDefault();
  window.scrollTo({ top: 0, behavior: "smooth" });
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") hideOverlays();
});

// ---------- Init ----------
renderChips();
renderGrid();
renderCartBadge();
