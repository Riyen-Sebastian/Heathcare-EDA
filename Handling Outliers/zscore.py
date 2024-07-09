import pandas as pd
import numpy as np
from scipy import stats


df = pd.read_csv('Heathcare-EDA\Healthcare Data\census_2011.csv')


z_scores = np.abs(stats.zscore(df.select_dtypes(include=[np.number])))


threshold = 3


outliers = (z_scores > threshold)


df['Outlier'] = outliers.any(axis=1)
print(df)

df.to_csv('data_with_outliers.csv', index=False)
