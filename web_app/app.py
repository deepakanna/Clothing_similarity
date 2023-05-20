#Import the required libraries
import pandas as pd 
from bs4 import BeautifulSoup
import requests

import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.metrics.pairwise import cosine_similarity
import json

from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import nltk
nltk.download('stopwords')

import nltk
nltk.download('punkt')

import nltk
nltk.download('wordnet')
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form['message']
        result = process_message(text)  # Call your function here passing the text message
        return render_template('result.html', result=result)
    return render_template('index.html')

def process_message(text):
    suggested_URLs=Clothing_similarity_search("This is a stylish and comfortable t-shirt")
    # Implement your logic to process the text message here
    # This is just a sample function that returns the reversed message
    return suggested_URLs

def instore_db():
    base_url = "https://instore.co.in/collections/offers"
    page = 1
    all_links = []

    while True:
        url = base_url if page == 1 else f"{base_url}?page={page}"
   
    # Send a GET request to the URL
        response = requests.get(url)
   
    # Create a BeautifulSoup object from the response text
        soup = BeautifulSoup(response.text, "html.parser")
   
    # Find all elements with class 'grid-product__link'
        link_elements = soup.find_all("a", class_="grid-product__link")
   
    # If no links found, exit the loop
        if not link_elements:
            break
   
    # Extract the href attribute from each link element
        for link in link_elements:
            href = link.get("href")
            all_links.append(href)
   
    # Move to the next page
        page += 1
    des=[]
    lk1=[]
    

# Print all the collected links
    #for link in all_links:
        #print(link)
    for link in all_links:
        lk="https://instore.co.in/"+link
        #print(lk)
        #list1=[]
        #for i in all_links[0:10]:
        r=requests.get(lk)
        #print(r.text)
        soup1=BeautifulSoup(r.content,"html.parser")
        #print(soup1.title.getText())
        cloth=soup1.find('h1',{'class':'h2 product-single__title'})
        #print(cloth)
        for a in cloth:
            title=a.getText().strip().split('\n')
        
        cloth1=soup1.find("div",{'class':'product-single__description rte'})
        desc=cloth1.getText().strip()
        tt=' '.join(title)
        des.append([tt+desc])
        lk1.append(lk)
    df=pd.DataFrame(des,columns=['Description'])
    df['link']=lk1
            #color=soup1.find("span",{'class':'Fabric'})
        #print(cloth)
        #print(color.getText().strip())
        
        #list1.append(data)
        #df['prod_desc']=
        #df['link']=i
        #list_t=list_t.append(list_d)
    return df
def pluss_db():

    base_url = "https://www.pluss.in/men"
    page = 1
    all_links = []

    while page<30:
        url = base_url if page == 1 else f"{base_url}?page={page}"

        # Send a GET request to the URL
        response = requests.get(url)

        # Create a BeautifulSoup object from the response text
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all the <a> tags in the soup
        link_elements = soup.find_all("a")

        # If no links found, exit the loop
        if not link_elements:
            break

            # Iterate over the link elements and extract the href attribute
        for link in link_elements:
            href = link.get("href")

            # Check if the link starts with the desired base URL and ends with ".html"
            if href and href.startswith(base_url) and href.endswith(".html"):
                if len(all_links)<20:
                    print(href)
                    all_links.append(href)

    # Move to the next page
        page += 1

# Print all the collected links
    des=[]
    lk1=[]
    # Print all the collected links
    for link in all_links:
        print(link)
        list1=[]
        for i in all_links:
            r=requests.get(i)
            soup1=BeautifulSoup(r.text,"html.parser")
    #print(soup1.title.getText())
            cloth=soup1.find('div',{'class':'prodDis'})
            title=cloth.getText().strip().split('\n')
            price=soup1.find("span",{'class':'prodFinalPrice'})
            price1=price.getText().strip().split(' ')
            tt=' '.join(title)
            des.append([tt])
            lk1.append(link)
    #color=soup1.find("span",{'class':'Fabric'})
    #print(cloth)
    #print(color.getText().strip())
           # list1.append(title)
           # list1.append(i)
        df=pd.DataFrame(des,columns=['Description'])
        df['link']=lk1
    #list1.append(data)
    #df['prod_desc']=
    #df['link']=i
    return df   

def create_database():
    db_plus=pluss_db()
    #db_plus['sno']=range(1,db_plus.shape[0]+1)
    db_instore=instore_db()
    #db_instore['sno']=range(1,db_instore.shape[0]+1)
    db=pd.concat([db_instore,db_plus],axis=0)
    db['sno']=range(1,db.shape[0]+1)
    return db

def data_analysis(df):
    #print("The shape of the DataFrame is ",df.shape)
    #print("The null values in the DataFrame are:")
    #print(df.isnull().sum())
    #print("There may be some null strings in the Description which has to be replaced as nan")
    df['Description']=df['Description'].replace("",np.nan)
    #print(df['Description'].isnull().sum())
    df=df.dropna()
    #print("The Shape of the DataFrame after null values are removed:",df.shape)

def tokenize(text):
    '''
    INPUT:
    text: (String) - the Text which is to be tokenized
    
    OUTPUT:
    clean_tokens - (String) Clean Tokens 
    
    Process:
    The text is converted to lower case and any special characters are removed. The sentence is then converted to tokens 
    and stopwords are removed. WordNetlemmatizer is applied to lemmatize and clean tokens are obtained.
    '''
    #col=df_content['doc_full_name']
    #print(col)
    clean_tokens=[]
    #for ln in text:
        #print(ln)
    sent=str(text)
    sent=sent.lower()
    sent1=re.sub('[0-9]','',sent)
    sp=re.compile('<.*?(#-,)>')
    sent2=re.sub(sp,'',sent1)
    tokens=word_tokenize(sent2)
    words=[w for w in tokens if len(w)>3 if w not in stopwords.words('english')]
    lemmatizer=WordNetLemmatizer()
    for tok in words:
        cl=lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(cl)
    clean_tokens=' '.join(clean_tokens)  # s=set(clean_tokens)
    return clean_tokens

def similarity_rank(df,inp_text):
    '''
    INPUT:
    df: (DataFrame) - the DataFrame containing the scraped data from websites
    inp_text: (String) -  The input string for which similar url's are to be determined
    
    OUTPUT:
    suggested_urls - json - A json object of suggested URL's that are similar to the input text
    
    
    '''
    
    input_cl=tokenize(inp_text)
    #print(input_cl)
    cv=CountVectorizer()
    word_count=cv.fit_transform(df['Description'])
    #print(word_count.shape)
    cv.fit(df['Description'])
    inp_vect=cv.transform([input_cl])
    ds_vect=cv.transform(df['Description'])
    sim1=cosine_similarity(inp_vect,ds_vect)
    sort_ind=sim1.argsort()[0][::-1]
    #print(sort_ind)
    sugg=[]
    
    for i in sort_ind[:15]:
        u=df[df['sno']==i].link.values[0]
        if u not in sugg:
            sugg.append(u)
    suggested={
        'suggestions':sugg
        
    }
    
    
    suggested_urls=json.dumps(suggested,indent=1)
    #sg=sorted(set(map(tuple,sugg)),reverse=True)
    return suggested_urls

def Clothing_similarity_search(input_text):
     
    df_final=create_database()
    #df_final=df
    data_analysis(df_final)
    df_final['Description']=df_final['Description'].apply(tokenize)

    urls=similarity_rank(df_final,input_text)
    return urls


if __name__ == '__main__':
    app.run(debug=True)
