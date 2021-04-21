import json
import time
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.predict import Predict, SentimentRequest, SentimentResponse
from routes.tweet import TweeterBack, TweetRequest, TweetResponse


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

@app.post("/predict", response_model=SentimentResponse)
async def predict(request: SentimentRequest):
  sentiment, confidence, probabilities = torch_nlp.predict(request.text)
  return SentimentResponse(text=request.text, sentiment=sentiment, confidence=confidence, probabilities=probabilities)

@app.post("/gettweet", response_model=TweetResponse)
async def search(request: TweetRequest, count: int = 200):
  start = time.time()
  tweets = tweet_api.search(request.text, count=count)
  print(f'Fetch tweets: {round(time.time() - start, 3)}s')
  for tw in tweets:
    tw['sentiment'], tw['confidence'] = torch_nlp.predict(tweet_api.re_tweet(tw['text']))
  print(f'Process time: {round(time.time() - start, 3)}s')
  return TweetResponse(tweets=tweets)