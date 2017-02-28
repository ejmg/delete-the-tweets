"""
this script deletes tweets off of your timeline
"""

from secrets import ACCESS_SECRET, ACCESS_TOKEN, CONSUMER_KEY, CONSUMER_SECRET
import tweepy as ty
from tweetIDS.handles import USER_NAMES
import time
import csv
import sys
from nltk.tokenize import TweetTokenizer


def setTwitterAuth():
    """
    obtains authorization from twitter API
    """
    # sets the auth tokens for twitter using tweepy
    auth = ty.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = ty.API(auth)
    return api


def handleLimit(cursor):
    while True:
        try:
            yield cursor.next()
        except ty.RateLimitError:
            print("sleeping! {}".format(time.localtime()))
            time.sleep(60 * 15)


def mineHomeTimeline(api):

    timeline = [status for status in
                handleLimit(ty.Cursor(api.user_timeline).items())]
    return timeline


def recordTweet(tweet, record):
    if hasattr(tweet, "retweeted_status"):
            record.write("id: {}, text: {}, favorites: {},"
                         " reply_tweet_ID: {}, quoted_status_id: {}, "
                         "quoted: {} \n"
                         .format(tweet.id,
                                 tweet.text,
                                 tweet.favorite_count,
                                 tweet.in_reply_to_screen_name,
                                 tweet.retweeted_status.id,
                                 tweet.retweeted_status.author.screen_name))
    else:

            record.write("id: {}, text: {}, favorites: {},"
                         " reply to userID: {} \n"
                         .format(tweet.id,
                                 tweet.text,
                                 tweet.favorite_count,
                                 tweet.in_reply_to_screen_name))


def check_names(csv_status, important):
    token = TweetTokenizer()
    tweet_tokens = token.tokenize(csv_status)
    for words in tweet_tokens:
        for key in USER_NAMES:
            if words[1:].lower() == key.lower():
                important = True
    return important


def retrieve_status(api, status_id):
    retrieved = False
    exists = True
    while not retrieved:
        try:
            status = api.get_status(status_id)
            print("status retrieved!")
            retrieved = True
            return status, exists
        except ty.RateLimitError as e:
            print(e)
            print("Sleeping!")
            time.sleep(60*15)
        except ty.TweepError as e:
            print(e)
            print("Tweet didn't exist, skipping!")
            exists = False
            retrieved = True
            status = None
            return status, exists


def delete_tweets(api, status, important, delete):
    while not important:
        try:
            api.destroy_status(status.id)
            print("Tweet destroyed!")
            delete += 1
            important = True
        except ty.RateLimitError as e:
            print(e)
            print("Sleeping!")
            time.sleep(60 * 15)
        except ty.TweepError as e:
            print(e)
            print("Non-Limit Error while deleting, skipping!")
            important = True


if __name__ == "__main__":

    api = setTwitterAuth()
    user = api.me()
    try:
        csvfile = open(file="./tweets/tweets.csv", mode="r")
        reader = csv.reader(csvfile, delimiter=",")
    except Exception as e:
        print("Error accessing tweets.csv, aborting. Error: {}".format(e))
    else:
        confirmation = False
        print(
            """
Successfully accessed csv file, about to begin processing.
Before continuing, have you entered the keywords to ignore? Other options?

Deleting tweets is a permanent process and cannot be undone once
finished. Please enter "yes" to continue, else enter "no" now or simply
press ^C or ^D to abort the process at any time.
            """)
        answer = input()
        if answer.lower() != "yes":
            print("Confirmation failed, aborting process. Retry when ready.")
            sys.exit()
        print("Confirmation! Delete the tweets!")
        time.sleep(3)
        count = 0
        delete = 0
        important = False
        for row in reader:
            if count == 0:
                count += 1
                continue
            else:
                # index 0 = ID, index 5 = text of status
                print("Tweet count: {}".format(count))
                print("Tweet id: " + row[0])
                print("Tweet status: " + row[5])
                csv_status = row[5]
                status_id = row[0]
                if len(USER_NAMES) > 0:
                    important = check_names(csv_status, important)
                if not important:
                    status, exists = retrieve_status(api, status_id)
                    if not exists:
                        count += 1
                        continue
                    if status.favorite_count >= 3:
                        important = True
                    # probably should add clause to check specific tweet ids
                if not important:
                    delete_tweets(api, status, important, delete)
            important = False
            count += 1
    print("Went through {} tweets total".format(count))
    print("Delete {} of total tweets".format(delete))
    print("done!")
