import tweepy
import pandas as pd

#KEYS
consumer_key = ":)"
consumer_secret = :)
access_key = :)
access_secret = :)

#AUTHENTICATION
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

#CALLING API
api = tweepy.API(auth, wait_on_rate_limit=True, timeout=100)

c = pd.DataFrame(columns=['account',
                          'followers'])

accounts = open("ECCCtwitteraccount.txt", 'r')
accounts = accounts.read().splitlines()

for account in accounts:
    print account
    print api.followers(id=account)
    c = c.append({'account': account,
                  'followers': api.followers(id=account)}, ignore_index=True)


c.to_csv('./ECCCFollows.csv')
