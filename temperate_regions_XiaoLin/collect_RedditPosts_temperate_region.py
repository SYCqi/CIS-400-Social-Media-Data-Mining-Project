# TEMPLATE FOR REDDIT POSTS COLLECTING----------------------------------------------------------------------------------
# Version: 1
# If you modified the code please change the version number and the file name "collectRedditPostsV#" the version number
# and save it then upload to Github so we can always have a copy of each version of the program just in case we need it.
#
# First please install all the required libraries that will be used for this program.
#   Praw: !pip install praw
#   Pandas: !pip install pandas
#
#-----------------------------------------------------------------------------------------------------------------------

# IMPORTING LIBRARIES---------------------------------------------------------------------------------------------------
import praw
import pandas as pd
import sqlite3
from datetime import datetime, timezone

# Setting Up Reddit API Connection--------------------------------------------------------------------------------------
reddit = praw.Reddit(
    client_id = 'VGIGXi6jj8EPQXf6pigTVw',         
    client_secret = 'oNd_djMb0sODY_mn6lYRzjPEFKUbTA', 
    user_agent = 'weather analysis'  

)

# Defining Queries or Weather-Related Keywords--------------------------------------------------------------------------
#
# You can always add new list variables or keywords based on your filter needs.
# Just note put in keywords that are most relevant to the weather can help filter the data more precisely.
#
identifier_keywords = ["weather", "temperature"]
weather_keywords = ["rainy", "wet", "rain", "storm", "thunderstorm", "misty", "drizzle", "downpour"]
attitude_keywords = ["love", "hate", "enjoy", "dislike", "annoying", "happy", "annoyed", "comfortable"]

# Defining Regional State Based On Climate Zones------------------------------------------------------------------------
#
# Replace the state name with the state that you are working on in the dictionary, so it knows to look for
# the specific location (state) that we wanted only.
#
regional_states = {
    "Kansas": "kansas",
    "Kentucky": "kentucky"
}

# Collecting Data From Reddit API---------------------------------------------------------------------------------------
#
# We are searching for posts only from 2023-Present
#
data = []

for state, subreddit_name in regional_states.items():
    subreddit = reddit.subreddit(subreddit_name)

    # Search for Combinations of Identifier, Weather, and Attitude Keywords
    for identifier in identifier_keywords:
        for weather in weather_keywords:
            for attitude in attitude_keywords:
                search_query = f"{identifier} {weather} {attitude}"
                posts = subreddit.search(search_query, limit=100)
                for submission in posts:
                    post_date = datetime.fromtimestamp(submission.created_utc, timezone.utc)
                    if 2023 <= post_date.year:
                        data.append({
                            "ID": len(data) + 1,
                            "STATE": state,
                            "KEYWORD TYPE": "IDENTIFIER-WEATHER-ATTITUDE",
                            "KEYWORD": f"{identifier}, {weather}, {attitude}",
                            "TITLE": submission.title,
                            "TEXT": submission.selftext,
                            "UTC": post_date
                        })


# Storing Data Into a Data Frame----------------------------------------------------------------------------------------
df = pd.DataFrame(data)                             # Initialize the data frame

# Saving Data Into CSV Files--------------------------------------------------------------------------------------------
#
# After the program runs successfully recommend you to open the csv file with excel or sheets to double check.
#
df.to_csv("temperate_region_rainyData.csv", index=False)

print("Successfully collected data from Reddit API and created the csv file!")

# Saving Data Into a Database File--------------------------------------------------------------------------------------
# Establish connection to SQLite database, if the file DNE then it will create the file
#
conn = sqlite3.connect("temperate_region_rainyData.db")
cursor = conn.cursor()

# Create a table for storing Reddit data
cursor.execute("""
CREATE TABLE IF NOT EXISTS RedditPosts (
    ID INTEGER PRIMARY KEY,
    STATE TEXT,
    KEYWORD_TYPE TEXT,
    KEYWORD TEXT,
    TITLE TEXT,
    TEXT TEXT,
    UTC TEXT
)
""")

# Insert data into the table
df.to_sql("RedditPosts", conn, if_exists="replace", index=False)
cursor = conn.cursor()

# Commit changes and close the connection
conn.commit()
conn.close()

print("Successfully collected data from Reddit API and created the db file!")