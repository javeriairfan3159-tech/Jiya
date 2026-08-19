#!/usr/bin/env python3
"""Generate 8 Google Play Android XR screenshots (16:9 spatial). No Jiya branding."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "html"
ASSETS = "../../../etsy-listing/assets"

LOGO = """
<div class="logo">
  <svg viewBox="0 0 48 48" fill="none" width="20" height="20">
    <circle cx="24" cy="24" r="7" stroke="white" stroke-width="2"/>
    <path d="M24 6 L26 18 L24 24 L22 18 Z" fill="white"/>
    <path d="M24 42 L22 30 L24 24 L26 30 Z" fill="white" opacity=".85"/>
    <path d="M6 24 L18 22 L24 24 L18 26 Z" fill="white" opacity=".7"/>
    <path d="M42 24 L30 26 L24 24 L30 22 Z" fill="white"/>
  </svg>
</div>
"""


def topbar(active="explore"):
    items = [("explore", "Explore"), ("trips", "My Trips"), ("profile", "Profile")]
    nav = "".join(f'<span class="{"on" if k==active else ""}">{lab}</span>' for k, lab in items)
    return f"""
    <div class="topbar">
      <div class="nav">{nav}</div>
      <div style="display:flex;align-items:center;gap:14px"><span>3:14</span>{LOGO}</div>
    </div>
    """


def device(inner, active="explore"):
    return f"""
    <div class="glass">
      <div class="screen">{topbar(active)}{inner}</div>
    </div>
    """


def place_card(img, kind, country, name, city, dollars="$$"):
    return f"""
    <div class="place">
      <img src="{ASSETS}/{img}" alt="{name}">
      <div class="meta">
        <span class="tag">{kind}</span><span class="country">{country}</span>
        <h3>{name}</h3>
        <div class="city">{city}</div>
        <div class="place-foot">
          <div class="dollar">{dollars}</div>
          <div class="loc-btn">◈ Check Location</div>
        </div>
      </div>
    </div>
    """


def screen_home():
    inner = """
    <div class="app">
      <div class="split">
        <div>
          <div class="title" style="margin-bottom:8px">Welcome</div>
          <div class="muted" style="margin-bottom:12px">Always carry a small first-aid kit with essentials like band-aids and pain relievers.</div>
          <div class="ai">
            <div class="q">?</div>
            <h4>Travel AI Assistant</h4>
            <p>Have a travel question? Ask our AI Assistant and get instant answers for your journey!</p>
            <button class="cta">START CHATTING</button>
          </div>
        </div>
        <div>
          <div style="font-weight:800;font-size:18px;margin-bottom:10px">Essential Tools</div>
          <div class="tools">
            <div class="tool">🔧<span>Money</span></div>
            <div class="tool">✎<span>Notes</span></div>
            <div class="tool">◎<span>Explore</span></div>
          </div>
          <div style="display:flex;justify-content:space-between;align-items:center;margin:16px 0 10px">
            <div style="font-weight:800;font-size:18px">Your Journeys</div>
            <div style="background:#6b5cff;color:#fff;border-radius:8px;padding:2px 10px;font-weight:800">1</div>
          </div>
          <div class="wallet-card" style="padding:14px 16px"><div><div style="font-weight:800">Rome weekend</div><div class="muted">3 days · Italy</div></div></div>
        </div>
      </div>
    </div>
    """
    return device(inner, "trips")


def screen_explore(filter_on, cards, cols="three"):
    chips = "".join(f'<div class="chip {"on" if n==filter_on else ""}">{n}</div>' for n in ["All","Beaches","Mountains","Attractions","Restaurants"])
    grid = "cards two" if cols == "two" else "cards"
    inner = f"""
    <div class="app">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <div class="title">Explore Places</div>
        <div class="loc-btn">◈ Check Location</div>
      </div>
      <div class="filters">{chips}</div>
      <div class="{grid}">{''.join(cards)}</div>
    </div>
    """
    return device(inner, "explore")


def screen_wallet():
    inner = """
    <div class="app">
      <div class="title">Wallet &amp; Expenses</div>
      <div class="split">
        <div style="display:flex;flex-direction:column;gap:10px">
          <div class="wallet-card">
            <div class="ring"></div>
            <div><div class="muted">Total Spent</div><div class="amt">$1,240.50</div><div class="used">65% of $2,000 used</div></div>
          </div>
          <div class="expense"><span>Trains · Rome</span><span>$86.00</span></div>
          <div class="expense"><span>Dinner · Trastevere</span><span>$64.40</span></div>
          <div class="expense"><span>Museum tickets</span><span>$42.00</span></div>
        </div>
        <div class="two">
          <div class="action">↗ Split Bill</div>
          <div class="action">☰ Converter</div>
          <div class="action" style="background:#4a3aff;color:#fff">＋ Add Expense</div>
        </div>
      </div>
    </div>
    """
    return device(inner, "trips")


def screen_split():
    inner = """
    <div class="app">
      <div class="title">Split Bill &amp; Converter</div>
      <div class="split">
        <div class="wallet-card" style="flex-direction:column;align-items:stretch;gap:12px">
          <div style="font-weight:800;font-size:20px">Dinner in Rome · $96.00</div>
          <div class="muted">Split equally · 3 people</div>
          <div class="row-person"><span>You</span><b>$32.00</b></div>
          <div class="row-person"><span>Sam</span><b>$32.00</b></div>
          <div class="row-person"><span>Alex</span><b>$32.00</b></div>
          <div class="action" style="background:#4a3aff;color:#fff;padding:12px">Share split</div>
        </div>
        <div class="wallet-card" style="flex-direction:column;align-items:stretch;gap:12px">
          <div style="font-weight:800;font-size:20px">Currency converter</div>
          <div class="conv-box"><span class="muted">USD</span><b>$50.00</b></div>
          <div class="muted" style="text-align:center">→ 0.92 EUR</div>
          <div class="conv-box"><span class="muted">EUR</span><b>€46.00</b></div>
          <div class="action">Check live rate</div>
        </div>
      </div>
    </div>
    """
    return device(inner, "trips")


def screen_notes():
    inner = """
    <div class="app">
      <div class="tabs"><div class="tab on">Notes</div><div class="tab">Reminders</div></div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;flex:1;align-content:start">
        <div class="note-card"><h4>Packing list</h4><p>Passport, adapters, first-aid kit, comfortable walking shoes.</p></div>
        <div class="note-card"><h4>Rome day 2</h4><p>Colosseum morning, Trastevere dinner, sunset at Gianicolo.</p></div>
        <div class="note-card"><h4>Currency</h4><p>Keep some cash for small cafés. Card works almost everywhere.</p></div>
        <div class="note-card"><h4>Flight home</h4><p>Terminal 3. Reach 3 hours early. Seat 14A.</p></div>
      </div>
      <div class="fab orange">＋</div>
    </div>
    """
    return device(inner, "trips")


def screen_profile():
    inner = """
    <div class="app" style="align-items:center;text-align:center;justify-content:center">
      <div class="logo" style="width:88px;height:88px;margin:0 auto">
        <svg viewBox="0 0 48 48" fill="none" width="44" height="44">
          <circle cx="24" cy="24" r="7" stroke="white" stroke-width="2"/>
          <path d="M24 6 L26 18 L24 24 L22 18 Z" fill="white"/>
          <path d="M24 42 L22 30 L24 24 L26 30 Z" fill="white" opacity=".85"/>
          <path d="M6 24 L18 22 L24 24 L18 26 Z" fill="white" opacity=".7"/>
          <path d="M42 24 L30 26 L24 24 L30 22 Z" fill="white"/>
        </svg>
      </div>
      <div class="title" style="margin-top:10px">Welcome</div>
      <div class="muted">Adventure Enthusiast</div>
      <div class="stats" style="width:58%;margin:16px auto">
        <div><b>3</b><span>Trips</span></div>
        <div><b>8</b><span>Places</span></div>
        <div><b>2</b><span>Badges</span></div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;width:48%;margin-bottom:14px">
        <div class="badge">✈ First Trip</div>
        <div class="badge">★ Explorer</div>
      </div>
      <div class="edit">✎ Edit Profile</div>
      <div class="logout">Log Out</div>
    </div>
    """
    return device(inner, "profile")


def wrap(title, kicker, headline, sub, caption, inner):
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css">
</head>
<body>
  <div class="frame">
    <div class="copy">
      <div class="kicker">{kicker}</div>
      <div class="headline">{headline}</div>
      <div class="subhead">{sub}</div>
      <div class="caption">{caption}</div>
    </div>
    <div class="xr-wrap">{inner}</div>
  </div>
</body>
</html>
"""


def main():
    HTML.mkdir(parents=True, exist_ok=True)
    shots = {
        "01-ai": wrap("AI", "Spatial travel", "Ask. Plan. Go.", "Travel AI Assistant in Android XR.", "Instant answers for packing, seasons, and trip questions", screen_home()),
        "02-explore": wrap("Explore", "Destinations", "Explore Places", "Beaches, mountains, attractions, restaurants.", "Save spots and check the location before you go", screen_explore("All", [
            place_card("bondi.jpg", "BEACH", "Australia", "Bondi Beach", "Sydney", "$"),
            place_card("cafe.jpg", "CAFE", "France", "Café de Flore", "Paris", "$$"),
            place_card("eiffel.jpg", "ATTRACTION", "France", "Eiffel Tower", "Paris", "$$"),
        ])),
        "03-attractions": wrap("Attractions", "Discover", "Find landmarks", "Filter by what you actually want to see.", "From Rome to Paris — your next stop is in the app", screen_explore("Attractions", [
            place_card("colosseum.jpg", "ATTRACTION", "Italy", "Colosseum", "Rome", "$$"),
            place_card("eiffel.jpg", "ATTRACTION", "France", "Eiffel Tower", "Paris", "$$"),
        ], cols="two")),
        "04-mountains": wrap("Mountains", "Get outside", "Mountain trips", "Plan views, not just checklists.", "Browse places, then build the journey around them", screen_explore("Mountains", [
            place_card("fuji.jpg", "MOUNTAIN", "Japan", "Mount Fuji", "Honshu", "$$"),
            place_card("alps.jpg", "MOUNTAIN", "Switzerland", "Swiss Alps", "Interlaken", "$$"),
        ], cols="two")),
        "05-wallet": wrap("Wallet", "Money tools", "Stay on budget", "See spending against your trip total.", "Track $1,240.50 of a $2,000 trip in one glance", screen_wallet()),
        "06-split": wrap("Split", "Travel with friends", "Split the bill", "Convert currency while you travel.", "Add expenses. Split costs. Check rates.", screen_split()),
        "07-notes": wrap("Notes", "Capture ideas", "Notes & Reminders", "Keep memories and lists in one place.", "Nothing gets lost mid-flight or at 2 a.m.", screen_notes()),
        "08-profile": wrap("Profile", "Your journey", "Trips, places, badges", "A profile made for people who actually go.", "Track trips, places, and badges as you travel", screen_profile()),
    }
    for name, html in shots.items():
        (HTML / f"{name}.html").write_text(html, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
