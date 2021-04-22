from __future__ import annotations
import re
import emoji
import tweepy
from enum import Enum
from typing import List, Dict, Any
from pydantic import BaseModel


class TweetRequest(BaseModel):
    text: str


class TweetResponse(BaseModel):
    tweets: List[Dict[str, str]]


class ErrorResponse(BaseModel):
    err: str


class TweeterBack:
    def __init__(self, conf) -> None:
        consumer_key = conf["consumerKey"]
        consumer_secret = conf["consumerSecret"]
        access_token = conf["accessToken"]
        access_token_secret = conf["accessTokenSecret"]

        # Create the authentication object
        authenticate = tweepy.OAuthHandler(consumer_key, consumer_secret)

        # Set the access token and access token secret
        authenticate.set_access_token(access_token, access_token_secret)

        # Creating the API object while passing in auth information
        self.api = tweepy.API(authenticate, wait_on_rate_limit=True)

    def search(self, input: str, count: int = 50) -> List[Dict[str, Any]]:
        return [
            {
                "id": t.id,
                "name": t.author.screen_name,
                "text": self.regex_tweets(t.full_text),
            }
            for t in tweepy.Cursor(
                self.api.search,
                q=input,
                lang="en",
                tweet_mode="extended",
            ).items(count)
        ]

    def user(self, input: str, count: int = 50) -> List[Dict[str, Any]]:
        return [
            {
                "id": t.id,
                "name": t.user.screen_name,
                "text": self.regex_tweets(t.full_text),
            }
            for t in tweepy.Cursor(
                self.api.user_timeline,
                screen_name=input.replace("@", ""),
                exclude_replies=True,
                tweet_mode="extended",
            ).items(count)
        ]

    def regex_tweets(self, text: str) -> str:
        expr = [
            r"https?:\/\/.*[\r\n]*",  # URLs
            r"R?T? ?@\w*",  # Users
            r"\B#\w*[a-zA-Z]+\w*",  # Hashtags
            r"\n",  # Carriage Returns
        ]

        for e in expr:
            text = re.sub(e, "", text, flags=re.MULTILINE)
        return emoji.get_emoji_regexp().sub(u"", text)

    @staticmethod
    def is_user(user):
        return " " not in user and "@" == user[0]
