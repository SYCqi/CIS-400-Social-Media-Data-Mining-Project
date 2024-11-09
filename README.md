Regional Attitudes Toward Weather Conditions on Social Media Across the U.S.
============================================================================

Objective: This project aims to analyze how people’s attitudes are affected by various weather conditions across different regions in the United States. By examining social media posts from specific states that represent different climate zones (hot, cold, temperate) we will explore how sentiments vary toward weather conditions (sunny, rainy, snowy,cloudy).
The study will focus on states representing diverse climates to capture a variety of emotional responses—Hot regions: Florida, Hawaii; Cold regions: Alaska, North Dakota; Temperate regions: Kansas, Kentucky. By analyzing posts that mention weather-related keywords, we will use sentiment analysis to classify attitudes (positive, negative, or neutral) and determine whether certain weather conditions are associated with different emotional responses across these regions. This approach will help us understand regional attitudes toward weather conditions and uncover potential climate-based preferences in how people react to various weather experiences.
![planting-climate-region1](https://github.com/user-attachments/assets/ee31aecc-1431-447b-b6f9-f0954524add9)

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
