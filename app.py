import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import urllib.request

# ── Sample Data ────────────────────────────────────────────────────────────────
states_data = {
    "State": [
        "Maharashtra","Uttar Pradesh","Karnataka","Tamil Nadu","Rajasthan",
        "Gujarat","Delhi","West Bengal","Andhra Pradesh","Telangana",
        "Madhya Pradesh","Bihar","Punjab","Haryana","Kerala",
        "Odisha","Jharkhand","Assam","Chhattisgarh","Uttarakhand",
        "Himachal Pradesh","Jammu and Kashmir","Goa","Tripura","Meghalaya",
        "Manipur","Nagaland","Arunachal Pradesh","Mizoram","Sikkim"
    ],
    "Transactions": [
        4200000000, 3800000000, 3200000000, 2900000000, 2040000000,
        2600000000, 2400000000, 2100000000, 1900000000, 1800000000,
        1600000000, 1400000000, 1300000000, 1200000000, 1100000000,
        900000000,  800000000,  700000000,  600000000,  500000000,
        300000000,  280000000,  270000000,  150000000,  140000000,
        120000000,  100000000,   80000000,   60000000,   40000000
    ],
    "Payment_Value": [
        85000, 62000, 71000, 58000, 27900,
        64000, 78000, 43000, 39000, 42000,
        31000, 28000, 35000, 38000, 29000,
        19000, 16000, 14000, 12000, 10000,
         7000,  6500,  8000,  3000,  2800,
         2400,  2000,  1600,  1200,   800
    ],
    "Avg_Value": [
        1450, 1180, 1620, 1380, 1367,
        1520, 1890, 1240, 1310, 1420,
        1190, 1050,  980, 1150, 1280,
         980,  920,  870,  840,  780,
         720,  690,  950,  620,  600,
         580,  560,  540,  520,  500
    ],
    "Quarter": ["Q4 2024"] * 30
}

categories_data = {
    "Category": [
        "Merchant payments",
        "Peer-to-peer payments",
        "Recharge & bill payments",
        "Financial Services",
        "Others"
    ],
    "Count": [
        1741919808,
        936820428,
        139252917,
        32113340,
        72172360
    ]
}

df = pd.DataFrame(states_data)
df_cat = pd.DataFrame(categories_data)

quarters = ["Q1 2023","Q2 2023","Q3 2023","Q4 2023",
            "Q1 2024","Q2 2024","Q3 2024","Q4 2024"]

# ── Helpers ────────────────────────────────────────────────────────────────────
def fmt_indian(n):
    """Format number in Indian system (lakhs/crores)."""
    n = int(n)
    s = str(n)
    if len(s) <= 3:
        return s
    result = s[-3:]
    s = s[:-3]
    while len(s) > 2:
        result = s[-2:] + "," + result
        s = s[:-2]
    if s:
        result = s + "," + result
    return result

def fmt_crore(val):
    cr = val / 10000000
    if cr >= 100:
        return f"₹{cr:,.0f} Cr"
    return f"₹{cr:,.2f} Cr"

# ── GeoJSON ────────────────────────────────────────────────────────────────────
GEOJSON_URL = (
    "https://raw.githubusercontent.com/Subhash9325/"
    "GeoJson-Data-of-Indian-States/master/Indian_States"
)
try:
    with urllib.request.urlopen(GEOJSON_URL, timeout=8) as r:
        india_geo = json.loads(r.read().decode())
    geo_key = "NAME_1"
except Exception:
    india_geo = None
    geo_key = None

# ── Map Figure ─────────────────────────────────────────────────────────────────
def make_map(filtered_df):
    if india_geo:
        fig = px.choropleth(
            filtered_df,
            geojson=india_geo,
            locations="State",
            featureidkey=f"properties.{geo_key}",
            color="Transactions",
            color_continuous_scale=["#0d4f8c","#1a7abf","#f5a623","#e84545","#ff6b35"],
            hover_name="State",
            hover_data={"Transactions": True, "Payment_Value": True, "Avg_Value": True},
        )
    else:
        fig = px.choropleth(
            filtered_df,
            locations="State",
            locationmode="country names",
            color="Transactions",
            color_continuous_scale=["#0d4f8c","#1a7abf","#f5a623","#e84545","#ff6b35"],
            scope="asia",
        )

    fig.update_geos(
        fitbounds="locations",
        visible=False,
        bgcolor="#1a0533",
        showcoastlines=False,
        showland=True, landcolor="#1a0533",
        showocean=True, oceancolor="#0d0020",
        showlakes=False,
        showrivers=False,
    )
    fig.update_layout(
        paper_bgcolor="#1a0533",
        plot_bgcolor="#1a0533",
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_showscale=False,
        hoverlabel=dict(
            bgcolor="#2d1060",
            font_color="white",
            font_size=13,
        ),
        geo=dict(bgcolor="#1a0533"),
    )
    fig.update_traces(
        marker_line_color="#3a1080",
        marker_line_width=0.5,
    )
    return fig

# ── Category Bar ───────────────────────────────────────────────────────────────
def make_cat_bar():
    fig = go.Figure(go.Bar(
        y=df_cat["Category"],
        x=df_cat["Count"],
        orientation="h",
        marker=dict(
            color=["#f5a623","#1a7abf","#e84545","#2ecc71","#9b59b6"],
            line=dict(width=0),
        ),
        text=[fmt_indian(c) for c in df_cat["Count"]],
        textposition="outside",
        textfont=dict(color="white", size=11),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=60, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(
            tickfont=dict(color="#c8b8e8", size=11),
            showgrid=False,
        ),
        height=200,
        bargap=0.35,
    )
    return fig

# ── App Layout ─────────────────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap"
    ],
    title="PhonePe Pulse – The Beat of Progress"
)

PURPLE_BG   = "#12002e"
PANEL_BG    = "#1e0545"
CARD_BG     = "#2a0d5e"
ACCENT      = "#7c3aed"
ACCENT2     = "#a855f7"
ORANGE      = "#f5a623"
TEXT_MAIN   = "#ffffff"
TEXT_SUB    = "#c4a8f0"
TEXT_MUTED  = "#8b6bb1"
BORDER      = "#3d1a7a"

app.layout = html.Div(style={
    "backgroundColor": PURPLE_BG,
    "minHeight": "100vh",
    "fontFamily": "'DM Sans', sans-serif",
    "color": TEXT_MAIN,
}, children=[

    # ── Top Nav ──────────────────────────────────────────────────────────────
    html.Div(style={
        "backgroundColor": PANEL_BG,
        "padding": "0 32px",
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "space-between",
        "borderBottom": f"1px solid {BORDER}",
        "height": "52px",
    }, children=[
        html.Div(style={"display":"flex","alignItems":"center","gap":"10px"}, children=[
            html.Div("📱", style={"fontSize":"22px"}),
            html.Span("PhonePe", style={
                "fontFamily": "'Baloo 2', sans-serif",
                "fontWeight": "800",
                "fontSize": "18px",
                "color": "#a855f7",
            }),
            html.Span("Pulse", style={
                "fontFamily": "'Baloo 2', sans-serif",
                "fontWeight": "600",
                "fontSize": "18px",
                "color": TEXT_MAIN,
            }),
            html.Span("THE BEAT OF PROGRESS", style={
                "fontSize": "9px",
                "color": TEXT_MUTED,
                "letterSpacing": "2px",
                "marginLeft": "8px",
                "marginTop": "2px",
            }),
        ]),
        html.Div(style={"display":"flex","gap":"32px"}, children=[
            html.Span("EXPLORE DATA", style={
                "fontSize": "12px", "fontWeight": "600",
                "color": ACCENT2, "borderBottom": f"2px solid {ACCENT2}",
                "paddingBottom": "4px", "cursor": "pointer",
            }),
            html.Span("REPORTS",  style={"fontSize":"12px","color":TEXT_MUTED,"cursor":"pointer"}),
            html.Span("INSIGHTS", style={"fontSize":"12px","color":TEXT_MUTED,"cursor":"pointer"}),
            html.Span("DATA APIs",style={"fontSize":"12px","color":TEXT_MUTED,"cursor":"pointer"}),
        ]),
    ]),

    # ── Main Body ─────────────────────────────────────────────────────────────
    html.Div(style={
        "display": "grid",
        "gridTemplateColumns": "1fr 340px",
        "height": "calc(100vh - 52px)",
    }, children=[

        # ── Left: Map + controls ──────────────────────────────────────────
        html.Div(style={
            "backgroundColor": PANEL_BG,
            "position": "relative",
            "borderRight": f"1px solid {BORDER}",
        }, children=[

            # All India badge
            html.Div("All India", style={
                "position": "absolute", "top": "16px", "left": "16px",
                "backgroundColor": CARD_BG,
                "border": f"1px solid {BORDER}",
                "borderRadius": "6px",
                "padding": "5px 12px",
                "fontSize": "13px", "fontWeight": "600",
                "color": TEXT_MAIN, "zIndex": "10",
            }),

            # Dropdowns
            html.Div(style={
                "position": "absolute", "top": "52px", "left": "16px",
                "display": "flex", "gap": "8px", "zIndex": "10",
            }, children=[
                dcc.Dropdown(
                    id="metric-dd",
                    options=[
                        {"label": "Transactions", "value": "Transactions"},
                        {"label": "Payment Value", "value": "Payment_Value"},
                        {"label": "Avg Value",     "value": "Avg_Value"},
                    ],
                    value="Transactions",
                    clearable=False,
                    style={"width":"150px","fontSize":"12px"},
                    className="dark-dd",
                ),
                dcc.Dropdown(
                    id="quarter-dd",
                    options=[{"label": q, "value": q} for q in quarters],
                    value="Q4 2024",
                    clearable=False,
                    style={"width":"110px","fontSize":"12px"},
                    className="dark-dd",
                ),
            ]),

            # Map
            dcc.Graph(
                id="india-map",
                config={"displayModeBar": False},
                style={"height": "calc(100vh - 52px)", "width": "100%"},
            ),

            # Fun Fact strip
            html.Div(style={
                "position": "absolute", "bottom": "0", "left": "0", "right": "0",
                "display": "flex", "gap": "12px", "padding": "12px 16px",
                "backgroundColor": "rgba(10,0,30,0.85)",
                "borderTop": f"1px solid {BORDER}",
            }, children=[
                html.Div(style={
                    "flex": "1", "backgroundColor": CARD_BG,
                    "borderRadius": "8px", "padding": "10px 14px",
                    "border": f"1px solid {BORDER}",
                }, children=[
                    html.Span("FUN FACT", style={
                        "fontSize":"9px","color":ORANGE,
                        "letterSpacing":"2px","fontWeight":"700",
                    }),
                    html.P("₹5,050 spent on an avg by a Mizoram resident on PhonePe in Q3 2021 — the highest ATV in the country!", style={
                        "fontSize":"11px","color":TEXT_SUB,"margin":"4px 0 6px",
                    }),
                    html.Span("See data for Mizoram →", style={
                        "fontSize":"11px","color":ACCENT2,"cursor":"pointer",
                    }),
                ]),
                html.Div(style={
                    "flex": "1", "backgroundColor": CARD_BG,
                    "borderRadius": "8px", "padding": "10px 14px",
                    "border": f"1px solid {BORDER}",
                }, children=[
                    html.Span("FUN FACT", style={
                        "fontSize":"9px","color":ORANGE,
                        "letterSpacing":"2px","fontWeight":"700",
                    }),
                    html.P("With a 50% spurt, Chandigarh grew its transactions more than any other city in Q3 2021.", style={
                        "fontSize":"11px","color":TEXT_SUB,"margin":"4px 0 6px",
                    }),
                    html.Span("See data for Chandigarh →", style={
                        "fontSize":"11px","color":ACCENT2,"cursor":"pointer",
                    }),
                ]),
            ]),
        ]),

        # ── Right Panel ───────────────────────────────────────────────────
        html.Div(style={
            "backgroundColor": PURPLE_BG,
            "overflowY": "auto",
            "padding": "20px 18px",
        }, children=[

            html.H3("Transactions", style={
                "fontFamily": "'Baloo 2', sans-serif",
                "fontWeight": "700",
                "fontSize": "22px",
                "margin": "0 0 4px",
                "color": TEXT_MAIN,
            }),
            html.P("All PhonePe transactions (UPI + Cards + Wallets)", style={
                "fontSize": "11px", "color": TEXT_MUTED, "margin": "0 0 16px",
            }),

            # Big transaction number
            html.Div(id="big-number", style={
                "fontFamily": "'Baloo 2', sans-serif",
                "fontWeight": "800",
                "fontSize": "34px",
                "color": ORANGE,
                "lineHeight": "1.1",
                "marginBottom": "16px",
                "letterSpacing": "-1px",
            }),

            # KPI mini cards
            html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"10px","marginBottom":"22px"}, children=[
                html.Div(id="kpi-payment", style={
                    "backgroundColor": CARD_BG,
                    "borderRadius": "10px",
                    "padding": "12px 14px",
                    "border": f"1px solid {BORDER}",
                }),
                html.Div(id="kpi-avg", style={
                    "backgroundColor": CARD_BG,
                    "borderRadius": "10px",
                    "padding": "12px 14px",
                    "border": f"1px solid {BORDER}",
                }),
            ]),

            # Divider
            html.Hr(style={"borderColor": BORDER, "margin": "0 0 18px"}),

            # Categories
            html.H4("Categories", style={
                "fontFamily": "'Baloo 2', sans-serif",
                "fontWeight": "700",
                "fontSize": "16px",
                "margin": "0 0 12px",
            }),

            dcc.Graph(
                id="cat-bar",
                figure=make_cat_bar(),
                config={"displayModeBar": False},
                style={"height": "200px"},
            ),

            # Tabs
            html.Div(style={
                "display": "flex",
                "gap": "0",
                "marginTop": "18px",
                "borderRadius": "8px",
                "overflow": "hidden",
                "border": f"1px solid {BORDER}",
            }, children=[
                html.Div("States",       style={"flex":"1","textAlign":"center","padding":"8px","backgroundColor":ACCENT,"fontSize":"12px","fontWeight":"600","cursor":"pointer"}),
                html.Div("Districts",    style={"flex":"1","textAlign":"center","padding":"8px","backgroundColor":CARD_BG,"fontSize":"12px","color":TEXT_MUTED,"cursor":"pointer"}),
                html.Div("Postal Codes", style={"flex":"1","textAlign":"center","padding":"8px","backgroundColor":CARD_BG,"fontSize":"12px","color":TEXT_MUTED,"cursor":"pointer"}),
            ]),

            # State list
            html.Div(id="state-list", style={"marginTop":"12px"}),
        ]),
    ]),
])

# ── Styles ─────────────────────────────────────────────────────────────────────
app.index_string = '''<!DOCTYPE html>
<html>
<head>
{%metas%}
<title>{%title%}</title>
{%favicon%}
{%css%}
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: #12002e; }
  ::-webkit-scrollbar-thumb { background: #3d1a7a; border-radius: 3px; }

  .dark-dd .Select-control {
    background-color: #2a0d5e !important;
    border: 1px solid #3d1a7a !important;
    color: white !important;
    border-radius: 6px !important;
  }
  .dark-dd .Select-value-label { color: white !important; }
  .dark-dd .Select-menu-outer {
    background-color: #2a0d5e !important;
    border: 1px solid #3d1a7a !important;
  }
  .dark-dd .VirtualizedSelectOption { color: white !important; }
  .dark-dd .VirtualizedSelectFocusedOption { background-color: #3d1a7a !important; }
  .Select-arrow { border-color: #a855f7 transparent transparent !important; }
</style>
</head>
<body>
{%app_entry%}
<footer>{%config%}{%scripts%}{%renderer%}</footer>
</body>
</html>'''

# ── Callbacks ──────────────────────────────────────────────────────────────────
@app.callback(
    Output("india-map",   "figure"),
    Output("big-number",  "children"),
    Output("kpi-payment", "children"),
    Output("kpi-avg",     "children"),
    Output("state-list",  "children"),
    Input("metric-dd",    "value"),
    Input("quarter-dd",   "value"),
)
def update_dashboard(metric, quarter):
    filtered = df[df["Quarter"] == quarter]

    # Map
    map_fig = make_map(filtered)

    # KPIs
    total_tx  = filtered["Transactions"].sum()
    total_pay = filtered["Payment_Value"].sum()
    avg_val   = filtered["Avg_Value"].mean()

    big_num = fmt_indian(total_tx)

    kpi_pay = [
        html.P("Total payment value", style={"fontSize":"10px","color":"#8b6bb1","marginBottom":"4px"}),
        html.P(fmt_crore(total_pay * 10000000), style={
            "fontFamily":"'Baloo 2',sans-serif","fontWeight":"700",
            "fontSize":"16px","color":"white",
        }),
    ]
    kpi_avg = [
        html.P("Avg. transaction value", style={"fontSize":"10px","color":"#8b6bb1","marginBottom":"4px"}),
        html.P(f"₹{avg_val:,.0f}", style={
            "fontFamily":"'Baloo 2',sans-serif","fontWeight":"700",
            "fontSize":"16px","color":"white",
        }),
    ]

    # State list top 8
    top = filtered.nlargest(8, "Transactions")
    max_tx = top["Transactions"].max()
    rows = []
    for i, row in enumerate(top.itertuples(), 1):
        pct = row.Transactions / max_tx
        rows.append(html.Div(style={
            "marginBottom":"10px",
        }, children=[
            html.Div(style={"display":"flex","justifyContent":"space-between","marginBottom":"3px"}, children=[
                html.Span(f"{i}. {row.State}", style={"fontSize":"12px","color":"#c4a8f0"}),
                html.Span(fmt_indian(row.Transactions), style={"fontSize":"12px","color":"white","fontWeight":"600"}),
            ]),
            html.Div(style={"backgroundColor":"#2a0d5e","borderRadius":"3px","height":"4px"}, children=[
                html.Div(style={
                    "backgroundColor":"#a855f7",
                    "width": f"{pct*100:.0f}%",
                    "height":"4px",
                    "borderRadius":"3px",
                }),
            ]),
        ]))
    return map_fig, big_num, kpi_pay, kpi_avg, rows


if __name__ == "__main__":
    app.run(debug=True, port=8050)
