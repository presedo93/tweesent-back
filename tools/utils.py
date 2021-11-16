import re
import os
import json
import emoji

from typing import Dict, List
from pydantic import BaseModel


class TweetRequest(BaseModel):
    query: str
    max_results: int



class TweetResponse(BaseModel):
    tweets: List[Dict[str, str]]


def open_conf(conf_path: str) -> Dict:
    """Loads the config JSON.
    Args:
        conf_path (str): config file path.
    Returns:
        dict: config values as dict.
    """
    with open(os.path.join(os.getcwd(), conf_path), "r") as f:
        conf = json.load(f)

    return conf


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