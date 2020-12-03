from typing import Dict
from fastapi import Depends, FastAPI
from pydantic import BaseModel

from routes.predict import Predict


app = FastAPI()
predict = Predict('/backend/config.json')

class SentimentRequest(BaseModel):
  text: str


class SentimentResponse(BaseModel):
  text: str
  probabilities: Dict[str, float]
  sentiment: str
  confidence: float


@app.post("/predict", response_model=SentimentResponse)
def predict(request: SentimentRequest, model: Predict = Depends(predict.get_model)):
  sentiment, confidence, probabilities = model.predict(request.text)
  return SentimentResponse(text=request.text, sentiment=sentiment, confidence=confidence, probabilities=probabilities)