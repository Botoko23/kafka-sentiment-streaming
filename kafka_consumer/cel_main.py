from celery import Celery
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import time


nltk.download('vader_lexicon')
sentiment_analyzer = SentimentIntensityAnalyzer()

# Initialize the Celery app
app = Celery(
    'sentiment_task',
    broker='redis://localhost:6379/0',  # Message broker (Redis in this case)
    # backend='redis://localhost:6379/0'  # Result backend
)

@app.task
def sentiment_task(sentence):
    # Simulate processing the data
    sentiment_scores = sentiment_analyzer.polarity_scores(sentence)
    print(sentiment_scores)
    time.sleep(4)
