import json
import asyncio

from typing import Any, Dict
from tweepy.asynchronous import AsyncStream

class TweeSentStream():
    def __init__(self, conf: Dict) -> None:
        consumer_key = conf["consumerKey"]
        consumer_secret = conf["consumerSecret"]
        access_token = conf["accessToken"]
        access_token_secret = conf["accessTokenSecret"]

        self.aclient = AsyncStream(consumer_key, consumer_secret, access_token, access_token_secret)
        self.aclient.on_data = self.on_data
        self.aclient.on_connect = self.on_connect

        self.aclient.sample()

    async def on_data(self, raw_data: Any):
        await asyncio.sleep(10)
        data = json.loads(raw_data.decode("utf8"))
        print("RAW:", data)

    async def on_connect(self):
        print("Connnnecteeeed")