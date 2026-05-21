import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(
    page_title="PhonePe Dashboard",
    layout="wide"
)

# --------------------------------
# CUSTOM CSS
# --------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #16002E;
}

/* Text Color */
h1,h2,h3,h4,h5,h6,p,div,label {
    color: white !important;
}

/* Cards */
.card {
    background: linear-gradient(135deg, #2A0A4A, #4B0082);
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# SIDEBAR
# --------------------------------

st.sidebar.title("📱 Filters")

quarter = st.sidebar.selectbox(
    "Select Quarter",
    ["Q1", "Q2", "Q3", "Q4"]
)

# --------------------------------
# HEADER
# --------------------------------

st.title("📱 PhonePe Pulse Dashboard")

# --------------------------------
# KPI CARDS
# --------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>Total Transactions</h3>
        <h2>2,82,19,25,55,839</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>Total Payment Value</h3>
        <h2>₹35,99,880 Cr</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3>Avg Transaction</h3>
        <h2>₹1,276</h2>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------
# MAIN SECTION
# --------------------------------

left, right = st.columns([2,1])

# --------------------------------
# MAP SECTION
# --------------------------------

with left:

    st.subheader("🗺️ India Transactions Map")

    map_data = pd.DataFrame({
        "lat": [28.61, 19.07, 26.91, 22.57],
        "lon": [77.20, 72.87, 75.78, 88.36]
    })

    st.map(map_data)

# --------------------------------
# CATEGORY SECTION
# --------------------------------

with right:

    st.subheader("📊 Categories")

    st.markdown("""
    <div class="card">
        <h4>🛒 Merchant Payments</h4>
        <h3>17,41,91,91,808</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h4>💸 Peer-to-Peer Payments</h4>
        <h3>9,36,82,04,284</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h4>📱 Recharge & Bill Payments</h4>
        <h3>1,39,25,29,171</h3>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------
# PIE CHART
# --------------------------------

st.subheader("📈 Transaction Categories")

pie_data = pd.DataFrame({
    "Category": ["Merchant", "P2P", "Recharge"],
    "Value": [45, 35, 20]
})

fig = px.pie(
    pie_data,
    names="Category",
    values="Value",
    hole=0.5
)

fig.update_layout(
    paper_bgcolor="#16002E",
    font_color="white"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# BOTTOM INFO
# --------------------------------

col4, col5 = st.columns(2)

with col4:
    st.markdown("""
    <div class="card">
        <h4>📌 Fun Fact</h4>
        <p>Rajasthan showed strong growth in Q4.</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="card">
        <h4>📌 Insight</h4>
        <p>Maharashtra has highest transaction volume.</p>
    </div>
    """, unsafe_allow_html=True)
    
 