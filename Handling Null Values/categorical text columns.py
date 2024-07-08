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
