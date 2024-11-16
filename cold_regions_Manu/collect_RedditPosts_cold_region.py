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
from datetime import datetime

# Setting Up Reddit API Connection--------------------------------------------------------------------------------------
reddit = praw.Reddit(
    # stored in praw.ini
)

# Defining Queries or Weather-Related Keywords--------------------------------------------------------------------------
#
# You can always add new list variables or keywords based on your filter needs.
# Just note put in keywords that are most relevant to the weather can help filter the data more precisely.
#
weather_keywords = ["weather", "sunny", "rainy", "snowy", "cloudy", "hot", "cold", "freezing", "Climate change", "Storm", "Rainy day", "Sunny", "Snowstorm", "Blizzard", "Hurricane", "Tornado", "Windy", "Thunderstorm", "Lightning", "Freezing", "Heatwave", "Cold snap", "Flooding", "Drought", "Overcast", "Forecast", "Polar vortex", "Global warming"]
attitude_keywords = ["love", "hate", "enjoy", "dislike", "like", "annoying", "annoyed", "worried", "relieved", "Thrilled", "scared", "excited", "Ruined"]

# Defining Regional State Based On Climate Zones------------------------------------------------------------------------
#
# Replace the state name with the state that you are working on in the dictionary, so it knows to look for
# the specific location (state) that we wanted only.
#
regional_states = {
    "Alaska": "alaska",
    "North Dakota": "northdakota"
}

# Collecting Data From Reddit API---------------------------------------------------------------------------------------
#
# We are searching for posts only from 2023-Present
#
data = []

for state, subreddit_name in regional_states.items():
    subreddit = reddit.subreddit(subreddit_name)

    # Search for Combinations of Weather and Attitude Keywords
    for weather in weather_keywords:
        for attitude in attitude_keywords:
            search_query = f"{weather} {attitude}"
            posts = subreddit.search(search_query, limit=100)
            for submission in posts:
                post_date = datetime.utcfromtimestamp(submission.created_utc)
                if 2023 <= post_date.year:
                    data.append({
                        "STATE": state,
                        "KEYWORD TYPE": "BOTH",
                        "KEYWORD": weather + ',' + attitude,
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
df.to_csv("cold_regions.csv", index=False)

print("Successfully collected data from Reddit API and created new cold_regions.csv file")
