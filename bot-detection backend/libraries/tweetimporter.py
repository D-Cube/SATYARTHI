import unicodedata
from models import Tweet, User

class TweetImporter(object):
    def __init__(self, twitter_client):
        self.twitter_client = twitter_client

    def createUser(self, screen_name, is_bot=False):
        api_user = self.twitter_client.user_shows(screen_name=screen_name)

        user = User.create(
            screen_name=screen_name,
            is_bot=is_bot,
            followers=api_user.followers_count,
            following=api_user.friends_count
        )

        return user

    def fromUser(self, screen_name, tweets_number=10, is_bot=False):
        user = self.createUser(screen_name, is_bot)

        tweets = self.twitter_client.user_timeline(screen_name=screen_name, count=tweets_number)
        for i, status in enumerate(tweets):
            tweet = status._json
            text = tweet['text']
            date = tweet['created_at']
            entities = tweet['entities']
            user_mentions = entities['user_mentions']
            mentions_list = []

            if len(user_mentions) > 0:
                for mention in user_mentions:
                    mentions_list.append(mention['screen_name'])

            text_string = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
            date_string = unicodedata.normalize('NFKD', date).encode('ascii','ignore')
            name_mentions_string = ",".join(mentions_list)

            Tweet.create(
                    user = user,
                    text = text_string,
                    date = date_string,
                    source = status.source,
                    mentions = name_mentions_string
            )

    def fromFollowers(self, user, tweets_number=10):
        followers = self.twitter_client.followers_list(screen_name=user, count=200)

        for j, follower in enumerate(followers):
            self.fromUser(follower, tweets_number)

