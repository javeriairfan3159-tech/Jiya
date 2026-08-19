#!/usr/bin/env python3
"""Generate 8 Google Play phone screenshots (9:16). No Jiya branding."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "html"
ASSETS = "../../../etsy-listing/assets"

LOGO = """
<div class="logo" aria-hidden="true">
  <svg viewBox="0 0 48 48" fill="none">
    <circle cx="24" cy="24" r="7" stroke="white" stroke-width="2"/>
    <path d="M24 6 L26 18 L24 24 L22 18 Z" fill="white"/>
    <path d="M24 42 L22 30 L24 24 L26 30 Z" fill="white" opacity=".85"/>
    <path d="M6 24 L18 22 L24 24 L18 26 Z" fill="white" opacity=".7"/>
    <path d="M42 24 L30 26 L24 24 L30 22 Z" fill="white"/>
  </svg>
</div>
"""

NAV = """
<div class="nav">
  <div class="nav-item {explore}"><div class="nav-ico">⌕</div>Explore</div>
  <div class="nav-item {trips}"><div class="nav-ico">▣</div>My Trips</div>
  <div class="nav-item {profile}"><div class="nav-ico">☺</div>Profile</div>
</div>
<div class="home-bar"></div>
"""


def nav(active="explore"):
    return NAV.format(
        explore="active" if active == "explore" else "",
        trips="active" if active == "trips" else "",
        profile="active" if active == "profile" else "",
    )


def status(time="3:14"):
    return f"""
    <div class="island"></div>
    <div class="status"><span>{time}</span><span>􀙇 􀛨</span></div>
    """


def phone(inner, active="explore"):
    return f"""
    <div class="phone">
      <div class="screen">
        {status()}
        {inner}
        {nav(active)}
      </div>
    </div>
    """


def place_card(img, kind, country, name, city, dollars="$$"):
    return f"""
    <div class="place">
      <div class="meta" style="padding:10px 14px 0">
        <div class="tags"><span class="tag">{kind}</span><span class="country">{country}</span></div>
      </div>
      <img src="{ASSETS}/{img}" alt="{name}">
      <div class="meta">
        <div style="display:flex;justify-content:space-between;align-items:flex-start">
          <div>
            <h3>{name}</h3>
            <div class="city">{city}</div>
          </div>
        </div>
        <div class="place-foot">
          <div class="dollar">{dollars}</div>
          <div class="loc-btn">◈ Check Location</div>
        </div>
      </div>
    </div>
    """


def screen_home():
    inner = f"""
    <div class="app">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <div>
          <div class="title">Welcome</div>
          <div class="muted" style="font-size:13px;margin-top:4px;max-width:280px">Always carry a small first-aid kit with essentials like band-aids and pain relievers.</div>
        </div>
        {LOGO}
      </div>
      <div class="ai">
        <div class="q">?</div>
        <h4>Travel AI Assistant</h4>
        <p>Have a travel question? Ask our AI Assistant and get instant answers for your journey!</p>
        <button class="cta">START CHATTING</button>
      </div>
      <div style="font-weight:800;font-size:20px">Essential Tools</div>
      <div class="tools">
        <div class="tool"><div class="ico" style="color:#16a34a">🔧</div>Money</div>
        <div class="tool"><div class="ico" style="color:#f97316">✎</div>Notes</div>
        <div class="tool"><div class="ico" style="color:#6b5cff">◎</div>Explore</div>
      </div>
      <div style="display:flex;justify-content:space-between;align-items:center">
        <div style="font-weight:800;font-size:20px">Your Journeys</div>
        <div style="background:#6b5cff;color:#fff;border-radius:8px;padding:2px 10px;font-size:14px;font-weight:800">0</div>
      </div>
    </div>
    <div class="fab">＋</div>
    """
    return phone(inner, "trips")


def screen_explore(filter_on, cards):
    chips = []
    for name in ["All", "Beaches", "Mountains", "Attractions", "Restaurants"]:
        on = "on" if name == filter_on else ""
        chips.append(f'<div class="chip {on}">{name}</div>')
    inner = f"""
    <div class="app">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <div class="title">Explore Places</div>
        <div class="loc-btn">◈ Check Location</div>
      </div>
      <div class="filters">{''.join(chips)}</div>
      {''.join(cards)}
    </div>
    """
    return phone(inner, "explore")


def screen_wallet():
    inner = """
    <div class="app">
      <div class="title">Wallet &amp; Expenses</div>
      <div class="wallet-card">
        <div class="ring"></div>
        <div>
          <div class="muted" style="font-size:15px">Total Spent</div>
          <div class="amt">$1,240.50</div>
          <div class="used">65% of $2,000 used</div>
        </div>
      </div>
      <div class="two">
        <div class="action">↗ Split Bill</div>
        <div class="action">☰ Converter</div>
      </div>
      <div style="flex:1"></div>
    </div>
    <div class="fab">＋ Add Expense</div>
    """
    return phone(inner, "trips")


def screen_notes():
    inner = """
    <div class="app">
      <div class="tabs">
        <div class="tab on">Notes</div>
        <div class="tab">Reminders</div>
      </div>
      <div class="empty">
        <div style="font-size:64px;opacity:.35">🗒️</div>
        <div style="font-size:24px;font-weight:800;color:#444">No Notes Found</div>
        <div>Capture your travel ideas<br>and memories here.</div>
      </div>
    </div>
    <div class="fab orange">＋</div>
    """
    return phone(inner, "trips")


def screen_profile():
    inner = """
    <div class="app" style="align-items:center;text-align:center">
      <div class="logo" style="width:110px;height:110px">
        <svg viewBox="0 0 48 48" fill="none" width="60" height="60">
          <circle cx="24" cy="24" r="7" stroke="white" stroke-width="2"/>
          <path d="M24 6 L26 18 L24 24 L22 18 Z" fill="white"/>
          <path d="M24 42 L22 30 L24 24 L26 30 Z" fill="white" opacity=".85"/>
          <path d="M6 24 L18 22 L24 24 L18 26 Z" fill="white" opacity=".7"/>
          <path d="M42 24 L30 26 L24 24 L30 22 Z" fill="white"/>
        </svg>
      </div>
      <div class="title" style="margin-top:10px">Welcome</div>
      <div class="muted">Adventure Enthusiast</div>
      <div class="stats" style="width:100%">
        <div><b>3</b><span>Trips</span></div>
        <div><b>8</b><span>Places</span></div>
        <div><b>2</b><span>Badges</span></div>
      </div>
      <div style="width:100%;text-align:left;font-weight:800;font-size:20px">Account Settings</div>
      <div class="edit" style="width:100%">✎ Edit Profile</div>
      <div class="logout" style="width:100%">Log Out</div>
    </div>
    """
    return phone(inner, "profile")


def wrap(title, kicker, headline, sub, phone_html, caption):
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
    <div class="kicker">{kicker}</div>
    <div class="headline">{headline}</div>
    <div class="subhead">{sub}</div>
    <div class="phone-wrap">{phone_html}</div>
    <div class="caption">{caption}</div>
  </div>
</body>
</html>
"""


def main():
    HTML.mkdir(parents=True, exist_ok=True)
    shots = {
        "01-ai": wrap(
            "AI Assistant",
            "Travel Planner",
            "Ask. Plan. Go.",
            "Built-in Travel AI Assistant",
            screen_home(),
            "Instant answers for packing, seasons, and trip questions",
        ),
        "02-explore": wrap(
            "Explore",
            "Destinations",
            "Explore Places",
            "Beaches, mountains, attractions, restaurants",
            screen_explore("All", [
                place_card("bondi.jpg", "BEACH", "Australia", "Bondi Beach", "Sydney", "$"),
                place_card("cafe.jpg", "CAFE", "France", "Café de Flore", "Paris", "$$"),
            ]),
            "Save spots and check the location before you go",
        ),
        "03-attractions": wrap(
            "Attractions",
            "Discover",
            "Find landmarks",
            "Filter by what you actually want to see",
            screen_explore("Attractions", [
                place_card("colosseum.jpg", "ATTRACTION", "Italy", "Colosseum", "Rome", "$$"),
                place_card("eiffel.jpg", "ATTRACTION", "France", "Eiffel Tower", "Paris", "$$"),
            ]),
            "From Rome to Paris — your next stop is in the app",
        ),
        "04-mountains": wrap(
            "Mountains",
            "Get outside",
            "Mountain trips",
            "Plan views, not just checklists",
            screen_explore("Mountains", [
                place_card("fuji.jpg", "MOUNTAIN", "Japan", "Mount Fuji", "Honshu", "$$"),
                place_card("alps.jpg", "MOUNTAIN", "Switzerland", "Swiss Alps", "Interlaken", "$$"),
            ]),
            "Browse places, then build the journey around them",
        ),
        "05-wallet": wrap(
            "Wallet",
            "Money tools",
            "Stay on budget",
            "See spending against your trip total",
            screen_wallet(),
            "Track $1,240.50 of a $2,000 trip in one glance",
        ),
        "06-split": wrap(
            "Split & convert",
            "Travel with friends",
            "Split the bill",
            "Convert currency on the go",
            screen_wallet(),
            "Add expenses. Split costs. Check rates.",
        ),
        "07-notes": wrap(
            "Notes",
            "Capture ideas",
            "Notes & Reminders",
            "Keep memories and lists in one place",
            screen_notes(),
            "Nothing gets lost mid-flight or at 2 a.m.",
        ),
        "08-profile": wrap(
            "Profile",
            "Your journey",
            "Trips, places, badges",
            "A profile made for people who actually go",
            screen_profile(),
            "Track trips, places, and badges as you travel",
        ),
    }
    for name, html in shots.items():
        path = HTML / f"{name}.html"
        path.write_text(html, encoding="utf-8")
        print("wrote", path)


if __name__ == "__main__":
    main()
