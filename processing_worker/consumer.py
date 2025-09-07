import sys
import os
import pika
import json
import django
from datetime import datetime
from nltk.sentiment import SentimentIntensityAnalyzer

# Get the project root directory and add it to the path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# This line tells the script where to find your Django project's settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'analytics_project.settings')
django.setup()

from processing_worker.models import SocialMediaPost

# This is the function that will be called every time a message arrives
def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f" [x] Received {data}")

    try:
        sid = SentimentIntensityAnalyzer()
        sentiment_scores = sid.polarity_scores(data['message'])
        compound_score = sentiment_scores['compound']
        
        if compound_score >= 0.05:
            sentiment = "positive"
        elif compound_score <= -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"
            
        SocialMediaPost.objects.create(
            user_id=data['user_id'],
            message=data['message'],
            timestamp=datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00')),
            sentiment=sentiment
        )
        print(f" [x] Saved post by {data['user_id']} to database with sentiment: {sentiment}.")
    
    except Exception as e:
        print(f" [x] Failed to save post: {e}")
        import traceback
        traceback.print_exc()

    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='social_media_posts')
        channel.basic_consume(queue='social_media_posts', on_message_callback=callback)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()