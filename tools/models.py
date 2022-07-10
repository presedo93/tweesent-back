from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class TweetIn(BaseModel):
    query: str = Field(..., alias="Query")
    max_results: int = Field(10, alias="numTweets")
    allow_retweets: Optional[bool] = Field(False, alias="allowRt")
    allow_replies: Optional[bool] = Field(False, alias="allowRe")
    token: Optional[str] = Field(None)


class TweetOut(BaseModel):
    tweets: List[Dict[str, Any]]
    token: Optional[str] = None
