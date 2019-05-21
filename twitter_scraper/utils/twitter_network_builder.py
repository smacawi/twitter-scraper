"""
Converts dataset of raw twitter objects to edges and nodes for network analysis.
"""
import pandas as pd

class TwitterNetworkBuilder:
    def __init__(self, df: pd.DataFrame = None):
        self.df = self._validate_df(df)

    @classmethod
    def from_csv(cls, csv_path: str):
        df = pd.read_csv(csv_path)
        return cls(df)

    @classmethod
    def from_pkl(cls, pkl_path: str):
        df = pd.read_pickle(pkl_path)
        return cls(df)

    def _validate_df(self, df):
        # TODO: make sure df has right columns
        return df

    def get_user_nodes(self):
        """Create user nodes from raw twitter data.

        A user node consists of a UserID and associated account information.
        Any information that changes between tweets for a given user is resolved to the latest value.
        """
        # TODO: get nodes from retweets/mentions/replies
        df_nodes = self.df[['user','user_created_at','user_location']]
        return df_nodes.drop_duplicates(subset=['user'],keep='last')

    def get_user_edges(self):
        """Create user edges from raw twitter data

        An edge consists of source and target user nodes and edge type (retweet/quote, reply, mention).
        """
        df_edges = pd.DataFrame()
        df_edges['Source'] = self.df['user']
        df_edges['Target'] = "@NoEdge"
        df_edges['Kind'] = "@NoEdge"
        df_edges['timeset'] = self.df['created_at']

        df_edges.loc[~self.df['user_mentions'].isna(), 'Kind'] = "Mention"
        df_edges.loc[~self.df['user_mentions'].isna(), 'Target'] = self.df['user_mentions']
        df_edges.loc[~self.df['rt_id'].isna(), 'Kind'] = "Retweet"
        df_edges.loc[~self.df['rt_id'].isna(), 'Target'] = self.df['rt_user']
        df_edges.loc[~self.df['qt_id'].isna(), 'Kind'] = "Quote"
        df_edges.loc[~self.df['qt_id'].isna(), 'Target'] = self.df['qt_user']
        df_edges.loc[~self.df['reply_to_tweet_id'].isna(), 'Kind'] = "Reply"
        df_edges.loc[~self.df['reply_to_tweet_id'].isna(), 'Target'] = self.df['reply_to_user']

        def expand_mentions(df, mention_col):
            """Converts row with list of mentions to many rows with one mention each.
            """
            new_rows = []
            for i,r in df.iterrows():
                new_r = r.to_dict()
                for u in r[mention_col].split(","):
                    new_r[mention_col] = u
                    new_rows.append(new_r)
            return pd.DataFrame(new_rows)

        df_edges = expand_mentions(df_edges, 'Target')
        df_edges = df_edges.groupby(['Kind', 'Source', 'Target'], as_index=False).agg(lambda x: x.tolist())
        df_edges.drop(df_edges.loc[df_edges['Kind'] == "@NoEdge"].index, inplace=True)
        df_edges['weight'] = df_edges.timeset.apply(lambda x: len(x))
        return df_edges







