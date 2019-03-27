import tweepy
import pandas as pd

#KEYS
consumer_key = "T76lbMQkhhEacC7ctSbS3D8gn"
consumer_secret = "UM0nN7DvIv9mUXVjFcHvu0zvduxa95C9RrNsMloOGuLIhmUG1r"
access_key = "2620068925-ZshJvZXSRQj6iNJBw3iG4wfPQeMylPGAM50kKml"
access_secret = "8gJrohS0yPUDvBTY1xeYYDCwaXdVdqmIvayutkgCPPxVM"

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
