import tweepy
import sys

#KEYS
consumer_key = 
consumer_secret = 
access_key = 
access_secret = 

#AUTHENTICATION
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

#CALLING API
api = tweepy.API(auth,wait_on_rate_limit=True,timeout=100)

#LOADING LIST OF ACCOUNTS
accounts = open(sys.argv[1], 'r')
accounts = accounts.readlines()

print(accounts)

