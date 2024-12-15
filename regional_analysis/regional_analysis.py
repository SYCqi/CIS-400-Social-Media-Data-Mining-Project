# TEMPLATE FOR ANALYZING THE RESULT AFTER VADER SENTIMENT ANALYSIS----------------------------------------------------------------------------------
# Version: 2
# If you modified the code please change the file name into a relevant name
#
# After running the "Vader_sentiment_analysis.py" our 12 dataset was updated with 4 new columns ('positive', 'negative', 'neutral', 'compound'). 
# Each Reddit posts from the 12 dataset has been analyzed to tell the attitude of the post toward the weather condition.
#
# In this python program all 12 dataset are analyzed together and make a overall analyzation of the final results to let us 
# later develop vizualization graphs to visualize this projects final result of regional attitude toward the weather condition.
#
# https://ds3.ssrc.msstate.edu/2021/01/14/using-vadersentiment-to-intuitively-predict-the-sentiment-of-social-media-posts/
#-----------------------------------------------------------------------------------------------------------------------

import sqlite3
import pandas as pd

# Mapping regions with corresponding states-----------------------------------------------------------------------------
region_state_mapping = {
    "cold": ["Alaska", "North Dakota"],
    "hot": ["Florida", "Hawaii"],
    "temperate": ["Kentucky", "Kansas"]
}

# List all db files to import-------------------------------------------------------------------------------------------
db_files = [
    'vader_cold_region_cloudyData.db',
    'vader_cold_region_rainyData.db',
    'vader_cold_region_snowyData.db',
    'vader_cold_region_sunnyData.db',
    'vader_hot_region_cloudyData.db',
    'vader_hot_region_rainyData.db',
    'vader_hot_region_snowyData.db',
    'vader_hot_region_sunnyData.db',
    'vader_temperate_region_cloudyData.db',
    'vader_temperate_region_rainyData.db',
    'vader_temperate_region_snowyData.db',
    'vader_temperate_region_sunnyData.db'
]

# Function to classify sentiment based on the compound score------------------------------------------------------------
def classify_sentiment(compound_score):
    if compound_score > 0.5:
        return "positive"
    elif compound_score < -0.5:
        return "negative"
    else:
        return "neutral"

# Extract Region & Weather from file name-------------------------------------------------------------------------------
results = []

for db_file in db_files:
    try:
        conn = sqlite3.connect(db_file)             # Connect to db files
        query = "SELECT * FROM sentiment_results"   # Load sentiment_results table
        data = pd.read_sql_query(query, conn)

# Determine region and weather based on the file name-------------------------------------------------------------------
        if "cold" in db_file:
            region = "Cold Region"
            states = region_state_mapping["cold"]
        elif "hot" in db_file:
            region = "Hot Region"
            states = region_state_mapping["hot"]
        elif "temperate" in db_file:
            region = "Temperate Region"
            states = region_state_mapping["temperate"]

        if "cloudy" in db_file:
            weather = "Cloudy"
        elif "rainy" in db_file:
            weather = "Rainy"
        elif "snowy" in db_file:
            weather = "Snowy"
        elif "sunny" in db_file:
            weather = "Sunny"

        # Processing each state
        for state in states:
            state_data = data[data['STATE'] == state].copy()

# Count based on proportions--------------------------------------------------------------------------------------------
            # Classify sentiment
            state_data.loc[:, 'classified_sentiment'] = state_data['compound'].apply(classify_sentiment)

            # Count sentiment types
            positive_count = (state_data['classified_sentiment'] == 'positive').sum()
            neutral_count = (state_data['classified_sentiment'] == 'neutral').sum()
            negative_count = (state_data['classified_sentiment'] == 'negative').sum()
            total_count = len(state_data)

# Calculate percentages-------------------------------------------------------------------------------------------------
            positive_percentage = (positive_count / total_count * 100) if total_count > 0 else 0
            neutral_percentage = (neutral_count / total_count * 100) if total_count > 0 else 0
            negative_percentage = (negative_count / total_count * 100) if total_count > 0 else 0

# Average compound------------------------------------------------------------------------------------------------------
            average_compound = state_data['compound'].mean()
            if average_compound > 0.5:
                overall_sentiment = "Positive"
            elif average_compound < -0.5:
                overall_sentiment = "Negative"
            else:
                overall_sentiment = "Neutral"

# Find the most frequent sentiment based on percentage------------------------------------------------------------------
            sentiment_percentages = {
                "Positive": positive_percentage,
                "Neutral": neutral_percentage,
                "Negative": negative_percentage
            }
            most_frequent_sentiment = max(sentiment_percentages, key=sentiment_percentages.get)

# Calculate dominance strength (difference between highest and second highest percentage)-------------------------------
            sorted_percentages = sorted(sentiment_percentages.values(), reverse=True)
            dominance_strength = round(sorted_percentages[0] - sorted_percentages[1], 2)

# Append results to list------------------------------------------------------------------------------------------------
            results.append({
                "Region": region,
                "State": state,
                "Weather": weather,
                "Total Counts": total_count,
                "Positive Counts": positive_count,
                "Neutral Counts": neutral_count,
                "Negative Counts": negative_count,
                "Positive (%)": round(positive_percentage, 2),
                "Neutral (%)": round(neutral_percentage, 2),
                "Negative (%)": round(negative_percentage, 2),
                "Average Compound": round(average_compound, 2),
                "Overall Sentiment (by Compound)": overall_sentiment,
                "Most Frequent Sentiment (by %)": most_frequent_sentiment,
                "Dominance Strength (%)": dominance_strength
            })

        conn.close()
    except Exception as e:
        print(f"Error processing file {db_file}: {e}")

# Create a DataFrame from the list--------------------------------------------------------------------------------------
df = pd.DataFrame(results)

# Create a CSV file-----------------------------------------------------------------------------------------------------
df.to_csv('regional_analysis.csv', index=False)
