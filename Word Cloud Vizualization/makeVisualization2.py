# Creating word clouds for the preprocessed data for vizualization
#
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load the data
# Remember to change the file_path to yours where you have stored the preprocessed data of the format clean_(region)_region_(weather)Data.csv
#
file_path = r"C:\Users\mlors\PycharmProjects\cis400Project\cleanData\clean_temperate_region_sunnyData.csv" 
data = pd.read_csv(file_path)

# Extract the third keyword from the 'KEYWORD' column
data["Third_Keyword"] = data["KEYWORD"].apply(lambda x: x.split(",")[2].strip() if len(x.split(",")) >= 3 else None)

# Combine all third keywords into a single string
third_keyword_text = " ".join(data["Third_Keyword"].dropna())

# Generate the word cloud
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(third_keyword_text)

# Plot the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Sunny Weather in Temperate Regions")
plt.show()
