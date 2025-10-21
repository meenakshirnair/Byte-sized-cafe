import streamlit as st
import pandas as pd
import plotly.express as px
from math import ceil
from textwrap import dedent

st.set_page_config(page_title="Byte-Sized Café ☕", page_icon="☕", layout="wide")

# ===== Styles (coffee gradient + readable cards + story mode) =====
st.markdown("""
<style>
:root{
  --text:#f8fafc; --muted:#e5e7eb;
  --border:#5b4636;            /* cocoa border */
  --panel:rgba(24,18,14,0.55); /* glass panels */
  --card:rgba(28,22,18,0.62);
  --accent:#f59e0b; --accent2:#22c55e;
}

/* Warm coffee gradient background */
html, body, [data-testid="stAppViewContainer"]{
  background: linear-gradient(145deg, #3e2723 0%, #2b1b14 45%, #1a120c 100%) !important;
  color: var(--text) !important;
}

.big {font-size:2.4rem; font-weight:800; letter-spacing:.3px}

/* KPI + controls + cards */
.kpi{
  padding:1rem; border:1px solid var(--border); border-radius:18px;
  background: var(--panel); backdrop-filter: blur(6px);
}
.menu-controls{
  padding:.75rem 1rem; border:1px solid var(--border); border-radius:16px;
  background: var(--panel); margin-bottom:1rem; backdrop-filter: blur(4px);
}
.menu-grid{ display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:16px; }
.menu-card{
  position:relative; border:1px solid var(--border); border-radius:18px; overflow:hidden;
  background: var(--card); box-shadow: 0 10px 30px rgba(0,0,0,.35);
  transition: transform .18s ease, box-shadow .18s ease; backdrop-filter: blur(6px);
}
.menu-card:hover{ transform: translateY(-3px); box-shadow:0 16px 40px rgba(0,0,0,.5) }
.menu-top{
  padding:14px 16px; display:flex; align-items:center; gap:10px;
  background: linear-gradient(90deg, rgba(245,158,11,.35), transparent 55%);
  border-bottom:1px solid var(--border);
}
.menu-name{font-weight:800; font-size:1.05rem}
.menu-price{margin-left:auto; font-weight:800; color:#ffe8b3}
.menu-body{padding:14px 16px}
.chips{display:flex; gap:8px; flex-wrap:wrap}
.chip{
  font-size:.8rem; padding:4px 8px; border-radius:999px; border:1px solid #7b5d49;
  background: rgba(35,26,20,0.7); color:var(--muted)
}
.chip.strong{ border-color:#22553b; color:#b7ffd3 }
.chip.light{ border-color:#554722; color:#ffe6a7 }
.ribbon{
  position:absolute; top:12px; right:-36px; transform:rotate(35deg);
  background:linear-gradient(90deg,#f59e0b,#f97316); color:#0b1020;
  font-weight:900; padding:6px 48px; letter-spacing:.5px; box-shadow:0 6px 18px rgba(0,0,0,.35)
}
hr{ border:0; height:1px; background:#6b4e3a; margin:18px 0 }
a {color:#facc15 !important; text-decoration:none;}
a:hover{text-decoration:underline;}

/* Hero banner wrapper (Home page) */
.hero{
  position:relative; overflow:hidden; border-radius:22px;
  border:1px solid var(--border); margin: 8px 0 18px 0;
  box-shadow: 0 16px 44px rgba(0,0,0,.45);
}
.hero img{
  width:100%; height:360px; object-fit:cover; display:block; filter: saturate(105%);
}
.hero .overlay{
  position:absolute; inset:0; background: linear-gradient(0deg, rgba(0,0,0,0.55), rgba(0,0,0,0.25));
}
.hero .caption{
  position:absolute; left:20px; bottom:14px; color:#f5f5f4; font-size:0.9rem; opacity:.9;
}
.hero .headline{
  position:absolute; left:24px; top:18px; font-weight:800; font-size:1.6rem;
  color:#fffdec; text-shadow: 0 2px 10px rgba(0,0,0,.35);
}

/* Story Mode scroll-snap (for the Streamlit-native story if you ever want it) */
.story-wrap { scroll-snap-type: y mandatory; height: 85vh; overflow-y: scroll; }
.story { scroll-snap-align: start; min-height: 85vh; padding: 28px;
         border:1px solid var(--border); border-radius:22px;
         background: var(--panel); backdrop-filter: blur(6px);
         margin-bottom: 16px; display:flex; flex-direction:column; justify-content:center; }
.story h2 { margin: 0 0 10px 0; }
.story .sub { opacity:.85; margin-bottom:14px; }
</style>
""", unsafe_allow_html=True)

# ===== Data =====
menu = pd.DataFrame([
    {"Drink":"Espresso","Price":3.0,"Caffeine_mg":75,"Calories":5},
    {"Drink":"Americano","Price":3.5,"Caffeine_mg":75,"Calories":10},
    {"Drink":"Latte","Price":4.5,"Caffeine_mg":80,"Calories":190},
    {"Drink":"Cappuccino","Price":4.5,"Caffeine_mg":80,"Calories":120},
    {"Drink":"Mocha","Price":5.0,"Caffeine_mg":80,"Calories":260},
    {"Drink":"Cold Brew","Price":4.0,"Caffeine_mg":155,"Calories":15},
])

addins = pd.DataFrame([
    {"Add-in":"Extra shot","Add_Price":1.0,"Caffeine_mg":75,"Calories":0},
    {"Add-in":"Oat milk","Add_Price":0.7,"Caffeine_mg":0,"Calories":90},
    {"Add-in":"Vanilla syrup","Add_Price":0.5,"Caffeine_mg":0,"Calories":80},
    {"Add-in":"Whipped cream","Add_Price":0.6,"Caffeine_mg":0,"Calories":100},
])

# ===== Helper =====
def drink_icon(name: str) -> str:
    n = name.lower()
    if "espresso" in n: return "⚡️"
    if "americano" in n: return "🌊"
    if "latte" in n: return "🥛"
    if "cappuccino" in n: return "☁️"
    if "mocha" in n: return "🍫"
    if "cold brew" in n: return "🧊"
    return "☕"

# ===== Sidebar nav =====
page = st.sidebar.radio(
    "Navigate",
    ["Home","Menu","Build Your Drink","Budget Planner","Sustainability","Story Mode","Contact"]
)

# ==================== Pages ====================

if page == "Home":
    st.markdown("<div class='big'>Byte-Sized Café ☕</div>", unsafe_allow_html=True)

    # Hero banner with the café image (not background, for readability)
    st.markdown("""
    <div class="hero">
      <img src="https://images.unsplash.com/photo-1511920170033-f8396924c348?auto=format&fit=crop&w=1600&q=80" alt="Cafe ambience"/>
      <div class="overlay"></div>
      <div class="headline">A tiny café where coffee meets data.</div>
      <div class="caption">Photo: Unsplash / Thomas Vimare</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("""
Welcome to **Byte-Sized Café**, where we brew creativity with a dash of analytics.  
Explore the menu, build your perfect drink, plan your coffee budget, and peek at sustainability — all in one cozy spot.
""")

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='kpi'>", unsafe_allow_html=True)
        st.metric("Menu Items", len(menu))
        st.metric("Avg Price", f"${menu.Price.mean():.2f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='kpi'>", unsafe_allow_html=True)
        st.metric("Strongest Brew", "Cold Brew")
        st.caption("Highest caffeine on the menu")
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='kpi'>", unsafe_allow_html=True)
        st.metric("Lightest Choice", "Espresso")
        st.caption("Lowest calories")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Price vs Caffeine ☕📊")
    fig = px.scatter(menu, x="Caffeine_mg", y="Price", text="Drink", size=[8]*len(menu))
    fig.update_traces(textposition="top center")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Menu":
    st.subheader("Our Menu")

    # Controls
    with st.container():
        st.markdown("<div class='menu-controls'>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns([1.3, 1.2, 1, 1])
        with c1:
            search = st.text_input("Search drink", "")
        with c2:
            sort_by = st.selectbox(
                "Sort by",
                ["Recommended","Price (low → high)","Price (high → low)","Caffeine (high → low)","Calories (low → high)"]
            )
        with c3:
            max_price = st.slider("Max price ($)", 3.0, 6.0, 6.0, 0.5)
        with c4:
            show_light = st.checkbox("Show lighter options", value=False)
        st.markdown("</div>", unsafe_allow_html=True)

    # Filter
    m = menu.copy()
    if search:
        m = m[m["Drink"].str.contains(search, case=False, regex=False)]
    m = m[m["Price"] <= max_price]
    if show_light:
        m = m[m["Calories"] <= 150]

    # Sort
    if sort_by == "Price (low → high)":
        m = m.sort_values("Price")
    elif sort_by == "Price (high → low)":
        m = m.sort_values("Price", ascending=False)
    elif sort_by == "Caffeine (high → low)":
        m = m.sort_values("Caffeine_mg", ascending=False)
    elif sort_by == "Calories (low → high)":
        m = m.sort_values("Calories")
    else:
        m = m.assign(score=(m["Caffeine_mg"]/m["Price"]).rank(ascending=False)).sort_values("score")

    # Empty state or grid render
    if m.empty:
        st.info("No drinks match your filters. Try widening the price or clearing search.")
    else:
        st.markdown("<div class='menu-grid'>", unsafe_allow_html=True)
        for _, r in m.iterrows():
            strong = r.Caffeine_mg >= 120
            light = r.Calories <= 80

            st.markdown("<div class='menu-card'>", unsafe_allow_html=True)

            # Ribbon
            if strong:
                st.markdown("<div class='ribbon'>STRONG</div>", unsafe_allow_html=True)
            elif light:
                st.markdown("<div class='ribbon' style='background:linear-gradient(90deg,#22c55e,#16a34a)'>LIGHT</div>", unsafe_allow_html=True)

            # Card top
            st.markdown(f"""
            <div class="menu-top">
              <div style="font-size:1.2rem">{drink_icon(r.Drink)}</div>
              <div class="menu-name">{r.Drink}</div>
              <div class="menu-price">${r.Price:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

            # Card body
            st.markdown("<div class='menu-body'>", unsafe_allow_html=True)
            st.markdown("Try this if you like smooth flavor and a balanced kick." if r.Drink!="Cold Brew" else "Bold, smooth, and extra caffeinated.")

            chips = [
                f"<span class='chip {'strong' if strong else ''}'>☕ {r.Caffeine_mg} mg</span>",
                f"<span class='chip {'light' if light else ''}'>🔥 {r.Calories} kcal</span>"
            ]
            st.markdown(f"<div class='chips'>{''.join(chips)}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "Build Your Drink":
    st.subheader("Customize your drink")
    base = st.selectbox("Base drink", menu.Drink)
    chosen = menu.set_index("Drink").loc[base].to_dict()

    st.write("Add-ins:")
    cols = st.columns(2)
    add_flags = {}
    for i, add in addins.iterrows():
        with cols[i % 2]:
            add_flags[add["Add-in"]] = st.checkbox(f"{add['Add-in']} (+${add.Add_Price:.2f}, {add.Calories} kcal)")

    # Totals
    total_price = chosen["Price"]
    total_caf = chosen["Caffeine_mg"]
    total_cal = chosen["Calories"]
    for i, add in addins.iterrows():
        if add_flags[add["Add-in"]]:
            total_price += add["Add_Price"]
            total_caf += add["Caffeine_mg"]
            total_cal += add["Calories"]

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("Your price", f"${total_price:.2f}")
    c2.metric("Caffeine", f"{total_caf} mg")
    c3.metric("Calories", f"{total_cal} kcal")
    st.caption("Tip: Screenshot this card for your order 😄")

elif page == "Budget Planner":
    st.subheader("How much do you spend on coffee?")
    freq = st.slider("Cups per week", 0, 21, 7)
    avg_price = st.slider("Avg price per cup ($)", 1.0, 10.0, float(menu.Price.mean()), 0.1)
    weeks = st.slider("Weeks to plan", 1, 52, 12)

    weekly = freq * avg_price
    total = weekly * weeks
    st.markdown("---")
    c1, c2 = st.columns(2)
    c1.metric("Weekly spend", f"${weekly:.2f}")
    c2.metric(f"{weeks}-week total", f"${total:.2f}")

    st.markdown("### What if… you switch 2 cups/week to Americano?")
    alt_price = float(menu.loc[menu.Drink=="Americano","Price"].iloc[0])
    switch = min(2, freq)
    saved = (avg_price - alt_price) * switch * weeks
    st.success(f"Potential savings: **${saved:.2f}** over {weeks} weeks")

elif page == "Sustainability":
    st.subheader("Small habits, big impact 🌎")
    cups = st.slider("Cups you drink per week", 0, 21, 7)
    reusable_rate = st.slider("Reusable cup adoption", 0, 100, 40) / 100
    weeks = st.slider("Weeks considered", 1, 52, 26)

    total_cups = cups * weeks
    disposables_avoided = ceil(total_cups * reusable_rate)
    trees_saved_est = disposables_avoided * 0.0025

    c1, c2, c3 = st.columns(3)
    c1.metric("Total cups", f"{total_cups}")
    c2.metric("Disposables avoided", f"{disposables_avoided}")
    c3.metric("Trees saved (est.)", f"{trees_saved_est:.2f}")

    df = pd.DataFrame({
        "Metric":["Disposable cups","Avoided with reusable"],
        "Count":[total_cups, disposables_avoided]
    })
    fig = px.bar(df, x="Metric", y="Count", text="Count")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Illustrative only — factors vary by material & local recycling.")

elif page == "Story Mode":
    st.subheader("Story Mode 🎬 — Prezi-style inside Streamlit")

    # Embed a minimal impress.js deck (zoom/pan between steps)
    html = dedent("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/impress.js/0.5.3/impress-demo.css">
    <style>
      #impress { height: 80vh; }
      .step {
        background: rgba(20,20,20,0.55);
        color: #f8fafc; border-radius: 16px; padding: 24px;
        border: 1px solid rgba(255,255,255,.15);
        box-shadow: 0 10px 30px rgba(0,0,0,.35);
      }
      .kpi { font-size: 2rem; font-weight: 800; letter-spacing: .5px; }
      a { color: #facc15; text-decoration: none; }
      a:hover { text-decoration: underline; }
      body { background: transparent; }
    </style>

    <div id="impress">

      <!-- Slide 1: Hero -->
      <div id="intro" class="step" data-x="0" data-y="0" data-scale="1.4">
        <h1>Business Analytics in Action</h1>
        <p>From data to decisions — a tiny, zoomable tour.</p>
        <p style="opacity:.8">Use arrow keys or click to advance.</p>
      </div>

      <!-- Slide 2: KPI cluster -->
      <div class="step" data-x="1200" data-y="0" data-scale="1">
        <div class="kpi">91.9% — Attrition Model Accuracy</div>
        <div class="kpi">100% — SLA via Routing Optimization</div>
        <div class="kpi">25% — Cycle time reduction</div>
        <p style="opacity:.85">Metrics that matter to the business.</p>
      </div>

      <!-- Slide 3: Optimization story -->
      <div class="step" data-x="1200" data-y="900" data-rotate="5" data-scale="0.9">
        <h2>Optimization Story</h2>
        <p>Minimized compute cost while keeping SLA at 100% via linear programming.</p>
        <ul>
          <li>Decision variables: route to model backends</li>
          <li>Constraint: SLA ≥ target</li>
          <li>Objective: Cost ↓</li>
        </ul>
        <p><a href="https://github.com/meenakshirnair" target="_blank">View code on GitHub ↗</a></p>
      </div>

      <!-- Slide 4: Forecasting -->
      <div class="step" data-x="-800" data-y="600" data-rotate="-5" data-scale="1.2">
        <h2>Forecasting Snapshot</h2>
        <p>R² 0.81 rent prediction with explainable features.</p>
        <blockquote style="opacity:.9">“Great coffee is an experience — and so is great data.”</blockquote>
      </div>

      <!-- Slide 5: Wrap -->
      <div class="step" data-x="0" data-y="1400" data-scale="1.3">
        <h2>Thanks!</h2>
        <p>Want the full portfolio? Jump back to the site, or reach me any time.</p>
        <p><a href="mailto:meenakshirnair712@gmail.com">meenakshirnair712@gmail.com</a></p>
      </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/impress.js/0.5.3/impress.min.js"></script>
    <script>impress().init();</script>
    """)

    st.components.v1.html(html, height=700, scrolling=False)

elif page == "Contact":
    st.subheader("Say hello 👋")
    st.write("""
Thanks for visiting **Byte-Sized Café** — a little experiment that blends storytelling, design, and data analytics.  
If you enjoyed the experience or want to connect, here’s how to reach me:

- 📧 **Email:** [meenakshirnair712@gmail.com](mailto:meenakshirnair712@gmail.com)  
- 💼 **LinkedIn:** [Meenakshi Rajeev Nair](https://www.linkedin.com/in/meenakshi-rajeev-nair-43301b248)  
- 💻 **GitHub:** [meenakshirnair](https://github.com/meenakshirnair)

Built with ❤️ — because data should feel as inviting as your favorite café corner.
""")

    with st.form("contact"):
        name = st.text_input("Your name")
        msg = st.text_area("Your message or feedback")
        sent = st.form_submit_button("Send")
        if sent:
            st.success("☕ Thanks for your message! If this were a real café, your reply would come with latte art.")
