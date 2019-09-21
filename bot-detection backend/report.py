import os
from libraries.models import Tweet, User
from config import app_config as cfg
from libraries.graphs.graph import Graph

# Twitter API configuration
consumer_key = cfg.twitter["consumer_key"]
consumer_secret = cfg.twitter["consumer_secret"]

access_token = cfg.twitter["access_token"]
access_token_secret = cfg.twitter["access_token_secret"]


# Start
current_path = os.path.dirname(os.path.abspath(__file__))
graph = Graph()

human_tweets = Tweet.get_sample()
bot_tweets = Tweet.get_sample(is_bot=True)
human_users = User.get_sample()
bot_users = User.get_sample(True)

# top sources
path ="{}/images/top_sources.png".format(current_path)
graph.top_sources(
    Tweet.top_sources(human_tweets),
    Tweet.top_sources(bot_tweets),
    path
)

# Average mentions per user
path ="{}/images/avg_mentions.png".format(current_path)
graph.avg_tweets(
    Tweet.avg_mentions_per_user(human_tweets).values(),
    Tweet.avg_mentions_per_user(bot_tweets).values(),
    path
)

## Vocabulary size per users
path ="{}/images/vocabulary.png".format(current_path)
graph.vocabulary(
    Tweet.vocabulary_size(human_tweets).values(),
    Tweet.vocabulary_size(bot_tweets).values(),
    path
)

# number of tweets during active days
path ="{}/images/density.png".format(current_path)
tweet_density_per_user, mean_count_user, median_count_user = Tweet.tweet_density(human_tweets)
tweet_density_per_bot, mean_count_bot, median_count_bot = Tweet.tweet_density(bot_tweets)
graph.hist_density(
    tweet_density_per_user,
    tweet_density_per_bot,
    mean_count_user,
    median_count_user,
    mean_count_bot,
    median_count_bot,
    path
)

# number of tweets per week days
path ="{}/images/weekdays.png".format(current_path)
graph.hist_weekday(
    Tweet.tweet_weekday(human_tweets),
    Tweet.tweet_weekday(bot_tweets),
    path
)

# Nb followers/following
path ="{}/images/followers_following.png".format(current_path)
graph.Nb_followers_following(
User.followers_friends_per_users(human_users),
User.followers_friends_per_users(bot_users),
    path
)

