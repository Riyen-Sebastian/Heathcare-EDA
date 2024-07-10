import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# List of CSV files (update these with your actual file names)
csv_files = [
    'Healthcare Data/census_2011.csv',
    'Healthcare Data/Hospitals and Beds maintained by Railways.csv',
    'Healthcare Data/government_hospitals.csv',
    'Healthcare Data/Employees State Insurance Corporation.csv',
    'Healthcare Data/Hospitals and Beds maintained by Ministry of Defence.csv',
    'Healthcare Data/hospitals.csv',
    'Healthcare Data/housing.csv'
    ]

#Function to study dataframe
def study_dataframe(df,name):
    print(f"\n--- Studying {name} ---")
       #insert data studying functions here

      # Basic information
    print("\nBasic Info:")
    print(df.info())
    
    # Summary statistics for numeric columns
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    if not numeric_columns.empty:
        print("\nSummary Statistics for Numeric Columns:")
        print(df[numeric_columns].describe())
    
    # Missing values
    print("\nMissing Values:")
    missing_values = df.isnull().sum()
    print(missing_values)
    print("\nPercentage of Missing Values:")
    print(100 * missing_values / len(df))
    
   #Data types
    print("\nData Types:")
    print(df.dtypes)

    #Unique values in each column
    print("\nUnique Values in Each Column:")
    for column in df.columns:
        print(f"{column}: {df[column].nunique()} unique values")
    # Correlation heatmap for numeric columns
    if len(numeric_columns) > 1:
        plt.figure(figsize=(12, 10))
        sns.heatmap(df[numeric_columns].corr(), annot=True, cmap='coolwarm')
        plt.title(f'Correlation Heatmap - {name}')
        plt.savefig(f'{name}_correlation_heatmap.png')
        plt.close()

    # Boxplots for numeric columns to identify outliers
    for column in numeric_columns:
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=df[column])
        plt.title(f'Boxplot of {column}')
        plt.savefig(f'{name}boxplot{column}.png')
        plt.close()

  # For categorical columns, show value counts
    categorical_columns = df.select_dtypes(include=['object']).columns
    for column in categorical_columns:
        print(f"\nValue counts for {column}:")
        value_counts = df[column].value_counts(normalize=True)
        print(value_counts.head(10))  # Print top 10 categories
        
        # Bar plot for top categories
        plt.figure(figsize=(10, 6))
        value_counts.head(10).plot(kind='bar')
        plt.title(f'Top 10 Categories in {column}')
        plt.savefig(f'{name}top_categories{column}.png')
        plt.close()

    # Identify potential outliers in numeric columns
    if not numeric_columns.empty:
        print("\nPotential Outliers (values beyond 3 standard deviations):")
        for column in numeric_columns:
            mean = df[column].mean()
            std = df[column].std()
            outliers = df[(df[column] < mean - 3*std) | (df[column] > mean + 3*std)]
            if not outliers.empty:
                print(f"\n{column}:")
                print(outliers[column].head())  # Print first few outliers      


    

#To study each data frame
for file in csv_files:
    df=pd.read_csv(file)
    study_dataframe(df,file.split('/')[-1])

