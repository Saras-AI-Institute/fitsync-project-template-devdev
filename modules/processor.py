import pandas as pd
from datetime import datetime

def load_data():
    """
    Load and clean the health data from CSV file.
    This function handles missing values intelligently and converts date strings into datetime objects.
    It returns a cleaned pandas DataFrame.
    """
    # Step 1: Load the CSV file into a pandas DataFrame
    file_path = 'data/health_data.csv'
    data = pd.read_csv(file_path)

    # Step 2: Fill missing 'Steps' values with the median
    data['Steps'].fillna(data['Steps'].median(), inplace=True)

    # Step 3: Fill missing 'Sleep_Hours' values with a fixed value of 7
    data['Sleep_Hours'].fillna(7, inplace=True)

    # Step 4: Fill missing 'Heart_Rate_bpm' values with a fixed value of 68
    data['Heart_Rate_bpm'].fillna(68, inplace=True)

    # Step 5: Fill missing values in other columns with their respective medians
    for column in ['Calories_Burned', 'Active_Minutes']:
        data[column].fillna(data[column].median(), inplace=True)

    # Step 6: Convert 'Date' column to datetime objects
    data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')

    return data

def calculate_recovery_score(df):
    """
    Calculate and add a 'Recovery_Score' (0 to 100) to the DataFrame.
    This score represents how well the person’s body has recovered based on sleep, heart rate, and activity levels.
    The logic for scoring is simple and considers healthy ranges for each factor.
    """
    # Initialize the 'Recovery_Score' to 50 for everyone (neutral starting point)
    df['Recovery_Score'] = 50

    # Adjust score based on Sleep_Hours
    # Sleep more than 7 hours improves recovery score
    df.loc[df['Sleep_Hours'] >= 7, 'Recovery_Score'] += 20
    # Sleep less than 6 hours reduces recovery score
    df.loc[df['Sleep_Hours'] < 6, 'Recovery_Score'] -= 20

    # Adjust score based on Heart_Rate_bpm
    # Lower heart rates improve recovery score
    df.loc[df['Heart_Rate_bpm'] < 60, 'Recovery_Score'] += 10  # Excellent
    df.loc[df['Heart_Rate_bpm'] > 80, 'Recovery_Score'] -= 10  # Needs improvement

    # Adjust score based on Steps
    # Moderate steps improve score, too few or too many decrease score
    df.loc[(df['Steps'] >= 8000) & (df['Steps'] <= 12000), 'Recovery_Score'] += 10  # Optimal steps
    df.loc[df['Steps'] < 4000, 'Recovery_Score'] -= 5   # Too few steps
    df.loc[df['Steps'] > 16000, 'Recovery_Score'] -= 5  # Possible overexertion

    # Ensure Recovery_Score stays within 0 to 100
    df['Recovery_Score'] = df['Recovery_Score'].clip(lower=0, upper=100)

    return df