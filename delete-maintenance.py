"""
this is a maintenance script to delete tweets from a users timeline based on
some set of requirements. This script accounts for the number of likes,
keywords, and some max # of tweets to delete going backwards on the timeline.
"""

from secrets import ACCESS_SECRET, ACCESS_TOKEN, CONSUMER_KEY, CONSUMER_SECRET
import tweepy as ty
from tweets.options import KEY_WORDS, LIKES, MAX
import time
from nltk.tokenize import TweetTokenizer

__author__ = "elias garcia"


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
    """
    old method, may use for maintenance script
    """
    while True:
        try:
            yield cursor.next()
        except ty.RateLimitError:
            print("sleeping! {}".format(time.localtime()))
            time.sleep(60 * 15)
        except ty.TweepError as e:
            print("Non-rate limited error: {}".format(e))
            break


def mineHomeTimeline(api):
    """
    old method, may use for maintenance script
    """
    if MAX is not None:
        timeline = [status for status in
                    handleLimit(ty.Cursor(api.user_timeline).items(MAX))]
    else:
        timeline = [status for status in
                    handleLimit(ty.Cursor(api.user_timeline).items())]
    return timeline


def check_keywords(status, important):
    """
    checks for presence of keywords in the tweet currently being process,
    returns boolean important indicating whether it is to be deleted or not
    """
    token = TweetTokenizer()
    tweet_tokens = token.tokenize(status)
    for words in tweet_tokens:
        for key in KEY_WORDS:
            if words[1:].lower() == key.lower():
                important = True
    return important


def delete_tweets(api, status, important, delete, record):
    """
    deletion method, will attempt to delete status passed
    returns delete counter which will increment upon successful deletion
    """
    while not important:
        try:
            api.destroy_status(status.id)
            print("Tweet destroyed!")
            record.writelines(status.text + "\n")
            delete += 1
            important = True
            return delete
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
    timeline = mineHomeTimeline(api)

    important = False
    count = 0
    delete = 0
    record = open("deleted-tweets.txt", "a")
    for status in timeline:
        count += 1
        print("Tweet text: {}".format(status.text))
        print("Tweet id: {}".format(status.id))
        if len(KEY_WORDS) > 0:
            important = check_keywords(status.text, important)
        if not important:
            if LIKES is not None and status.favorite_count >= LIKES:
                important = True
        if not important:
            delete = delete_tweets(api, status, important, delete, record)
        important = False
    record.close()
    print("Script finished!")
    print("Script processed {} tweets and deleted {} total".format(count,
                                                                   delete))
