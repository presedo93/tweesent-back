import json
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
def search(request: TweetRequest, count: int = 0):
  tweets = tweet_api.search(request.text, count=count)
  return TweetResponse(tweets=tweets)