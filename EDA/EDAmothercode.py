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

def reduce_dimensions_with_pca(df, n_components=2):
    scaler = StandardScaler()
    numeric_df = df.select_dtypes(include=[np.number])
    scaled_data = scaler.fit_transform(numeric_df)
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(scaled_data)
    pca_df = pd.DataFrame(data=principal_components, columns=[f'PC{i+1}' for i in range(n_components)])
    explained_variance = pca.explained_variance_ratio_
    
    loadings = pd.DataFrame(pca.components_.T, columns=[f'PC{i+1}' for i in range(n_components)], index=numeric_df.columns)
    
    top_features_dict = {f'PC{i+1}': ', '.join(loadings[f'PC{i+1}'].abs().sort_values(ascending=False).head(3).index.tolist()) for i in range(n_components)}
    
    print(f"Explained variance ratio by PCA: {explained_variance}")
    return pd.concat([df.reset_index(drop=True), pca_df], axis=1), loadings, top_features_dict, explained_variance

def plot_explained_variance(explained_variance):
    plt.figure(figsize=(10, 6))
    plt.bar(range(1, len(explained_variance) + 1), explained_variance, align='center', alpha=0.8)
    plt.title('Explained Variance Ratio by Principal Components')
    plt.xlabel('Principal Component')
    plt.ylabel('Explained Variance Ratio')
    plt.xticks(range(1, len(explained_variance) + 1))
    plt.grid(True)
    plt.savefig('explained_variance.png')  # Save the figure to a file
    plt.close()  # Close the figure to release resources

def biplot(pca_df, loadings):
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=pca_df, x='PC1', y='PC2')
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.title('Biplot of PC1 and PC2')
    
    for i in loadings.index:
        plt.arrow(0, 0, loadings.loc[i, 'PC1'], loadings.loc[i, 'PC2'], color='r', alpha=0.5)
        plt.text(loadings.loc[i, 'PC1']*1.1, loadings.loc[i, 'PC2']*1.1, i, color='g', ha='center', va='center')

    plt.grid(True)
    plt.savefig('plots/biplot.png')
    plt.close()

def perform_eda(file_paths):
    for file_path in file_paths:
        df = load_and_preview(file_path)
        
        print("\nPerforming Univariate Analysis on Original Data:")
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        combined_analysis(df, numeric_columns, plot_univariate, prefix="univariate")
        
        print("\nPerforming Bivariate Analysis on Original Data:")
        combined_analysis(df, numeric_columns, plot_bivariate, prefix="bivariate")
        
        print("\nPerforming Multivariate Analysis on Original Data:")
        plot_correlation_heatmap(df[numeric_columns], prefix="original_correlation_heatmap")
        
        print("\nReducing dimensions with PCA...")
        pca_df, loadings, top_features_dict, explained_variance = reduce_dimensions_with_pca(df)
        
        print("\nPerforming Univariate Analysis on PCA Components:")
        pca_columns = [col for col in pca_df.columns if col.startswith('PC')]
        combined_analysis(pca_df, pca_columns, plot_univariate, prefix="univariate_pca")
        
        print("\nPerforming Bivariate Analysis on PCA Components:")
        combined_analysis(pca_df, pca_columns, plot_bivariate, prefix="bivariate_pca")
        
        print("\nPerforming Multivariate Analysis on PCA Components:")
        plot_correlation_heatmap(pca_df[pca_columns], prefix="pca_correlation_heatmap")
        
        print("\nPlotting Explained Variance by PCA Components:")
        plot_explained_variance(explained_variance)
        
        print("\nCreating Biplot of First Two Principal Components:")
        biplot(pca_df, loadings)

        print("\nPCA Loadings (Feature Contributions):")
        print(loadings)
        
        print("\nTop Contributing Features per Principal Component:")
        for pc, features in top_features_dict.items():
            print(f"{pc}: {features}")

# List of CSV files
csv_files = [
    'Healthcare Data\housing.csv'
    # Add all your CSV files here
]

# Perform EDA
perform_eda(csv_files)
