import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

class SentimentAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def get_sentiment(self, text):
        sentiment_scores = self.sia.polarity_scores(text)
        return sentiment_scores['compound']

    def get_emotional_quotient(self, text):
        sentiment_scores = self.sia.polarity_scores(text)
        emotional_quotient = (sentiment_scores['pos'] + sentiment_scores['neu']) / (sentiment_scores['pos'] + sentiment_scores['neu'] + sentiment_scores['neg'])
        return emotional_quotient