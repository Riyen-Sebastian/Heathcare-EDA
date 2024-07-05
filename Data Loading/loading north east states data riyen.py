import pandas as pd

# Load the cities into a pandas Series
states = pd.read_csv('C:/Users/Riyen/Healthcare EDA project/Heathcare-EDA/Healthcare Data/north_east_states.txt')

# Display the first few cities
print("First few cities:")
print(states.head())

# Display the number of cities
print(f"\nNumber of cities: {len(states)}")

# Display basic information about the Series
print("\nSeries Info:")
print(states.info())

# Display some basic statistics (this might not be very meaningful for city names, but included for completeness)
print("\nSeries Description:")
print(states.describe())

