import sys
import os
from geo import GeoPosition
from state import load_states
from country import Country
from parse import load_sentiments
import json
from tweet import Tweet
from colors import get_sentiment_color


TWEET_FILES = ["tweets_with_time.json", "tweets_with_time_2.json", "tweets_with_time_3.json", "tweets_with_time_4.json"]
#TWEET_FILES = ["tweets.json", "tweets2.json", "tweets3.json", "tweets4.json", "tweets5.json"]
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
        state_totals = dict()
        for tweet in self.tweets:
            if all(query_word in tweet.message() for query_word in query_list):  # if every query word is in the tweet
                sent = self.weigh_message(tweet.message())
                place = self.place_tweet(tweet.position())
                if sent != -1:  # word was actually weighted
                    if place not in state_totals:
                        state_totals[place] = [0, 0]
                    state_totals[place][0] += sent
                    state_totals[place][1] += 1
                    num += 1

        for state in self.states:
            if state.abbrev() in state_totals:
                state_totals[state.abbrev()][0] /= float(state_totals[state.abbrev()][1])
                self.usa.setFillColor(state.abbrev(), get_sentiment_color(state_totals[state.abbrev()][0]))
                print(state.abbrev(), state_totals[state.abbrev()][1])
            else:
                self.usa.setFillColor(state.abbrev(), get_sentiment_color(None))
        print num
    def place_tweet(self, position):
        min_dist = 9999999999
        close_state = None
        geo_pos = GeoPosition(position[0], position[1])
        for state in self.states:
            deltax = position[0] - state.centroid().longitude()
            deltay = position[1] - state.centroid().latitude()
            dist = deltax * deltax + deltay * deltay
            if dist < min_dist:
                min_dist = dist
                close_state = state

        return close_state.abbrev()

    def weigh_message(self, message):
        total = 0
        split_str = message.split(' ')
        num_words = 0
        for word in self.sentiments:
            if word in message:
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
                tweet = Tweet(data['text'], None, data['coordinates'])
                tweets.add(tweet)
    return tweets

if __name__ == "__main__":
    query = None
    if len(sys.argv) > 1:
        query = sys.argv[1:]
    else:
        query = ["bieber"]

    print query

    sa = SentimentAnalysis()
    sa.show_country()
    sa.update_sentiments(query)

