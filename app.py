import asyncio

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from routes.predict import Predict, SentimentRequest, SentimentResponse
from routes.tweet import TweeSentClient
from routes.stream import TweeSentStream
from tools.utils import open_conf, TweetRequest, TweetResponse


conf = open_conf("config/config.json")
keys = open_conf("config/keys.json")

app = FastAPI()
# torch_nlp = Predict(conf["bert"])
twitter_client = TweeSentClient(keys)

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


@app.post("/search_recent_tweets", response_model=TweetResponse)
def search(request: TweetRequest, count: int = 50):
    # If text starts with @ and is only one word.
    if tweet_api.is_user(request.text):
        tweets = tweet_api.user(request.text, count=count)
    else:
        tweets = tweet_api.search(request.text, count=count)

@app.get("/search_user_tweets/{query}/{max_results}")
def search(query: str, max_results: int = 100):
    tweets = twitter_client.get_users_tweets(query, max_results)

    # for tw in tweets:
    #     tw["sentiment"], tw["confidence"] = torch_nlp.predict(tw["text"])
    # return TweetResponse(tweets=tweets)
    return tweets

@app.websocket("/stream")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()
    stream = TweeSentStream(conf["tweepy"])
    while True:
        # data = await websocket.receive_text()
        # data = await stream.on_data()
        await asyncio.sleep(10)
        await websocket.send_text(f"Message text was: {2}")
