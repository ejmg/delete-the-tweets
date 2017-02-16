"""
this script deletes tweets off of your timeline
"""

from secrets import ACCESS_SECRET, ACCESS_TOKEN, CONSUMER_KEY, CONSUMER_SECRET
import tweepy as ty
import time
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
                handleLimit(ty.Cursor(api.user_timeline,
                                      max_id=794777388743847936).items())]
    return timeline


if __name__ == "__main__":

    api = setTwitterAuth()
    user = api.me()
    timeline = mineHomeTimeline(api)
    record = open("tweets2.txt", "a")
    print("Acquired {} total tweets! Writing to file.".format(len(timeline)))
    i = 1
    important = False
    for tweet in timeline:
        # print(tweet.extended_entities["media"][0]["media_url"])
        print("Tweet #{}".format(i))
        print(tweet.text)
        print(tweet.id)

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

        if tweet.favorite_count >= 3:
            important = True
        #elif hasattr(tweet, "extended_entities"):
            #important = True
        else:
            token = TweetTokenizer()
            tweet_tokens = token.tokenize(tweet.text)
            for words in tweet_tokens:
                for key in USER_NAMES:
                    if words[1:].lower() == key.lower():
                        important = True

        if not important:
            #            try:
            api.destroy_status(tweet.id)
           # except ty.RateLimitError:
            #    print("sleeping! {}".format(time.localtime()))
             #   time.sleep(60 * 15)
        i += 1
        important = False
    record.close()

    print("done!")
    # tweets = [tweet.text for tweet in timeline]
