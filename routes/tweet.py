import tweepy
from typing import List, Dict, Any, Tuple


class TweeSentClient:
    def __init__(self, keys: Dict) -> None:
        bearer_token = keys["bearerToken"]
        consumer_key = keys["consumerKey"]
        consumer_secret = keys["consumerSecret"]
        access_token = keys["accessToken"]
        access_token_secret = keys["accessTokenSecret"]

        self.client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)

    def search_recent_tweets(self, query: str, max_results: int = 100) -> List[Dict[str, Any]]:
        tweets, includes = list(), list()

        max_results, iters, rest = self.get_pagination(max_results)

        rsp = self.client.search_recent_tweets(query, max_results=max_results, expansions=["author_id"])
        tweets += rsp.data
        includes += rsp.includes

        for _ in range(iters):
            rsp = self.client.search_recent_tweets(query, max_results=max_results, expansions=["author_id"], next_token=rsp.meta["next_token"])
            tweets += rsp.data
            includes += rsp.includes

        return tweets[:-rest]

    def get_users_tweets(self, username: str, max_results: int = 100, exclude: List[str] = ["retweets", "replies"]) -> List[Dict[str, Any]]:
        # List to store all the tweets fetched.
        tweets = list()

        # With APIv2 we can get the user data from username.
        user = self.client.get_user(username=username)

        max_results, iters, rest = self.get_pagination(max_results)
        
        # Just make a first fetch.
        rsp = self.client.get_users_tweets(user.data.id, max_results=max_results, exclude=exclude)
        tweets += rsp.data

        # And then the rest until get the max_results.
        for _ in range(iters):
            rsp = self.client.get_users_tweets(user.data.id, max_results=100, exclude=exclude, pagination_token=rsp.meta["next_token"])
            tweets += rsp.data

        return tweets[:-rest]

    @staticmethod
    def get_pagination(max_results: int) -> Tuple[int, int, int]:
        # If we want to search for more than 100 results we need to set everything for pagination tokens.
        rest = 100 - max_results % 100 if max_results > 100 else -max_results
        iters = max_results // 100 if max_results > 100 else 0
        max_results = 100 if max_results > 100 else max_results

        return max_results, iters, rest
