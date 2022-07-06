import config
import tweepy
from textblob import TextBlob
import plotly.express as px
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer


auth = tweepy.OAuthHandler(config.API_KEY,config.API_SECRET_KEY)
auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def percentage(part, whole):
    return 100 * float(part) / float(whole)

def getInput(): #gets keyword and number of tweets to analyze then searches Twitter
    global keyword
    global noOfTweet
    global tweets
    keyword = input('Please enter keyword or hashtag to search: ')
    noOfTweet = int(input('Please enter how many tweets to analyze: '))
    tweets = tweepy.Cursor(api.search, q=keyword).items(noOfTweet)

# Sentiment Analysis
def sentiment_analysis():
    positive = int(0)
    negative = int(0)
    neutral = int(0)
    polarity = int(0)
    tweet_list = []
    neutral_list = []
    negative_list = []
    positive_list = []
    neutral_list2 = []
    negative_list2 = []
    positive_list2 = []
    for tweet in tweets:

        tweet_list.append(tweet.text)
        analysis = TextBlob(tweet.text)
        score = SentimentIntensityAnalyzer().polarity_scores(tweet.text) # returns dict with neg, neu, pos, & compound as keys
        neg = score["neg"] #sets variable to key neg from score
        neu = score["neu"]
        pos = score["pos"]
        comp = score["compound"]
        polarity += analysis.sentiment.polarity #gets polarity(how neg or pos from TextBlob)

        #checks if tweet is neg, pos, or neutral by comparing numerical value from score
        if neg > pos:
            negative_list.append(tweet.text)
            negative_list2.append('negative')
            negative += 1
        elif pos > neg:
            positive_list.append(tweet.text)
            positive_list2.append('positive')
            positive += 1
        elif pos == neg:
            neutral_list.append(tweet.text)
            neutral_list2.append('neutral')
            neutral += 1

    positive = percentage(positive, noOfTweet)
    negative = percentage(negative, noOfTweet)
    neutral = percentage(neutral, noOfTweet)

    #Number of Tweets (Total, Positive, Negative, Neutral)
    tweet_list = pd.DataFrame([tweet_list])
    neutral_list = pd.DataFrame(neutral_list)
    negative_list = pd.DataFrame(negative_list)
    positive_list = pd.DataFrame(positive_list)

    tweet_list.drop_duplicates(inplace=True)
    new_list = negative_list2
    new_list.extend(positive_list2)
    new_list.extend(neutral_list2)
    sentiment_list = pd.DataFrame({'Sentiment': new_list})
    sentiment_list = sentiment_list['Sentiment'].value_counts() \
        .to_frame('count').rename_axis('Sentiment') \
        .reset_index()
    long_df = sentiment_list
    fig = px.bar(long_df, x="Sentiment", y="count", title="Tweet Sentiment")
    fig.show()


if __name__ == '__main__':
    getInput()
    sentiment_analysis()
