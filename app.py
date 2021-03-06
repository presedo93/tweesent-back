from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from routes.predict import OnnxPredict
from routes.tweet import TweeSentClient
from routes.stream import TweeSentStream

from tools.models import TweetIn, TweetOut
from tools.utils import open_conf, regex_tweets, weights_folder


conf = open_conf("config/config.json")
keys = open_conf("config/keys.json")

app = FastAPI()
inference = OnnxPredict(conf)
twitter_client = TweeSentClient(keys)

origins = ["http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    weights_folder()


@app.post("/search_tweets", response_model=TweetOut)
def search_tweets(request: TweetIn):
    if request.query[0] != "@":
        data, users, token = twitter_client.search_tweets(
            request.query, request.max_results, request.token
        )
    else:
        data, users, token = twitter_client.user_tweets(
            request.query[1:], request.max_results, request.token
        )

    tweets = [
        TweeSentClient.compose_tweet(d, u, inference.predict(regex_tweets(d["text"])))
        for d, u in zip(data, users)
    ]

    return TweetOut(tweets=tweets, token=token)


@app.websocket("/stream/{interval}/{filter}")
async def websocket_stream(websocket: WebSocket, filter: str, interval: int):
    await websocket.accept()
    stream = TweeSentStream(keys, inference, filter, interval)
    try:
        while True:
            tweet = await stream.tweets.get()
            await websocket.send_json(tweet)
    except BaseException:
        stream.aclient.disconnect()
