from msvcrt import setmode
import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from extract_dataframe import read_json, TweetDfExtractor


st.title('Tweet sentiment analysis')
st.markdown("THis is all about tweet data sentiment analysis")

st.sidebar.title("sentiment analiysis of twitter data")
st.sidebar.markdown("We will analyse tweets")

data = pd. read_json(r"C:\Users\meron\Desktop\Week0\Twitter-Data-Analysis\data\Economic_Twitter_Data.json")
tweet = TweetDfExtractor(tweets_list)
tweet_df = tweet.get_tweet_df() 
if st.checkbox("Show Data"):
    st.write(data.head(50))
st.sidebar.subheader("Tweets analyser")
tweets = st.sidebar.radio('sentiment type', ('positive', 'negative', 'neutral'))
st.write(data.query('sentiments==@tweets')[['text']].sample(1).iat[0,0])
st.write(data.query('sentiments==@tweets')[['text']].sample(1).iat[0,0])
st.write(data.query('sentiments==@tweets')[['text']].sample(1).iat[0,0])

select = st.sidebar.selectionbox('Visulization of Tweets', ['Histogtam', 'Pie Chard'], key =1)

sentiment= data["sentiments"].value_counts()
sentiment = pd.tweet({'Sentiment': sentiment.index, 'Tweets':sentiment.value})
st.markdown("sentiment count")
if select == "Histogram":
    fig = px.bar(sentiment, x='Sentiment', y='Tweets', color = 'Tweets', height = 500)
    st.plotly_chart(fig)
else:
    fig = px.pie(sentiment, value= 'Tweets', name= 'Sentiment')
    st.plotiy