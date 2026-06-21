import streamlit as st

st.set_page_config(
    page_title = "Mobility Command Center",
    page_icon  = "💼",
    layout     = "wide",
    initial_sidebar_state = "expanded",
)

st.markdown("""
<style>
  .main { background: #F8FAFF !important; }
  .block-container {
    padding: 1.5rem 2.5rem !important;
    max-width: 1400px !important;
  }
  section[data-testid="stSidebar"] {
    background: white !important;
    border-right: 1px solid #E2E8F0 !important;
  }

  /* Hero */
  .hero {
    background: linear-gradient(135deg, #4338CA 0%, #6D28D9 100%);
    border-radius: 20px;
    padding: 36px 44px;
    margin-bottom: 28px;
    box-shadow: 0 12px 40px rgba(79,70,229,0.2);
  }
  .hero-top {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 20px;
  }
  .hero-title {
    color: #FFFFFF !important;
    font-size: 36px;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.03em;
    line-height: 1.15;
  }
  .hero-sub {
    color: rgba(255,255,255,0.8);
    font-size: 16px;
    margin: 8px 0 0;
    font-weight: 400;
  }
  .hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 10px;
    padding: 10px 18px;
    color: rgba(255,255,255,0.9);
    font-size: 13px;
    font-weight: 500;
  }

  /* Cards */
  .home-card {
    background: white;
    border: 1px solid #E8EDF5;
    border-radius: 18px;
    padding: 28px 24px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.04);
  }
  .card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 18px;
    padding-bottom: 14px;
    border-bottom: 1px solid #F1F5F9;
  }
  .card-title {
    font-size: 13px;
    font-weight: 700;
    color: #4F46E5;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 0;
  }
  .nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    border-radius: 10px;
    color: #374151;
    font-size: 15px;
    font-weight: 500;
    margin-bottom: 3px;
  }

  /* Stat items */
  .stat-item {
    padding: 16px 4px;
    border-bottom: 1px solid #F1F5F9;
  }
  .stat-item:last-child { border-bottom: none; }
  .stat-name {
    font-size: 13px;
    font-weight: 600;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 6px;
  }
  .stat-number {
    font-size: 36px;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1;
  }

  /* Status items */
  .status-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 13px 16px;
    border-radius: 12px;
    margin-bottom: 10px;
    font-size: 14px;
    font-weight: 600;
  }
  .s-red    { background:#FEF2F2; color:#DC2626; border:1px solid #FEE2E2; }
  .s-yellow { background:#FFFBEB; color:#B45309; border:1px solid #FEF3C7; }
  .s-green  { background:#F0FDF4; color:#059669; border:1px solid #D1FAE5; }
  .s-blue   { background:#EFF6FF; color:#1D4ED8; border:1px solid #DBEAFE; }

  /* Fix page_link styling */
  [data-testid="stPageLink"] a {
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    padding: 10px 12px !important;
    border-radius: 10px !important;
    color: #374151 !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    text-decoration: none !important;
    background: transparent !important;
    margin-bottom: 3px !important;
    transition: all 0.15s !important;
  }
  [data-testid="stPageLink"] a:hover {
    background: #EEF2FF !important;
    color: #4F46E5 !important;
  }
  [data-testid="stPageLink"] p {
    font-size: 15px !important;
    font-weight: 500 !important;
    margin: 0 !important;
  }

  .footer {
    text-align: center;
    color: #CBD5E1;
    font-size: 13px;
    margin-top: 32px;
    padding-top: 20px;
    border-top: 1px solid #F1F5F9;
  }
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
  <div class="hero-top">
    <div style="font-size:56px;line-height:1;flex-shrink:0;">💼</div>
    <div>
      <h1 class="hero-title">Mobility Operations<br>Command Center</h1>
      <p class="hero-sub">
        One screen &nbsp;·&nbsp; Every assignee &nbsp;·&nbsp;
        Every service &nbsp;·&nbsp; Every cost &nbsp;·&nbsp; Real time
      </p>
    </div>
  </div>
  <div class="hero-badge">
    ⚠️ &nbsp;Demo Version — All data is completely fictional
    and randomly generated
  </div>
</div>
""", unsafe_allow_html=True)

# 3 Cards
c1, c2, c3 = st.columns([1.1, 1, 1], gap="large")

with c1:
    with st.container(border=True):
        st.markdown("""
        <div class="card-header">
          <span style="font-size:18px;">🗺️</span>
          <p class="card-title">Navigate</p>
        </div>
        """, unsafe_allow_html=True)

        st.page_link("pages/1_War_Room.py",
                     label="🎯  War Room Dashboard")
        st.page_link("pages/2_Assignee_Journey.py",
                     label="💼  Assignee Journeys")
        st.markdown("""
        <div class="nav-item">🛂  Service Management</div>
        <div class="nav-item">💰  Cost Intelligence</div>
        <div class="nav-item">🛡️  Compliance Center</div>
        <div class="nav-item">🏭  Vendor Network</div>
        <div class="nav-item">🤖  AI Advisor</div>
        <div class="nav-item">📄  Reports</div>
        """, unsafe_allow_html=True)

with c2:
    with st.container(border=True):
        st.markdown("""
        <div class="card-header">
          <span style="font-size:18px;">📊</span>
          <p class="card-title">Platform Stats</p>
        </div>
        <div class="stat-item">
          <div class="stat-name">Active Assignments</div>
          <div class="stat-number" style="color:#4F46E5;">300</div>
        </div>
        <div class="stat-item">
          <div class="stat-name">Service Tracks</div>
          <div class="stat-number" style="color:#7C3AED;">1,680+</div>
        </div>
        <div class="stat-item">
          <div class="stat-name">Vendors Tracked</div>
          <div class="stat-number" style="color:#0284C7;">24</div>
        </div>
        <div class="stat-item">
          <div class="stat-name">Countries Covered</div>
          <div class="stat-number" style="color:#059669;">15</div>
        </div>
        """, unsafe_allow_html=True)

with c3:
    with st.container(border=True):
        st.markdown("""
        <div class="card-header">
          <span style="font-size:18px;">⚡</span>
          <p class="card-title">Quick Status</p>
        </div>
        <div class="status-item s-red">
          🚨 &nbsp;Critical alerts need attention
        </div>
        <div class="status-item s-yellow">
          ⚠️ &nbsp;Check compliance deadlines
        </div>
        <div class="status-item s-green">
          ✅ &nbsp;AI Advisor is active
        </div>
        <div class="status-item s-green">
          ✅ &nbsp;Database connected
        </div>
        <div class="status-item s-blue">
          📊 &nbsp;Weekly report due Friday
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
  Built with Python + Claude AI 🤖
  &nbsp;·&nbsp; Personal Project
  &nbsp;·&nbsp; All data fictional
</div>
""", unsafe_allow_html=True)