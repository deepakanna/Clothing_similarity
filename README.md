# Clothing_similarity
## 1. Introduction
 The goal of this project is to create a machine learning model capable of receiving text describing a clothing item and returning a ranked list of links to similar items from different websites. The solution is a function deployed on Google Cloud that accepts a text string and returns JSON responses with ranked suggestions. Also a Flask framework is used to 
##  2.Collect and preprocess data.
 Web scraping tools are used to gather a dataset of clothing item descriptions.
 The text data is preprocessed by cleaning it.

## 3.Measure similarity.
 A method is developed for extracting useful features from the text descriptions.
 The similarity between the input text and the texts in the database is computed. 

## 4.Return ranked results.
 A function is designed that accepts a text string, extracts its features, computes similarities with the items in the database, ranks them based on similarity, and returns the URLs of the top-N most similar items.

## 5. Deploy the function.
 The function is deployed on Google Cloud Functions or Google Cloud Run.

