import streamlit as st

st.set_page_config(
    page_title='Mobility Operations Command Center',
    page_icon="",
    layout="wide",
    initial_sidebar_state='expanded'
)

st.markdown("""
<style>
  .main { background: #0F1117; }
  [data-testid="stSidebar"] {
    background: #1A1D27;
    border-right: 1px solid #2D2F3E;
  }
  [data-testid="stMetric"] {
    background: #1E2130;
    border-radius: 10px;
    padding: 10px;
    border: 1px solid #2D2F3E;
  }
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown('## 💼 Mobility Command Center')
    st.markdown("*Global Mobility Operations Platform*")
    st.divider()
    st.info("""
    ⚠️ Demo Version
    All data shown is completely
    fictional and randomly generated.
    """)

    st.title("💼 Mobility Operations Command Center")
    st.caption("One Screen. Every assignee. Every Service. Every cost. Real time")
    st.divider()

    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown("""
    ### 🗺️ Navigate
    Use the sidebar pages:
    - 🎯 War Room Dashboard
    - 💼 Assignee Journeys
    - 🛂 Service Management
    - 💰 Cost Intelligence
    - 🛡️ Compliance Center
    - 🏭 Vendor Network
    - 🤖 AI Advisor
    - 📄 Reports
    """)
    
    with col2:
        st.markdown("###  📊  Platform Stats")
        st.metric("Active Assignment ", "300")
        st.metric("Service Tracks",'1,680+')
        st.metric('Vendors Tracked','24')

    with col3:
        st.markdown("### ⚡ Quick Status")
        st.error("🚨 Critical alerts need attention")
        st.warning("⚠️ Check compliance deadlines")
        st.success('✅ AI Advisor is active')
