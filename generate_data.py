
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Start date
start_date = datetime(2025, 1, 1)

# Generate 365 dates
dates = [start_date + timedelta(days=i) for i in range(365)]

# Realistic data generation
np.random.seed(0)  # For reproducibility

# Steps: normal distribution around 8500, clipped between 3000 and 18000
steps = np.clip(np.random.normal(loc=8500, scale=1500, size=365), 3000, 18000)

# Sleep Hours: normal distribution around 7.2, clipped between 4.5 and 9.5
sleep_hours = np.clip(np.random.normal(loc=7.2, scale=1.0, size=365), 4.5, 9.5)

# Heart Rate: normal distribution around 68 bpm with standard deviation of 10
heart_rate_bpm = np.clip(np.random.normal(loc=68, scale=10, size=365), 48, 110)

# Calories Burned: linear combination of steps and active minutes with random factors
calories_burned = np.clip(0.04 * steps + 6 * np.random.normal(loc=40, scale=15, size=365), 1800, 4200)

# Active Minutes: normal distribution around 60 minutes, clipped between 20 and 180
active_minutes = np.clip(np.random.normal(loc=60, scale=20, size=365), 20, 180)

# Introduce 5% missing values
mask = np.random.rand(365, 5) < 0.05

steps[mask[:, 0]] = np.nan
sleep_hours[mask[:, 1]] = np.nan
heart_rate_bpm[mask[:, 2]] = np.nan
calories_burned[mask[:, 3]] = np.nan
active_minutes[mask[:, 4]] = np.nan

# Create DataFrame
fitness_data = pd.DataFrame({
    "Date": dates,
    "Steps": steps,
    "Sleep_Hours": sleep_hours,
    "Heart_Rate_bpm": heart_rate_bpm,
    "Calories_Burned": calories_burned,
    "Active_Minutes": active_minutes
})

# Save to a CSV file
fitness_data.to_csv("data/health_data.csv", index=False)
