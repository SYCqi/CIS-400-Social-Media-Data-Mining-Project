Regional Attitudes Toward Weather Conditions on Social Media Across the U.S.
============================================================================

Team Members: Marissa Orsley, Xiao Lin Zheng, Manu Shergill, Sonya Yim

Objective: This project aims to analyze how people’s attitudes are affected by various weather conditions across different regions in the United States. By examining social media posts from specific states that represent different climate zones (hot, cold, temperate) we will explore how sentiments vary toward weather conditions (sunny, rainy, snowy,cloudy).
The study will focus on states representing diverse climates to capture a variety of emotional responses—Hot regions: Florida, Hawaii; Cold regions: Alaska, North Dakota; Temperate regions: Kansas, Kentucky. By analyzing posts that mention weather-related keywords, we will use sentiment analysis to classify attitudes (positive, negative, or neutral) and determine whether certain weather conditions are associated with different emotional responses across these regions. This approach will help us understand regional attitudes toward weather conditions and uncover potential climate-based preferences in how people react to various weather experiences.

![planting-climate-region1](https://github.com/user-attachments/assets/ee31aecc-1431-447b-b6f9-f0954524add9)

The timestamp will be from 2023-Present.
- Hot regions: Florida, Hawaii
- Cold regions: Alaska, North Dakota
- Temperate regions: Kansas, Kentucky

  
## Guide to Setting Up Reddit API
- First go to Reddit Developer Portal:
   https://www.reddit.com/login/?dest=https%3A%2F%2Fwww.reddit.com%2Fprefs%2Fapps

  You will see this page, please sign in or create an account.
  ![image](https://github.com/user-attachments/assets/3ff13e1e-6f56-4108-8e48-ba9938976910)

- Then you will come to this page click on "create another app..."
  ![image](https://github.com/user-attachments/assets/a6ee7761-8c29-4e4d-bc86-14436e3e633a)

- Now you will have to fill out a few things
  - name: give any name you want for the application
  - select 'script'
  - description: optional, you can write what this application is used for
  - redirect uri: put in 'http://localhost:8080'
  - Check 'I'm not a robot'
  - click 'create app' button
![image](https://github.com/user-attachments/assets/1b3b7ac0-8c58-44f4-8858-cfc9182fcd76)

- After you create the app you will have this on the page the highlighted part are important information you will need to connect to the Reddit API.
![image](https://github.com/user-attachments/assets/942af98f-72ca-4437-84b1-452e4912a544)


You are all ready now go into the "Social Media Posts Data Retrieval" folder and download the "collect_RedditPosts.py" file.


## Running the Code

- Just download the whole zip folder for this project and run in the following sequence below:
  
- Open 'Social Media Posts Data Retrieval' folder and run the 'collect_RedditPosts.py' to collect the 12 dataset (total of 24 dataset, 12 as csv and 12 as db, but both data are the same just the file type is different) to start with. Remember to read the "Guide to Setting Up Reddit API" for it to work properly.
  
- After having the 12 dataset open the 'Data Preprocessing' folder and run the 'data_preprocessing.py' to clean and organize the datasets. Remember to replace the csv file name of the dataset you are working on (becuase we seperate the data amoungst the four of us so we make the code to only read one csv file at a time). 

- With the preprocessed dataset you can run the 'emotion_detection.py' first in the "Emotioin Detection" folder for 12 new dataset that include emotion and then run the 'emotion_detection_analysis.py' to analyze the emotion analysis of our dataset with graphs.

- Next open up 'VADER Sentiment Analysis' to conduct the sentiment analysis for the 12 db dataset from the preprocessed data the one in the format of 'clean_(region)_region_(weather)Data.db' (we already have a copy of the preprocessed data in the "preprocessData" folder) and get the new 12 dataset with the sentiment info for them.

- Then you can open up 'Final Analysis and Vizualization Graphs' folder and rin 'regional_analysis.py' where it will create a 'region_analysis.csv' that analyze the 12 vader dataset into one csv file for later used for creating vizualization graphs of our findings. For the vizualization graph for the final analysis run 'graphics_by_region.py'.

- Lastly, you can open 'ML and roBERTa Sentiment Analysis' folder and run ml_analysis.py' and 'roBERTa_sentiment.iypnb' (in Google Colab) the preprocessed data from before is also saved in the 'preprocessedData' folder so just make sure you have that folder when you run the program.

- Also, you can open the folder 'Word Cloud Vizualization" to run 'makeVisualization1.py' (for SabarChart.png) and 'makeVizualization2.py' (for word clouds png) just make sure to change the file path with the preprocessed dataset you wanted to create for.
