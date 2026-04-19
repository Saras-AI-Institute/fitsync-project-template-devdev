import streamlit as st
from modules.processor import process_data
import pandas as pd

# Set the page configuration
st.set_page_config(layout="wide", page_title="FitSync")

# Title of the dashboard
st.title("FitSync - Personal Health Analytics")

# Add sidebar for filtering after the title
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    options=["Last 7 Days", "Last 30 Days", "All Time"],
    index=2
)
# Load and process data
st.write("Loading and processing data...")
df = process_data()

# Filter the data based on the selected time range
today = pd.to_datetime("today")

if time_range == "Last 7 Days":
    df = df[df['Date'] >= (today - pd.Timedelta(days=7))]
elif time_range == "Last 30 Days":
    df = df[df['Date'] >= (today - pd.Timedelta(days=30))]
# If "All Time", we use the full dataframe by default
# Calculate average metrics from the filtered data
average_steps = df['Steps'].mean()
average_sleep_hours = df['Sleep_Hours'].mean()
average_recovery_score = df['Recovery_Score'].mean()

# Display metrics in the respective columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Average Steps", value=f"{average_steps:.0f}", delta=None)

with col2:
    st.metric(label="Average Sleep Hours", value=f"{average_sleep_hours:.1f}", delta=None)

with col3:
    st.metric(label="Average Recovery Score", value=f"{average_recovery_score:.1f}", delta=None)

# Display data summary
st.write("### Data Summary")
st.dataframe(df.describe())

# Display the full processed dataset
st.write("### Processed Health Data")
st.dataframe(df)

# Add additional components and visualizations as needed
# Example: Plotting, insights, etc.

# Placeholder for future extensions and detailed insights
st.write("### Insights and Analysis")
st.info("Further analysis and visualizations can be added here.")