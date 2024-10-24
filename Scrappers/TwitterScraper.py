from ntscraper import Nitter
tweets = Nitter().get_tweets("donaldtusk", mode='user', number=100)
print(tweets)
