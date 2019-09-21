import tweepy

class TwitterClient(object):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def followers_list(self, screen_name, count=5):
        followers =  tweepy.Cursor(self.api.followers, screen_name=screen_name).items()

        return [ follower.screen_name for follower in followers if follower.protected == False]

    def user_timeline(self, screen_name, count=10):
        return self.api.user_timeline(screen_name = screen_name, count=count)

    def user_shows(self, screen_name):
        return self.api.get_user(screen_name)