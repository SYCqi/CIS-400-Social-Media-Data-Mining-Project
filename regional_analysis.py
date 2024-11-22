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

# Extract Region & Weather from file name-------------------------------------------------------------------------------
results = []        # initialize a list

for db_file in db_files:
    try:
        conn = sqlite3.connect(db_file)                     # Connect to db files
        query = "SELECT * FROM sentiment_results"           # Load sentiment_results table (all db table name are same)
        data = pd.read_sql_query(query, conn)


        if "cold" in db_file:                       # Extract region from the vader db file name
            region = "Cold Region"
            states = region_state_mapping["cold"]
        elif "hot" in db_file:
            region = "Hot Region"
            states = region_state_mapping["hot"]
        elif "temperate" in db_file:
            region = "Temperate Region"
            states = region_state_mapping["temperate"]

        if "cloudy" in db_file:                     # Extract weather from the vader db file name
            weather = "Cloudy"
        elif "rainy" in db_file:
            weather = "Rainy"
        elif "snowy" in db_file:
            weather = "Snowy"
        elif "sunny" in db_file:
            weather = "Sunny"

# Count Pos, Neg, Neu for each states-----------------------------------------------------------------------------------
        for state in states:
            state_data = data[data['STATE'] == state]

            positive_count = (state_data['compound'] > 0.2).sum()
            neutral_count = ((state_data['compound'] >= -0.2) & (state_data['compound'] <= 0.2)).sum()
            negative_count = (state_data['compound'] < -0.2).sum()
            total_count = positive_count + neutral_count + negative_count

# Calculate percentage of the counts------------------------------------------------------------------------------------
            positive_pct = (positive_count / total_count * 100) if total_count > 0 else 0
            neutral_pct = (neutral_count / total_count * 100) if total_count > 0 else 0
            negative_pct = (negative_count / total_count * 100) if total_count > 0 else 0

# Calculate average compound score and overall sentiment----------------------------------------------------------------
            average_compound = state_data['compound'].mean()
            if average_compound > 0.1:
                overall_sentiment = "Positive"
            elif average_compound < -0.1:
                overall_sentiment = "Negative"
            else:
                overall_sentiment = "Neutral"

# Identify most frequent sentiment type based on percentages------------------------------------------------------------
            sentiments = {
                "Positive": positive_pct,
                "Neutral": neutral_pct,
                "Negative": negative_pct
            }
            most_frequent_sentiment = max(sentiments, key=sentiments.get)

# Add the results to the list-------------------------------------------------------------------------------------------
            results.append({
                "Region": region,
                "State": state,
                "Weather": weather,
                "Total Counts": total_count,
                "Positive Counts": positive_count,
                "Neutral Counts": neutral_count,
                "Negative Counts": negative_count,
                "Positive (%)": round(positive_pct, 2),
                "Neutral (%)": round(neutral_pct, 2),
                "Negative (%)": round(negative_pct, 2),
                "Average Compound": round(average_compound, 2),
                "Overall Sentiment (by Compound)": overall_sentiment,
                "Most Frequent Sentiment (by %)": most_frequent_sentiment
            })


        conn.close()
    except Exception as e:
        print(f"Error processing file {db_file}: {e}")

# Create a DataFrame from the list--------------------------------------------------------------------------------------
df = pd.DataFrame(results)

# Create a CSV file-----------------------------------------------------------------------------------------------------
df.to_csv('regional_analysis.csv', index=False)
