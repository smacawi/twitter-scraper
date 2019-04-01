from pathlib import Path
import json
from datetime import date

import tweepy
from tweepy import OAuthHandler, Status

import dataset

import plac

class TwitterScraper(object):
    def __init__(self, auth_dict: dict, db: str, table: str):
        self.api = self._load_api(auth_dict)
        self.db_table = self._create_db(db, table)
        self.stream_listener = self._create_stream_listener()


    @classmethod
    def from_json(cls, json_path: str, kwargs):
        """Loads auth key/value pairs from json file.

        Parameters
        ----------
        json_path : str
            Path to auth json containing 'consumer_key', 'consumer_secret', 'access_token', 'access_token_secret'

        Returns
        -------
        TwitterScraper
        """
        with Path(json_path).open() as j:
            auth_dict = json.load(j)
        return cls(auth_dict, **kwargs)

    def _load_api(self, auth_dict : dict):
        """Validate auth keys/tokens and return tweepy api object.

        Parameters
        ----------
        auth_dict : dict
            A dictionary with 'consumer_key', 'consumer_secret', 'access_token', 'access_token_secret'.

        Returns
        -------
        tweepy.API
            API object if authorization is successful.

        """
        required_keys = ['consumer_key', 'consumer_secret', 'access_token', 'access_token_secret']
        assert all(k in auth_dict for k in required_keys), print(f"Required keys: {required_keys}")

        auth = OAuthHandler(auth_dict['consumer_key'], auth_dict['consumer_secret'])
        auth.set_access_token(auth_dict['access_token'], auth_dict['access_token_secret'])
        return tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def _create_db(self, db, table):
        # TODO: ensure no issues with existing db/table
        db = dataset.connect(f"sqlite:///{db}.db")
        return db.create_table(table, primary_id=False)

    def _create_stream_listener(self):
        """Creates stream listener object from nested class so that stream listener can access `_parse_tweet` method.
        """
        return TwitterScraper.StreamListener(self)

    class StreamListener(tweepy.StreamListener):
        def __init__(self, twitter_scraper):
            super().__init__()
            self.twitter_scraper = twitter_scraper

        def on_status(self, tweet):
            self.twitter_scraper.db_table.insert(self.twitter_scraper.parse_tweet(tweet))
            print(tweet.text)

        def on_error(self, status_code):
            # TODO: complete error handling
            if status_code == 420:
                return False

    def parse_tweet(self, tweet: tweepy.Status):
        """Parses relevant information from tweet object.

        For reference, with regards to tweet object:
        https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html

        Parameters
        ----------
        tweet : tweepy.Status
            Tweet object, response from Twitter API.

        Returns
        -------
        parsed_tweet : dict
            Dictionary with relevant information from tweet object.
        """
        tweet = tweet._json
        if 'extended_tweet' in tweet:
            text = tweet['extended_tweet']['full_text']
        else:
            text = tweet['text']

        if 'retweeted_status' in tweet:
            rt = tweet['retweeted_status']
            rt_extended = 'extended_tweet' in rt
            rt_text = rt['text'] if not rt_extended else rt['extended_tweet']['full_text']
            rt_user_id = rt['user']['id']
            rt_user = rt['user']['screen_name']
            rt_id = rt['id']
        else:
            rt_text = ""
            rt_user_id = ""
            rt_user = ""
            rt_id = ""

        if 'quoted_status' in tweet:
            qt = tweet['quoted_status']
            qt_extended = 'extended_tweet' in qt
            qt_text = qt['text'] if not qt_extended else qt['extended_tweet']['full_text']
            qt_user_id = qt['user']['id']
            qt_user = qt['user']['screen_name']
            qt_id = qt['id']
        else:
            qt_text = ""
            qt_user_id = ""
            qt_user = ""
            qt_id = ""

        parsed_tweet = dict(
            # tweet information
            id=tweet['id_str'],
            text=text,
            hashtags=",".join([ht['text'] for ht in tweet['entities']['hashtags']]),
            user_mentions_id=",".join([um['id_str'] for um in tweet['entities']['user_mentions']]),
            user_mentions=",".join([um['screen_name'] for um in tweet['entities']['user_mentions']]),
            # user information
            user_id=tweet['user']['id_str'],
            user=tweet['user']['screen_name'],
            user_name=tweet['user']['name'],
            user_followers_count=tweet['user']['followers_count'],
            user_friends_count=tweet['user']['friends_count'],
            user_favourites_count=tweet['user']['favourites_count'],
            user_statuses_count=tweet['user']['statuses_count'],
            user_listed_count=tweet['user']['listed_count'],
            user_location=tweet['user']['location'],
            user_verified=tweet['user']['verified'],
            user_created_at=tweet['user']['created_at'],
            # reply information
            reply_to_tweet_id=tweet['in_reply_to_status_id'] if tweet['in_reply_to_status_id'] is not None else "",
            reply_to_user=tweet['in_reply_to_screen_name'] if tweet['in_reply_to_screen_name'] is not None else "",
            reply_to_user_id=tweet['in_reply_to_user_id_str'] if tweet['in_reply_to_user_id_str'] is not None else "",
            # retweet information
            rt_text=rt_text,
            rt_id=rt_id,
            rt_user=rt_user,
            rt_user_id=rt_user_id,
            # quote information
            qt_text=qt_text,
            qt_user_id=qt_user_id,
            qt_user=qt_user,
            qt_id=qt_id,
            # time/location information
            created_at=tweet['created_at'],
            coordinates=str(tweet['coordinates']),
            place=str(tweet['place'])
        )
        return parsed_tweet

    def search_tweets(self, query, max_tweets=100):
        """Searches tweets using Twitter API search endpoint.

        For reference, with regard to search endpoint:
        https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators

        Parameters
        ----------
        query : str
            String representation of search endpoint query.

        max_tweets : int
            Maximum number of tweets to retrieve

        Returns
        -------
        tweets : dict[list]
            List of parsed tweets as dictionaries
        """
        tweets = []
        tweet_count = 0
        tweets_per_query = 100

        while tweet_count < max_tweets:
            try:
                new_tweets = self.api.search(q=query, count=tweets_per_query)
                tweet_count += tweets_per_query
                tweets += [self.parse_tweet(t) for t in new_tweets]
            except tweepy.TweepError as e:
                print("Tweepy error : " + str(e))
                break
        return tweets

    def stream_tweets(self, tw_filter):
        stream = tweepy.Stream(self.api.auth, self.stream_listener)
        stream.filter(**tw_filter)


@plac.annotations(
    auth=plac.Annotation("Path to .json containing twitter auth information: "
                         "\n'consumer_key', 'consumer_secret', 'access_token', 'access_token_secret'. ",
                         kind="option", type=str),
    filter=plac.Annotation("Path to .json containing comma separated values for stream filters: "
                           "\n'track', 'languages', 'locations', 'filter_level'. ",
                           kind="option", type=str),
    db=plac.Annotation("Name of database with table where tweets will be stored. ",
                       kind="option", type=str),
    table=plac.Annotation("Name of table in database where tweets will be stored. ",
                          kind="option", type=str)
)
def main(auth="tweepy_auth.json",
         filter="stream_filter.json",
         db="nebraska_floods",
         table="live_tweets"):
    # instantiate twitter scraper
    # TODO: give user more insight on table/db (e.g. to prevent appending to wrong table)
    ts = TwitterScraper.from_json(auth, dict(db=db, table=table))

    # instantiate twitter streamer
    # TODO: clean-up, consider passing individual filters through plac.
    with open(filter) as f:
        filter_dict = {k:v.split(",") for k,v in (json.load(f)).items()}
        if filter_dict['locations'] == [""]:
            filter_dict['locations'] = None
        else:
            filter_dict['locations'] = list(map(float, filter_dict['locations']))

        if filter_dict['filter_level'] == [""]:
            filter_dict['filter_level'] = None
        else:
            filter_dict['filter_level'] = filter_dict['filter_level'][0]
    ts.stream_tweets(filter_dict)


if __name__ == '__main__':
    plac.call(main)