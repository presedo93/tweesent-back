from __future__ import annotations
import re
import emoji
import tweepy
from typing import List, Dict, Any
from pydantic import BaseModel


class TweetRequest(BaseModel):
  text: str


class TweetResponse(BaseModel):
  tweets: List[Dict[str, Any]]


class TweeterBack:
  def __init__(self, conf) -> None:
    consumerKey = conf["consumerKey"]
    consumerSecret = conf["consumerSecret"]
    accessToken = conf["accessToken"]
    accessTokenSecret = conf["accessTokenSecret"]

    # Create the authentication object
    authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)

    # Set the access token and access token secret
    authenticate.set_access_token(accessToken, accessTokenSecret)

    # Creating the API object while passing in auth information
    self.api = tweepy.API(authenticate, wait_on_rate_limit = True)

  def get_instance(self) -> TweeterBack:
    return self

  def search(self, input: str, count: int = 50) -> List:
    posts = self.api.search(q=input, count=count, lang="en", tweet_mode="extended")
    return [{'id': t.id, 'name': t.author.screen_name, 'text': t.full_text} for t in posts]

  # https://medium.com/analytics-vidhya/working-with-twitter-data-b0aa5419532
  def re_urls(self, text: str) -> str:
    return re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)

  def re_hash(self, text: str) -> str:
    return re.sub(r'\B#\w*[a-zA-Z]+\w*', '', text, flags=re.MULTILINE)

  def re_carr(self, text: str) -> str:
    return re.sub(r'\n', '', text, flags=re.MULTILINE)

  def re_emoji(self, text: str) -> str:
    return emoji.get_emoji_regexp().sub(u'', text)

  def re_tweet(self, text: str) -> str:
    return self.re_carr(self.re_hash(self.re_urls(self.re_emoji(text))))