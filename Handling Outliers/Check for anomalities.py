import pandas as pd
import numpy as np
from scipy import stats

def check_normality(file_path, significance_level=0.05):
    # Load the data
    df = pd.read_csv(file_path)
    
    # Select numeric columns
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    results = {}
    
    for column in numeric_columns:
        # Perform normality test
        _, p_value = stats.normaltest(df[column].dropna())
        
        # Interpret results
        if p_value < significance_level:
            interpretation = "Not normally distributed"
        else:
            interpretation = "Normally distributed"
        
        results[column] = {
            "p-value": p_value,
            "Interpretation": interpretation
        }