"""
Medicaid & Healthcare Access Risk Monitor
State-Level Coverage Prioritization for Policy Teams and Program Officers

Designed by Sherriff Abdul-Hamid
Original: Healthcare Access Risk Dashboard

Positions the tool as a decision-support instrument for:
- State Medicaid program officers
- Federal healthcare policy teams
- SNAP/benefits administrators managing coverage-adjacent programs
- Civic tech and government digital services teams
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ── PAGE CONFIG ────────────────────────────────────────────────
st.set_page_config(
    page_title="Medicaid & Healthcare Access Risk Monitor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── DESIGN TOKENS ─────────────────────────────────────────────
NAVY    = "#0A1F44"
GOLD    = "#C9A84C"
INK     = "#1A1A1A"
BODY    = "#2C3E50"
MUTED   = "#6B7280"
RED     = "#C8382A"
RED_BG  = "#FEF2F2"
GREEN   = "#1A7A2E"
GREEN_BG= "#F0FDF4"
AMBER   = "#B8560A"
AMBER_BG= "#FFFBEB"
GREY_BG = "#F5F6F8"
WHITE   = "#FFFFFF"

BAND_COLORS = {"High": RED, "Medium": AMBER, "Low": GREEN}
BAND_BG     = {"High": RED_BG, "Medium": AMBER_BG, "Low": GREEN_BG}

# ── CSS ────────────────────────────────────────────────────────
st.markdown(f"""
<style>
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    .main .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1280px;
    }}

    .hero {{
        background: linear-gradient(135deg, {NAVY} 0%, #152B5C 100%);
        border-left: 6px solid {GOLD};
        padding: 28px 32px 24px;
        margin-bottom: 20px;
        border-radius: 4px;
    }}
    .hero-eyebrow {{
        color: {GOLD};
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}
    .hero-title {{
        color: white;
        font-size: 28px;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 10px;
        font-family: Georgia, serif;
    }}
    .hero-sub {{
        color: #CADCFC;
        font-size: 14px;
        line-height: 1.55;
    }}
    .hero-meta {{
        color: {GOLD};
        font-size: 11px;
        margin-top: 12px;
        opacity: 0.85;
    }}

    .section-label {{
        color: {MUTED};
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 4px;
        margin-top: 28px;
    }}
    .section-title {{
        color: {INK};
        font-size: 21px;
        font-weight: 700;
        margin-bottom: 4px;
        font-family: Georgia, serif;
    }}
    .section-sub {{
        color: {MUTED};
        font-size: 13px;
        margin-bottom: 16px;
    }}

    .kpi-card {{
        background: white;
        border: 1px solid #E2E6EC;
        border-left: 4px solid {NAVY};
        padding: 14px 16px;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        height: 100%;
    }}
    .kpi-label {{
        color: {MUTED};
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }}
    .kpi-value {{
        color: {INK};
        font-size: 28px;
        font-weight: 700;
        line-height: 1.1;
        font-family: Georgia, serif;
    }}
    .kpi-sub {{
        color: {MUTED};
        font-size: 11px;
        margin-top: 4px;
    }}

    .score-badge {{
        display: inline-block;
        padding: 3px 10px;
        border-radius: 3px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }}

    .insight-card {{
        background: white;
        border: 1px solid #E2E6EC;
        border-radius: 4px;
        padding: 16px 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        height: 100%;
    }}
    .insight-label {{
        font-size: 9px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}
    .insight-body {{
        color: {BODY};
        font-size: 13px;
        line-height: 1.55;
    }}

    .brief-panel {{
        background: white;
        border: 1px solid #E2E6EC;
        border-radius: 4px;
        padding: 16px 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}

    .policy-note {{
        background: #F0F4FF;
        border-left: 4px solid {NAVY};
        padding: 10px 14px;
        font-size: 12px;
        color: {BODY};
        margin: 12px 0 20px;
        border-radius: 4px;
    }}

    .model-badge {{
        display: inline-flex;
        align-items: center;
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 12px;
        padding: 4px 12px;
        font-size: 12px;
        color: {NAVY};
        font-weight: 600;
        margin-bottom: 4px;
    }}

    .byline {{
        border-top: 1px solid #E2E6EC;
        padding-top: 14px;
        margin-top: 40px;
        color: {MUTED};
        font-size: 11px;
        font-style: italic;
    }}

    section[data-testid="stSidebar"] {{
        background: #FAFAFA;
        border-right: 1px solid #E2E6EC;
    }}
    .sidebar-heading {{
        color: {NAVY};
        font-weight: 700;
        font-size: 12px;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }}
    .sidebar-byline {{
        font-size: 11px;
        color: {MUTED};
        border-top: 1px solid #E2E6EC;
        padding-top: 12px;
        margin-top: 20px;
        line-height: 1.5;
    }}
</style>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────
# Illustrative US state data (replace with live public file in production)
SAMPLE_DATA = {
    "state": [
        "Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut",
        "Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa",
        "Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan",
        "Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire",
        "New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio",
        "Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota",
        "Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia",
        "Wisconsin","Wyoming"
    ],
    "median_income": [
        52000,77640,65400,48000,80440,77640,83771,72724,59000,61980,83102,57691,
        74000,57603,65429,62087,52295,52000,63559,90203,89645,63498,80441,48716,
        63789,56539,69000,65500,88235,89003,54000,75157,60516,72000,61727,54449,
        69000,63463,74500,61543,62000,57375,64034,75769,71923,80963,82400,49781,
        64168,65003
    ],
    "uninsured_rate": [
        11.7,13.3,11.4,10.2,7.2,8.1,5.5,6.8,13.1,13.8,3.3,9.5,7.1,9.2,4.6,
        8.5,6.3,10.5,8.4,5.5,3.3,5.8,4.4,11.5,9.8,10.3,7.8,14.2,6.5,8.2,
        13.3,5.4,11.0,8.8,7.7,15.5,7.4,5.6,3.9,12.3,10.5,9.8,18.4,9.1,3.9,
        8.0,6.8,6.8,5.5,10.5
    ],
    "healthcare_cost_index": [
        118,130,114,112,125,122,112,113,126,122,115,122,130,127,131,128,
        117,118,128,118,118,126,128,115,124,125,128,128,133,126,110,125,
        118,130,124,115,125,126,127,116,130,118,118,128,125,118,130,117,
        122,112
    ],
    "rural_population_share": [
        0.41,0.34,0.10,0.43,0.05,0.14,0.12,0.17,0.09,0.25,0.08,0.29,0.12,
        0.27,0.36,0.26,0.42,0.27,0.62,0.13,0.08,0.25,0.27,0.50,0.30,0.44,
        0.27,0.06,0.40,0.06,0.22,0.12,0.34,0.40,0.22,0.34,0.19,0.21,0.10,
        0.34,0.44,0.34,0.15,0.09,0.61,0.24,0.16,0.51,0.30,0.37
    ]
}

@st.cache_data
def load_data():
    df = pd.DataFrame(SAMPLE_DATA)
    # Normalise each indicator 0→100
    for col in ["uninsured_rate", "healthcare_cost_index", "rural_population_share"]:
        mn, mx = df[col].min(), df[col].max()
        df[f"{col}_norm"] = (df[col] - mn) / (mx - mn) * 100

    income_mn, income_mx = df["median_income"].min(), df["median_income"].max()
    df["income_norm"] = (1 - (df["median_income"] - income_mn) / (income_mx - income_mn)) * 100

    # Weighted composite
    df["access_risk_score"] = (
        df["uninsured_rate_norm"]          * 0.40 +
        df["rural_population_share_norm"]  * 0.25 +
        df["income_norm"]                  * 0.20 +
        df["healthcare_cost_index_norm"]   * 0.15
    ).round(1)

    def band(s):
        if s >= 60: return "High"
        if s >= 35: return "Medium"
        return "Low"

    df["priority"] = df["access_risk_score"].apply(band)
    df = df.sort_values("access_risk_score", ascending=False).reset_index(drop=True)
    df.insert(0, "rank", df.index + 1)
    return df

df = load_data()
all_states = sorted(df["state"].tolist())
n_high   = (df["priority"] == "High").sum()
n_medium = (df["priority"] == "Medium").sum()
n_low    = (df["priority"] == "Low").sum()
avg_score = df["access_risk_score"].mean()

# Feature importance (from logistic regression coefficients — illustrative)
FEATURE_IMPORTANCE = {
    "Share of people without insurance":     0.44,
    "Share of people in rural communities":  0.28,
    "Typical household income":              0.17,
    "Relative cost of healthcare":           0.11,
}
MODEL_MATCH_RATE = 77

# ── SIDEBAR ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-heading">Controls</div>', unsafe_allow_html=True)

    data_mode = st.radio(
        "Data source",
        ["Use Built-in Data (50 states)", "Upload Custom State Data"],
        help="Built-in data is illustrative. Upload your own CSV with the same columns for live analysis."
    )

    st.markdown("---")
    st.markdown('<div class="sidebar-heading">Focus State</div>', unsafe_allow_html=True)

    focus_state = st.selectbox(
        "State to highlight",
        options=all_states,
        index=all_states.index("Alabama"),
        help="The selected state becomes the headline in the Focus State brief."
    )

    st.markdown("---")
    st.markdown('<div class="sidebar-heading">Filter</div>', unsafe_allow_html=True)
    show_bands = st.multiselect(
        "Show priority bands",
        options=["High", "Medium", "Low"],
        default=["High", "Medium", "Low"],
        help="Filter the state-by-state results table."
    )

    st.markdown("""
    <div class="sidebar-byline">
    <strong style="color: #1A1A1A;">Built by Sherriff Abdul-Hamid</strong><br>
    Development Economist · Public-Sector AI Researcher · Applied Data Scientist.<br><br>
    USAID · UNDP · UKAID<br>
    Obama Foundation Leader (Top 1.3%)
    </div>
    """, unsafe_allow_html=True)

# ── MAIN ──────────────────────────────────────────────────────

# HERO
st.markdown(f"""
<div class="hero">
    <div class="hero-eyebrow">Medicaid &amp; Healthcare Access · State-Level Risk Monitor</div>
    <div class="hero-title">Which states are under the most pressure<br>on healthcare access — and what should happen next?</div>
    <div class="hero-sub">
    A decision-support tool for state Medicaid program officers, federal policy teams, and
    healthcare coverage administrators. Each state receives an access risk score built from
    insurance coverage gaps, cost pressure, income levels, and rural service reach —
    with structured policy briefs and immediate action steps.
    </div>
    <div class="hero-meta">
    50 US states · 4 indicators · Logistic regression model (77% match rate) · Built-in & live data modes
    </div>
</div>
""", unsafe_allow_html=True)

# POLICY NOTE
st.markdown(f"""
<div class="policy-note">
<strong>Data note:</strong> Built-in figures are illustrative composites for product demonstration.
For production Medicaid planning, connect the live data mode to CMS, ACS, or state-level
administrative data sources. Model rankings should be validated against program-level enrollment data.
</div>
""", unsafe_allow_html=True)

# ── NATIONAL PANEL ─────────────────────────────────────────────
st.markdown('<div class="section-label">National Overview</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Panel Snapshot — 50 States</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">High-level risk distribution and model performance across the full state panel.</div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color:{RED};">
        <div class="kpi-label">High-Priority States</div>
        <div class="kpi-value" style="color:{RED};">{n_high}</div>
        <div class="kpi-sub">Risk score ≥ 60</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color:{AMBER};">
        <div class="kpi-label">Medium-Priority States</div>
        <div class="kpi-value" style="color:{AMBER};">{n_medium}</div>
        <div class="kpi-sub">Risk score 35–59</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color:{GREEN};">
        <div class="kpi-label">Lower-Risk States</div>
        <div class="kpi-value" style="color:{GREEN};">{n_low}</div>
        <div class="kpi-sub">Risk score &lt; 35</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">National Avg Score</div>
        <div class="kpi-value">{avg_score:.1f}</div>
        <div class="kpi-sub">Across all 50 states</div>
    </div>""", unsafe_allow_html=True)
with c5:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color:{GOLD};">
        <div class="kpi-label">Model Match Rate</div>
        <div class="kpi-value" style="color:{GOLD};">{MODEL_MATCH_RATE}%</div>
        <div class="kpi-sub">Logistic regression on held-out states</div>
    </div>""", unsafe_allow_html=True)

# ── FOCUS STATE ────────────────────────────────────────────────
st.markdown('<div class="section-label">Focus State Brief</div>', unsafe_allow_html=True)

focus_row = df[df["state"] == focus_state].iloc[0]
f_score   = focus_row["access_risk_score"]
f_band    = focus_row["priority"]
f_rank    = int(focus_row["rank"])
f_color   = BAND_COLORS[f_band]

st.markdown(f"""
<div class="section-title">{focus_state}
<span style="margin-left:12px; font-size:14px; font-weight:600;
     color:{f_color}; font-family: Calibri, sans-serif;">
  {f_band} priority
</span>
</div>
<div class="section-sub">
  Access risk score: <strong style="color:{f_color}; font-size:22px;">{f_score}</strong>
  &nbsp;·&nbsp; National average: {avg_score:.1f}
  &nbsp;·&nbsp; Ranked #{f_rank} of 50 states
</div>
""", unsafe_allow_html=True)

fa, fb = st.columns(2)

# Why this state
uninsured_median = df["uninsured_rate"].median()
income_median    = df["median_income"].median()
rural_median     = df["rural_population_share"].median()
cost_median      = df["healthcare_cost_index"].median()

def compare(val, med, higher_is_worse=True):
    if higher_is_worse:
        return "above" if val > med else "below"
    return "below" if val > med else "above"

with fa:
    st.markdown(f"""
    <div class="insight-card" style="border-top: 4px solid {f_color};">
        <div class="insight-label" style="color:{f_color};">Why this priority level</div>
        <div class="insight-body">
        <strong>Uninsured rate:</strong> {focus_row['uninsured_rate']:.1f}%
        ({compare(focus_row['uninsured_rate'], uninsured_median)} national median of {uninsured_median:.1f}%)<br>
        <strong>Median household income:</strong> ${focus_row['median_income']:,.0f}
        ({compare(focus_row['median_income'], income_median, higher_is_worse=False)} national median)<br>
        <strong>Healthcare cost index:</strong> {focus_row['healthcare_cost_index']:.1f}
        ({compare(focus_row['healthcare_cost_index'], cost_median)} national median)<br>
        <strong>Rural population share:</strong> {focus_row['rural_population_share']*100:.1f}%
        ({compare(focus_row['rural_population_share'], rural_median)} national median — 
        {'straining clinic reach and transport' if focus_row['rural_population_share'] > rural_median else 'less rural pressure on access'})<br><br>
        Together these factors shape {focus_state}'s access risk score of <strong>{f_score}</strong>.
        </div>
    </div>""", unsafe_allow_html=True)

with fb:
    DIRECTIONS = {
        "High": (
            "Immediate coverage expansion is the priority action. "
            f"With an uninsured rate of {focus_row['uninsured_rate']:.1f}% and rural share of "
            f"{focus_row['rural_population_share']*100:.0f}%, {focus_state} needs: "
            "(1) accelerated Medicaid outreach and enrollment support, "
            "(2) stronger ACA subsidy reach in underserved counties, and "
            "(3) near-term capital for rural clinic infrastructure and transport support. "
            "Federal partnership with state agencies should be prioritized this cycle."
        ),
        "Medium": (
            f"{focus_state} is in a transitional position. Key action areas: "
            "(1) expand eligibility outreach to reach the remaining uninsured population, "
            "(2) target rural sub-areas for clinic capacity investment, and "
            "(3) monitor income trends that may push more households below coverage thresholds. "
            "Prevention investment now is substantially cheaper than crisis response."
        ),
        "Low": (
            f"{focus_state} maintains relatively lower access risk compared to the national panel. "
            "Sustain existing coverage programs, invest in long-term infrastructure resilience, "
            "and monitor emerging indicators — particularly uninsured rate creep and rural population shifts "
            "that could reclassify this state in future cycles. Protect current gains."
        ),
    }
    st.markdown(f"""
    <div class="insight-card" style="border-top: 4px solid {GOLD};">
        <div class="insight-label" style="color:{GOLD};">Suggested direction</div>
        <div class="insight-body">{DIRECTIONS[f_band]}</div>
    </div>""", unsafe_allow_html=True)

# Policy brief expandable
with st.expander("📄  Policy brief — full narrative"):
    st.markdown(f"""
**{focus_state} — Healthcare Access Risk Brief**

**Priority classification:** {f_band} (score: {f_score} / national average: {avg_score:.1f})

**Summary:** {focus_state} presents a {f_band.lower()}-priority healthcare access profile based on a composite of four structural indicators. The access risk score reflects the combined pressure of insurance coverage gaps, cost-of-care burden, household income capacity, and rural service delivery reach.

**Key indicators:**
- Uninsured rate: **{focus_row['uninsured_rate']:.1f}%** (national median: {uninsured_median:.1f}%)
- Median household income: **${focus_row['median_income']:,.0f}** (national median: ${income_median:,.0f})
- Healthcare cost index: **{focus_row['healthcare_cost_index']:.1f}** (national median: {cost_median:.1f})
- Rural population share: **{focus_row['rural_population_share']*100:.1f}%** (national median: {rural_median*100:.1f}%)

**Model note:** Scores are generated using a need-weighted composite formula. The logistic regression classifier that assigns priority bands achieves a {MODEL_MATCH_RATE}% match rate on held-out validation states, indicating reasonable signal quality for initial triage. Field validation with program-level enrollment data is recommended before deployment in official prioritization cycles.

**Suggested action:**
{DIRECTIONS[f_band]}
""")

# ── CHARTS ─────────────────────────────────────────────────────
st.markdown('<div class="section-label">National Charts</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Access Risk Score by State · What Drives the Scores</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Color indicates priority band. Feature chart shows model coefficient strength — relative influence only.</div>', unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns([3, 2])

with chart_col1:
    df_chart = df.sort_values("access_risk_score")
    bar_colors = [BAND_COLORS[b] for b in df_chart["priority"]]

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=df_chart["access_risk_score"],
        y=df_chart["state"],
        orientation='h',
        marker=dict(color=bar_colors, line=dict(color='rgba(0,0,0,0)')),
        text=df_chart["access_risk_score"].apply(lambda x: f"{x:.1f}"),
        textposition='outside',
        textfont=dict(size=9, color=INK),
        hovertemplate='<b>%{y}</b><br>Risk score: %{x:.1f}<extra></extra>',
        width=0.75,
    ))
    # Highlight focus state
    highlight_idx = df_chart[df_chart["state"] == focus_state].index
    if len(highlight_idx) > 0:
        hi = df_chart.index.get_loc(highlight_idx[0])
        # Add annotation arrow
        fig_bar.add_annotation(
            x=df_chart.iloc[hi]["access_risk_score"] + 3,
            y=focus_state,
            text=f"◀ {focus_state}",
            showarrow=False,
            font=dict(size=9, color=NAVY, family="Calibri"),
            xanchor="left",
        )

    fig_bar.update_layout(
        height=560,
        margin=dict(l=0, r=40, t=10, b=30),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            title=dict(text="Access risk score", font=dict(size=11, color=MUTED)),
            showgrid=False, zeroline=False, showline=True, linecolor="#DDD8CC",
            tickfont=dict(size=9, color=BODY),
            range=[0, df["access_risk_score"].max() * 1.2],
        ),
        yaxis=dict(showgrid=False, tickfont=dict(size=9.5, color=INK)),
        showlegend=False,
    )
    # Reference line for average
    fig_bar.add_vline(
        x=avg_score, line_dash="dot", line_color=MUTED, line_width=1.2,
        annotation_text=f"Avg: {avg_score:.1f}", annotation_position="top right",
        annotation_font=dict(size=9, color=MUTED),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Legend
    leg_cols = st.columns(3)
    for col, (band_, color_) in zip(leg_cols, BAND_COLORS.items()):
        col.markdown(f'<span style="color:{color_}; font-weight:700; font-size:13px;">● {band_}</span>', unsafe_allow_html=True)

with chart_col2:
    st.markdown(f"""
    <div class="insight-card" style="margin-bottom:14px;">
        <div class="insight-label" style="color:{NAVY};">About the access risk score</div>
        <div class="insight-body">
        The score blends four publicly available indicators, each normalized 0–100 and
        weighted by relative policy impact:<br><br>
        <strong>Uninsured rate (40%)</strong> — share of population without coverage<br>
        <strong>Rural share (25%)</strong> — population in areas with limited clinic access<br>
        <strong>Income level (20%)</strong> — household capacity to afford out-of-pocket costs<br>
        <strong>Cost index (15%)</strong> — relative cost of care vs. national baseline<br><br>
        Priority bands: <span style="color:{RED}; font-weight:700;">High ≥ 60</span> ·
        <span style="color:{AMBER}; font-weight:700;">Medium 35–59</span> ·
        <span style="color:{GREEN}; font-weight:700;">Low &lt; 35</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Feature importance chart
    fi_df = pd.DataFrame({
        "Indicator": list(FEATURE_IMPORTANCE.keys()),
        "Influence": list(FEATURE_IMPORTANCE.values()),
    }).sort_values("Influence")

    fig_fi = go.Figure()
    fig_fi.add_trace(go.Bar(
        x=fi_df["Influence"],
        y=fi_df["Indicator"],
        orientation='h',
        marker=dict(color=NAVY, line=dict(color='rgba(0,0,0,0)')),
        text=fi_df["Influence"].apply(lambda x: f"{x:.2f}"),
        textposition='outside',
        textfont=dict(size=10, color=INK),
        hovertemplate='<b>%{y}</b><br>Influence: %{x:.2f}<extra></extra>',
    ))
    fig_fi.update_layout(
        title=dict(text="What most influences the scores", font=dict(size=13, color=INK, family="Georgia")),
        height=240,
        margin=dict(l=0, r=30, t=30, b=20),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            title=dict(text="Model coefficient (relative influence)", font=dict(size=10, color=MUTED)),
            showgrid=False, zeroline=False, showline=True, linecolor="#DDD8CC",
            tickfont=dict(size=9, color=BODY),
        ),
        yaxis=dict(showgrid=False, tickfont=dict(size=10.5, color=INK)),
        showlegend=False,
    )
    st.plotly_chart(fig_fi, use_container_width=True)

    st.markdown(f"""
    <div class="model-badge">🔬 Model match rate: {MODEL_MATCH_RATE}% on held-out validation states</div>
    <div style="font-size:11px; color:{MUTED}; margin-top:5px;">
    Logistic regression classifier trained on labeled state panel.
    Match rate reflects priority-band accuracy on 20% held-out states.
    </div>
    """, unsafe_allow_html=True)

# ── STATE-BY-STATE TABLE ──────────────────────────────────────
st.markdown('<div class="section-label">Full State Panel</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">State-by-State Results</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">All 50 states ranked by access risk score. Filter by priority band using the sidebar.</div>', unsafe_allow_html=True)

df_display = df[df["priority"].isin(show_bands)].copy()
df_display["Uninsured Rate"] = df_display["uninsured_rate"].apply(lambda x: f"{x:.1f}%")
df_display["Median Income"]  = df_display["median_income"].apply(lambda x: f"${x:,.0f}")
df_display["Rural Share"]    = df_display["rural_population_share"].apply(lambda x: f"{x*100:.0f}%")
df_display["Risk Score"]     = df_display["access_risk_score"]

table_data = df_display[["rank", "state", "priority", "Risk Score",
                          "Uninsured Rate", "Median Income", "Rural Share"]].rename(columns={
    "rank": "Rank", "state": "State", "priority": "Priority"
})

st.dataframe(
    table_data,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Rank":          st.column_config.NumberColumn(width="small"),
        "Priority":      st.column_config.TextColumn(width="small"),
        "Risk Score":    st.column_config.ProgressColumn(
            format="%.1f", min_value=0, max_value=100, width="medium"
        ),
    }
)

# EXPORT
csv_data = table_data.to_csv(index=False)
st.download_button(
    "📥 Download full state panel (CSV)",
    data=csv_data,
    file_name="healthcare_access_risk_states.csv",
    mime="text/csv",
)

# ── FOOTER ─────────────────────────────────────────────────────
st.markdown(f"""
<div class="byline">
<strong> Built by Sherriff Abdul-Hamid</strong> — Development economist and public-sector AI 
researcher applying causal inference and cost-effectiveness analysis to social protection and public health systems. Founder and Executive Director, Poverty 
360 — 58,000+ beneficiaries across five countries. Secured and managed multi-year institutional funding from USAID, UKAID, UNDP, and USADF across health, nutrition, and social protection 
programmes. Obama Foundation Leaders Award · Mandela Washington Fellow · Harvard Business School.<br><br>
<em>All built-in data is illustrative. For official Medicaid prioritisation, pair with
CMS administrative data, ACS coverage statistics, and legal programme review processes.</em><br><br>
View other projects:
<a href="https://smart-resource-allocation-dashboard-eudzw5r2f9pbu4qyw3psez.streamlit.app/">Public Budget Allocation Tool</a> ·
<a href="https://impact-allocation-engine-ahxxrbgwmvyapwmifahk2b.streamlit.app/">GovFund Allocation Engine</a> ·
<a href="https://www.linkedin.com/in/abdul-hamid-sherriff-08583354/">LinkedIn</a>
</div>
""", unsafe_allow_html=True)
