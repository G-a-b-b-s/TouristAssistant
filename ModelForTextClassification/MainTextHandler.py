#preprocessing
import os

from ModelForTextClassification.LanguageDetector import LanguageDetector
from ModelForTextClassification.TextCleaner import TextCleaner
from ModelForTextClassification.ToEnglishConverter import ToEnglishConverter

text = ""

directory = "../Scrappers/dataScrappedFromSocialMedia/Text"
for file in os.listdir(directory):
    file_path = os.path.join(directory, file)
    if os.path.isfile(file_path):
        text_cleaner = TextCleaner(file_path)
        text += text_cleaner.process()

#wykryj język i w razie potrzeby przetłumacz
for line in text.split('\n'):
    language_detector = LanguageDetector(line)
    language = language_detector.process()

    if language!='en' and language!='sw':
        english_sentence = ToEnglishConverter(line, language)
        line = english_sentence

#classify the text


