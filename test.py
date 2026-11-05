from modules.processor import load_data, process_data

def test_data_pipeline():
    print("=== FitSync Smoke Test: Data Loading & Processing ===")
    
    # Test load_data
    raw_df = load_data()
    print(f"[OK] Loaded {len(raw_df)} records successfully.")
    
    # Ensure no missing values remain
    missing = raw_df.isnull().sum().sum()
    print(f"[OK] Total missing values after imputation: {missing}")
    assert missing == 0, "Missing values detected after cleaning!"
    
    # Test process_data (includes Recovery_Score calculation)
    df = process_data()
    assert 'Recovery_Score' in df.columns, "Recovery_Score column missing!"
    assert df['Recovery_Score'].min() >= 0, "Recovery_Score below 0 found!"
    assert df['Recovery_Score'].max() <= 100, "Recovery_Score above 100 found!"
    
    print(f"[OK] Recovery Score range: [{df['Recovery_Score'].min()}, {df['Recovery_Score'].max()}]")
    print("\nPreview of processed records:")
    print(df[['Date', 'Steps', 'Sleep_Hours', 'Heart_Rate_bpm', 'Recovery_Score']].head(10))
    print("\n[SUCCESS] All data pipeline smoke checks passed!")

if __name__ == "__main__":
    test_data_pipeline()
