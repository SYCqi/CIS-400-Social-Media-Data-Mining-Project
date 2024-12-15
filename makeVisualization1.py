import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load the data
file_path = "regional_analysis.csv"  # Replace with the path to your CSV
data = pd.read_csv("regional_analysis.csv")

# Step 2: Group the data by Region and Weather
grouped_data = data.groupby(['Region', 'Weather'])[['Positive Counts', 'Neutral Counts', 'Negative Counts']].sum().reset_index()

# Step 3: Reshape the data for easier plotting
melted_data = grouped_data.melt(id_vars=['Region', 'Weather'],
                                value_vars=['Positive Counts', 'Neutral Counts', 'Negative Counts'],
                                var_name='Sentiment', value_name='Counts')

# Step 4: Create the plot with Seaborn's FacetGrid
g = sns.FacetGrid(melted_data, col="Region", sharey=True, height=5, aspect=1.5)
g.map_dataframe(sns.barplot, x="Weather", y="Counts", hue="Sentiment", ci=None, palette="Set2")

# Step 5: Customize the plot
g.set_axis_labels("Weather Type", "Counts")
g.set_titles(col_template="{col_name}")
g.add_legend(title="Sentiment")

# Step 6: Adjust layout and display the plot
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()