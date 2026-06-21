import streamlit as st
import pandas as pd
import sqlite3
from config import DB_PATH

st.set_page_config(
    page_title = "Assignee Journey",
    page_icon  = "💼",
    layout     = "wide"
)

st.markdown("""
<style>
  .main {
    background: linear-gradient(135deg, #F8FAFF 0%, #EEF2FF 50%, #F0F9FF 100%) !important;
  }
  [data-testid="stSidebar"] {
    background: rgba(255,255,255,0.95) !important;
    border-right: 1px solid rgba(0,0,0,0.06) !important;
  }
  .hero-header {
    background: linear-gradient(135deg, rgba(79,70,229,0.08), rgba(124,58,237,0.06));
    backdrop-filter: blur(30px);
    border: 1px solid rgba(79,70,229,0.15);
    border-radius: 24px;
    padding: 32px 36px;
    margin-bottom: 24px;
    box-shadow: 0 4px 24px rgba(79,70,229,0.08);
  }
  .mini-metric {
    background: rgba(255,255,255,0.9);
    border: 1px solid rgba(255,255,255,0.9);
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    transition: all 0.2s;
  }
  .mini-metric:hover {
    box-shadow: 0 8px 32px rgba(79,70,229,0.12);
    transform: translateY(-2px);
  }
  .metric-value { font-size: 32px; font-weight: 800; }
  .metric-label {
    font-size: 11px; color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.08em; margin-top: 4px;
  }
  .pill {
    display: inline-block; padding: 4px 14px;
    border-radius: 50px; font-size: 11px;
    font-weight: 700; letter-spacing: 0.05em;
    text-transform: uppercase;
  }
  .pill-risk  { background:rgba(239,68,68,0.1);  color:#DC2626; border:1px solid rgba(239,68,68,0.2); }
  .pill-delay { background:rgba(249,115,22,0.1); color:#EA580C; border:1px solid rgba(249,115,22,0.2); }
  .pill-track { background:rgba(16,185,129,0.1); color:#059669; border:1px solid rgba(16,185,129,0.2); }
  .pill-prog  { background:rgba(79,70,229,0.1);  color:#4F46E5; border:1px solid rgba(79,70,229,0.2); }
  .pill-done  { background:rgba(14,165,233,0.1); color:#0284C7; border:1px solid rgba(14,165,233,0.2); }
  .info-chip {
    background: rgba(255,255,255,0.9);
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 10px; padding: 6px 12px;
    font-size: 12px; color: #64748B; margin: 3px;
    display: inline-block;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  }
  .info-chip span { color: #1E293B; font-weight: 600; }
  .service-card {
    background: rgba(255,255,255,0.9);
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 16px; padding: 16px 10px;
    text-align: center; transition: all 0.2s;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  }
  .service-card:hover {
    box-shadow: 0 8px 24px rgba(79,70,229,0.12);
    transform: translateY(-2px);
    border-color: rgba(79,70,229,0.2);
  }
  .progress-wrap {
    background: rgba(0,0,0,0.06);
    border-radius: 10px; height: 6px; overflow: hidden; margin: 8px 0;
  }
  .risk-gauge {
    background: rgba(255,255,255,0.7);
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 14px; padding: 14px 18px;
    margin-top: 16px; display: flex;
    align-items: center; gap: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  }
  .glass-divider {
    border: none;
    border-top: 1px solid rgba(0,0,0,0.06); margin: 16px 0;
  }
  [data-testid="stExpander"] {
    background: rgba(255,255,255,0.8) !important;
    border: 1px solid rgba(0,0,0,0.06) !important;
    border-radius: 16px !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04) !important;
    margin-bottom: 8px !important;
  }
  .stSelectbox > div > div {
    background: rgba(255,255,255,0.9) !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
    border-radius: 12px !important;
    color: #1E293B !important;
  }
  .stTextInput > div > div > input {
    background: rgba(255,255,255,0.9) !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
    border-radius: 12px !important;
    color: #1E293B !important;
  }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=60)
def load_data():
    conn      = sqlite3.connect(DB_PATH)
    assignees = pd.read_sql("SELECT * FROM assignees", conn)
    services  = pd.read_sql("SELECT * FROM services",  conn)
    conn.close()
    return assignees, services

try:
    assignees, services = load_data()
except Exception as e:
    st.error(f"Run db_setup.py first! {e}")
    st.stop()

st.markdown("""
<div class="hero-header">
  <div style="display:flex;align-items:center;gap:16px;">
    <div style="font-size:44px;">💼</div>
    <div>
      <h1 style="color:#1E1B4B;margin:0;font-size:28px;
                 font-weight:800;letter-spacing:-0.02em;">
        Assignee Journey Tracker
      </h1>
      <p style="color:#6366F1;margin:4px 0 0;font-size:14px;font-weight:500;">
        6 service tracks · Real-time visibility · Risk intelligence
      </p>
    </div>
  </div>
</div>
<p style="color:#94A3B8;font-size:12px;margin-bottom:20px;">
  ⚠️ All data is 100% fictional and randomly generated for demo purposes.
</p>
""", unsafe_allow_html=True)

total     = len(assignees)
critical  = len(assignees[assignees["status"].isin(["Delayed","At Risk"])])
on_track  = len(assignees[assignees["status"] == "On Track"])
completed = len(assignees[assignees["status"] == "Completed"])

k1, k2, k3, k4 = st.columns(4)
metrics = [
    (k1, "💼", str(total),     "Total Assignees",   "#4F46E5"),
    (k2, "🚨", str(critical),  "Critical / At Risk", "#DC2626"),
    (k3, "✅", str(on_track),  "On Track",           "#059669"),
    (k4, "🏁", str(completed), "Completed",          "#0284C7"),
]
for col, icon, val, label, color in metrics:
    with col:
        st.markdown(f"""
        <div class="mini-metric" style="border-top:3px solid {color};">
          <div style="font-size:22px;">{icon}</div>
          <div class="metric-value" style="color:{color};">{val}</div>
          <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)
with f1:
    status_filter = st.selectbox("🔍 Filter by Status",
        ["All","At Risk","Delayed","On Track","In Progress","Completed"])
with f2:
    risk_filter = st.selectbox("⚡ Filter by Risk",
        ["All","High Risk (>75)","Medium (50-75)","Low (<50)"])
with f3:
    search = st.text_input("🔎 Search assignee name")

filtered = assignees.copy()
if status_filter != "All":
    filtered = filtered[filtered["status"] == status_filter]
if risk_filter == "High Risk (>75)":
    filtered = filtered[filtered["risk_score"] > 75]
elif risk_filter == "Medium (50-75)":
    filtered = filtered[(filtered["risk_score"] >= 50) & (filtered["risk_score"] <= 75)]
elif risk_filter == "Low (<50)":
    filtered = filtered[filtered["risk_score"] < 50]
if search:
    filtered = filtered[filtered["name"].str.contains(search, case=False)]

st.markdown(f"""
<p style="color:#64748B;font-size:13px;margin:16px 0 8px;font-weight:500;">
  Showing {len(filtered)} assignees
</p>
""", unsafe_allow_html=True)

STATUS_CFG = {
    "At Risk":     ("pill-risk",  "#DC2626"),
    "Delayed":     ("pill-delay", "#EA580C"),
    "On Track":    ("pill-track", "#059669"),
    "In Progress": ("pill-prog",  "#4F46E5"),
    "Completed":   ("pill-done",  "#0284C7"),
}

SERVICE_CFG = {
    "Moving/HHG":           ("📦", "#4F46E5"),
    "Temporary Housing":    ("🏠", "#059669"),
    "Immigration/Visa":     ("🛂", "#D97706"),
    "Destination Services": ("🌍", "#0284C7"),
    "Tax Assistance":       ("💰", "#7C3AED"),
    "School Search":        ("🎓", "#EA580C"),
}
SERVICE_TYPES = list(SERVICE_CFG.keys())

for _, assignee in filtered.head(15).iterrows():
    status     = assignee["status"]
    pill_class = STATUS_CFG.get(status, ("pill-prog","#4F46E5"))[0]
    risk       = assignee["risk_score"]
    risk_color = "#DC2626" if risk > 75 else "#D97706" if risk > 50 else "#059669"

    with st.expander(
        f"  {assignee['name']}   |   "
        f"{assignee['origin_city']} → {assignee['dest_city']}   |   "
        f"Risk {risk:.0f}%   |   {status}"
    ):
        st.markdown(f"""
        <span class="pill {pill_class}">{status}</span>
        <span class="info-chip">🏢 <span>{assignee['company']}</span></span>
        <span class="info-chip">📋 <span>{assignee['policy_tier']}</span></span>
        <span class="info-chip">👨‍👩‍👧 <span>Family: {assignee['family_size']}</span></span>
        <span class="info-chip">🎯 <span>{assignee['coordinator']}</span></span>
        <span class="info-chip">📅 <span>Target: {assignee['target_date']}</span></span>
        """, unsafe_allow_html=True)

        st.markdown("<hr class='glass-divider'>", unsafe_allow_html=True)
        st.markdown("""
        <p style="color:#64748B;font-size:11px;font-weight:700;
                  letter-spacing:0.08em;margin-bottom:12px;">
          SERVICE TRACKS
        </p>
        """, unsafe_allow_html=True)

        assignee_svcs = services[services["assignee_id"] == assignee["id"]]
        cols = st.columns(6)

        for i, stype in enumerate(SERVICE_TYPES):
            icon, color = SERVICE_CFG[stype]
            svc = assignee_svcs[assignee_svcs["service_type"] == stype]

            with cols[i]:
                if svc.empty:
                    pct, svc_status = 0, "N/A"
                else:
                    svc_status = svc.iloc[0]["status"]
                    pct = {
                        "Completed": 100, "In Progress": 60,
                        "At Risk": 35, "Delayed": 35, "Not Started": 0
                    }.get(svc_status, 0)

                st.markdown(f"""
                <div class="service-card">
                  <div style="font-size:24px;">{icon}</div>
                  <div style="font-size:9px;color:#94A3B8;margin:6px 0 4px;
                              font-weight:700;letter-spacing:0.06em;">
                    {stype.split("/")[0].upper()}
                  </div>
                  <div class="progress-wrap">
                    <div style="height:100%;width:{pct}%;
                                background:{'linear-gradient(90deg,'+color+','+color+'88)' if pct>0 else 'transparent'};
                                border-radius:10px;transition:width 0.8s;">
                    </div>
                  </div>
                  <div style="font-size:13px;font-weight:800;
                              color:{'#059669' if pct==100 else '#D97706' if pct>0 else '#94A3B8'};">
                    {pct}%
                  </div>
                  <div style="font-size:9px;color:#94A3B8;margin-top:2px;">{svc_status}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="risk-gauge">
          <div style="flex:1;">
            <div style="font-size:11px;color:#94A3B8;font-weight:700;
                        letter-spacing:0.06em;margin-bottom:8px;">
              ASSIGNMENT RISK SCORE
            </div>
            <div class="progress-wrap" style="height:8px;">
              <div style="height:100%;width:{risk}%;
                          background:linear-gradient(90deg,{risk_color},{risk_color}66);
                          border-radius:10px;">
              </div>
            </div>
          </div>
          <div style="font-size:32px;font-weight:800;color:{risk_color};
                      min-width:72px;text-align:right;letter-spacing:-0.02em;">
            {risk:.0f}%
          </div>
        </div>
        """, unsafe_allow_html=True)
