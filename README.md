# Clothing_similarity
## 1. Introduction
 The goal of this project is to create a machine learning model capable of receiving text describing a clothing item and returning a ranked list of links to similar items from different websites. The solution is a function deployed on Google Cloud that accepts a text string and returns JSON responses with ranked suggestions. Also a Flask web application framework is used to suggest a ranked list of URLs similar to the text given by the user.
 
##  2.Collect and preprocess data.
- Web scraping tools are used to gather a dataset of clothing item descriptions. BeautifulSoup is the python web scraping tool used to scrap data from the clothing store websites https://instore.co.in and www.pluss.in. The dataset has attributes sno as index, description and the link of the website from where it is scraped.The data scraped is saved as a csv file. 
- The scraped data is loaded from csv file and analysed to understand the shape of the data, the null values present. The null values are removed and the text data is cleaned. The description attribute is then tokenized and cleaned data is obtained by 
    * converting to lower case letters
    * removing special characters from the text, 
    * converting the sentences to tokens
    * removing stopwords 
    * and lemmatizing
 Hence, Useful features are extracted from the text descriptions.
 
## 3.Measure similarity.
 The similarity between the input text and the texts in the database is computed. CountVectorizer is used to convert preprocessed description text to numerical data. Cosine similarity is a measure of the similarity between two non zero vectors. The input text is also tokenized to obtain important features and converted to numerical data using countvectorizer. Cosine similarity is used to find the similarity between the input text and the description text in the dataset. 

## 4.Return ranked results
The similarity values are sorted in decending order to obtain the top similar description that matches the text data. The top 10 descriptions in the dataset that are similar to the input text are determined and the corresponding url of the website is obtained from the dataset. The urls obtained are serialized to json format and returned to the user. A flask web framework with a input text box and a button is used to input the text values for which similarity is to be otained. The button is used to call the function that retrieves the suggested urls.
 
## 5. Deploy the function
 The function is deployed on Google Cloud Functions. The URL is 
Pass the input text as parameter to the URL given as 

