import os
import re
import pandas as pd
from transformers import pipeline, AutoTokenizer

# Define the input folder and output folder
input_directory = 'preprocessedData'
output_directory = 'processedData'
os.makedirs(output_directory, exist_ok=True)

# Load the emotion detection model and tokenizer
model_name = "j-hartmann/emotion-english-distilroberta-base"
emotion_classifier = pipeline("text-classification", model=model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Function to truncate text to fit within the model's token limit
def truncate_text(text, max_tokens=512):
    if isinstance(text, str):
        tokens = tokenizer(text, truncation=True, max_length=max_tokens, return_tensors="pt")
        return tokenizer.decode(tokens['input_ids'][0], skip_special_tokens=True)
    return text

# Initialize a dictionary to hold processed data by region and weather
processed_data = {}

# Define a regex pattern to extract region and weather
filename_pattern = re.compile(r"clean_(\w+)_region_(\w+)Data\.csv")

# Loop through all CSV files in the folder
for filename in os.listdir(input_directory):
    if filename.endswith('.csv'):  # Process only CSV files
        file_path = os.path.join(input_directory, filename)

        # Match the filename pattern
        match = filename_pattern.match(filename)
        if not match:
            print(f"Skipping file with unexpected name format: {filename}")
            continue

        # Extract region and weather from the matched groups
        region, weather = match.groups()

        print(f"Processing file: {filename} (Region: {region}, Weather: {weather})")
        
        # Load the CSV file
        df = pd.read_csv(file_path)
        
        # Truncate text to fit within the model's token limit
        df['TEXT'] = df['TEXT'].apply(lambda text: truncate_text(text))
        
        # Apply emotion detection to the 'TEXT' column
        df['Emotion'] = df['TEXT'].apply(
            lambda text: emotion_classifier(text)[0]['label'] if isinstance(text, str) else 'neutral'
        )
        
        # Add to processed data
        if region not in processed_data:
            processed_data[region] = {}
        if weather not in processed_data[region]:
            processed_data[region][weather] = []
        
        processed_data[region][weather].append(df)

# Save the processed data to separate files by region and weather
for region, weather_data in processed_data.items():
    for weather, dfs in weather_data.items():
        output_file = f"{output_directory}/{region}_{weather}_emotion_data.csv"
        consolidated_df = pd.concat(dfs, ignore_index=True)
        consolidated_df.to_csv(output_file, index=False)
        print(f"Saved processed data for {region} - {weather} to {output_file}")
