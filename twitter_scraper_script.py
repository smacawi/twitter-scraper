import plac
import json
from twitter_scraper.TwitterScraper import TwitterScraper


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
def main(auth="_tweepy_auth.json",
         filter="stream_filter.json",
         db="flood_test",
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