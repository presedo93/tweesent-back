import json
from torch import nn
from transformers import BertModel


class Sentiment(nn.Module):
    def __init__(self, conf):
        super(Sentiment, self).__init__()
        n_classes = len(conf["classes"])
        self.bert = BertModel.from_pretrained(conf["type"])
        self.drop = nn.Dropout(p=0.3)
        self.out = nn.Linear(self.bert.config.hidden_size, n_classes)

    def forward(self, inputs):
        _, pooled_output = self.bert(**inputs).values()
        output = self.drop(pooled_output)
        return self.out(output)
