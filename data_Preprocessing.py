# TEMPLATE FOR DATA PREPROCESSING ON COLLECTED CSV DATA FILE----------------------------------------------------------------
# Version:1
#
# This Python program will perform data preprocessing to the csv files that you have created from "collect_RedditPosts.py".
# The reason we are only performing data preprocessing on the csv file because the csv and db file are exactly the same
# so, I choose to just do it on the csv file and later at the end create a new db file from the filtered csv file from
# thi program.
#
# For this Program to work you have to download the 'pandas package' and the 'NLTK package'
#       Pandas: !pip install pandas
#       NLTK: !pip install nltk
#
#----------------------------------------------------------------------------------------------------------------------------
import nltk
import pandas as pd

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# download nltk corpus (first time only)
import nltk
nltk.download('all')

# Importing CSV file----------------------------------------------------------------------------------------------------
# Make sure to replace the 'read_csv' with the corresponding
#
csvData = pd.read_csv('hot_region_sunnyData.csv')
print(f"Total Data: {len(csvData)}")


# Normalize Data--------------------------------------------------------------------------------------------------------
# Have 'Title' and 'TEXT' to become all lowercase which helps with our further filtering are identified more accurately
#
csvData['TITLE'] = csvData['TITLE'].str.lower()
csvData['TEXT'] = csvData['TEXT'].str.lower()


# Convert UTC to Date time----------------------------------------------------------------------------------------------
# https://www.geeksforgeeks.org/how-to-convert-datetime-to-date-in-pandas/
# https://www.geeksforgeeks.org/how-to-drop-one-or-multiple-columns-in-pandas-dataframe/
#
csvData['DATE'] = pd.to_datetime(csvData['UTC']).dt.date            # Create a new column 'DATE' by vonverting UTC to
                                                                    # date only.
csvData = csvData.drop('UTC', axis=1)                         # Remove the 'UTC' column


# Organize Data By State & Date-----------------------------------------------------------------------------------------
csvData = csvData.sort_values(by=['STATE', 'DATE'])


# Re-assign 'ID' to Each Row--------------------------------------------------------------------------------------------
# Need to reassign 'ID' to each row of data because after organizing the data by 'DATE' the 'ID' number is not organized
# in a pattern, so we have to reassign the 'ID' number again.
#
csvData = csvData.reset_index(drop=True)
csvData['ID'] = range(1, len(csvData) + 1)


# Remove Duplicate Posts------------------------------------------------------------------------------------------------
# Searching for duplicate 'Title' and 'Text' of the csv file and remove them and keeping the first filtered duplicate
# data in csv file.
# https://www.geeksforgeeks.org/python-pandas-dataframe-drop_duplicates/
#
csvData = csvData.drop_duplicates(subset=['TITLE', 'TEXT'],keep='first')
print(f"Total Data (Remove Duplicate): {len(csvData)}")

# Remove 'TEXT' < 20 Characters-----------------------------------------------------------------------------------
csvData = csvData[csvData['TEXT'].str.len() >= 20]

print(f"Total Data (Remove 'TEXT' < 20 Characters): {len(csvData)}")


# Remove Data with Missing Values---------------------------------------------------------------------------------------
# https://www.geeksforgeeks.org/drop-rows-from-pandas-dataframe-with-missing-values-or-nan-in-columns/
#
csvData = csvData.dropna()
print(f"Total Data (Remove Missing Data): {len(csvData)}")


# Remove Special Characters & URLs From 'TITLE' & 'TEXT'----------------------------------------------------------------
# https://www.geeksforgeeks.org/pandas-remove-rows-with-special-characters/
#
remove_url = r'http\S+|www.\S+'                     # Define URL's template
remove_specialChar = r'[^A-Za-z0-9\s]+'             # Define characters from A-Z, a-z, 0-9, and whitespace characters to
                                                    # remove any special characters that are not included within these 3
                                                    # sections.

# Remove URLs
csvData['TEXT'] = csvData['TEXT'].str.replace(remove_url, '', regex=True)
csvData['TITLE'] = csvData['TITLE'].str.replace(remove_url, '', regex=True)

# Remove Special Characters
csvData['TEXT'] = csvData['TEXT'].str.replace(remove_specialChar, '', regex=True)
csvData['TITLE'] = csvData['TITLE'].str.replace(remove_specialChar, '', regex=True)

# Remove Excessive Whitespace Characters
csvData['TEXT'] = csvData['TEXT'].str.strip()
csvData['TITLE'] = csvData['TITLE'].str.strip()

print(f"Total Data (Remove Special Characters): {len(csvData)}")


# NLTK Preprocessing: Tokenization, Stop Word Removal, and Lemmatization------------------------------------------
# https://www.datacamp.com/tutorial/text-analytics-beginners-nltk
#
def NLTK_preprocess(text):
    if not isinstance(text, str):       # Check if string
        return ''

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stop words
    filtered_tokens = [word for word in tokens if word not in stopwords.words('english')]

    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

    # Join the tokens back into a string
    preprocessed_text = ' '.join(lemmatized_tokens)
    return preprocessed_text

# Apply to 'TITLE' & 'TEXT'
csvData['TITLE'] = csvData['TITLE'].apply(NLTK_preprocess)
csvData['TEXT'] = csvData['TEXT'].apply(NLTK_preprocess)

# Save Changes to CSV & DB File-----------------------------------------------------------------------------------------
csvData.to_csv('test.csv', index=False)
