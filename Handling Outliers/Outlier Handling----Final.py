import pandas as pd
import numpy as np
from scipy import stats

def handle_outliers(file_path):
    df = pd.read_csv(file_path)
    
    for column in df.select_dtypes(include=[np.number]).columns:
        # Check for normality
        _, p_value = stats.normaltest(df[column].dropna())
        
        if p_value < 0.05:  # Not normally distributed
            # Use IQR method
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df[column] = df[column].clip(lower_bound, upper_bound)
            print(f"Used IQR method for {column}")
        else:  # Normally distributed
            # Use Z-score method
            z_scores = np.abs(stats.zscore(df[column]))
            df[column] = df[column].mask(z_scores > 3, df[column].median())
            print(f"Used Z-score method for {column}")
        
    
    df.to_csv(file_path, index=False)
    print(f"Handled outliers in {file_path}")
    return df

# List of CSV files
csv_files = [
    'Healthcare Data/census_2011.csv',
    'Healthcare Data/Hospitals and Beds maintained by Railways.csv',
    'Healthcare Data/government_hospitals.csv',
    'Healthcare Data/housing-colnames.csv',
    'Healthcare Data/Employees State Insurance Corporation.csv',
    'Healthcare Data/Hospitals and Beds maintained by Ministry of Defence.csv',
    'Healthcare Data/hospitals.csv',
    'Healthcare Data/housing.csv',
    'Healthcare Data/metadata.csv',
    'Healthcare Data/Telangana.txt',
    'Healthcare Data/north_east_states.txt']

# Process each CSV file
for file_name in csv_files:
    processed_df = handle_outliers(file_name)