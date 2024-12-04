import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, pipeline

# Load the tokenizer and sentiment analysis pipeline
# Using Roberta model for sentiment analysis because it outputs positive, neutral, and negative sentiment scores unlike DistilBert 
# trained on twitter, so not perfect for reddit data but better than DistilBert
model_name = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
sentiment_analyzer = pipeline("sentiment-analysis", model=model_name)

def truncate_and_analyze_sentiment(text, max_length=512):
    """
    Tokenize and truncate the text to fit the model's maximum token length, then perform sentiment analysis.
    Args:
        text (str): The input text.
        max_length (int): The maximum token length for the model.
    Returns:
        dict: Sentiment analysis result (positive, neutral, negative).
    """
    # Tokenize and truncate text to max_length
    tokens = tokenizer.encode(text, add_special_tokens=True, truncation=True, max_length=max_length)
    truncated_text = tokenizer.decode(tokens, skip_special_tokens=True)  # Reconstruct text from tokens

    # Perform sentiment analysis
    result = sentiment_analyzer(truncated_text)

    # Map result to positive, neutral, negative
    sentiment = result[0]
    label_mapping = {"LABEL_0": "negative", "LABEL_1": "neutral", "LABEL_2": "positive"}
    
    sentiment_scores = {
        label_mapping.get(sentiment["label"], "unknown"): sentiment["score"]
    }

    return sentiment_scores

def process_database(file_path):
    """
    Process a SQLite database file, analyze sentiments, and return the sentiment scores.
    Args:
        file_path (str): Path to the SQLite database file.
    Returns:
        pd.DataFrame: DataFrame containing sentiment scores for the posts.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(file_path)
    query = "SELECT TEXT FROM RedditPosts"  # Assuming the table is named 'RedditPosts' with a 'TEXT' column
    data = pd.read_sql_query(query, conn)
    conn.close()

    # Validate and clean the text data
    data = data[data['TEXT'].notnull()]  # Remove nulls
    data = data[data['TEXT'].str.strip() != ""]  # Remove empty rows

    # Analyze sentiment
    sentiments = []
    for text in data['TEXT']:
        sentiment = truncate_and_analyze_sentiment(text)
        sentiments.append(sentiment)

    # Add sentiment scores to the DataFrame
    data['Positive'] = [s.get('positive', 0) for s in sentiments]
    data['Neutral'] = [s.get('neutral', 0) for s in sentiments]
    data['Negative'] = [s.get('negative', 0) for s in sentiments]

    # Return the data with sentiment scores
    return data

def process_directory(directory_path):
    """
    Process all SQLite .db files in the directory and analyze sentiment for each region and weather condition.
    It generates both individual region outputs and aggregated outputs.
    Args:
        directory_path (str): Path to the directory containing .db files.
    """
    all_data = pd.DataFrame()
    region_weather_data = {}

    # Iterate through all files in the directory
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".db"):  # Only process .db files
            db_path = os.path.join(directory_path, file_name)
            print(f"Processing file: {file_name}")
            
            # Process the database and get sentiment results
            region_data = process_database(db_path)
            
            # Add metadata about the file (e.g., region and weather type)
            region, weather = file_name.replace(".db", "").split("_")
            region_data['Region'] = region
            region_data['Weather'] = weather
            
            # Store the data for later plotting
            region_weather_data[(region, weather)] = region_data
            
            # Append the region data to the all_data DataFrame
            all_data = pd.concat([all_data, region_data], ignore_index=True)

   # Plot results for each region and weather condition
    for (region, weather), data in region_weather_data.items():
        plot_sentiments(data, region, weather)

    # Plot the aggregated results for all regions and weather conditions
    plot_sentiments(all_data, "All Regions", "All Weather Conditions")

def plot_sentiments(data, region_name, weather_name):
    """
    Plot sentiment analysis results for a specific region and weather condition, or for all regions and weather conditions.
    Args:
        data (pd.DataFrame): DataFrame containing sentiment scores.
        region_name (str): The region name to label the plot.
        weather_name (str): The weather condition to label the plot.
    """
    # Aggregate scores by sentiment
    total_sentiments = data[['Positive', 'Neutral', 'Negative']].mean()

    # capitlize names
    region_name = region_name.capitalize()

    # Plot a bar chart
    plt.figure(figsize=(8, 6))
    total_sentiments.plot(kind='bar', color=['green', 'grey', 'red'], alpha=0.7)
    plt.title(f"Average Sentiment Strength for {region_name} Region - {weather_name}")
    plt.ylabel("Score")
    plt.xlabel("Sentiment Type")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f"{region_name}_{weather_name}.png")
    plt.show()

    plt.figure(figsize=(6, 6))
    total_sentiments.plot(kind='pie', autopct='%1.1f%%', colors=['green', 'grey', 'red'], startangle=90)
    plt.title(f"Sentiment Distribution for {region_name} - {weather_name}")
    plt.ylabel("")  # Hide y-axis label
    plt.tight_layout()
    plt.savefig(f"{region_name}_{weather_name}_pie.png")
    plt.show()

if __name__ == "__main__":
    directory_path = "preprocessedData" 
    process_directory(directory_path)
