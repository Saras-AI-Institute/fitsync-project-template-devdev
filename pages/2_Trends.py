import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from modules.processor import process_data
from modules.theme import init_theme, render_theme_toggle, apply_custom_css, style_plotly_chart, get_current_theme

# Page Configuration
st.set_page_config(
    page_title="FitSync — Trends & Analytics",
    page_icon="📈",
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
    Loads and caches processed health data for fast page switching.
    """
    return process_data()

full_df = get_cached_health_data().copy()

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Trends Filters")
time_range = st.sidebar.selectbox(
    "Select Time Window",
    options=["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"],
    index=3  # Default to All Time for macro statistical trends
)

# Copy dataframe before applying filter
filtered_df = full_df.copy()
if 'Date' in filtered_df.columns and not filtered_df.empty:
    max_date = filtered_df['Date'].max()
    if time_range == "Last 7 Days":
        filtered_df = filtered_df[filtered_df['Date'] >= (max_date - pd.Timedelta(days=7))].copy()
    elif time_range == "Last 30 Days":
        filtered_df = filtered_df[filtered_df['Date'] >= (max_date - pd.Timedelta(days=30))].copy()
    elif time_range == "Last 90 Days":
        filtered_df = filtered_df[filtered_df['Date'] >= (max_date - pd.Timedelta(days=90))].copy()

    filtered_df = filtered_df.sort_values('Date').reset_index(drop=True)

st.sidebar.caption(f"Analyzing **{len(filtered_df)}** days of records")

# --- HEADER SECTION ---
st.title("📈 Long-Term Trends & Statistical Analysis")
st.markdown(
    f"In-depth exploratory data analysis and distribution modeling for **{time_range}**."
)

# --- SUMMARY STATISTICS SECTION ---
st.subheader("📊 Summary Statistics")
summary_cols = ['Steps', 'Sleep_Hours', 'Heart_Rate_bpm', 'Calories_Burned', 'Active_Minutes', 'Recovery_Score']
valid_summary_cols = [c for c in summary_cols if c in filtered_df.columns]

if not filtered_df.empty and valid_summary_cols:
    stats_df = filtered_df[valid_summary_cols].describe().T
    stats_df = stats_df[['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']]
    st.dataframe(
        stats_df.style.format({
            'count': '{:.0f}',
            'mean': '{:.1f}',
            'std': '{:.1f}',
            'min': '{:.1f}',
            '25%': '{:.1f}',
            '50%': '{:.1f}',
            '75%': '{:.1f}',
            'max': '{:.1f}'
        }),
        use_container_width=True
    )

st.markdown("---")

# --- DISTRIBUTIONS SECTION ---
st.subheader("📊 Metric Distributions")
col_dist1, col_dist2 = st.columns(2)

with col_dist1:
    fig_steps = px.histogram(
        filtered_df,
        x="Steps",
        nbins=20,
        marginal="rug",
        color_discrete_sequence=[theme['primary']],
        title="Distribution of Daily Step Counts",
        labels={"Steps": "Steps"}
    )
    # Add mean line
    mean_steps = filtered_df['Steps'].mean()
    fig_steps.add_vline(
        x=mean_steps,
        line_dash="dash",
        line_color=theme['secondary'],
        annotation_text=f"Mean: {mean_steps:,.0f}",
        annotation_position="top right"
    )
    style_plotly_chart(fig_steps)
    st.plotly_chart(fig_steps, use_container_width=True)

with col_dist2:
    fig_cal = px.histogram(
        filtered_df,
        x="Calories_Burned",
        nbins=20,
        marginal="rug",
        color_discrete_sequence=[theme['secondary']],
        title="Distribution of Calories Burned (kcal)",
        labels={"Calories_Burned": "Calories Burned"}
    )
    mean_cal = filtered_df['Calories_Burned'].mean()
    fig_cal.add_vline(
        x=mean_cal,
        line_dash="dash",
        line_color=theme['primary'],
        annotation_text=f"Mean: {mean_cal:,.0f}",
        annotation_position="top right"
    )
    style_plotly_chart(fig_cal)
    st.plotly_chart(fig_cal, use_container_width=True)

st.markdown("---")

# --- LONGITUDINAL TRENDS & AGGREGATIONS ---
col_trend1, col_trend2 = st.columns(2)

with col_trend1:
    st.subheader("😴 Sleep Duration Longitudinal Trend")
    fig_sleep = px.line(
        filtered_df,
        x="Date",
        y="Sleep_Hours",
        title="Daily Sleep Duration Over Time",
        markers=True,
        labels={"Sleep_Hours": "Sleep Hours (hrs)", "Date": "Date"}
    )
    fig_sleep.update_traces(line_color=theme['primary'])
    # Baseline benchmark line
    fig_sleep.add_hline(
        y=7.0,
        line_dash="dash",
        line_color="#E056FD",
        annotation_text="7.0h Baseline",
        annotation_position="bottom right"
    )
    style_plotly_chart(fig_sleep)
    st.plotly_chart(fig_sleep, use_container_width=True)

with col_trend2:
    st.subheader("🗓️ Average Recovery Score by Month")
    if 'Date' in filtered_df.columns and len(filtered_df) > 1:
        # String conversion to prevent JSON serialization errors
        trend_copy = filtered_df.copy()
        trend_copy["Month"] = trend_copy["Date"].dt.to_period("M").astype(str)
        monthly_avg = (
            trend_copy.groupby("Month")["Recovery_Score"]
            .mean()
            .reset_index()
        )
        fig_month = px.bar(
            monthly_avg,
            x="Month",
            y="Recovery_Score",
            title="Monthly Mean Recovery Score",
            text_auto=".1f",
            color="Recovery_Score",
            color_continuous_scale="Teal",
            labels={"Recovery_Score": "Avg Recovery Score", "Month": "Month"}
        )
        style_plotly_chart(fig_month)
        st.plotly_chart(fig_month, use_container_width=True)
    else:
        st.info("Insufficient date span for monthly breakdown.")

st.markdown("---")

# --- ADVANCED STATISTICAL INSIGHTS ---
col_stat1, col_stat2 = st.columns(2)

with col_stat1:
    st.subheader("🔥 Metric Correlation Heatmap")
    corr_cols = [c for c in ['Steps', 'Sleep_Hours', 'Heart_Rate_bpm', 'Calories_Burned', 'Active_Minutes', 'Recovery_Score'] if c in filtered_df.columns]
    if len(corr_cols) > 1 and len(filtered_df) > 2:
        corr_matrix = filtered_df[corr_cols].corr()
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
            title="Pearson Correlation Matrix",
            labels=dict(color="Correlation")
        )
        style_plotly_chart(fig_corr)
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.info("Not enough data points for correlation matrix.")

with col_stat2:
    st.subheader("📅 Day of the Week Performance")
    if 'Date' in filtered_df.columns and len(filtered_df) >= 7:
        dow_df = filtered_df.copy()
        dow_df['Day_of_Week'] = dow_df['Date'].dt.day_name()
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dow_avg = dow_df.groupby('Day_of_Week')[['Steps', 'Recovery_Score']].mean().reindex(days_order).reset_index()
        
        fig_dow = go.Figure()
        fig_dow.add_trace(go.Bar(
            x=dow_avg['Day_of_Week'],
            y=dow_avg['Recovery_Score'],
            name="Avg Recovery Score",
            marker_color=theme['primary']
        ))
        fig_dow.update_layout(
            title="Mean Recovery Score by Day of Week",
            xaxis_title="Day of Week",
            yaxis_title="Recovery Score (0-100)",
            yaxis=dict(range=[0, 100])
        )
        style_plotly_chart(fig_dow)
        st.plotly_chart(fig_dow, use_container_width=True)
    else:
        st.info("Need at least 7 days of data for day-of-week breakdown.")
