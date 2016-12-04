import sys
import os
from geo import GeoPosition
from state import load_states
from country import Country
from parse import load_sentiments
import json
from tweet import Tweet
from colors import get_sentiment_color
import ast


#TWEET_FILES = ["tweets_with_time.json", "tweets_with_time_2.json", "tweets_with_time_3.json", "tweets_with_time_4.json"]
TWEET_FILES = ["tweets.json", "tweets2.json", "tweets3.json", "tweets4.json", "tweets5.json"]
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
        state_totals = dict()
        for tweet in self.tweets:
            if all(query_word.lower() in tweet.message().lower() for query_word in query_list):  # if every query word is in the tweet
                sent = self.weigh_message(tweet.message().lower())
                place = self.place_tweet(tweet.position())
                if sent != -1:  # word was actually weighted
                    if place not in state_totals:
                        state_totals[place] = [0, 0]
                    state_totals[place][0] += sent  # total sentiment value
                    state_totals[place][1] += 1  # total number of tweets from state

        for state in self.states:
            if state.abbrev() in state_totals:
                average_sent = state_totals[state.abbrev()][0] / state_totals[state.abbrev()][1]
                self.usa.setFillColor(state.abbrev(), get_sentiment_color(average_sent))
                print(state.abbrev(), state_totals[state.abbrev()][1])
            else:
                self.usa.setFillColor(state.abbrev(), get_sentiment_color(None))

    def place_tweet(self, position):
        min_dist = 999999999999  # a really big number
        close_state = None
        geo_pos = GeoPosition(position[1], position[0])
        for state in self.states:
            dist = state.centroid().distance(geo_pos)
            if dist < min_dist:
                min_dist = dist
                close_state = state

        return close_state.abbrev()  # using abbrev as keys instead of reference makes debugging a bit easier

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
        total /= num_words

        return total


def load_tweets():
    tweets = set()
    for tweet_file in TWEET_FILES:
        with open(DATA_LOCATION + tweet_file) as data_file:
            for line in data_file:
                data = json.loads(line)
                tweet = Tweet(data['text'], None, data['coordinates'])
                tweets.add(tweet)
    return tweets

if __name__ == "__main__":
    query = None
    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        print("error, searching with default query")
        query = "['i']"

    if query[0] =='[':  # if the user input a list
        query = ast.literal_eval(query)
    else:
        query = [query]  # if the user input a string

    print query

    sa = SentimentAnalysis()
    sa.show_country()
    sa.update_sentiments(query)

