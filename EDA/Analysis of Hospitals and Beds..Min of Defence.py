import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os

# Use Agg backend for Matplotlib
import matplotlib
matplotlib.use('Agg')

def load_and_preview(file_path):
    df = pd.read_csv(file_path)
    print(f"Preview of {file_path}:")
    print(df.info())
    print(df.head())
    return df

def plot_univariate(df, column, ax):
    sns.histplot(df[column], kde=True, ax=ax)
    ax.set_title(column)
    ax.set_xlabel(column)
    ax.set_ylabel('Frequency')

def plot_bivariate(df, col1, col2, ax):
    sns.scatterplot(data=df, x=col1, y=col2, ax=ax)
    ax.set_title(f'{col1} vs {col2}')

def plot_correlation_heatmap(df, prefix="correlation_heatmap"):
    os.makedirs("plots", exist_ok=True)
    plt.figure(figsize=(12, 10))
    corr_matrix = df.corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title(f'{prefix.replace("_", " ").title()}')
    plt.savefig(f'plots/{prefix}.png')
    plt.close()

def combined_analysis(df, columns, plot_func, batch_size=10, prefix="analysis"):
    os.makedirs("plots", exist_ok=True)
    for i in range(0, len(columns), batch_size):
        batch_columns = columns[i:i+batch_size]
        num_columns = len(batch_columns)
        num_rows = (num_columns + 2) // 3  # 3 columns per row
        fig, axes = plt.subplots(num_rows, 3, figsize=(20, 5 * num_rows))
        axes = axes.flatten()
        
        for j, column in enumerate(batch_columns):
            if plot_func == plot_univariate:
                plot_func(df, column, axes[j])
            else:
                for k in range(j+1, len(batch_columns)):
                    plot_func(df, batch_columns[j], batch_columns[k], axes[j])
        
        for j in range(len(batch_columns), len(axes)):
            fig.delaxes(axes[j])
        
        plt.tight_layout()
        plt.savefig(f'plots/{prefix}_batch{i//batch_size + 1}.png')
        plt.close()

def plot_top_10_states(df, column, title):
    plt.figure(figsize=(12, 6))
    df_sorted = df.sort_values(column, ascending=False).head(10)
    sns.barplot(x=column, y='Name of State', data=df_sorted)
    plt.title(f'Top 10 States by {title}')
    plt.tight_layout()
    plt.savefig(f'plots/top_10_{column.lower().replace(" ", "_")}.png')
    plt.close()

def plot_beds_per_hospital(df):
    df['Beds per Hospital'] = df['No. of beds'] / df['No. of Hospitals']
    plt.figure(figsize=(12, 6))
    df_sorted = df.sort_values('Beds per Hospital', ascending=False).head(10)
    sns.barplot(x='Beds per Hospital', y='Name of State', data=df_sorted)
    plt.title('Top 10 States by Beds per Hospital')
    plt.tight_layout()
    plt.savefig('plots/top_10_beds_per_hospital.png')
    plt.close()

def perform_eda(file_path):
    df = load_and_preview(file_path)
    
    # Remove the 'Total' row
    df = df[df['Name of State'] != 'Total']
    
    print("\nPerforming Univariate Analysis:")
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    combined_analysis(df, numeric_columns, plot_univariate, prefix="univariate")
    
    print("\nPerforming Bivariate Analysis:")
    combined_analysis(df, numeric_columns, plot_bivariate, prefix="bivariate")
    
    print("\nPerforming Multivariate Analysis:")
    plot_correlation_heatmap(df[numeric_columns], prefix="correlation_heatmap")
    
    print("\nPlotting Top 10 States by Number of Hospitals:")
    plot_top_10_states(df, 'No. of Hospitals', 'Number of Hospitals')
    
    print("\nPlotting Top 10 States by Number of Beds:")
    plot_top_10_states(df, 'No. of beds', 'Number of Beds')
    
    print("\nPlotting Top 10 States by Beds per Hospital:")
    plot_beds_per_hospital(df)

    return df

# Analyze the file
df = perform_eda('Healthcare Data\Hospitals and Beds maintained by Ministry of Defence.csv')

#conclusions
print("\nConclusions from the analysis:")
print(f"1. Total number of states/UTs: {len(df)}")
print(f"2. Total number of hospitals: {df['No. of Hospitals'].sum():.0f}")
print(f"3. Total number of beds: {df['No. of beds'].sum():.0f}")
print(f"4. State with the most hospitals: {df.loc[df['No. of Hospitals'].idxmax(), 'Name of State']} ({df['No. of Hospitals'].max():.0f} hospitals)")
print(f"5. State with the most beds: {df.loc[df['No. of beds'].idxmax(), 'Name of State']} ({df['No. of beds'].max():.0f} beds)")
print(f"6. Average number of beds per hospital: {df['No. of beds'].sum() / df['No. of Hospitals'].sum():.2f}")
