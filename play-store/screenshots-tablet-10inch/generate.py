#!/usr/bin/env python3
"""Generate 8 Google Play 10-inch tablet screenshots (16:9). No Jiya branding."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "html"
ASSETS = "../../../etsy-listing/assets"

LOGO = """
<div class="logo">
  <svg viewBox="0 0 48 48" fill="none" width="24" height="24">
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
    nav = []
    for key, label in items:
        cls = "on" if key == active else ""
        nav.append(f'<span class="{cls}">{label}</span>')
    return f"""
    <div class="topbar">
      <div class="nav">{''.join(nav)}</div>
      <div style="display:flex;align-items:center;gap:18px">
        <span>3:14</span>
        {LOGO}
      </div>
    </div>
    """


def tablet(inner, active="explore"):
    return f"""
    <div class="tablet">
      <div class="screen">
        {topbar(active)}
        {inner}
      </div>
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
          <div class="title" style="margin-bottom:10px">Welcome</div>
          <div class="muted" style="margin-bottom:16px;font-size:17px">Always carry a small first-aid kit with essentials like band-aids and pain relievers.</div>
          <div class="ai">
            <div class="q">?</div>
            <h4>Travel AI Assistant</h4>
            <p>Have a travel question? Ask our AI Assistant and get instant answers for your journey!</p>
            <button class="cta">START CHATTING</button>
          </div>
        </div>
        <div>
          <div style="font-weight:800;font-size:22px;margin-bottom:12px">Essential Tools</div>
          <div class="tools">
            <div class="tool">🔧<span>Money</span></div>
            <div class="tool">✎<span>Notes</span></div>
            <div class="tool">◎<span>Explore</span></div>
          </div>
          <div style="display:flex;justify-content:space-between;align-items:center;margin:20px 0 12px">
            <div style="font-weight:800;font-size:22px">Your Journeys</div>
            <div style="background:#6b5cff;color:#fff;border-radius:8px;padding:3px 12px;font-weight:800">1</div>
          </div>
          <div class="wallet-card" style="padding:18px 20px">
            <div>
              <div style="font-weight:800;font-size:20px">Rome weekend</div>
              <div class="muted">3 days · Italy</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    """
    return tablet(inner, "trips")


def screen_explore(filter_on, cards, cols="three"):
    chips = []
    for name in ["All", "Beaches", "Mountains", "Attractions", "Restaurants"]:
        on = "on" if name == filter_on else ""
        chips.append(f'<div class="chip {on}">{name}</div>')
    grid = "cards two" if cols == "two" else "cards"
    inner = f"""
    <div class="app">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <div class="title">Explore Places</div>
        <div class="loc-btn">◈ Check Location</div>
      </div>
      <div class="filters">{''.join(chips)}</div>
      <div class="{grid}">{''.join(cards)}</div>
    </div>
    """
    return tablet(inner, "explore")


def screen_wallet():
    inner = """
    <div class="app">
      <div class="title">Wallet &amp; Expenses</div>
      <div class="split">
        <div style="display:flex;flex-direction:column;gap:14px">
          <div class="wallet-card">
            <div class="ring"></div>
            <div>
              <div class="muted">Total Spent</div>
              <div class="amt">$1,240.50</div>
              <div class="used">65% of $2,000 used</div>
            </div>
          </div>
          <div class="expense"><span>Trains · Rome</span><span class="amt-sm">$86.00</span></div>
          <div class="expense"><span>Dinner · Trastevere</span><span class="amt-sm">$64.40</span></div>
          <div class="expense"><span>Museum tickets</span><span class="amt-sm">$42.00</span></div>
        </div>
        <div>
          <div class="two" style="grid-template-columns:1fr;height:100%">
            <div class="action">↗ Split Bill</div>
            <div class="action">☰ Converter</div>
            <div class="action" style="background:#4a3aff;color:#fff">＋ Add Expense</div>
          </div>
        </div>
      </div>
    </div>
    """
    return tablet(inner, "trips")


def screen_split():
    inner = """
    <div class="app">
      <div class="title">Split Bill &amp; Converter</div>
      <div class="split">
        <div class="wallet-card" style="flex-direction:column;align-items:stretch;gap:16px">
          <div style="font-weight:800;font-size:24px">Dinner in Rome · $96.00</div>
          <div class="muted">Split equally · 3 people</div>
          <div class="row-person"><span>You</span><b>$32.00</b></div>
          <div class="row-person"><span>Sam</span><b>$32.00</b></div>
          <div class="row-person"><span>Alex</span><b>$32.00</b></div>
          <div class="action" style="background:#4a3aff;color:#fff;padding:14px">Share split</div>
        </div>
        <div class="wallet-card" style="flex-direction:column;align-items:stretch;gap:16px">
          <div style="font-weight:800;font-size:24px">Currency converter</div>
          <div class="conv-box"><span class="muted">USD</span><b>$50.00</b></div>
          <div class="muted" style="text-align:center">→ 0.92 EUR</div>
          <div class="conv-box"><span class="muted">EUR</span><b>€46.00</b></div>
          <div class="action">Check live rate</div>
        </div>
      </div>
    </div>
    """
    return tablet(inner, "trips")


def screen_notes():
    inner = """
    <div class="app">
      <div class="tabs">
        <div class="tab on">Notes</div>
        <div class="tab">Reminders</div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;flex:1;align-content:start">
        <div class="note-card">
          <h4>Packing list</h4>
          <p>Passport, adapters, first-aid kit, comfortable walking shoes.</p>
        </div>
        <div class="note-card">
          <h4>Rome day 2</h4>
          <p>Colosseum morning, Trastevere dinner, sunset at Gianicolo.</p>
        </div>
        <div class="note-card">
          <h4>Currency</h4>
          <p>Keep some cash for small cafés. Card works almost everywhere.</p>
        </div>
        <div class="note-card">
          <h4>Flight home</h4>
          <p>Terminal 3. Reach 3 hours early. Seat 14A.</p>
        </div>
      </div>
      <div class="fab orange">＋</div>
    </div>
    """
    return tablet(inner, "trips")


def screen_profile():
    inner = """
    <div class="app" style="align-items:center;text-align:center;justify-content:center">
      <div class="logo" style="width:120px;height:120px;margin:0 auto">
        <svg viewBox="0 0 48 48" fill="none" width="56" height="56">
          <circle cx="24" cy="24" r="7" stroke="white" stroke-width="2"/>
          <path d="M24 6 L26 18 L24 24 L22 18 Z" fill="white"/>
          <path d="M24 42 L22 30 L24 24 L26 30 Z" fill="white" opacity=".85"/>
          <path d="M6 24 L18 22 L24 24 L18 26 Z" fill="white" opacity=".7"/>
          <path d="M42 24 L30 26 L24 24 L30 22 Z" fill="white"/>
        </svg>
      </div>
      <div class="title" style="margin-top:12px">Welcome</div>
      <div class="muted" style="font-size:18px">Adventure Enthusiast</div>
      <div class="stats" style="width:62%;margin:22px auto">
        <div><b>3</b><span>Trips</span></div>
        <div><b>8</b><span>Places</span></div>
        <div><b>2</b><span>Badges</span></div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;width:55%;margin-bottom:18px">
        <div class="badge">✈ First Trip</div>
        <div class="badge">★ Explorer</div>
      </div>
      <div class="edit">✎ Edit Profile</div>
      <div class="logout">Log Out</div>
    </div>
    """
    return tablet(inner, "profile")


def wrap(title, kicker, headline, sub, caption, tablet_html):
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
    <div class="tablet-wrap">{tablet_html}</div>
  </div>
</body>
</html>
"""


def main():
    HTML.mkdir(parents=True, exist_ok=True)
    shots = {
        "01-ai": wrap(
            "AI", "Travel Planner", "Ask. Plan. Go.",
            "Travel AI Assistant on a 10-inch tablet.",
            "Instant answers for packing, seasons, and trip questions",
            screen_home(),
        ),
        "02-explore": wrap(
            "Explore", "Destinations", "Explore Places",
            "Beaches, mountains, attractions, restaurants.",
            "Save spots and check the location before you go",
            screen_explore("All", [
                place_card("bondi.jpg", "BEACH", "Australia", "Bondi Beach", "Sydney", "$"),
                place_card("cafe.jpg", "CAFE", "France", "Café de Flore", "Paris", "$$"),
                place_card("eiffel.jpg", "ATTRACTION", "France", "Eiffel Tower", "Paris", "$$"),
            ]),
        ),
        "03-attractions": wrap(
            "Attractions", "Discover", "Find landmarks",
            "Filter by what you actually want to see.",
            "From Rome to Paris — your next stop is in the app",
            screen_explore("Attractions", [
                place_card("colosseum.jpg", "ATTRACTION", "Italy", "Colosseum", "Rome", "$$"),
                place_card("eiffel.jpg", "ATTRACTION", "France", "Eiffel Tower", "Paris", "$$"),
            ], cols="two"),
        ),
        "04-mountains": wrap(
            "Mountains", "Get outside", "Mountain trips",
            "Plan views, not just checklists.",
            "Browse places, then build the journey around them",
            screen_explore("Mountains", [
                place_card("fuji.jpg", "MOUNTAIN", "Japan", "Mount Fuji", "Honshu", "$$"),
                place_card("alps.jpg", "MOUNTAIN", "Switzerland", "Swiss Alps", "Interlaken", "$$"),
            ], cols="two"),
        ),
        "05-wallet": wrap(
            "Wallet", "Money tools", "Stay on budget",
            "See spending against your trip total.",
            "Track $1,240.50 of a $2,000 trip in one glance",
            screen_wallet(),
        ),
        "06-split": wrap(
            "Split", "Travel with friends", "Split the bill",
            "Convert currency while you travel.",
            "Add expenses. Split costs. Check rates.",
            screen_split(),
        ),
        "07-notes": wrap(
            "Notes", "Capture ideas", "Notes & Reminders",
            "Keep memories and lists in one place.",
            "Nothing gets lost mid-flight or at 2 a.m.",
            screen_notes(),
        ),
        "08-profile": wrap(
            "Profile", "Your journey", "Trips, places, badges",
            "A profile made for people who actually go.",
            "Track trips, places, and badges as you travel",
            screen_profile(),
        ),
    }
    for name, html in shots.items():
        path = HTML / f"{name}.html"
        path.write_text(html, encoding="utf-8")
        print("wrote", path)


if __name__ == "__main__":
    main()
