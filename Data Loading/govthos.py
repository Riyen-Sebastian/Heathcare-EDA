import pandas as pd

# Load the CSV file
df1 = pd.read_csv('Healthcare Data\government_hospitals.csv')

# Display basic information about the dataframe
print("Data1 Info:")
print(df1.info())

# Display the first few rows
print("\nFirst few rows of Data1:")
print(df1.head())

print("Data1 has been loaded successfully")