import tweepy
import pandas as pd

#KEYS
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

#AUTHENTICATION
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

#CALLING API
api = tweepy.API(auth,wait_on_rate_limit=True,timeout=100)


#SETTING UP THE DATAFRAME

#Opening accounts and Preprocessing
accounts = open("commercial_accounts.txt", 'r')
accounts = accounts.read().splitlines()

for account in accounts:
    c = pd.DataFrame(columns=['tweet',
                              'id',
                              'time',
                              'user',
                              'location',
                              'favourites',
                              'retweet-count',
                               #Only available with premium 'reply-count',
                              'hashtags'
                              ])

    for tweet in tweepy.Cursor(api.user_timeline, id=account).items():
        print tweet.text

        hashytaggy = tweet.entities.get('hashtags')
        hashtags = [tag['text'] for tag in hashytaggy]

        c = c.append({'tweet':tweet.text,
                              'id':tweet.id,
                              'time':str(tweet.created_at),
                              'user':tweet.user.id,
                              'location':tweet.author.location,
                              'favourites': tweet.favorite_count,
                              'retweet-count':tweet.retweet_count,
                             #Only available with premium 'reply-count': tweet.reply_count,
                              'hashtags':hashtags}, ignore_index=True)

    c.to_csv('./{}-tweets.csv'.format(account), encoding='utf-8')
