if p_value < 0.05:  # Not normally distributed
            # Use IQR method
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df[column] = df[column].clip(lower_bound, upper_bound)
            print(f"Used IQR method for {column}")
        else:  # Normally distributed
            # Use Z-score method
            z_scores = np.abs(stats.zscore(df[column]))
            df[column] = df[column].mask(z_scores > 3, df[column].median())
            print(f"Used Z-score method for {column}")
            
# By Archie           