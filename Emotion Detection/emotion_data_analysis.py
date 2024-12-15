import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# the folder containing processed data
processed_directory = 'processedData'
graphs_directory = os.path.join(processed_directory, 'graphs')
os.makedirs(graphs_directory, exist_ok=True)

# Initialize a dictionary to store summary data
emotion_summary = {}

# Loop through processed files to load and analyze
for filename in os.listdir(processed_directory):
    if filename.endswith('.csv') and 'graphs' not in filename:
        # Extract region and weather from the filename
        region, weather = filename.split('_')[0], filename.split('_')[1]

        # Load the data
        file_path = os.path.join(processed_directory, filename)
        df = pd.read_csv(file_path)

        # Count the emotions
        emotion_counts = df['Emotion'].value_counts()

        # Store the counts in a nested dictionary
        if region not in emotion_summary:
            emotion_summary[region] = {}
        emotion_summary[region][weather] = emotion_counts

# Create a DataFrame for easier analysis
all_emotions = []
for region, weather_data in emotion_summary.items():
    for weather, counts in weather_data.items():
        for emotion, count in counts.items():
            all_emotions.append({'Region': region, 'Weather': weather, 'Emotion': emotion, 'Count': count})

emotion_df = pd.DataFrame(all_emotions)

# Save the summarized data for reference
emotion_df.to_csv(os.path.join(processed_directory, 'emotion_summary.csv'), index=False)

# Step 1: Region-wise emotion distribution
for region, group in emotion_df.groupby('Region'):
    plt.figure(figsize=(10, 6))
    group.groupby('Emotion')['Count'].sum().plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title(f'Emotion Distribution in {region.capitalize()} Region')
    plt.xlabel('Emotion')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Save the graph as a PNG file
    graph_path = os.path.join(graphs_directory, f'{region}_emotion_distribution.png')
    plt.savefig(graph_path)
    plt.close()
    print(f"Saved graph: {graph_path}")

# Step 2: Weather-wise emotion distribution
for weather, group in emotion_df.groupby('Weather'):
    plt.figure(figsize=(10, 6))
    group.groupby('Emotion')['Count'].sum().plot(kind='bar', color='orange', edgecolor='black')
    plt.title(f'Emotion Distribution in {weather.capitalize()} Weather')
    plt.xlabel('Emotion')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Save the graph as a PNG file
    graph_path = os.path.join(graphs_directory, f'{weather}_emotion_distribution.png')
    plt.savefig(graph_path)
    plt.close()
    print(f"Saved graph: {graph_path}")

# Step 3: Compare across regions and weather
pivot_df = emotion_df.pivot_table(index='Emotion', columns=['Region', 'Weather'], values='Count', fill_value=0)

plt.figure(figsize=(12, 8))
sns.heatmap(pivot_df, cmap='coolwarm', annot=True, fmt='d', linewidths=.5)
plt.title('Emotion Distribution Across Regions and Weather')
plt.ylabel('Emotion')
plt.xlabel('Region-Weather')
plt.tight_layout()
# Save the heatmap as a PNG file
heatmap_path = os.path.join(graphs_directory, 'region_weather_emotion_heatmap.png')
plt.savefig(heatmap_path)
plt.close()
print(f"Saved heatmap: {heatmap_path}")
