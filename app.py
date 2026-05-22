import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
import requests

st.set_page_config(page_title="PhonePe Pulse Dashboard", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background-color: #0D0020; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A0035 0%, #0D0020 100%);
    border-right: 1px solid #3D0080;
}
[data-testid="stSidebar"] * { color: white !important; }
h1,h2,h3,h4,h5,h6,p,div,label,span { color: white !important; }
.kpi-card {
    background: linear-gradient(135deg, #2D0060 0%, #1A0040 100%);
    border: 1px solid #6600CC;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 12px;
    box-shadow: 0 4px 20px rgba(102,0,204,0.3);
}
.kpi-label { font-size: 11px; color: #BB88FF !important; font-weight: 600; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px; }
.kpi-value { font-size: 26px; font-weight: 700; color: white !important; line-height: 1.2; }
.cat-card {
    background: linear-gradient(135deg, #1E0045 0%, #120030 100%);
    border: 1px solid #4400AA;
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.cat-name { font-size: 13px; color: #CC99FF !important; font-weight: 500; }
.cat-value { font-size: 15px; font-weight: 700; color: white !important; }
.section-title { font-size: 16px; font-weight: 600; color: white !important; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #3D0080; }
.top-bar { background: linear-gradient(90deg, #6600FF, #9900CC); padding: 6px 16px; border-radius: 8px; display: inline-block; font-size: 12px; font-weight: 600; letter-spacing: 1px; color: white !important; margin-bottom: 16px; }
</style>
""", unsafe_allow_html=True)

# ---- STATE DATA ----
state_data = {
    "Andhra Pradesh":    {"txn_cr": 162.0, "value_cr": 260000, "intensity": 55},
    "Arunachal Pradesh": {"txn_cr":   1.5, "value_cr":   3000, "intensity":  2},
    "Assam":             {"txn_cr":  38.0, "value_cr":  60000, "intensity": 18},
    "Bihar":             {"txn_cr":  82.0, "value_cr": 120000, "intensity": 35},
    "Chhattisgarh":      {"txn_cr":  32.0, "value_cr":  55000, "intensity": 16},
    "Goa":               {"txn_cr":   9.0, "value_cr":  18000, "intensity":  6},
    "Gujarat":           {"txn_cr": 186.0, "value_cr": 320000, "intensity": 60},
    "Haryana":           {"txn_cr":  78.0, "value_cr": 140000, "intensity": 33},
    "Himachal Pradesh":  {"txn_cr":  12.0, "value_cr":  22000, "intensity":  8},
    "Jammu and Kashmir": {"txn_cr":   8.0, "value_cr":  15000, "intensity":  5},
    "Jharkhand":         {"txn_cr":  42.0, "value_cr":  70000, "intensity": 20},
    "Karnataka":         {"txn_cr": 321.0, "value_cr": 620000, "intensity": 85},
    "Kerala":            {"txn_cr":  72.0, "value_cr": 130000, "intensity": 30},
    "Madhya Pradesh":    {"txn_cr": 108.0, "value_cr": 180000, "intensity": 44},
    "Maharashtra":       {"txn_cr": 452.0, "value_cr": 850000, "intensity": 95},
    "Manipur":           {"txn_cr":   3.0, "value_cr":   6000, "intensity":  3},
    "Meghalaya":         {"txn_cr":   4.0, "value_cr":   7000, "intensity":  3},
    "Mizoram":           {"txn_cr":   1.2, "value_cr":   2500, "intensity":  1},
    "Nagaland":          {"txn_cr":   2.0, "value_cr":   4000, "intensity":  2},
    "Odisha":            {"txn_cr":  54.0, "value_cr":  90000, "intensity": 25},
    "Punjab":            {"txn_cr":  95.0, "value_cr": 160000, "intensity": 40},
    "Rajasthan":         {"txn_cr": 204.3, "value_cr": 279305, "intensity": 62},
    "Sikkim":            {"txn_cr":   0.8, "value_cr":   1500, "intensity":  1},
    "Tamil Nadu":        {"txn_cr": 253.0, "value_cr": 490000, "intensity": 75},
    "Telangana":         {"txn_cr": 145.0, "value_cr": 240000, "intensity": 52},
    "Tripura":           {"txn_cr":   5.0, "value_cr":   9000, "intensity":  4},
    "Uttar Pradesh":     {"txn_cr": 228.0, "value_cr": 380000, "intensity": 68},
    "Uttarakhand":       {"txn_cr":  28.0, "value_cr":  48000, "intensity": 14},
    "West Bengal":       {"txn_cr": 123.0, "value_cr": 210000, "intensity": 48},
    "NCT of Delhi":      {"txn_cr": 285.0, "value_cr": 580000, "intensity": 80},
}

df = pd.DataFrame([
    {"state": k, "txn_cr": v["txn_cr"], "intensity": v["intensity"]}
    for k, v in state_data.items()
])

# ---- SIDEBAR ----
with st.sidebar:
    st.markdown('<div style="font-size:20px;font-weight:700;margin-bottom:20px;">📱 PhonePe Pulse</div>', unsafe_allow_html=True)
    view    = st.selectbox("View",    ["All India", "State", "District"])
    metric  = st.selectbox("Metric",  ["Transactions", "Payment Value", "Avg Transaction"])
    quarter = st.selectbox("Quarter", ["Q4 2024", "Q3 2024", "Q2 2024", "Q1 2024"])
    st.markdown("---")
    st.markdown('<div style="font-size:12px;color:#9966CC;">Data source: PhonePe Pulse</div>', unsafe_allow_html=True)

# ---- HEADER ----
st.markdown('<div class="top-bar">📱 PHONEPE PULSE · THE BEAT OF PROGRESS</div>', unsafe_allow_html=True)

# ---- LAYOUT ----
map_col, stats_col = st.columns([3, 1.2])

with map_col:
    st.markdown('<div class="section-title">🗺️ India Transactions Map</div>', unsafe_allow_html=True)

    @st.cache_data(show_spinner=False)
    def load_india_geojson():
        url = "https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.geojson"
        r = requests.get(url, timeout=15)
        return r.json()

    try:
        geojson = load_india_geojson()

        # PhonePe-style color scale: dark purple → teal → orange → red
        colorscale = [
            [0.00, "#0D001A"],
            [0.10, "#2D0060"],
            [0.25, "#6600CC"],
            [0.45, "#0099AA"],
            [0.65, "#FF6600"],
            [0.85, "#FF2200"],
            [1.00, "#FF0000"],
        ]

        # Build lookup: GeoJSON NAME_1 → intensity
        intensity_lookup = {}
        for feat in geojson["features"]:
            name = feat["properties"].get("NAME_1", "")
            if name in state_data:
                intensity_lookup[name] = state_data[name]["intensity"]
            elif name == "Telangana" and "Telangana" in state_data:
                intensity_lookup[name] = state_data["Telangana"]["intensity"]
            else:
                intensity_lookup[name] = 0

        # Create dark folium map
        m = folium.Map(
            location=[22.5, 82.5],
            zoom_start=5,
            tiles="CartoDB dark_matter",
            prefer_canvas=True,
        )

        # Choropleth layer
        choropleth = folium.Choropleth(
            geo_data=geojson,
            name="Transactions",
            data=df,
            columns=["state", "intensity"],
            key_on="feature.properties.NAME_1",
            fill_color="YlOrRd",
            fill_opacity=0.85,
            line_opacity=0.4,
            line_color="#6600CC",
            legend_name="Transaction Intensity",
            nan_fill_color="#1A0035",
            highlight=True,
        ).add_to(m)

        # Custom color: override default with purple→orange→red feel
        # Add tooltip
        choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(
                fields=["NAME_1"],
                aliases=["State:"],
                style="background-color:#1A0035;color:white;border:1px solid #6600CC;border-radius:8px;padding:8px;"
            )
        )

        # Style each feature
        def style_func(feature):
            name = feature["properties"].get("NAME_1", "")
            val  = intensity_lookup.get(name, 0)
            if val >= 80:   color = "#FF0000"
            elif val >= 65: color = "#FF3300"
            elif val >= 50: color = "#FF6600"
            elif val >= 35: color = "#FF9900"
            elif val >= 20: color = "#9900CC"
            elif val >= 10: color = "#6600AA"
            elif val >= 5:  color = "#330088"
            else:           color = "#1A0040"
            return {
                "fillColor":   color,
                "color":       "#9900FF",
                "weight":      1.2,
                "fillOpacity": 0.85,
            }

        folium.GeoJson(
            geojson,
            name="India States",
            style_function=style_func,
            tooltip=folium.GeoJsonTooltip(
                fields=["NAME_1"],
                aliases=["📍 State:"],
                style="background-color:#1A0035;color:white;font-family:Inter;border:1px solid #6600CC;border-radius:8px;padding:8px;font-size:13px;"
            ),
        ).add_to(m)

        st_folium(m, width=None, height=500, returned_objects=[])

    except Exception as e:
        st.error(f"Map could not load: {e}")
        # Fallback bar chart
        fig_fb = px.bar(
            df.sort_values("intensity", ascending=True).tail(15),
            x="intensity", y="state", orientation="h",
            color="intensity",
            color_continuous_scale=["#3300AA","#9900FF","#FF6600","#FF0000"],
            labels={"intensity": "Intensity", "state": "State"},
        )
        fig_fb.update_layout(paper_bgcolor="#0D0020", plot_bgcolor="#0D0020",
                             font_color="white", height=500, coloraxis_showscale=False)
        st.plotly_chart(fig_fb, use_container_width=True)

with stats_col:
    st.markdown('<div class="section-title">📊 Transactions</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-label">All PhonePe Transactions (UPI + Cards + Wallets)</div>
        <div class="kpi-value">28,21,92,55,839</div>
    </div>""", unsafe_allow_html=True)

    ca, cb = st.columns(2)
    with ca:
        st.markdown("""<div class="kpi-card" style="padding:14px;">
            <div class="kpi-label" style="font-size:10px;">Total payment value</div>
            <div class="kpi-value" style="font-size:16px;">₹35,99,880 Cr</div>
        </div>""", unsafe_allow_html=True)
    with cb:
        st.markdown("""<div class="kpi-card" style="padding:14px;">
            <div class="kpi-label" style="font-size:10px;">Avg transaction value</div>
            <div class="kpi-value" style="font-size:16px;">₹1,276</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title" style="margin-top:16px;">📋 Categories</div>', unsafe_allow_html=True)
    for name, value in [
        ("🛒 Merchant payments",        "17,41,91,91,808"),
        ("💸 Peer-to-peer payments",    "9,36,82,04,284"),
        ("📱 Recharge & bill payments", "1,39,25,29,171"),
        ("🏦 Financial Services",       "3,21,13,340"),
        ("⚙️ Others",                   "72,17,236"),
    ]:
        st.markdown(f"""<div class="cat-card">
            <span class="cat-name">{name}</span>
            <span class="cat-value">{value}</span>
        </div>""", unsafe_allow_html=True)

# ---- BOTTOM CHARTS ----
st.markdown("---")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<div class="section-title">📈 Category Split</div>', unsafe_allow_html=True)
    pie_df = pd.DataFrame({
        "Category": ["Merchant", "P2P", "Recharge", "Financial", "Others"],
        "Value":    [61.7, 33.2, 4.9, 0.11, 0.02]
    })
    fig_pie = px.pie(pie_df, names="Category", values="Value", hole=0.55,
                     color_discrete_sequence=["#9900FF","#FF6600","#FF0066","#00CCFF","#FFCC00"])
    fig_pie.update_layout(paper_bgcolor="#0D0020", font_color="white",
                          margin=dict(l=10,r=10,t=10,b=10), height=260,
                          legend=dict(font=dict(color="white")))
    fig_pie.update_traces(textfont_color="white")
    st.plotly_chart(fig_pie, use_container_width=True)

with c2:
    st.markdown('<div class="section-title">📊 Top 5 States</div>', unsafe_allow_html=True)
    top5 = df.nlargest(5, "txn_cr")[["state","txn_cr"]]
    fig_bar = px.bar(top5, x="txn_cr", y="state", orientation="h",
                     color="txn_cr",
                     color_continuous_scale=["#3300AA","#9900FF","#FF6600"],
                     labels={"txn_cr": "Transactions (Cr)", "state": ""})
    fig_bar.update_layout(paper_bgcolor="#0D0020", plot_bgcolor="#0D0020",
                          font_color="white", margin=dict(l=0,r=10,t=10,b=10),
                          height=260, coloraxis_showscale=False)
    st.plotly_chart(fig_bar, use_container_width=True)

with c3:
    st.markdown('<div class="section-title">📅 Quarterly Trend</div>', unsafe_allow_html=True)
    trend_df = pd.DataFrame({
        "Quarter":      ["Q1 2024","Q2 2024","Q3 2024","Q4 2024"],
        "Transactions": [22.1, 24.5, 26.3, 28.2]
    })
    fig_line = px.line(trend_df, x="Quarter", y="Transactions", markers=True,
                       color_discrete_sequence=["#9900FF"])
    fig_line.update_traces(line_width=3, marker_size=8, marker_color="#FF6600")
    fig_line.update_layout(paper_bgcolor="#0D0020", plot_bgcolor="#1A0035",
                           font_color="white", margin=dict(l=0,r=10,t=10,b=10),
                           height=260,
                           xaxis=dict(color="white", gridcolor="#3D0080"),
                           yaxis=dict(color="white", gridcolor="#3D0080"))
    st.plotly_chart(fig_line, use_container_width=True)

# ---- FUN FACTS ----
st.markdown("---")
f1, f2 = st.columns(2)
with f1:
    st.markdown("""<div class="kpi-card">
        <div class="kpi-label">🎯 Fun Fact</div>
        <p style="color:white;font-size:14px;margin:6px 0 0 0;">
        Rajasthan showed strong growth in Q4 2024 with transactions crossing 2 Cr mark.
        </p></div>""", unsafe_allow_html=True)
with f2:
    st.markdown("""<div class="kpi-card">
        <div class="kpi-label">💡 Insight</div>
        <p style="color:white;font-size:14px;margin:6px 0 0 0;">
        Maharashtra leads with highest transaction volume — 452 Cr transactions in Q4 2024.
        </p></div>""", unsafe_allow_html=True)

    
 