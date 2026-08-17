#!/usr/bin/env python3
"""Generate 10 Etsy listing mockup HTML slides for Jiya Travel Planner."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SLIDES = ROOT / "slides"
ASSETS = "../assets"

LOGO = """
<div class="logo" aria-hidden="true">
  <svg viewBox="0 0 48 48" fill="none">
    <circle cx="24" cy="24" r="7" stroke="white" stroke-width="2"/>
    <path d="M24 6 L26 18 L24 24 L22 18 Z" fill="white"/>
    <path d="M24 42 L22 30 L24 24 L26 30 Z" fill="white" opacity=".85"/>
    <path d="M6 24 L18 22 L24 24 L18 26 Z" fill="white" opacity=".7"/>
    <path d="M42 24 L30 26 L24 24 L30 22 Z" fill="white"/>
    <path d="M12 12 L20 20" stroke="white" stroke-width="1.4" opacity=".7"/>
    <path d="M36 36 L28 28" stroke="white" stroke-width="1.4" opacity=".7"/>
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


def island_status(time="3:14"):
    return f"""
    <div class="island"></div>
    <div class="status"><span>{time}</span><span>􀙇 􀛨</span></div>
    """


def screen_home(size=""):
    cls = f"phone {size}".strip()
    return f"""
    <div class="{cls}">
      <div class="screen">
        {island_status()}
        <div class="app">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <div>
              <div class="title">Jiya</div>
              <div class="muted" style="font-size:11px;font-style:italic;max-width:210px;margin-top:4px">Always carry a small first-aid kit with essentials like band-aids and pain relievers.</div>
            </div>
            {LOGO}
          </div>
          <div class="ai">
            <div class="q">?</div>
            <h4>Travel AI Assistant</h4>
            <p>Have a travel question? Ask our AI Assistant and get instant answers for your journey!</p>
            <button class="cta">START CHATTING</button>
          </div>
          <div style="font-weight:800;font-size:16px">Essential Tools</div>
          <div class="tools">
            <div class="tool"><div class="ico" style="color:#16a34a">🔧</div>Money</div>
            <div class="tool"><div class="ico" style="color:#f97316">✎</div>Notes</div>
            <div class="tool"><div class="ico" style="color:#6b5cff">◎</div>Explore</div>
          </div>
          <div style="display:flex;justify-content:space-between;align-items:center">
            <div style="font-weight:800;font-size:16px">Your Journeys</div>
            <div style="background:#6b5cff;color:#fff;border-radius:8px;padding:2px 8px;font-size:12px;font-weight:800">0</div>
          </div>
        </div>
        <div class="fab">＋</div>
        {nav("trips")}
      </div>
    </div>
    """


def place_card(img, kind, country, name, city, dollars="$$"):
    return f"""
    <div class="place">
      <div class="meta" style="padding:8px 12px 0">
        <div class="tags"><span class="tag">{kind}</span><span class="country">{country}</span></div>
      </div>
      <img src="{ASSETS}/{img}" alt="{name}">
      <div class="meta">
        <div style="display:flex;justify-content:space-between;align-items:flex-start">
          <div>
            <h3>{name}</h3>
            <div class="city">{city}</div>
          </div>
          <div style="width:18px;height:18px;border:2px solid #cfc;border-radius:4px"></div>
        </div>
        <div class="place-foot">
          <div class="dollar">{dollars}</div>
          <div class="loc-btn">◈ Check Location</div>
        </div>
      </div>
    </div>
    """


def screen_explore(filter_on="All", cards=None, size=""):
    cards = cards or [
        place_card("bondi.jpg", "BEACH", "Australia", "Bondi Beach", "Sydney", "$"),
        place_card("cafe.jpg", "CAFE", "France", "Café de Flore", "Paris", "$$"),
    ]
    chips = []
    for name in ["All", "Beaches", "Mountains", "Attractions", "Restaurants"]:
        on = "on" if name == filter_on else ""
        chips.append(f'<div class="chip {on}">{name}</div>')
    cls = f"phone {size}".strip()
    return f"""
    <div class="{cls}">
      <div class="screen">
        {island_status()}
        <div class="app">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <div class="title">Explore Places</div>
            <div class="loc-btn">◈ Check Location</div>
          </div>
          <div class="filters">{''.join(chips)}</div>
          {''.join(cards)}
        </div>
        {nav("explore")}
      </div>
    </div>
    """


def screen_wallet(size=""):
    cls = f"phone {size}".strip()
    return f"""
    <div class="{cls}">
      <div class="screen">
        {island_status()}
        <div class="app">
          <div class="title">Wallet & Expenses</div>
          <div class="wallet-card">
            <div class="ring"></div>
            <div>
              <div class="muted" style="font-size:13px">Total Spent</div>
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
        {nav("trips")}
      </div>
    </div>
    """


def screen_profile(size=""):
    cls = f"phone {size}".strip()
    return f"""
    <div class="{cls}">
      <div class="screen">
        {island_status()}
        <div class="app" style="align-items:center;text-align:center">
          <div class="logo" style="width:86px;height:86px">
            <svg viewBox="0 0 48 48" fill="none" width="48" height="48">
              <circle cx="24" cy="24" r="7" stroke="white" stroke-width="2"/>
              <path d="M24 6 L26 18 L24 24 L22 18 Z" fill="white"/>
              <path d="M24 42 L22 30 L24 24 L26 30 Z" fill="white" opacity=".85"/>
              <path d="M6 24 L18 22 L24 24 L18 26 Z" fill="white" opacity=".7"/>
              <path d="M42 24 L30 26 L24 24 L30 22 Z" fill="white"/>
            </svg>
          </div>
          <div class="title" style="margin-top:8px">Jiya</div>
          <div class="muted">Adventure Enthusiast</div>
          <div class="stats" style="width:100%">
            <div><b>3</b><span>Trips</span></div>
            <div><b>8</b><span>Places</span></div>
            <div><b>2</b><span>Badges</span></div>
          </div>
          <div style="width:100%;text-align:left;font-weight:800;font-size:16px">Account Settings</div>
          <div class="edit" style="width:100%">✎ Edit Profile</div>
          <div class="logout" style="width:100%">Log Out</div>
        </div>
        {nav("profile")}
      </div>
    </div>
    """


def screen_notes(size=""):
    cls = f"phone {size}".strip()
    return f"""
    <div class="{cls}">
      <div class="screen">
        {island_status("3:15")}
        <div class="app">
          <div class="tabs">
            <div class="tab on">Notes</div>
            <div class="tab">Reminders</div>
          </div>
          <div class="empty">
            <div style="font-size:54px;opacity:.35">🗒️</div>
            <div style="font-size:20px;font-weight:800;color:#444">No Notes Found</div>
            <div>Capture your travel ideas<br>and memories here.</div>
          </div>
        </div>
        <div class="fab orange">＋</div>
      </div>
    </div>
    """


def wrap(title, body):
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css">
</head>
<body>
{body}
</body>
</html>
"""


def canvas(inner, extra=""):
    return f"""
<div class="canvas">
  <div class="blob a"></div>
  <div class="blob b"></div>
  {inner}
</div>
"""


slides = {}

# 01 HERO
slides["01-hero"] = canvas(f"""
  <div style="position:absolute;left:90px;top:120px;width:860px;z-index:3">
    <div class="kicker">Digital download</div>
    <div class="h1 xl" style="margin:18px 0 22px">Travel<br>Planner<br>App</div>
    <div class="sub" style="max-width:760px">Mobile &amp; web trip planner — explore places, track expenses, and ask AI before you go.</div>
    <div class="pill-row" style="margin-top:36px">
      <div class="pill">Trip itinerary</div>
      <div class="pill">Travel budget</div>
      <div class="pill">AI assistant</div>
    </div>
    <div style="margin-top:40px" class="badge">Instant access • Phone + browser</div>
  </div>
  <div style="position:absolute;right:70px;top:210px;z-index:4;transform:rotate(-9deg)">{screen_explore(size="sm")}</div>
  <div style="position:absolute;right:390px;top:150px;z-index:5">{screen_home()}</div>
  <div style="position:absolute;right:720px;top:280px;z-index:3;transform:rotate(8deg)">{screen_wallet(size="sm")}</div>
  <div class="footer-note"><span>Jiya Travel Planner</span><span>Listing photo 01 / 10</span></div>
""")

# 02 WEB + MOBILE
web_home = f"""
<div style="padding:28px 36px 20px;display:grid;grid-template-columns:1.1fr .9fr;gap:28px">
  <div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:18px">
      <div>
        <div style="font-size:42px;font-weight:800;letter-spacing:-.04em">Jiya</div>
        <div style="color:#8a8494;font-size:16px">Adventure Enthusiast · Plan your next trip</div>
      </div>
      {LOGO}
    </div>
    <div class="ai" style="min-height:210px;padding:28px">
      <div class="q" style="font-size:140px">?</div>
      <h4 style="font-size:28px">Travel AI Assistant</h4>
      <p style="font-size:16px;max-width:90%">Have a travel question? Ask our AI Assistant and get instant answers for your journey!</p>
      <button class="cta" style="max-width:260px;font-size:14px;padding:12px 0;margin-top:18px">START CHATTING</button>
    </div>
  </div>
  <div>
    <div style="font-weight:800;font-size:22px;margin-bottom:12px">Essential Tools</div>
    <div class="tools" style="grid-template-columns:1fr;gap:12px">
      <div class="tool" style="height:70px;flex-direction:row;justify-content:flex-start;padding:0 18px;gap:12px"><span style="font-size:24px">🔧</span> Money · budget, split, convert</div>
      <div class="tool" style="height:70px;flex-direction:row;justify-content:flex-start;padding:0 18px;gap:12px"><span style="font-size:24px">✎</span> Notes · ideas &amp; reminders</div>
      <div class="tool" style="height:70px;flex-direction:row;justify-content:flex-start;padding:0 18px;gap:12px"><span style="font-size:24px">◎</span> Explore · beaches to cities</div>
    </div>
  </div>
</div>
"""
slides["02-web-mobile"] = canvas(f"""
  <div style="position:absolute;left:90px;top:90px;width:1820px">
    <div class="kicker">Works on phone and desktop</div>
    <div class="h1 lg" style="margin:10px 0 8px">Mobile + Web App</div>
    <div class="sub">Plan on your laptop. Open the same trip on your phone.</div>
  </div>
  <div style="position:absolute;left:70px;top:340px;z-index:2">
    <div class="laptop">
      <div class="browser">
        <div class="chrome-bar">
          <div class="dot r"></div><div class="dot y"></div><div class="dot g"></div>
          <div class="url">app.jiyatravelplanner.com/home</div>
        </div>
        {web_home}
      </div>
      <div class="base"></div>
    </div>
    <div class="hinge"></div>
    <div class="deck"></div>
  </div>
  <div style="position:absolute;right:90px;top:430px;z-index:5">{screen_home(size="md")}</div>
  <div class="footer-note"><span>Use in the browser — no App Store wait</span><span>Listing photo 02 / 10</span></div>
""")

# 03 EXPLORE
slides["03-explore"] = canvas(f"""
  <div style="position:absolute;left:90px;top:110px;width:900px">
    <div class="kicker">Destinations</div>
    <div class="h1 lg" style="margin:12px 0 18px">Explore<br>Places</div>
    <div class="sub" style="max-width:720px">Browse beaches, mountains, attractions, and restaurants. Save spots and check the location before you go.</div>
    <div class="pill-row" style="margin-top:32px">
      <div class="pill">Bondi Beach</div>
      <div class="pill">Mount Fuji</div>
      <div class="pill">Colosseum</div>
      <div class="pill">Eiffel Tower</div>
    </div>
  </div>
  <div style="position:absolute;left:980px;top:180px;z-index:4">{screen_explore("All")}</div>
  <div style="position:absolute;left:620px;top:320px;z-index:3;transform:rotate(-7deg)">{screen_explore("Mountains", [
        place_card("fuji.jpg", "MOUNTAIN", "Japan", "Mount Fuji", "Honshu", "$$"),
        place_card("alps.jpg", "MOUNTAIN", "Switzerland", "Swiss Alps", "Interlaken", "$$"),
    ], size="sm")}</div>
  <div class="footer-note"><span>Discover · filter · check location</span><span>Listing photo 03 / 10</span></div>
""")

# 04 BUDGET
slides["04-budget"] = canvas(f"""
  <div style="position:absolute;left:980px;top:160px;width:860px">
    <div class="kicker">Money tools</div>
    <div class="h1 lg" style="margin:12px 0 18px">Wallet &amp;<br>Expenses</div>
    <div class="sub">See how much of your trip budget is gone — then split the bill or convert currency on the spot.</div>
    <div style="margin-top:40px;display:flex;flex-direction:column;gap:18px">
      <div class="fcard" style="padding:22px 26px"><h3 style="font-size:28px;margin:0">Budget ring</h3><p style="font-size:22px">Track $1,240.50 of a $2,000 trip in one glance.</p></div>
      <div class="fcard" style="padding:22px 26px"><h3 style="font-size:28px;margin:0">Split Bill</h3><p style="font-size:22px">Share costs with friends instead of messy notes.</p></div>
      <div class="fcard" style="padding:22px 26px"><h3 style="font-size:28px;margin:0">Converter</h3><p style="font-size:22px">Check rates while you travel.</p></div>
    </div>
  </div>
  <div style="position:absolute;left:180px;top:220px;z-index:4">{screen_wallet()}</div>
  <div class="footer-note"><span>Stay on budget every trip</span><span>Listing photo 04 / 10</span></div>
""")

# 05 AI
slides["05-ai"] = canvas(f"""
  <div style="position:absolute;left:90px;top:130px;width:920px">
    <div class="kicker">Built-in help</div>
    <div class="h1 lg" style="margin:12px 0 18px">Travel AI<br>Assistant</div>
    <div class="sub">Ask a travel question and get an instant answer — from packing tips to “when should I visit Kyoto?”</div>
    <div style="margin-top:36px;background:#fff;border-radius:28px;padding:28px 32px;box-shadow:0 18px 40px rgba(20,16,40,.07);max-width:760px">
      <div style="font-size:22px;color:#6b5cff;font-weight:700;margin-bottom:10px">You</div>
      <div style="font-size:30px;font-weight:700;margin-bottom:22px">Best time to visit Kyoto?</div>
      <div style="font-size:22px;color:#6b5cff;font-weight:700;margin-bottom:10px">Assistant</div>
      <div style="font-size:28px;font-weight:600;color:#333">Spring cherry blossom season — late March to mid April.</div>
    </div>
  </div>
  <div style="position:absolute;right:140px;top:200px">{screen_home()}</div>
  <div class="footer-note"><span>Ask. Plan. Go.</span><span>Listing photo 05 / 10</span></div>
""")

# 06 INCLUDED
slides["06-included"] = canvas(f"""
  <div style="position:absolute;left:90px;top:90px;width:1820px">
    <div class="kicker">What you get</div>
    <div class="h1 lg" style="margin:8px 0 28px">Everything inside</div>
    <div class="feature-grid">
      <div class="fcard"><div class="ico-lg">◎</div><h3>Explore Places</h3><p>Filter beaches, mountains, attractions, and restaurants. Check locations on the map.</p></div>
      <div class="fcard"><div class="ico-lg">▣</div><h3>My Trips</h3><p>Keep journeys in one home screen with essential tools at your fingertips.</p></div>
      <div class="fcard"><div class="ico-lg">$</div><h3>Wallet &amp; Expenses</h3><p>Budget ring, add expense, split bill, and currency converter.</p></div>
      <div class="fcard"><div class="ico-lg">?</div><h3>Travel AI Assistant</h3><p>Instant answers for packing, seasons, and trip questions.</p></div>
      <div class="fcard"><div class="ico-lg">✎</div><h3>Notes &amp; Reminders</h3><p>Capture ideas and memories so nothing gets lost mid-trip.</p></div>
      <div class="fcard"><div class="ico-lg">☺</div><h3>Profile &amp; Badges</h3><p>Track trips, places, and badges — built for adventure enthusiasts.</p></div>
    </div>
  </div>
  <div class="footer-note"><span>One app. Full trip toolkit.</span><span>Listing photo 06 / 10</span></div>
""")

# 07 HOW IT WORKS
slides["07-how"] = canvas("""
  <div style="position:absolute;left:90px;top:140px;width:1820px">
    <div class="kicker">Easy start</div>
    <div class="h1 lg" style="margin:8px 0 18px">How it works</div>
    <div class="sub" style="margin-bottom:64px">Digital product — no shipping. Open it the same day.</div>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:32px">
      <div class="step"><div class="num">1</div><h3 style="font-size:36px;font-weight:800;margin-bottom:10px">Purchase</h3><p style="font-size:26px;color:#6b6570;line-height:1.35">Checkout on Etsy. Your files are ready instantly.</p></div>
      <div class="step"><div class="num">2</div><h3 style="font-size:36px;font-weight:800;margin-bottom:10px">Open access</h3><p style="font-size:26px;color:#6b6570;line-height:1.35">Download the PDF. Tap your private app link.</p></div>
      <div class="step"><div class="num">3</div><h3 style="font-size:36px;font-weight:800;margin-bottom:10px">Plan trips</h3><p style="font-size:26px;color:#6b6570;line-height:1.35">Explore places, log expenses, and ask the AI helper.</p></div>
    </div>
  </div>
  <div class="footer-note"><span>Instant digital download</span><span>Listing photo 07 / 10</span></div>
""")

# 08 PROFILE + NOTES
slides["08-more"] = canvas(f"""
  <div style="position:absolute;left:90px;top:110px;width:1820px">
    <div class="kicker">More inside</div>
    <div class="h1 lg" style="margin:8px 0 12px">Profile, notes &amp; reminders</div>
    <div class="sub">Save memories, edit your traveler profile, and keep trip ideas in one place.</div>
  </div>
  <div style="position:absolute;left:280px;top:380px">{screen_profile()}</div>
  <div style="position:absolute;right:280px;top:380px">{screen_notes()}</div>
  <div class="footer-note"><span>Made for travelers who actually go</span><span>Listing photo 08 / 10</span></div>
""")

# 09 PERFECT FOR
slides["09-perfect"] = canvas("""
  <div style="position:absolute;left:90px;top:130px;width:1820px">
    <div class="kicker">Who it’s for</div>
    <div class="h1 lg" style="margin:8px 0 50px">Perfect for</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:28px">
      <div class="fcard"><h3>Solo travelers</h3><p>Keep destinations, budget, and notes in your pocket.</p></div>
      <div class="fcard"><h3>Couples &amp; friends</h3><p>Split bills and plan stops without a messy group chat.</p></div>
      <div class="fcard"><h3>Weekend getaways</h3><p>Build a short trip fast with Explore + AI tips.</p></div>
      <div class="fcard"><h3>Long vacations</h3><p>Track spending against a $2,000-style budget as you go.</p></div>
    </div>
  </div>
  <div class="footer-note"><span>Vacation planner · holiday organizer · trip tracker</span><span>Listing photo 09 / 10</span></div>
""")

# 10 CTA
slides["10-cta"] = canvas(f"""
  <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:80px">
    <div class="kicker">Jiya Travel Planner</div>
    <div class="h1 xl" style="margin:20px 0 24px">Plan the trip.<br>Enjoy the trip.</div>
    <div class="sub" style="max-width:1100px">Travel planner mobile web app with itinerary tools, destination explore, expense tracker, and AI assistant — instant digital download.</div>
    <div class="pill-row" style="margin-top:40px;justify-content:center">
      <div class="badge">Add to cart</div>
      <div class="badge ghost">Instant download</div>
    </div>
  </div>
  <div style="position:absolute;left:80px;bottom:160px;transform:rotate(-8deg) scale(.78);transform-origin:left bottom">{screen_explore("Attractions", [
        place_card("colosseum.jpg", "ATTRACTION", "Italy", "Colosseum", "Rome", "$$"),
        place_card("eiffel.jpg", "ATTRACTION", "France", "Eiffel Tower", "Paris", "$$"),
    ], size="sm")}</div>
  <div style="position:absolute;right:80px;bottom:160px;transform:rotate(8deg) scale(.78);transform-origin:right bottom">{screen_wallet(size="sm")}</div>
  <div class="footer-note"><span>Not a printable PDF planner — this is the live app</span><span>Listing photo 10 / 10</span></div>
""")


def main():
    SLIDES.mkdir(parents=True, exist_ok=True)
    for name, html in slides.items():
        path = SLIDES / f"{name}.html"
        path.write_text(wrap(name, html), encoding="utf-8")
        print("wrote", path)


if __name__ == "__main__":
    main()
