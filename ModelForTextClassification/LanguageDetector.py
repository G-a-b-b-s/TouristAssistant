import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

class LanguageDetector():
    def __init__(self, text, model_ckpt="papluca/xlm-roberta-base-language-detection"):
        self.model_ckpt = model_ckpt
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_ckpt)
        self.text = text
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_ckpt)

    def process(self):
        inputs = self.tokenizer(self.text, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            logits = self.model(**inputs).logits
        preds = torch.softmax(logits, dim=-1)
        id2lang = self.model.config.id2label
        vals, idxs = torch.max(preds, dim=1)
        return id2lang[idxs.item()]

