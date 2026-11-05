from modules.processor import load_data, calculate_recovery_score

def test_recovery_scoring():
    print("=== FitSync Smoke Test: Recovery Score Verification ===")
    
    # Load and score
    df = load_data()
    df = calculate_recovery_score(df)
    
    # Assertions
    assert "Recovery_Score" in df.columns, "Recovery_Score column is missing!"
    assert df["Recovery_Score"].between(0, 100).all(), "Recovery Score out of bounds [0, 100]!"
    
    # Detailed inspection
    print("Scoring distribution summary:")
    print(df["Recovery_Score"].describe())
    
    print("\nSample preview:")
    print(df[['Date', 'Sleep_Hours', 'Heart_Rate_bpm', 'Steps', 'Recovery_Score']].head(10))
    print("\n[SUCCESS] Recovery scoring logic verified!")

if __name__ == "__main__":
    test_recovery_scoring()
