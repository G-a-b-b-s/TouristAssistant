
import os

import torch
from transformers import DistilBertTokenizer

from ModelForTextClassification.ClassifierForSocials import DistillBERTClass
from ModelForTextClassification.LanguageDetector import LanguageDetector
from ModelForTextClassification.TextCleaner import TextCleaner
from ModelForTextClassification.ToEnglishConverter import ToEnglishConverter


class PostTextContentAnalyzer():
    def __init__(self):
         self.text = ""
         self.results = []
         self.directory = "testingData"
         self.model_path = '../classification_model.pth'

    def  get_text(self):
        for file in os.listdir(self.directory):
            file_path = os.path.join(self.directory, file)
            if os.path.isfile(file_path):
                text_cleaner = TextCleaner(file_path)
                self.text += text_cleaner.process()
        return self.text

    def classify_text(self,text):
        tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        model = DistillBERTClass.from_pretrained(self.model_path)
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        model.eval()
        with torch.no_grad():
            outputs = model(**inputs)
        logits = outputs.logits
        prediction = torch.argmax(logits, dim=-1)
        return prediction.item()

    def evaluate_text(self):
        text = self.get_text()
        for line in text.split('\n'):
            language_detector = LanguageDetector(line)
            language = language_detector.process()
            if language != 'en' and language != 'sw':
                english_sentence = ToEnglishConverter(line, language)
                line = english_sentence.process()
            label = self.classify_text(line)
            self.results.append((line, label))
        return self.results

    def get_tourist_type(self):
        outcome = {
            'sports': 0,
            'culture': 0,
            'entertainment': 0
        }
        self.evaluate_text()
        # Print the results
        for line, label in self.results:
            print(f"Text: {line} - Predicted Label: {label}")
            if label == 0:
                outcome['sports'] += 1
            elif label == 1:
                outcome['culture'] += 1
            else:
                outcome['entertainment'] += 1

        print(outcome)

        toursitType = max(outcome, key=outcome.get)

        return toursitType


