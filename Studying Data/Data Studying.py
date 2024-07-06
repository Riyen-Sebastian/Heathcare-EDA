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

    

#To study each data frame
for file in csv_files:
    df=pd.read_csv(file)
    study_dataframe(df,file.split('/')[-1])