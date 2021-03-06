#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

cd /app  
# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
su - django -c "cd /app && celery -A mysite worker -l info"
