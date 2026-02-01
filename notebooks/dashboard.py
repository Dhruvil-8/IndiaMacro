"""
India Macro Research Dashboard V2 (Institutional Grade)
=====================================================
A "Master Control Room" for monitoring:
1. Nowcast (FCI) - Real-time Stress
2. Flows (Liquidity) - Structural Trends
3. Monetary (Credit) - Future Cycle
4. Regimes & Signals - Actionable Alpha

Run: streamlit run notebooks/dashboard_v2.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# --- Configuration ---
st.set_page_config(
    page_title="India Macro Alpha | Institutional",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Hedge Fund" Look
st.markdown("""
<style>
    .metric-card {
        background-color: #0e1117;
        border: 1px solid #30333d;
        border-radius: 5px;
        padding: 15px;
        text-align: center;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #f0f2f6;
    }
    .metric-label {
        font-size: 14px;
        color: #8b92a5;
    }
</style>
""", unsafe_allow_html=True)

DATA_PATH = Path("data_processed")

# --- Data Loading ---
@st.cache_data(ttl=3600)
def load_data():
    data = {}
    files = {
        "regimes": "macro_regime_states.parquet",
        "flows": "flow_regime_monthly.parquet",
        "fci": "india_fci_weekly.parquet",
        "monetary": "india_monetary_monthly.parquet",
        "signals": "rule_signals.parquet",
        "sectors": "sector_regime_performance.parquet"
    }
    
    for key, filename in files.items():
        path = DATA_PATH / filename
        if path.exists():
            try:
                data[key] = pd.read_parquet(path)
            except Exception as e:
                st.warning(f"Could not load {filename}: {e}")
    return data

data = load_data()

# --- Sidebar ---
st.sidebar.title("🏛️ Alpha Control")
st.sidebar.markdown("---")
view_mode = st.sidebar.radio("View Mode", ["Master Dashboard", "Deep Dive: Flows", "Deep Dive: Monetary", "Deep Dive: Stress"])
st.sidebar.markdown("---")
st.sidebar.info(f"Last Updated: {pd.Timestamp.now().strftime('%Y-%m-%d')}")

# --- Helper Functions ---
def render_metric(label, value, delta=None, color=None):
    delta_html = ""
    if delta is not None:
        delta_color = "#2ecc71" if delta > 0 else "#e74c3c" if delta < 0 else "#95a5a6"
        delta_symbol = "▲" if delta > 0 else "▼" if delta < 0 else "−"
        delta_html = f"<span style='color:{delta_color}; font-size:12px;'>{delta_symbol} {abs(delta):.2f}</span>"
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="color:{color if color else '#f0f2f6'}">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def gauge_chart(value, title, min_val=-3, max_val=3):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': title},
        gauge = {
            'axis': {'range': [min_val, max_val], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "white", 'thickness': 0.2},
            'bgcolor': "black",
            'steps': [
                {'range': [min_val, -1], 'color': '#2ecc71'}, # Loose/Bullish
                {'range': [-1, 1], 'color': '#f39c12'},   # Neutral
                {'range': [1, max_val], 'color': '#e74c3c'}    # Tight/Bearish
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
    return fig

# --- Main Dashboard ---
if view_mode == "Master Dashboard":
    st.title("🦅 India Macro: Institutional View")
    
    # --- Top Deck: The NOW (FCI & Regimes) ---
    col1, col2, col3, col4 = st.columns(4)
    
    if "fci" in data and not data["fci"].empty:
        fci_curr = data["fci"].iloc[-1]
        fci_z = fci_curr.get("FCI_COMPOSITE_Z", 0)
        fci_color = "#2ecc71" if fci_z < -1 else "#e74c3c" if fci_z > 1 else "#f39c12"
        with col1:
            render_metric("Financial Conditions (FCI)", f"{fci_z:.2f} σ", color=fci_color)
    
    if "flows" in data and not data["flows"].empty:
        flow_curr = data["flows"].iloc[-1]
        flow_z = flow_curr.get("FPI_NET_USD_ZSCORE", 0)
        with col2:
            render_metric("FII Flow Liquidty", f"{flow_z:.2f} σ", delta=flow_z - data["flows"].iloc[-2].get("FPI_NET_USD_ZSCORE", 0))

    if "monetary" in data and not data["monetary"].empty:
        mon_curr = data["monetary"].iloc[-1]
        impulse = mon_curr.get("CREDIT_IMPULSE", 0)
        with col3:
            render_metric("Credit Impulse", f"{impulse:.2f}%")

    if "regimes" in data and not data["regimes"].empty:
        curr_regime = data["regimes"]["COMPOSITE"].iloc[-1]
        regime_colors = {"Goldilocks": "#2ecc71", "Reflation": "#f39c12", "Stagflation": "#e74c3c", "Deflation": "#3498db"}
        with col4:
             st.markdown(f"""
            <div class="metric-card" style="border-color: {regime_colors.get(curr_regime, '#95a5a6')};">
                <div class="metric-label">Macro Regime</div>
                <div class="metric-value" style="color: {regime_colors.get(curr_regime, '#95a5a6')};">{curr_regime}</div>
            </div>
            """, unsafe_allow_html=True)

    # --- Row 2: Charts ---
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.subheader("Financial Stress Gauge")
        if "fci" in data:
            st.plotly_chart(gauge_chart(fci_z, "FCI Z-Score (Higher = Stress)"), use_container_width=True)
            
    with c2:
        st.subheader("Structural Flows (The Tide)")
        if "flows" in data:
            flow_df = data["flows"].reset_index()
            fig = px.area(flow_df, x="Date", y="FPI_NET_USD_ZSCORE", title="FII Liquidity Z-Score (3Y Rolling)", color_discrete_sequence=["#3498db"])
            fig.add_hline(y=0, line_dash="dash", line_color="white")
            st.plotly_chart(fig, use_container_width=True)

    # --- Row 3: Monetary Plumbing ---
    st.divider()
    st.subheader("🏦 Monetary Plumbing & Credit Cycle")
    
    mc1, mc2 = st.columns(2)
    if "monetary" in data:
        mon_df = data["monetary"].reset_index()
        
        with mc1:
            fig_impulse = go.Figure()
            fig_impulse.add_trace(go.Bar(x=mon_df['Date'], y=mon_df['CREDIT_IMPULSE'], name='Credit Impulse', marker_color='#9b59b6'))
            fig_impulse.update_layout(title="Credit Impulse (Change in New Lending)", yaxis_title="% of Credit Stock")
            st.plotly_chart(fig_impulse, use_container_width=True)
            
        with mc2:
            fig_mult = px.line(mon_df, x='Date', y='MONEY_MULTIPLIER', title="Money Multiplier (M3 / M0)", color_discrete_sequence=["#e67e22"])
            st.plotly_chart(fig_mult, use_container_width=True)

elif view_mode == "Deep Dive: Flows":
    st.header("🌊 Structural Liquidity Flows")
    if "flows" in data:
        st.dataframe(data["flows"].sort_index(ascending=False).head(20), use_container_width=True)
        
        flow_df = data["flows"].reset_index()
        fig = px.bar(flow_df, x='Date', y=['FDI_NET_USD', 'FPI_NET_USD'], barmode='group', title="Net Inflows (USD Millions)")
        st.plotly_chart(fig, use_container_width=True)

elif view_mode == "Deep Dive: Monetary":
    st.header("🏦 Monetary & Banking Analytics")
    if "monetary" in data:
        st.write("Monetary Plumbing Metrics:")
        st.dataframe(data["monetary"].sort_index(ascending=False).head(20), use_container_width=True)
        
        mon_df = data["monetary"].reset_index()
        
        # Chart 1: Fiscal Dominance
        fig_fiscal = px.line(mon_df, x='Date', y='FISCAL_DOMINANCE_RATIO', title="Fiscal Dominance: RBI Credit to Govt vs Private Sector", color_discrete_sequence=["#e74c3c"])
        st.plotly_chart(fig_fiscal, use_container_width=True)
        
        # Chart 2: Money Multiplier vs CD Ratio
        fig_bank = go.Figure()
        fig_bank.add_trace(go.Scatter(x=mon_df['Date'], y=mon_df['MONEY_MULTIPLIER'], name='Money Multiplier', yaxis='y1'))
        fig_bank.add_trace(go.Scatter(x=mon_df['Date'], y=mon_df['CD_RATIO'], name='Credit-Deposit Ratio', yaxis='y2', line=dict(dash='dash')))
        fig_bank.update_layout(
            title="Banking Efficiency & Tightness",
            yaxis=dict(title="Money Multiplier"),
            yaxis2=dict(title="CD Ratio (%)", overlaying='y', side='right')
        )
        st.plotly_chart(fig_bank, use_container_width=True)

elif view_mode == "Deep Dive: Stress":
    st.header("🔥 Financial Conditions & Stress")
    if "fci" in data:
        st.write("Components of FCI:")
        st.dataframe(data["fci"].sort_index(ascending=False).head(20), use_container_width=True)
        
        fci_df = data["fci"].reset_index()
        fig = px.line(fci_df, x='Date', y=['FCI_COMPOSITE_Z', 'GSEC_Z', 'FX_Z', 'FX_VOL_Z'], title="Stress Components Z-Scores")
        st.plotly_chart(fig, use_container_width=True)

else:
    st.write("Select a module from the sidebar.")
