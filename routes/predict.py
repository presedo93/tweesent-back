# from __future__ import annotations

# import torch
# import torch.nn.functional as f

# from typing import Dict, Tuple
# from pydantic import BaseModel
# from transformers import BertTokenizer

# from models.sentiment import Sentiment


# class SentimentRequest(BaseModel):
#     text: str


# class SentimentResponse(BaseModel):
#     text: str
#     probabilities: Dict[str, float]
#     sentiment: str
#     confidence: float


# class Predict:
#     def __init__(self, conf) -> None:
#         self.conf = conf
#         self.device = torch.device("cpu")
#         self.tokenizer = BertTokenizer.from_pretrained(conf["type"])
#         classifier = Sentiment(conf)
#         state_dict = torch.load(conf["weights"], map_location=self.device)
#         classifier.load_state_dict(state_dict, strict=False)
#         classifier.eval()
#         self.classifier = classifier.to(self.device)

#     def predict(self, text) -> Tuple[Dict[str, float], str, float]:
#         encoded_text = self.tokenizer.encode_plus(
#             text,
#             truncation=True,
#             max_length=self.conf["maxSeqLen"],
#             add_special_tokens=True,
#             return_token_type_ids=False,
#             padding=True,
#             return_attention_mask=True,
#             return_tensors="pt",
#         )

#         encoded_text = {k: v.to(self.device) for k, v in encoded_text.items()}

#         with torch.no_grad():
#             probabilities = f.softmax(self.classifier(encoded_text), dim=1)
#         confidence, predicted_cass = torch.max(probabilities, dim=1)

#         return (
#             self.conf["classes"][predicted_cass.cpu().item()],
#             confidence.cpu().item(),
#         )
