import pandas as pd

def load_and_analyze_health_data():
    # Load the CSV file into a DataFrame
    file_path = 'data/health_data.csv'
    data = pd.read_csv(file_path)
    
    # Print the first 5 rows
    print("First 5 rows of the dataset:\n", data.head())
    
    # Calculate and print the number of missing values in each column
    missing_values = data.isnull().sum()
    print("\nNumber of missing values in each column:\n", missing_values)

# Execute the function
load_and_analyze_health_data()