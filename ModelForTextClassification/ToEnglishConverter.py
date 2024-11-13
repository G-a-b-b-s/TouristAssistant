import emoji
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class ToEnglishConverter():
    def __init__(self, text, language):
        self.text = text
        self.language = language
        self.process()

    def extract_emojis(self, text):
        return ''.join(c for c in text if c in emoji.EMOJI_DATA)

    def remove_emoticons(self,text):
        return emoji.replace_emoji(text, replace='')

    def process(self):

        emojis = self.extract_emojis(self.text)

        self.text = self.remove_emoticons(self.text)
        #translate text to english
        tokenizer = AutoTokenizer.from_pretrained(f"Helsinki-NLP/opus-mt-{self.language}-en")
        model = AutoModelForSeq2SeqLM.from_pretrained(f"Helsinki-NLP/opus-mt-{self.language}-en")

        inputs = tokenizer(self.text, return_tensors="pt")
        translated_tokens = model.generate(**inputs)
        english_translation = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
        final_translation = english_translation + ' ' + emojis
        return final_translation