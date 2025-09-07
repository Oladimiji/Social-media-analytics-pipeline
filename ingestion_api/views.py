from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pika
import json
import datetime

class IngestDataView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        if not data:
            return Response({"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a unique user_id if not provided
        user_id = data.get('user_id', f"anonymous-{datetime.datetime.now().isoformat()}")
        message_data = {
            'user_id': user_id,
            'message': data.get('message'),
            'timestamp': datetime.datetime.now().isoformat()
        }

        # Connect to RabbitMQ using the service name 'rabbitmq'
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()

            channel.queue_declare(queue='social_media_posts')
            channel.basic_publish(
                exchange='',
                routing_key='social_media_posts',
                body=json.dumps(message_data)
            )
            print(f"Published message to RabbitMQ: {user_id}")
            connection.close()

            return Response({"status": "Data received and queued successfully."}, status=status.HTTP_200_OK)

        except pika.exceptions.AMQPConnectionError as e:
            print(f"Error connecting to RabbitMQ: {e}")
            return Response({"error": "Failed to connect to message queue."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)