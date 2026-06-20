import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from config import DB_PATH

st.set_page_config(
    page_title = "War Room",
    page_icon  = "🎯",
    layout     = "wide"
)

@st.cache_data(ttl=60)
def load_data():
    conn        = sqlite3.connect(DB_PATH)
    assignees   = pd.read_sql("SELECT * FROM assignees", conn)
    services    = pd.read_sql("SELECT * FROM services",  conn)
    compliance  = pd.read_sql("SELECT * FROM compliance",conn)
    alerts      = pd.read_sql("""
        SELECT * FROM alerts
        WHERE acknowledged = 0
        ORDER BY created_at DESC
        LIMIT 20
    """, conn)
    conn.close()
    return assignees, services, compliance, alerts

try:
    assignees, services, compliance, alerts = load_data()
except Exception as e:
    st.error(f"Run db_setup.py first!\n{e}")
    st.stop()

st.markdown("""
<div style="background:linear-gradient(135deg,#1E1B4B,#312E81);
            padding:16px 20px;border-radius:10px;margin-bottom:16px;">
    <h2 style="color:white;margin:0;">🎯 War Room Dashboard</h2>
    <p style="color:#A5B4FC;margin:4px 0 0;font-size:13px;">
    Complete portfolio overview · Real-time status
    </p>
</div>
""", unsafe_allow_html=True)

st.caption("⚠️ All data is 100% fictional.")

st.markdown("### 📊 Key Metrics")
k1, k2, k3, k4, k5 = st.columns(5)

total         = len(assignees)
critical      = len(assignees[assignees["status"].isin(["Delayed","At Risk"])])
on_track      = len(assignees[assignees["status"] == "On Track"])
completed     = len(assignees[assignees["status"] == "Completed"])
comp_critical = len(compliance[compliance["status"] == "CRITICAL"])

with k1:
    st.metric("💼 Total", total)
with k2:
    st.metric("🚨 Critical", critical)
with k3:
    st.metric("✅ On Track", on_track)
with k4:
    st.metric("🏁 Completed", completed)
with k5:
    st.metric("🛡️ Compliance", comp_critical)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 📈 Assignment Status")
    status_counts = assignees["status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    color_map = {
        "On Track":    "#10B981",
        "In Progress": "#4F46E5",
        "Completed":   "#0EA5E9",
        "At Risk":     "#F97316",
        "Delayed":     "#EF4444"
    }
    fig = px.bar(
        status_counts, x="Status", y="Count",
        color="Status",
        color_discrete_map=color_map,
        template="plotly_dark"
    )
    fig.update_layout(
        paper_bgcolor="#1A1D27",
        plot_bgcolor="#1A1D27",
        showlegend=False,
        height=280,
        margin=dict(l=10, r=10, t=10, b=30)
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### 🌍 By Destination")
    dest = assignees["dest_country"].value_counts().head(6).reset_index()
    dest.columns = ["Country", "Count"]
    fig2 = px.pie(
        dest, values="Count", names="Country",
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig2.update_layout(
        paper_bgcolor="#1A1D27",
        height=280,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    st.markdown("#### 📋 Policy Tiers")
    tiers = assignees["policy_tier"].value_counts().reset_index()
    tiers.columns = ["Tier", "Count"]
    tier_colors = {
        "Basic":     "#64748B",
        "Standard":  "#4F46E5",
        "Premium":   "#10B981",
        "Executive": "#F59E0B"
    }
    fig3 = px.pie(
        tiers, values="Count", names="Tier",
        template="plotly_dark",
        color="Tier",
        color_discrete_map=tier_colors
    )
    fig3.update_layout(
        paper_bgcolor="#1A1D27",
        height=280,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

st.markdown("### 🚨 Critical & At-Risk Assignments")
critical_df = assignees[
    assignees["status"].isin(["Delayed", "At Risk"])
].sort_values("risk_score", ascending=False).head(10)

if not critical_df.empty:
    display = critical_df[[
        "name", "company", "origin_city",
        "dest_city", "policy_tier",
        "risk_score", "status"
    ]].copy()
    display.columns = [
        "Name", "Company", "From",
        "To", "Policy", "Risk %", "Status"
    ]
    display["Risk %"] = display["Risk %"].apply(lambda x: f"{x:.1f}%")
    st.dataframe(display, use_container_width=True, hide_index=True)
else:
    st.success("No critical assignments!")

st.divider()

st.markdown("### 🔔 Recent Alerts")
if not alerts.empty:
    for _, alert in alerts.head(5).iterrows():
        sev = alert.get("severity", "LOW")
        if sev == "CRITICAL":
            st.error(f"🚨 {alert['alert_type']} — {alert['message']}")
        elif sev == "HIGH":
            st.warning(f"⚠️ {alert['alert_type']} — {alert['message']}")
        else:
            st.info(f"ℹ️ {alert['alert_type']} — {alert['message']}")
else:
    st.success("✅ No pending alerts!")