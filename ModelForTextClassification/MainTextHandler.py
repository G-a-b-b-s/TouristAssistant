#preprocessing
import os

import torch
from transformers import DistilBertTokenizer

from ModelForTextClassification.ClassifierForSocials import DistillBERTClass
from ModelForTextClassification.LanguageDetector import LanguageDetector
from ModelForTextClassification.TextCleaner import TextCleaner
from ModelForTextClassification.ToEnglishConverter import ToEnglishConverter

text = ""
results=[]

directory = "../Scrappers/dataScrappedFromSocialMedia/Text"
for file in os.listdir(directory):
    file_path = os.path.join(directory, file)
    if os.path.isfile(file_path):
        text_cleaner = TextCleaner(file_path)
        text += text_cleaner.process()
print(text)

tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistillBERTClass.from_pretrained('classification_model.pth')


def classify_text(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    prediction = torch.argmax(logits, dim=-1)
    return prediction.item()

for line in text.split('\n'):
    language_detector = LanguageDetector(line)
    language = language_detector.process()

    if language != 'en' and language != 'sw':
        english_sentence = ToEnglishConverter(line, language)
        line = english_sentence.process()

    label = classify_text(line)
    results.append((line, label))

# Print the results
for line, label in results:
    print(f"Text: {line} - Predicted Label: {label}")