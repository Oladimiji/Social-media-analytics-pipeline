This project is a robust and scalable backend system for social media analytics. It's designed to ingest social media data, process it asynchronously, and store it for analysis. The project uses a microservices architecture, with each component responsible for a specific part of the data pipeline.
Features
 * Asynchronous Ingestion: The API receives data and queues it for background processing, ensuring the system remains responsive even under heavy load.
 * Microservices Architecture: The project is composed of independent services (API, RabbitMQ, Worker) managed by Docker, which makes it easy to scale and maintain.
 * Message Queuing: Utilizes RabbitMQ to handle message brokering, providing a reliable buffer between the data ingestion and processing stages.
 * Background Processing: A dedicated worker service consumes messages from the queue to perform tasks like sentiment analysis and data storage.
 * Scalability: The system is designed to handle high volumes of data by allowing you to easily add more worker instances as needed.
Technologies Used
 * Python: The core programming language.
 * Django: The web framework for the API.
 * Django REST Framework (DRF): The toolkit for building the API endpoints.
 * Docker & Docker Compose: Used for containerization and managing the multi-container application.
 * RabbitMQ: The message broker for asynchronous tasks.
 * Pika: The Python library for interacting with RabbitMQ.
 * TextBlob: A library for performing sentiment analysis.
How to Run the Project
Follow these steps to get a local copy of the project running.
Prerequisites
 * Docker
 * Docker Compose
Steps
 * Clone the repository from your GitHub account.
   git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

 * Create a .env file in the root directory and add your API credentials for the social media platform you are using (e.g., Reddit, Twitter).
   # Example for Reddit
REDDIT_CLIENT_ID=YOUR_CLIENT_ID_HERE
REDDIT_CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE

 * Build and run the Docker containers: This will build the images for your API and worker and start all services, including RabbitMQ.
   docker-compose up --build

Usage
Ingesting Data
You can use the ingest_reddit management command to start listening to social media data.
 * Open a new terminal and enter the API container.
   docker-compose exec api bash

 * Run the management command inside the container, specifying a keyword and, optionally, a subreddit.
   python manage.py ingest_reddit "product review" --subreddit "ProductReviews"

This command will fetch posts from Reddit, push them to the RabbitMQ queue, and your worker will then process them.
Checking the Data
You can check your database or logs to see the processed data, including the sentiment.
 * Check Worker Logs: The worker terminal will show messages confirming that data has been received, processed, and saved.
 * Database: You can access your Django admin panel at http://localhost:8000/admin/ to view the saved posts and their sentiment.
Contributing
Feel free to open issues or submit pull requests.
License
