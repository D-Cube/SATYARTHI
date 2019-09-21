from collections import defaultdict

import numpy as np
from dateutil import parser
from pandas import DataFrame
from peewee import *
from playhouse.db_url import connect
from config import app_config as cfg

# Connect to the database URL defined in the app_config
db = connect(cfg.database['url'])


def create_database():
    db.connect()
    db.drop_tables([User, Tweet], True)
    db.create_tables([User, Tweet], True)

class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    screen_name = CharField()
    is_bot = BooleanField()
    followers = IntegerField()
    following = IntegerField()

    def reputation(self):
        if self.followers == 0:
            return 0
        else:
            return self.followers / float(self.followers + self.following)

    @classmethod
    def get_sample(self, is_bot=False):
        return User.select().where(User.is_bot == is_bot)

    @classmethod
    def followers_friends_per_users(self, users):
        data = [{
            "followers" : user.followers,
            "following" : user.following,
            "accountreputation" : user.reputation()
        } for user in users]

        df = DataFrame(data, columns=["followers", "following", "accountreputation", "CDFx", "CDFy"], index=range(len(users)))
        df_size = len(df.index)

        df["CDFx"] = np.sort(df["accountreputation"])
        df["CDFy"] = np.array(range(df_size)) / float(df_size)

        return df

    @classmethod
    def entropy(X):
        probs = [np.mean(X == c) for c in set(X)]

        return np.sum(-p * np.log2(p) for p in probs)

class Tweet(BaseModel):
    user = ForeignKeyField(User, related_name='tweets')
    text = CharField()
    date = CharField()
    source = CharField()
    mentions = CharField()

    @classmethod
    def get_sample(cls, is_bot=False, min_tweets=200):
        selected_users = Tweet.select(Tweet.user) \
            .group_by(Tweet.user) \
            .having(fn.Count(Tweet.user) >= min_tweets)

        tweets = (Tweet.select(Tweet).join(User)
            .where(
            User.is_bot == is_bot,
            User.id << selected_users
        ))

        return tweets

    @classmethod
    def avg_mentions_per_user(cls, tweets):
        mentions_per_user = defaultdict(lambda: [])
        for tweet in tweets:
            count = 0
            if len(tweet.mentions) > 0:
                count = len(tweet.mentions.split(","))
            mentions_per_user[tweet.user_id].append(count)

        avg_per_user = {user: np.mean(mentions) for (user, mentions) in mentions_per_user.iteritems()}

        return avg_per_user

    @classmethod
    def vocabulary_size(cls, tweets):
        words_per_user = defaultdict(lambda: set())
        for tweet in tweets:
            for word in tweet.text.split(" "):
                words_per_user[tweet.user_id].add(word)

        return {name: len(words) for (name, words) in words_per_user.iteritems()}

    @classmethod
    def tweet_density(cls, tweets):
        tweets_df = DataFrame(columns=["user_id", "date"], index=range(len(tweets)))
        for i, tweet in enumerate(tweets):
            date = parser.parse(tweet.date)

            tweets_df["date"][i] = str(date.year)+str(date.month)+str(date.day)
            tweets_df["user_id"][i] = tweet.user_id

        grouped = tweets_df.groupby(['user_id', 'date']).size().reset_index()

        count_list_by_user = grouped[0].apply(lambda x: x if (x < 6) else 6).tolist()
        mean_count = np.mean(count_list_by_user)
        median_count = np.median(count_list_by_user)

        return count_list_by_user, mean_count, median_count

    @classmethod
    def tweet_weekday(cls, tweets):
        tweets_df = DataFrame(columns=["user_id", "weekday"], index=range(len(tweets)))

        for i, tweet in enumerate(tweets):
            tweets_df["weekday"][i] = str(tweet.date.split(' ')[0])
            tweets_df["user_id"][i] = tweet.user_id

        grouped = tweets_df.groupby(['user_id', 'weekday']).size().reset_index()

        list_days = set(grouped["weekday"])
        stats_weekdays = DataFrame(columns=["weekday", "mean","std"], index=range(len(list_days)))
        stats_weekdays["weekday"] = list_days
        stats_weekdays["mean"] = list(map(lambda day : np.mean(grouped[0][grouped["weekday"] == day]),list_days))
        stats_weekdays["std"] = list(map(lambda day : np.std(grouped[0][grouped["weekday"] == day]),list_days))

        prop_weekdays = DataFrame(columns=["weekday", "prop","std"], index=range(len(list_days)))
        prop_weekdays["weekday"] = list_days
        prop_weekdays['prop'] = stats_weekdays['mean'] / sum(stats_weekdays['mean'])
        prop_weekdays['std'] = stats_weekdays['std'] / sum(stats_weekdays['mean'])
        sorted_weekdays = prop_weekdays.reindex([4,3,0,2,5,6,1])

        return sorted_weekdays

    @classmethod
    def top_sources(cls, tweets):
        sources = [{"source": tweet.source} for tweet in tweets]

        return DataFrame(sources).stack().value_counts()




