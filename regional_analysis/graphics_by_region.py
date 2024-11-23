import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = 'regional_analysis.csv'
data = pd.read_csv(file_path)

# Set a style for the plots
sns.set_theme(style="whitegrid")

# Aggregate data by Region
region_data = data.groupby('Region').sum()

# Bar Chart: Sentiment Distribution by Region
plt.figure(figsize=(10, 6))
region_data[['Positive Counts', 'Neutral Counts', 'Negative Counts']].plot(
    kind='bar', color=['green', 'gray', 'red'], figsize=(12, 6)
)
plt.title('Sentiment Distribution by Region', fontsize=14)
plt.ylabel('Total Count', fontsize=12)
plt.xlabel('Region', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title="Sentiment", loc='upper right')
plt.tight_layout()
# always save before show to avoid blank images
plt.savefig('sentiment_by_region.png')
plt.show()
plt.close()

# Heatmap: Dominance Strength by Region
region_dominance = data.groupby(['Region', 'Weather'])['Dominance Strength (%)'].mean().unstack()
plt.figure(figsize=(10, 6))
sns.heatmap(region_dominance, annot=True, fmt=".2f", cmap="coolwarm", cbar_kws={'label': 'Dominance Strength (%)'})
plt.title('Dominance Strength by Region and Weather', fontsize=14)
plt.ylabel('Region', fontsize=12)
plt.xlabel('Weather', fontsize=12)
plt.tight_layout()
plt.savefig('dominance_by_region_weather.png')  # Save image
plt.show()
plt.close()

# Scatter Plot: Weakly Positive/Negative Counts vs Dominance Strength (Per Region)
plt.figure(figsize=(10, 6))
for region, group in data.groupby('Region'):
    sns.scatterplot(
        data=group,
        x='Weakly Positive Counts',
        y='Dominance Strength (%)',
        label=region
    )
plt.title('Weakly Positive/Negative Counts vs Dominance Strength (by Region)', fontsize=14)
plt.ylabel('Dominance Strength (%)', fontsize=12)
plt.xlabel('Weakly Positive/Negative Counts', fontsize=12)
plt.legend(title="Region")
plt.tight_layout()
plt.savefig('weakly_counts_vs_dominance_by_region.png')  # Save image
plt.show()
plt.close()

print("Images saved successfully!")

