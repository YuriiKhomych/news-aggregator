#!/bin/sh

# wait for RabbitMQ server to start
sleep 30

# run Celery worker for our project news_aggregator with Celery configuration stored in Celeryconf
su -m myuser -c "celery worker -A news_aggregator -B -l info"