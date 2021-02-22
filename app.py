from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.predict import Predict, SentimentRequest, SentimentResponse
from routes.tweet import TweeterBack, TweetRequest, TweetResponse


app = FastAPI()
predict = Predict('/backend/config.json')
tweeter = TweeterBack()

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
def predict(request: SentimentRequest, model: Predict = Depends(predict.get_instance)):
  sentiment, confidence, probabilities = model.predict(request.text)
  return SentimentResponse(text=request.text, sentiment=sentiment, confidence=confidence, probabilities=probabilities)


@app.post("/gettweet", response_model=TweetResponse)
def search(request: TweetRequest, api: TweeterBack = Depends(tweeter.get_instance)):
  tweets = api.search(request.text, count=1)
  return TweetResponse(tweets=tweets)