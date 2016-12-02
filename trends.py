import sys
import os
import ast
from state import load_states
from country import Country
from parse import load_sentiments
import json
from tweet import Tweet
from colors import get_sentiment_color


TWEET_FILES = ["tweets_with_time.json", "tweets_with_time_2.json", "tweets_with_time_3.json", "tweets_with_time_4.json"]
DATA_LOCATION = "data" + os.sep


class SentimentAnalysis:
    def __init__(self):
        self.sentiments = load_sentiments()
        self.states = load_states()
        self.tweets = load_tweets()
        self.usa = None  # variables should always be defined in __init__

    def show_country(self):  # function names should not have capital letters
        self.usa = Country(self.states, 1200)

    def update_sentiments(self, query_list):
        average_sent = 0
        num = 0
        for tweet in self.tweets:
            if all(query_word in tweet.message() for query_word in query_list):  # tests if all of the query words are in a tweet
                print tweet.message()
                sent = self.weigh_message(tweet.message())
                if sent != -1:
                    average_sent += sent
                    num += 1

        average_sent /= num
        print average_sent

    def weigh_message(self, message):
        total = 0
        split_str = message.split()
        num_words = 0
        for word in split_str:
            if word in self.sentiments:
                num_words += 1
                total += self.sentiments[word]
        if not num_words:
            return -1

        return total


def load_tweets():
    tweets = set()
    for tweet_file in TWEET_FILES:
        with open(DATA_LOCATION + tweet_file) as data_file:
            for line in data_file:
                data = json.loads(line)
                tweet = Tweet(data['text'], data['created_at'], data['coordinates'])
                tweets.add(tweet)
    return tweets

if __name__ == "__main__":
    query = None
    if len(sys.argv) > 1:
        query = sys.argv[1:]
    else:
        query = ["hillary"]

    print query

    sa = SentimentAnalysis()
    sa.update_sentiments(query)
    #sa.showCountry()
