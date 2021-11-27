from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

# from routes.predict import Predict, SentimentRequest, SentimentResponse
from routes.tweet import TweeSentClient
from routes.stream import TweeSentStream

from tools.utils import open_conf
from tools.models import TweetIn, TweetOut


conf = open_conf("config/config.json")
keys = open_conf("config/keys.json")

app = FastAPI()
# torch_nlp = Predict(conf["bert"])
twitter_client = TweeSentClient(keys)

origins = ["http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

    # TODO: Replace for the DL inferencing.
    tweets = [TweeSentClient.compose_tweet(d, u) for d, u in zip(data, users)]

    return TweetOut(tweets=tweets, token=token)


@app.websocket("/stream/{interval}/{filter}")
async def websocket_stream(websocket: WebSocket, filter: str, interval: int):
    await websocket.accept()
    stream = TweeSentStream(keys, filter, interval)
    try:
        while True:
            tweet = await stream.tweets.get()
            await websocket.send_json(tweet)
    except BaseException:
        stream.aclient.disconnect()
