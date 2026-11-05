import os
import pandas as pd
from datetime import datetime

def get_default_data_path():
    """
    Resolve the default path to data/health_data.csv reliably,
    whether run from repository root or a subfolder.
    """
    candidates = [
        os.path.join("data", "health_data.csv"),
        os.path.join(os.path.dirname(__file__), "..", "data", "health_data.csv"),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "health_data.csv"))
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return "data/health_data.csv"

def load_data(file_path=None):
    """
    Load and clean the health data from CSV file.
    Handles missing values using statistical and domain defaults:
      - Steps: median
      - Sleep_Hours: fixed value of 7.0
      - Heart_Rate_bpm: fixed value of 68.0
      - Calories_Burned: median
      - Active_Minutes: median
    Converts 'Date' column to datetime objects and sorts chronologically.
    Returns a cleaned pandas DataFrame.
    """
    if file_path is None:
        file_path = get_default_data_path()

    data = pd.read_csv(file_path)

    # Clean missing values without deprecated inplace assignments
    if 'Steps' in data.columns:
        data['Steps'] = data['Steps'].fillna(data['Steps'].median())

    if 'Sleep_Hours' in data.columns:
        data['Sleep_Hours'] = data['Sleep_Hours'].fillna(7.0)

    if 'Heart_Rate_bpm' in data.columns:
        data['Heart_Rate_bpm'] = data['Heart_Rate_bpm'].fillna(68.0)

    for col in ['Calories_Burned', 'Active_Minutes']:
        if col in data.columns:
            data[col] = data[col].fillna(data[col].median())

    # Convert Date column to datetime
    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
        data = data.sort_values('Date').reset_index(drop=True)

    return data

def calculate_recovery_score(df):
    """
    Calculate and append a 'Recovery_Score' (clamped between 0 and 100) to the DataFrame.
    
    Recovery Logic:
      - Starting baseline: 50
      - Sleep >= 7 hrs: +20 | Sleep < 6 hrs: -20
      - Heart Rate < 60 bpm: +10 (optimal resting) | Heart Rate > 80 bpm: -10 (elevated strain)
      - Steps between 8,000 and 12,000: +10 (ideal target zone)
      - Steps < 4,000: -5 (sedentary day) | Steps > 16,000: -5 (overexertion)
    """
    df = df.copy()
    df['Recovery_Score'] = 50

    # Adjust for Sleep Hours
    if 'Sleep_Hours' in df.columns:
        df.loc[df['Sleep_Hours'] >= 7.0, 'Recovery_Score'] += 20
        df.loc[df['Sleep_Hours'] < 6.0, 'Recovery_Score'] -= 20

    # Adjust for Heart Rate
    if 'Heart_Rate_bpm' in df.columns:
        df.loc[df['Heart_Rate_bpm'] < 60.0, 'Recovery_Score'] += 10
        df.loc[df['Heart_Rate_bpm'] > 80.0, 'Recovery_Score'] -= 10

    # Adjust for Steps
    if 'Steps' in df.columns:
        df.loc[(df['Steps'] >= 8000) & (df['Steps'] <= 12000), 'Recovery_Score'] += 10
        df.loc[df['Steps'] < 4000, 'Recovery_Score'] -= 5
        df.loc[df['Steps'] > 16000, 'Recovery_Score'] -= 5

    # Clamp strictly between 0 and 100
    df['Recovery_Score'] = df['Recovery_Score'].clip(lower=0, upper=100)

    return df

def process_data(file_path=None):
    """
    End-to-end data pipeline:
    Loads raw CSV, imputes missing values, and computes Recovery_Score.
    """
    raw_df = load_data(file_path)
    processed_df = calculate_recovery_score(raw_df)
    return processed_df
