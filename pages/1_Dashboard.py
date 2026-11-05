import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.processor import process_data
from modules.theme import init_theme, render_theme_toggle, apply_custom_css, style_plotly_chart, get_current_theme

# Page Configuration
st.set_page_config(
    page_title="FitSync — Health Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize theme and custom CSS
init_theme()
apply_custom_css()
render_theme_toggle()
theme = get_current_theme()

# --- CACHED DATA PIPELINE ---
@st.cache_data
def get_cached_health_data():
    """
    Loads and caches processed health data to optimize UI responsiveness.
    """
    return process_data()

# Ensure we operate on a copy to prevent mutating cached state
full_df = get_cached_health_data().copy()

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Filters")

time_range = st.sidebar.selectbox(
    "Select Time Window",
    options=["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"],
    index=1
)

# Filter dataset
df = full_df.copy()
if 'Date' in df.columns and not df.empty:
    max_date = df['Date'].max()
    if time_range == "Last 7 Days":
        df = df[df['Date'] >= (max_date - pd.Timedelta(days=7))].copy()
    elif time_range == "Last 30 Days":
        df = df[df['Date'] >= (max_date - pd.Timedelta(days=30))].copy()
    elif time_range == "Last 90 Days":
        df = df[df['Date'] >= (max_date - pd.Timedelta(days=90))].copy()
    
    df = df.sort_values('Date').reset_index(drop=True)

st.sidebar.caption(f"Showing **{len(df)}** records for **{time_range}**")

# --- HEADER SECTION ---
st.title("📊 Primary Health Dashboard")
st.markdown(
    f"Monitor your core daily biometric indicators, recovery status, and trends for **{time_range}**."
)

# --- KPI METRICS ---
col1, col2, col3, col4 = st.columns(4)

avg_steps = df['Steps'].mean() if not df.empty else 0
avg_sleep = df['Sleep_Hours'].mean() if not df.empty else 0
avg_hr = df['Heart_Rate_bpm'].mean() if not df.empty else 0
avg_recovery = df['Recovery_Score'].mean() if not df.empty else 0

# Baseline comparisons
step_delta = avg_steps - 10000
sleep_delta = avg_sleep - 7.5
hr_delta = 70.0 - avg_hr  # Lower is generally better

with col1:
    st.metric(
        label="Average Daily Steps",
        value=f"{avg_steps:,.0f}",
        delta=f"{step_delta:+,.0f} vs 10k Goal"
    )

with col2:
    st.metric(
        label="Average Sleep Hours",
        value=f"{avg_sleep:.1f} hrs",
        delta=f"{sleep_delta:+.1f} hrs vs 7.5h Target"
    )

with col3:
    st.metric(
        label="Avg Resting Heart Rate",
        value=f"{avg_hr:.1f} bpm",
        delta=f"{hr_delta:+.1f} bpm (vs 70 avg)"
    )

with col4:
    recovery_status = "Optimal" if avg_recovery >= 75 else "Moderate" if avg_recovery >= 55 else "Needs Rest"
    st.metric(
        label="Avg Recovery Score",
        value=f"{avg_recovery:.1f} / 100",
        delta=f"Status: {recovery_status}"
    )

st.markdown("---")

# --- PLOTLY CHARTS ---
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📈 Recovery Score & Sleep Duration Trend")
    
    # Dual-axis line chart
    fig_trend = go.Figure()

    # Recovery Score Trace
    fig_trend.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Recovery_Score'],
        name="Recovery Score",
        mode='lines+markers',
        line=dict(color=theme['primary'], width=2.5),
        marker=dict(size=5),
        yaxis="y1"
    ))

    # Sleep Hours Trace
    fig_trend.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Sleep_Hours'],
        name="Sleep Hours",
        mode='lines+markers',
        line=dict(color=theme['secondary'], width=2, dash='dot'),
        marker=dict(size=4),
        yaxis="y2"
    ))

    fig_trend.update_layout(
        yaxis=dict(
            title="Recovery Score (0-100)",
            range=[0, 105],
            titlefont=dict(color=theme['primary']),
            tickfont=dict(color=theme['primary'])
        ),
        yaxis2=dict(
            title="Sleep Hours (hrs)",
            overlaying="y",
            side="right",
            range=[3, 11],
            titlefont=dict(color=theme['secondary']),
            tickfont=dict(color=theme['secondary'])
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    style_plotly_chart(fig_trend)
    st.plotly_chart(fig_trend, use_container_width=True)

with chart_col2:
    st.subheader("🎯 Recovery Score vs. Daily Steps")
    
    fig_scatter = px.scatter(
        df,
        x="Steps",
        y="Recovery_Score",
        color="Heart_Rate_bpm",
        size="Active_Minutes",
        hover_data=["Date", "Sleep_Hours", "Calories_Burned"],
        labels={
            "Steps": "Daily Steps",
            "Recovery_Score": "Recovery Score",
            "Heart_Rate_bpm": "Heart Rate (bpm)",
            "Active_Minutes": "Active Mins"
        },
        color_continuous_scale="Viridis",
        title="Activity Intensity vs Body Recovery"
    )
    style_plotly_chart(fig_scatter)
    st.plotly_chart(fig_scatter, use_container_width=True)

# Secondary row of insights
sec_col1, sec_col2 = st.columns(2)

with sec_col1:
    st.subheader("🔥 Daily Energy Expenditure & Active Time")
    fig_energy = px.bar(
        df,
        x="Date",
        y="Calories_Burned",
        color="Active_Minutes",
        color_continuous_scale="Tealgrn",
        labels={"Calories_Burned": "Calories Burned (kcal)", "Active_Minutes": "Active Minutes"},
        title="Calories Burned & Active Minutes"
    )
    style_plotly_chart(fig_energy)
    st.plotly_chart(fig_energy, use_container_width=True)

with sec_col2:
    st.subheader("❤️ Resting Heart Rate Distribution")
    fig_hr = px.histogram(
        df,
        x="Heart_Rate_bpm",
        nbins=15,
        marginal="box",
        color_discrete_sequence=[theme['primary']],
        labels={"Heart_Rate_bpm": "Heart Rate (bpm)"},
        title="Distribution of Daily Resting Heart Rate"
    )
    style_plotly_chart(fig_hr)
    st.plotly_chart(fig_hr, use_container_width=True)

# --- FILTERED DATA TABLE & DOWNLOAD ---
st.markdown("### 📥 Filtered Records & Export")
with st.expander("View Filtered Data Table", expanded=False):
    st.dataframe(
        df.style.format({
            "Steps": "{:.0f}",
            "Sleep_Hours": "{:.1f}",
            "Heart_Rate_bpm": "{:.1f}",
            "Calories_Burned": "{:.0f}",
            "Active_Minutes": "{:.0f}",
            "Recovery_Score": "{:.0f}"
        }),
        use_container_width=True
    )
    
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv_data,
        file_name=f"fitsync_data_{time_range.lower().replace(' ', '_')}.csv",
        mime="text/csv"
    )
