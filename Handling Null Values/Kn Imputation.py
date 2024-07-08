def smart_impute(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Function to determine if a column is numeric
    def is_numeric(col):
        return pd.api.types.is_numeric_dtype(df[col])
    

    
    for column in df.columns:
        if df[column].isnull().sum() > 0:  # Check if column has missing values
            if is_numeric(column):
                # For numeric columns, use KNN imputation
                imputer = KNNImputer(n_neighbors=5)
                df[column] = imputer.fit_transform(df[[column]])
                
 # Done by Archie. 
 # With Help of Riyen.        