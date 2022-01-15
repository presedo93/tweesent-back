import numpy as np
import onnxruntime as ort

from typing import Dict
from transformers import AutoTokenizer


class OnnxPredict:
    labels = ["negative", "neutral", "positive"]

    def __init__(self, conf: Dict) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(conf["tokenizer"])
        self.model = ort.InferenceSession(
            conf["model"], providers=["CUDAExecutionProvider"]
        )

        self.attention_mask = self.model.get_inputs()[0].name
        self.input_ids = self.model.get_inputs()[1].name

        self.labels = conf["classes"]

    def predict(self, tweet: str) -> str:
        sample = self.tokenizer(tweet, truncation=True)
        f_inputs = {
            self.attention_mask: np.expand_dims(sample["attention_mask"], axis=0),
            self.input_ids: np.expand_dims(sample["input_ids"], axis=0),
        }
        out = self.model.run(None, f_inputs)
        return self.labels[out[0].argmax()]
