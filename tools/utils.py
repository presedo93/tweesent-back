import re
import os
import json
import emoji

from typing import Dict


def weights_folder() -> None:
    if os.path.exists("weights/") is False:
        os.makedirs("weights/", exist_ok=True)


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


def regex_tweets(text: str) -> str:
    """Clears the raw data of URLs, users mentions, hashtags
    and carriage returns.

    Args:
        text (str): raw text of the tweet.

    Returns:
        str: cleared text.
    """
    expr = [
        r"https?:\/\/.*[\r\n]*",  # URLs
        r"R?T? ?@\w*",  # Users
        r"\B#\w*[a-zA-Z]+\w*",  # Hashtags
        r"\n",  # Carriage Returns
    ]

    for e in expr:
        text = re.sub(e, "", text, flags=re.MULTILINE)
    return emoji.get_emoji_regexp().sub(u"", text)
