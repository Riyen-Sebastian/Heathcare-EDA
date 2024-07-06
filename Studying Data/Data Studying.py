import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# List of CSV files (update these with your actual file names)
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

#Function to sttudy dataframe
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

    

#To study each data frame
for file in csv_files:
    df=pd.read_csv(file)
    study_dataframe(df,file.split('/')[-1])