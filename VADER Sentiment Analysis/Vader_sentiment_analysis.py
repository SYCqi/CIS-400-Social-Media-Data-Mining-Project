# Running the VADER Senrtiment Analysis on the preprocessed data
#
# pip install vaderSentiment pandas
# pip install vaderSentiment sqlite3 pandas

import os
import sqlite3
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

# 'preprocessedData' containing the preprocessed .db files
folder_path = 'preprocessedData' 

# perform sentiment analysis
def analyze_sentiment(text):
    scores = analyzer.polarity_scores(text)
    return scores['pos'], scores['neu'], scores['neg'], scores['compound']

# loop through each .db file in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.db'):  # Only process .db files and not the csv
        db_path = os.path.join(folder_path, file_name)
        
        conn = sqlite3.connect(db_path)
        
        query = "SELECT * FROM RedditPosts;"  # RedditPosts is the table name
        data = pd.read_sql_query(query, conn)
        conn.close()
        
        if 'TEXT' in data.columns: 
            data[['positive', 'neutral', 'negative', 'compound']] = data['TEXT'].apply(
                lambda x: pd.Series(analyze_sentiment(x))
            )
        
        # save results to a new .db file, removing "clean" from the name
        new_file_name = file_name.replace('clean_', '') 
        new_db_path = os.path.join(folder_path, f"vader_{new_file_name}")
        
        # save the processed data into the new database
        conn_new = sqlite3.connect(new_db_path)
        data.to_sql('sentiment_results', conn_new, if_exists='replace', index=False)
        conn_new.close()
        
        print(f"Processed and saved: {new_db_path}")
