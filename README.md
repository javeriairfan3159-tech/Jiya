# 🌙 Jiya Digital — Online Shop App

Aesthetic digital products shop — wallpapers, app icon packs, phone themes, digital planners aur printable wall art ke liye. (Etsy-style digital downloads store)

**Features:**
- 🛍️ Product catalog with categories (Wallpapers, App Icons, Phone Themes, Planners, Wall Art, Bundles)
- 🔍 Search + sort (price, rating, featured)
- ♥ Favorites (wishlist)
- 🛒 Shopping cart with quantity controls (saved automatically in browser)
- 💳 Checkout flow with order confirmation (demo — no real payment)
- 📱 Fully responsive — mobile aur desktop dono pe kaam karti hai

---

## App kaise chalayen? (Roman Urdu)

Ye app chalana bohat aasan hai — **kuch install karne ki zaroorat nahi!**

### Tareeqa 1 — Sab se aasan
1. Ye repository apne computer pe download karo (GitHub pe green **"Code"** button → **"Download ZIP"**)
2. ZIP file kholo (extract karo)
3. `index.html` file pe **double-click** karo — app browser mein khul jayegi! ✨

### Tareeqa 2 — GitHub Pages (free online website)
Apni shop ko internet pe live karne ke liye:
1. GitHub pe apni repository kholo
2. **Settings** → **Pages** pe jao
3. "Source" mein **main branch** select karo aur **Save** dabao
4. 1-2 minute baad tumhari shop is link pe live ho jayegi:
   `https://javeriairfan3159-tech.github.io/Jiya/`

---

## How to run (English)

No installation needed — it's a pure HTML/CSS/JavaScript app.

1. Download or clone this repository
2. Open `index.html` in any browser — done!

Or serve it locally:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

---

## Apne products kaise add karen?

Saare products is file mein hain: **`js/products.js`**

Har product aise likha hai:

```js
{
  id: "starry-night-walls",          // unique naam (English, no spaces)
  name: "Starry Night Wallpaper Pack", // product ka naam
  category: "Wallpapers",             // category
  price: 4.99,                        // price (dollars)
  oldPrice: 7.99,                     // purani price (sale dikhane ke liye) — ya null
  rating: 4.9,                        // rating (1-5)
  reviews: 312,                       // reviews ki tadaad
  bestseller: true,                   // bestseller badge dikhana hai?
  art: { from: "#2b2d5e", to: "#7b6cf6", emoji: "🌌" }, // thumbnail colors + emoji
  desc: "Product ki description...",
  includes: ["12 wallpapers", "iOS & Android sizes"],   // kya kya milega
}
```

Naya product add karne ke liye bas ek aur aisa block copy-paste kar ke details badal do. Shop ka naam badalne ke liye `index.html` mein "Jiya Digital" search kar ke apna naam likh do.

---

## File structure

```
├── index.html        → Main page (shop ka structure)
├── css/styles.css    → Design & colors
├── js/products.js    → Products ki list (yahan apne products likho)
└── js/app.js         → Shop ki logic (cart, search, checkout)
```

> **Note:** Checkout demo hai — real payment ke liye baad mein Stripe/PayPal add kiya ja sakta hai. Demo products ki jagah apne products aur images add karna na bhoolen!
