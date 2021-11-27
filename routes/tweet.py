import tweepy
from typing import List, Dict, Any, Tuple


class TweeSentClient:
    def __init__(self, keys: Dict) -> None:
        """TweeSentClient constructor that connects with the Twitter
        APIv2.

        Args:
            keys (Dict): keys for the Twitter APIv2.
        """
        bearer_token = keys["bearerToken"]
        consumer_key = keys["consumerKey"]
        consumer_secret = keys["consumerSecret"]
        access_token = keys["accessToken"]
        access_token_secret = keys["accessTokenSecret"]

        self.client = tweepy.Client(
            bearer_token,
            consumer_key,
            consumer_secret,
            access_token,
            access_token_secret,
        )

    def search_tweets(
        self,
        query: str,
        max_results: int = 100,
        next_token: str = None,
        filter: str = "-is:retweet",
    ) -> Tuple[List[Any], List[Any], str]:
        """Search a batch of tweets smaller than 100 (apiV2 limit). It includes
        in the results, the metrics as when it was created, public metrics
        and user info.

        Args:
            query (str): query for the search.
            max_results (int, optional): Number of results to ask the API for.
            Defaults to 100.
            next_token (str, optional): The token to resume the search in case
            of calling several times the method. Defaults to None.
            filter (str, optional): for the query to, for example,
            disable retweets, etc. Defaults to "-is:retweet".

        Returns:
            Tuple[List[Any], List[Any], str]: two lists with tweets and users
            and the token generated.
        """
        rsp = self.client.search_recent_tweets(
            f"{query} {filter}",
            max_results=max_results,
            expansions=["author_id", "referenced_tweets.id"],
            user_fields=["profile_image_url"],
            tweet_fields=["created_at", "public_metrics"],
            next_token=next_token,
        )

        return rsp.data, rsp.includes["users"], rsp.meta["next_token"]

    def user_tweets(
        self,
        username: str,
        max_results: int = 100,
        next_token: str = None,
        exclude: List[str] = ["retweets", "replies"],
    ) -> Tuple[List[Any], List[Any], str]:
        """Search the max_results tweets of a user. It includes user info
        as the image url of the profile, its name and username, etc.

        Args:
            username (str): user to search tweets of.
            max_results (int, optional): number of tweets to fetch. Defaults to 100.
            next_token (str, optional): allows to fetch tweets from a token point. Defaults to None.
            exclude (List[str], optional): excludes retweets or replies in the search. Defaults to ["retweets", "replies"].

        Returns:
            Tuple[List[Any], List[Any], str]: two lists with tweets and users and the token generated.
        """
        # With APIv2 we can get the user data from username.
        user = self.client.get_user(
            username=username,
            expansions=["pinned_tweet_id"],
            user_fields=["profile_image_url"],
        )

        # Fetch the user tweets.
        rsp = self.client.get_users_tweets(
            user.data.id,
            max_results=max_results,
            exclude=exclude,
            expansions=["author_id", "referenced_tweets.id"],
            tweet_fields=["created_at", "public_metrics"],
            pagination_token=next_token,
        )

        # Replate the user data to have the same len as tweets.
        users = [user.data] * len(rsp.data)

        return rsp.data, users, rsp.meta["next_token"]

    @staticmethod
    def compose_tweet(data: Dict, user: Dict) -> Dict:
        """Compose a tweet dict for TweeSent frontend.

        Args:
            data (Dict): data fields from the API.
            user (Dict): user fields from the API.

        Returns:
            Dict: dict with the user and data info.
        """
        return {
            "id": str(data["id"]),
            "text": data["text"],
            "created_at": data["created_at"],
            "retweets": data["public_metrics"]["retweet_count"],
            "likes": data["public_metrics"]["like_count"],
            "username": user["username"],
            "name": user["name"],
            "image": user["profile_image_url"],
        }
