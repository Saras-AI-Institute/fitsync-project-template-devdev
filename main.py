import streamlit as st
import pandas as pd
from modules.processor import process_data

# Title
st.title("FitSync - Personal Health Analytics")
# ----------- PAGE CONFIG -----------
st.set_page_config(
    page_title="FitSync",
    layout="wide"
)

# Sidebar filter
st.sidebar.header("Filters")
# ----------- SESSION STATE -----------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

time_range = st.sidebar.selectbox(
    "Select time range",
    options=["last 7 days", "last 30 days", "all time"],
    index=2
)
# ----------- TOGGLE BUTTON -----------
col1, col2 = st.columns([6,1])
with col2:
    if st.button("🌙" if st.session_state.dark_mode else "☀️"):
        st.session_state.dark_mode = not st.session_state.dark_mode

# Load data
df = process_data()
# ----------- THEME COLORS -----------
if st.session_state.dark_mode:
    bg_color = "#0E1117"
    text_color = "#FFFFFF"
    card_color = "#1c1f26"
    border_color = "#333"
    heading_color = "#00C9A7"
    sidebar_bg = "#161A22"
else:
    bg_color = "#F9F9F9"
    text_color = "#000000"
    card_color = "#FFFFFF"
    border_color = "#DDD"
    heading_color = "#007ACC"
    sidebar_bg = "#EAECEF"

# Filter by Date
if 'Date' in df.columns:
    if time_range == "last 7 days":
        df = df[df['Date'] >= (df['Date'].max() - pd.Timedelta(days=7))]
    elif time_range == "last 30 days":
        df = df[df['Date'] >= (df['Date'].max() - pd.Timedelta(days=30))]
# ----------- GLOBAL CSS -----------
st.markdown(f"""
    <style>
        /* App background */
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}

# Metrics
average_steps = df['Steps'].mean()
average_sleep_hours = df['Sleep_hours'].mean()
average_recovery_score = df['Recovery_Score'].mean()
        /* Sidebar background */
        section[data-testid="stSidebar"] {{
            background-color: {sidebar_bg};
        }}

# Columns
col1, col2, col3 = st.columns(3)
        /* ✅ FIX: Sidebar text visible */
        section[data-testid="stSidebar"] * {{
            color: {text_color} !important;
        }}

with col1:
    st.metric("Average Steps", f"{average_steps:.0f}")
        /* Text */
        h1, h2, h3, h4, h5, h6, p, div, span, label {{
            color: {text_color} !important;
        }}

with col2:
    st.metric("Average Sleep Hours", f"{average_sleep_hours:.1f}")
        /* Cards */
        .card {{
            background-color: {card_color};
            padding: 20px;
            border-radius: 15px;
            border: 1px solid {border_color};
            margin-bottom: 15px;
        }}

        /* Button */
        .stButton>button {{
            background-color: {heading_color};
            color: {"black" if st.session_state.dark_mode else "white"};
            border-radius: 10px;
            padding: 8px 16px;
            border: none;
        }}

        .stButton>button:hover {{
            opacity: 0.85;
        }}

        /* Info box */
        .stAlert {{
            background-color: {card_color};
            color: {text_color};
            border: 1px solid {border_color};
        }}
    </style>
""", unsafe_allow_html=True)

# ----------- MAIN CONTENT -----------
st.title("💪 Welcome to FitSync")

st.markdown("""
<div class="card">
    <h3>Your Personal Health Analytics Dashboard</h3>
    <p>Track your fitness, monitor your health, and stay consistent with your goals.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <h4>🚀 Features</h4>
    <ul>
        <li>📊 Health Data Tracking</li>
        <li>📈 Progress Visualization</li>
        <li>🤖 AI-Based Insights</li>
        <li>🎯 Goal Setting</li>
    </ul>
</div>
""", unsafe_allow_html=True)

with col3:
    st.metric("Average Recovery Score", f"{average_recovery_score:.1f}")
st.info("👉 Use the sidebar to navigate between different sections") 

# Table
st.write("## Processed Health Data")
st.dataframe(df)