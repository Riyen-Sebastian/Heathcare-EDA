import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

def smart_impute(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Function to determine if a column is numeric
    def is_numeric(col):
        return pd.api.types.is_numeric_dtype(df[col])
    
    # Function to determine if a column is datetime
    def is_datetime(col):
        return pd.api.types.is_datetime64_any_dtype(df[col])
    
    for column in df.columns:
        if df[column].isnull().sum() > 0:  # Check if column has missing values
            if is_numeric(column):
                # For numeric columns, use KNN imputation
                imputer = KNNImputer(n_neighbors=5)
                df[column] = imputer.fit_transform(df[[column]])
            elif is_datetime(column):
                # For datetime columns, forward fill and then backward fill
                df[column] = df[column].fillna(method='ffill').fillna(method='bfill')
            else:
                # For categorical/text columns, use mode
                df[column] = df[column].fillna(df[column].mode()[0])
    
    # Save the processed DataFrame back to the original file
    df.to_csv(file_path, index=False)
    print(f"Updated original file: {file_path}")
    
    return df
    

    
    # Save the processed DataFrame back to the original file
    df.to_csv(file_path, index=False)
    print(f"Updated original file: {file_path}")
    
    return df

# List of CSV files to process
csv_files = [
    'Healthcare Data/census_2011.csv',
    'Healthcare Data/Hospitals and Beds maintained by Railways.csv',
    'Healthcare Data/government_hospitals.csv',
    'Healthcare Data/Employees State Insurance Corporation.csv',
    'Healthcare Data/Hospitals and Beds maintained by Ministry of Defence.csv',
    'Healthcare Data/hospitals.csv',
    'Healthcare Data/housing.csv',
    'Healthcare Data/metadata.csv'
    ]

# Process each CSV file
for file_name in csv_files:
    processed_df = smart_impute(file_name)
    print(f"Processed {file_name}")