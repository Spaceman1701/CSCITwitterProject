import sys
from state import load_states
from country import Country
from parse import load_sentiments
import json
from tweet import Tweet
from colors import get_sentiment_color


TWEET_FILES = ["tweets_with_time.json", "tweets_with_time_2.json", "tweets_with_time_3.json", "tweets_with_time_4.json"]
DATA_LOCATION = "data/"


class SentimentAnalysis:
    def __init__(self):
        self.sentiments = load_sentiments()
        self.states = load_states()
        self.tweets = load_tweets()

    def showCountry(self):
        self.usa = Country(self.states, 1200)

    #finish


def load_tweets():
    tweets = set()
    for tweet_file in TWEET_FILES:
        with open(DATA_LOCATION + tweet_file) as file:
            for line in file:
                data = json.loads(line)
                tweet = Tweet(data['text'], data['created_at'], data['coordinates'])
                tweets.add(tweet)
    return tweets


if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
        print query
    else:
        print "error"

    sa = SentimentAnalysis()
    sa.showCountry()
    #finish