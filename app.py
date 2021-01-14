from typing import Dict
from fastapi import Depends, FastAPI
from pydantic import BaseModel

from routes.predict import Predict

from routes.tweet import TweeterBack


app = FastAPI()
predict = Predict('/backend/config.json')
tweeter = TweeterBack()


class SentimentRequest(BaseModel):
  text: str


class SentimentResponse(BaseModel):
  text: str
  probabilities: Dict[str, float]
  sentiment: str
  confidence: float


class TweetRequest(BaseModel):
  text:str


class TweetResponse(BaseModel):
  text: str


@app.post("/predict", response_model=SentimentResponse)
def predict(request: SentimentRequest, model: Predict = Depends(predict.get_model)):
  sentiment, confidence, probabilities = model.predict(request.text)
  return SentimentResponse(text=request.text, sentiment=sentiment, confidence=confidence, probabilities=probabilities)


@app.post("/gettweet", response_model=TweetResponse)
def search(request: TweetRequest, api: TweeterBack = Depends(tweeter.get_model)):
  api.search(request.text)
  return TweetResponse(text="OK")