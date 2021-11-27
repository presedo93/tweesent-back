from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class TweetIn(BaseModel):
    query: str
    max_results: int
    allow_retweets: Optional[bool] = False
    allow_replies: Optional[bool] = False
    token: Optional[str] = None


class TweetOut(BaseModel):
    tweets: List[Dict[str, Any]]
    token: Optional[str] = None
