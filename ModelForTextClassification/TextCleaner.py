import re
import emoji
class TextCleaner():
    def __init__(self,filepath):
        self.filepath = filepath
        self.hash_filepath = "../Scrappers/dataScrappedFromSocialMedia/Text/HashedWords.txt"
        self.process()


    def find_hashed_words(self,text):
        return re.findall(r'\B#\w+', text)

    def remove_hashed_words(self,text):
        return re.sub(r'\B#\w+', '', text)

    def remove_ats_and_numbers(self,text):
        text = text.replace('"', '')
        text = re.sub(r'\B@\w+', '', text)
        return re.sub (r'\d+', '', text)

    def remove_empty_lines(self,text):
        return '\n'.join([line for line in text.split('\n') if line.strip() and not re.fullmatch(r'\W+', line.strip())])

    def process(self):
        with open(self.filepath, 'r', encoding='utf-8') as file:
            text = file.read()

       # cleaned_text = self.remove_emoticons(text)
        hashed_words = self.find_hashed_words(text)

        with open(self.hash_filepath, 'a', encoding='utf-8') as file:
            for word in hashed_words:
                file.write(word + '\n')

        cleaned_text = self.remove_hashed_words(text)
        cleaned_text = self.remove_ats_and_numbers(cleaned_text)
        cleaned_text = self.remove_empty_lines(cleaned_text)
        return cleaned_text
