# How to start celery and redis

Open a new Terminal and install Redis with:
'''
apt install redis
'''
or similar with your favorite Package Manager.

Start redis server:
Open Terminal ''' redis-server '''

Then you can: ''' pip install -r requirements.txt '''

Tested from within PyCharm IDE:
Goto Terminal and type:

'''celery -A app worker -l info'''

Then Celery should start a Worker.