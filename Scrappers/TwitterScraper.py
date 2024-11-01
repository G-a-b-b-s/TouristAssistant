import os

from ntscraper import Nitter

class TwitterScrapper():
    def __init__(self, username):
        self.username = username
        self.scrap_twitter()

    def scrap_twitter(self):
        tweets = Nitter().get_tweets(self.username, mode='user')
        text = ""
        for tweet in tweets['tweets']:
            text+= tweet['text']
            text+= "\n"

        os.makedirs("./Scrappers/dataScrappedFromSocialMedia/Text/", exist_ok=True)
        with open("./Scrappers/dataScrappedFromSocialMedia/Text/Twitter.txt", "w", encoding='utf-8') as f:
            f.write(text)
