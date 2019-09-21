import argparse

from config import app_config as cfg

from libraries.tweetimporter import TweetImporter
from libraries.twitterclient import TwitterClient

from libraries.models import create_database

# Twitter API configuration
consumer_key = cfg.twitter["consumer_key"]
consumer_secret = cfg.twitter["consumer_secret"]

access_token = cfg.twitter["access_token"]
access_token_secret = cfg.twitter["access_token_secret"]

# Command line options
parser = argparse.ArgumentParser(description='provide additional information to run the bot detection')
parser.add_argument('specified_user', action="store", help='load tweets from the specified user')
parser.add_argument('--followers', action="store_true", help="load tweets from user's followers")
parser.add_argument('--create-db', action="store_true", help='create or drop the database if it already exists')
parser.add_argument('--is-bot', action="store_true", help='the specified user will be flag as bot')

args = parser.parse_args()

# Start
if args.create_db:
    create_database()

client = TwitterClient(consumer_key, consumer_secret, access_token, access_token_secret)
importer = TweetImporter(client)
importer.fromUser(args.specified_user, 200, args.is_bot)

if args.followers:
    importer.fromFollowers(args.specified_user, 200)