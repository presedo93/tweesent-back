import json
import asyncio

from typing import Any, Dict
from tweepy.asynchronous import AsyncStream

from tools.utils import regex_tweets
from routes.predict import OnnxPredict
from tools.settings import settings


class TweeSentStream:
    def __init__(self, infer: OnnxPredict, filter: str, interval: int) -> None:
        """Constructor of the TweeSentStream class. It connects with
        the tweepy class and creates the Queue to handle the received
        tweets.

        Args:
            filter (str): key words to match with the tweets.
            interval (int): seconds to stop per tweet found.
        """
        consumer_key = settings.CONSUMER_KEY
        consumer_secret = settings.CONSUMERT_SECRET
        access_token = settings.ACCESS_TOKEN
        access_token_secret = settings.ACCESS_TOKEN_SECRET

        # The predict class
        self.infer = infer

        # Create the asynchronous tweepy client.
        self.aclient = AsyncStream(
            consumer_key, consumer_secret, access_token, access_token_secret
        )

        # Set custom on_data method.
        self.aclient.on_data = self.on_data

        # Set the filters for the stream and an interval.
        self.aclient.filter(track=filter.split(","))
        self.interval = interval

        # Create an async Queue to store up to 25 tweets.
        self.tweets: asyncio.Queue = asyncio.Queue(25)

    async def on_data(self, raw_data: Any) -> None:
        """Async method called each time a tweet is received. Transforms
        the raw data in a Dict for TweeSent frontend and puts it in the
        Queue.

        Args:
            raw_data (Any): raw data received from the API.
        """
        await asyncio.sleep(self.interval)
        data = json.loads(raw_data.decode("utf8"))
        text = (
            data["extended_tweet"]["full_text"]
            if "extended_tweet" in data
            else data["text"]
        )
        pred = self.infer.predict(regex_tweets(text))
        tweet = self.compose_tweet(data, pred)
        await self.tweets.put(tweet)

    @staticmethod
    def compose_tweet(data: Dict, pred: str = None) -> Dict:
        """Compose a dict with the tweet data based on its fields.

        Args:
            data (Dict): raw data of the tweet.
            pred (str): prediction done by the NN.

        Returns:
            Dict: new dict with the desired format.
        """
        return {
            "id": str(data["id"]),
            "text": data["extended_tweet"]["full_text"]
            if "extended_tweet" in data
            else data["text"],
            "created_at": data["created_at"],
            "retweets": data["retweet_count"],
            "likes": data["favorite_count"],
            "username": data["user"]["screen_name"],
            "name": data["user"]["name"],
            "image": data["user"]["profile_image_url"],
            "sentiment": pred if pred is not None else "error",
        }
