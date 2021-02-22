import json
import torch
import torch.nn.functional as f

from typing import Dict
from pydantic import BaseModel
from transformers import BertTokenizer

from models.sentiment import Sentiment


class SentimentRequest(BaseModel):
  text: str


class SentimentResponse(BaseModel):
  text: str
  probabilities: Dict[str, float]
  sentiment: str
  confidence: float


class Predict:
  def __init__(self, conf):
    with open("config.json") as json_file:
      conf = json.load(json_file)
    self.conf = conf
    self.device = torch.device("cpu")
    self.tokenizer = BertTokenizer.from_pretrained(conf["bert_model"])
    classifier = Sentiment(conf)
    state_dict = torch.load(conf["pretrained_model"], map_location=self.device)
    classifier.load_state_dict(state_dict, strict=False)
    classifier.eval()
    self.classifier = classifier.to(self.device)

  def get_instance(self):
    return self

  def predict(self, text):
    encoded_text = self.tokenizer.encode_plus(
        text,
        max_length=self.conf["max_seq_len"],
        add_special_tokens=True,
        return_token_type_ids=False,
        pad_to_max_length=True,
        return_attention_mask=True,
        return_tensors="pt",
    )

    inputs = encoded_text["input_ids"].to(self.device)
    attention_mask = encoded_text["attention_mask"].to(self.device)

    with torch.no_grad():
      probabilities = f.softmax(self.classifier(inputs, attention_mask), dim=1)
    confidence, predicted_cass = torch.max(probabilities, dim=1)
    predicted_cass = predicted_cass.cpu().item()
    probabilities = probabilities.flatten().cpu().numpy().tolist()

    return (
        self.conf["class_names"][predicted_cass],
        confidence,
        dict(zip(self.conf["class_names"], probabilities)),
        )