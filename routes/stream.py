import json
import asyncio

from typing import Any, Dict
from tweepy.asynchronous import AsyncStream


class TweeSentStream:
    def __init__(self, keys: Dict, filter: str, interval: int) -> None:
        """Constructor of the TweeSentStream class. It connects with
        the tweepy class and creates the Queue to handle the received
        tweets.

        Args:
            keys (Dict): dict with the kyes to connect to Twitter API.
            filter (str): key words to match with the tweets.
            interval (int): seconds to stop per tweet found.
        """
        consumer_key = keys["consumerKey"]
        consumer_secret = keys["consumerSecret"]
        access_token = keys["accessToken"]
        access_token_secret = keys["accessTokenSecret"]

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
        tweet = self.compose_tweet(data)
        await self.tweets.put(tweet)

    @staticmethod
    def compose_tweet(data: Dict) -> Dict:
        """Compose a dict with the tweet data based on its fields.

        Args:
            data (Dict): raw data of the tweet.

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
        }
