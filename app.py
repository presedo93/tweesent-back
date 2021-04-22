import json
import time
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.predict import Predict, SentimentRequest, SentimentResponse
from routes.tweet import TweeterBack, TweetRequest, TweetResponse, ErrorResponse


with open("config.json") as json_file:
    conf = json.load(json_file)

app = FastAPI()
torch_nlp = Predict(conf["bert"])
tweet_api = TweeterBack(conf["tweepy"])

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/gettweet", response_model=TweetResponse)
def search(request: TweetRequest, count: int = 50):
    # If text starts with @ and is only one word.
    if tweet_api.is_user(request.text):
        tweets = tweet_api.user(request.text, count=count)
    else:
        tweets = tweet_api.search(request.text, count=count)

    for tw in tweets:
        tw["sentiment"], tw["confidence"] = torch_nlp.predict(tw["text"])
    return TweetResponse(tweets=tweets)
