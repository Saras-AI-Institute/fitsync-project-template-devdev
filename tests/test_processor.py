import pytest
import pandas as pd
from modules.processor import load_data, calculate_recovery_score, process_data

def test_load_data():
    df = load_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "Date" in df.columns
    assert "Steps" in df.columns
    assert "Sleep_Hours" in df.columns
    assert "Heart_Rate_bpm" in df.columns
    # Verify no NaN values exist in cleaned DataFrame
    assert df.isnull().sum().sum() == 0
    # Verify Date was parsed as datetime
    assert pd.api.types.is_datetime64_any_dtype(df["Date"])

def test_calculate_recovery_score():
    raw_df = load_data()
    df = calculate_recovery_score(raw_df)
    assert "Recovery_Score" in df.columns
    assert df["Recovery_Score"].min() >= 0
    assert df["Recovery_Score"].max() <= 100
    assert pd.api.types.is_numeric_dtype(df["Recovery_Score"])

def test_process_data_pipeline():
    df = process_data()
    assert isinstance(df, pd.DataFrame)
    assert "Recovery_Score" in df.columns
    assert len(df) > 0
    assert df.isnull().sum().sum() == 0

def test_recovery_score_rules():
    # Construct synthetic boundary conditions
    test_df = pd.DataFrame({
        "Date": pd.to_datetime(["2025-01-01", "2025-01-02", "2025-01-03"]),
        "Steps": [10000, 2000, 20000],          # +10, -5, -5
        "Sleep_Hours": [8.0, 5.0, 7.5],          # +20, -20, +20
        "Heart_Rate_bpm": [55.0, 85.0, 70.0],    # +10, -10, 0
        "Calories_Burned": [2500, 1800, 3200],
        "Active_Minutes": [60, 20, 120]
    })
    scored = calculate_recovery_score(test_df)
    # Row 0: 50 + 20(sleep) + 10(hr) + 10(steps) = 90
    assert scored.loc[0, "Recovery_Score"] == 90
    # Row 1: 50 - 20(sleep) - 10(hr) - 5(steps) = 15
    assert scored.loc[1, "Recovery_Score"] == 15
    # Row 2: 50 + 20(sleep) + 0(hr) - 5(steps) = 65
    assert scored.loc[2, "Recovery_Score"] == 65
