#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd   
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def scrapper():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.youtube.com/watch?v=rfscVS0vtbw')
    
    driver.execute_script('window.scrollTo(1, 500);')

    #now wait let load the comments
    time.sleep(7)
    
    #scroll window from x-cordinaate 0 to y-cordinate-3000
    driver.execute_script('window.scrollTo(1, 3000);')
    
    comment_div=driver.find_element_by_xpath('//*[@id="contents"]')
    
    #this is a list
    comments=comment_div.find_elements_by_xpath('//*[@id="content-text"]')
    #create list of comments
    comments_list = []
    #create list to store score of comments
    comment_score = []
    print("Comments : ")
    for comment in comments:
        print("\n",comment.text)
        comments_list.append(comment.text)
        
        #calculate score of that comment
        comment_score.append(analyze(comment.text))
        
    #create a dictionary with all the values
    data = {'Comment':comments_list,'Sentiment':comment_score}
    df = pd.DataFrame(data, columns=['Comment','Sentiment'])
    
    totalSentiment(df)
    
def analyze(comment):

    #analyzing the data
    score = SentimentIntensityAnalyzer().polarity_scores(comment)
    
    if score['compound'] >= 0.05 :
        sentiment = "Positive"
    elif score['compound'] <= - 0.05 :
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    return sentiment
      
def totalSentiment(df):
    #calculate the percentage of sentiments
    sentiment_list = df.loc[:,'Sentiment']
    count_Positive = 0
    count_Neutral = 0
    count_Negative = 0
    count = 0
    for sentiment in sentiment_list:
        if(sentiment == 'Positive'):
            count_Positive +=1
        elif(sentiment == 'Negative'):
            count_Negative +=1
        else:
            count_Neutral +=1
        
        count+=1
        
    if(count != 0):
        print("\nPositivity percentage : ",(count_Positive/count)*100)
        print("\nNegativity percentage: ",(count_Negative/count)*100)
        print("\nNeutrality percentage: ", (count_Neutral/count)*100)
    else:
        print("Issue with scrapping. Please try again!")
    
scrapper()