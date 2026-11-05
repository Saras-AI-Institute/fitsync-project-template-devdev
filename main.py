import streamlit as st
import pandas as pd
from modules.processor import process_data
from modules.theme import init_theme, render_theme_toggle, apply_custom_css, get_current_theme

# Page Configuration
st.set_page_config(
    page_title="FitSync — Personal Health Analytics",
    page_icon="🔶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize theme and inject custom CSS
init_theme()
apply_custom_css()
render_theme_toggle()

# Cached data loader
@st.cache_data
def get_cached_data():
    return process_data()

try:
    df = get_cached_data().copy()
    data_loaded = True
except Exception as e:
    df = pd.DataFrame()
    data_loaded = False
    load_error = str(e)

theme = get_current_theme()

# --- HERO SECTION ---
st.markdown(f"""
<div class="hero-container">
    <span class="hero-badge">🔶 AI-POWERED HEALTH INTELLIGENCE</span>
    <h1 class="hero-title">FitSync — Personal Health Analytics</h1>
    <p class="hero-subtitle">
        Empowering individuals to unlock meaningful patterns from wearable fitness tracking.
        FitSync cleanses raw telemetry, derives a multi-factor <strong>Recovery Score</strong>,
        and provides interactive visual intelligence on sleep, activity, and cardiovascular strain.
    </p>
</div>
""", unsafe_allow_html=True)

# --- QUICK STATS SUMMARY BAR ---
if data_loaded and not df.empty:
    total_days = len(df)
    avg_steps = df['Steps'].mean()
    avg_sleep = df['Sleep_Hours'].mean()
    avg_recovery = df['Recovery_Score'].mean()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">Monitored Window</div>
            <div class="kpi-value">{total_days} Days</div>
            <div class="kpi-subtitle">Continuous synthetic tracking</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">Average Daily Steps</div>
            <div class="kpi-value">{avg_steps:,.0f}</div>
            <div class="kpi-subtitle">Target: 10,000 steps/day</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">Average Sleep Hours</div>
            <div class="kpi-value">{avg_sleep:.1f} hrs</div>
            <div class="kpi-subtitle">Recommended: 7.0 - 9.0 hrs</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">Mean Recovery Score</div>
            <div class="kpi-value">{avg_recovery:.1f}<span style="font-size: 1rem; font-weight: 500; color:{theme['text_muted']};">/100</span></div>
            <div class="kpi-subtitle">Composite physical readiness</div>
        </div>
        """, unsafe_allow_html=True)

# --- CORE FEATURES GRID ---
st.markdown("### 🚀 Core Platform Features")
feat_col1, feat_col2, feat_col3 = st.columns(3)

with feat_col1:
    st.markdown("""
    <div class="custom-card">
        <div class="card-icon">📊</div>
        <h3 class="card-title">Dynamic KPI Dashboard</h3>
        <p class="card-body">
            Examine key performance indicators including steps, sleep, resting heart rate, and recovery score across 7-day, 30-day, and all-time interactive windows.
        </p>
    </div>
    """, unsafe_allow_html=True)

with feat_col2:
    st.markdown("""
    <div class="custom-card">
        <div class="card-icon">🧠</div>
        <h3 class="card-title">Algorithmic Recovery</h3>
        <p class="card-body">
            Computes physiological readiness using a multi-factor algorithm combining sleep sufficiency, resting cardiac rate, and step distribution.
        </p>
    </div>
    """, unsafe_allow_html=True)

with feat_col3:
    st.markdown("""
    <div class="custom-card">
        <div class="card-icon">📈</div>
        <h3 class="card-title">Statistical Trends & EDA</h3>
        <p class="card-body">
            Explore metric distributions, monthly recovery aggregations, and correlation matrices rendered with responsive Plotly visualizations.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- HOW IT WORKS (3-STEP PIPELINE) ---
st.markdown("### ⚙️ How FitSync Works")
step_col1, step_col2, step_col3 = st.columns(3)

with step_col1:
    st.markdown("""
    <div class="custom-card">
        <div style="display:flex; align-items:center; margin-bottom: 8px;">
            <span class="step-badge">1</span>
            <strong style="font-size: 1.05rem;">Data Imputation</strong>
        </div>
        <p class="card-body">
            Loads daily biometric CSV logs and replaces missing sensor data using statistical medians and clinical baseline anchors.
        </p>
    </div>
    """, unsafe_allow_html=True)

with step_col2:
    st.markdown("""
    <div class="custom-card">
        <div style="display:flex; align-items:center; margin-bottom: 8px;">
            <span class="step-badge">2</span>
            <strong style="font-size: 1.05rem;">Score Computation</strong>
        </div>
        <p class="card-body">
            Applies tiered scoring weights to evaluate sleep quantity, resting heart rate, and optimal step ranges clamped strictly to 0-100.
        </p>
    </div>
    """, unsafe_allow_html=True)

with step_col3:
    st.markdown("""
    <div class="custom-card">
        <div style="display:flex; align-items:center; margin-bottom: 8px;">
            <span class="step-badge">3</span>
            <strong style="font-size: 1.05rem;">Interactive Exploration</strong>
        </div>
        <p class="card-body">
            Presents findings through high-performance cached Streamlit pages with customizable filters and theme toggling.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- DATA PREVIEW SECTION ---
st.markdown("### 📋 Processed Telemetry Preview")
if data_loaded and not df.empty:
    with st.expander("🔍 Click to inspect processed dataset (First 10 records)", expanded=True):
        st.dataframe(
            df.head(10).style.format({
                "Steps": "{:.0f}",
                "Sleep_Hours": "{:.1f}",
                "Heart_Rate_bpm": "{:.1f}",
                "Calories_Burned": "{:.0f}",
                "Active_Minutes": "{:.0f}",
                "Recovery_Score": "{:.0f}"
            }),
            use_container_width=True
        )
        st.caption(f"Displaying 10 of {len(df)} cleaned and scored records.")
else:
    st.error(f"Unable to load data/health_data.csv: {load_error if 'load_error' in locals() else 'File not found'}. Run `python generate_data.py` to create the dataset.")

# --- CALL TO ACTION ---
st.markdown("---")
cta_col1, cta_col2 = st.columns([3, 1])
with cta_col1:
    st.info("👈 **Ready to explore?** Select **1_Dashboard** or **2_Trends** from the sidebar navigation to analyze your biometrics!")
with cta_col2:
    st.caption("Built for Saras AI Institute • Code with AI")
