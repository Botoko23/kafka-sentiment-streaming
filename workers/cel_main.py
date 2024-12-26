import os
import time

from celery import Celery
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import gspread
from google.oauth2.service_account import Credentials

broker = os.getenv("CELERY_BROKER_URL")

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)
wb = client.open_by_key('sheet id')

nltk.download('vader_lexicon')
sentiment_analyzer = SentimentIntensityAnalyzer()

# Initialize the Celery app
app = Celery(
    'sentiment_task',
    broker=broker,  # Message broker (Redis in this case)
    # backend='redis://localhost:6379/0'  # Result backend
)

@app.task
def sentiment_task(sentence):
    worker_name = sentiment_task.request.hostname
    print(worker_name)
    # Simulate processing the data
    sentiment_scores = sentiment_analyzer.polarity_scores(sentence)
    sentiment_scores['sentence'] = sentence
    data = list(sentiment_scores.values())
    if 'worker1' in worker_name:
        sheet = wb.worksheet('Worker1')
        update_row = len(sheet.col_values(col=1)) + 1
        sheet.update([data], f'A{update_row}:E{update_row}')
    elif 'worker2' in worker_name:
        sheet = wb.worksheet('Worker2')
        update_row = len(sheet.col_values(col=1)) + 1
        sheet.update([data], f'A{update_row}:E{update_row}')
    time.sleep(4)
