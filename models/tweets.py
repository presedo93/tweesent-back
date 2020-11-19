import tweepy

class Tweets:
  def __init__(self):
    # authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)
    self.tweets_list = ["Tweet1 from back", "Tweet2 from back"]

  def get_tweets(self):
    return self.tweets_list


