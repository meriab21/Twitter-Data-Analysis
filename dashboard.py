import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import re
from wordcloud import WordCloud, STOPWORDS
import plotly.express as px
from utils import (remove_mentions,
remove_hashtags,
remove_unfinished_letters,
remove_RT)

st.title(' Dashboard ')

DATA_URL = ('data\processed_tweet_data.csv')

def loadData(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    return data


data_load_state = st.text('Loading data...')
data = loadData(10000)

data_load_state.text('Loading data...success!')

def barChart(data, title, X, Y):
    title = title.title()
    st.title(f'{title} Chart')
    msgChart = (alt.Chart(data).mark_bar().encode(alt.X(f"{X}:N", sort=alt.EncodingSortField(field=f"{Y}", op="values",
                order='ascending')), y=f"{Y}:Q"))
    st.altair_chart(msgChart, use_container_width=True)





def polarity_pie():
    def classify_polarity(polarity):
        polarity = float(polarity)
        # polarity = -1 if type(polarity)==str else float(polarity)
        if polarity < 0:
            return "negative"
        elif polarity > 0:
            return "positive"
        else:
            return "neutral"
    data = loadData(1000)
    data = data[data['polarity']!="ko"]
    # data = data[data['polarity']!="ko"]
    data["polarity_label"] = data['polarity'].apply(lambda x: classify_polarity(x))
    data.dropna(subset=["polarity"],inplace=True)
    fig = px.pie(data,names="polarity_label",title ="Polarity count", width=500, height=350)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig)


def stBarChart():
    df = loadData(1000)
    dfCount = pd.DataFrame({'Tweet_count': df.groupby(['original_author'])['original_text'].count()}).reset_index()
    dfCount["original_author"] = dfCount["original_author"].astype(str)
    dfCount = dfCount.sort_values("Tweet_count", ascending=False)

    num = st.slider("Select number of Rankings", 0, 50, 5)
    title = f"Top {num} Ranking By Number of tweets"
    barChart(dfCount.head(num), title, "original_author", "Tweet_count")

def wordCloud():
    df = loadData(1000)
    cleanText = ''
    df["cleaned_text"] = df["original_text"].apply(lambda x: re.split('https:\/\/.*', str(x))[0])
    df["cleaned_text"] = df["cleaned_text"].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))
    df["cleaned_text"] = df["cleaned_text"].apply(lambda x: x.replace('\n',''))
    df["cleaned_text"] = df["cleaned_text"].apply(lambda x: remove_hashtags(x) )
    df["cleaned_text"] = df["cleaned_text"].apply(lambda x: remove_mentions(x) )
    df["cleaned_text"] = df["cleaned_text"].apply(lambda x: remove_unfinished_letters(x))
    df["cleaned_text"] = df["cleaned_text"].apply(lambda x: remove_RT(x))
    for text in df['cleaned_text']:
        tokens = str(text).lower().split()

        cleanText += " ".join(tokens) + " "
    weird_words =  ['s', 'kur', 'u', 't', 'rt', 'ti', 'o', 'd', 'vk', 'to', 'co',
                    'dqlw', 'z', 'nd', 'm', 'de', 'du', 'le', 'und', 'die', 'der', 'will', 'nicht']
    stopwords = STOPWORDS.union(weird_words)
    wc = WordCloud(stopwords=stopwords, width=650, height=450, background_color='white', min_font_size=5).generate(cleanText)
    st.title("Tweet Text Word Cloud")
    st.image(wc.to_array())



def langPie():
    df = data
    dfLangCount = pd.DataFrame({'Tweet_count': df.groupby(['lang'])['original_text'].count()}).reset_index()
    dfLangCount["lang"] = dfLangCount["lang"].astype(str)
    dfLangCount = dfLangCount.sort_values("Tweet_count", ascending=False)
    dfLangCount.loc[dfLangCount['Tweet_count'] < 10, 'lang'] = 'Other languages'
    st.title(" Tweets Language pie chart")
    fig = px.pie(dfLangCount, values='Tweet_count', names='lang', width=500, height=350)
    fig.update_traces(textposition='inside', textinfo='percent+label')

    colB1, colB2 = st.columns([2.5, 1])

    with colB1:
        st.plotly_chart(fig)
    with colB2:
        st.write(dfLangCount)

st.subheader('Raw data')
st.write(data)

st.title("Anlyzed Data Display")
# selectHashTag()
st.markdown("<p style='padding:10px; background-color:#ffffffff;color:#00ECB9;font-size:16px;border-radius:10px;'>Section Break</p>", unsafe_allow_html=True)
# selectLocAndAuth()
st.title("Data Visualizations")
wordCloud()
with st.expander("Show More Graphs"):
    stBarChart()
    langPie()
    polarity_pie()