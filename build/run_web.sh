#!/bin/sh

# wait for PSQL server to start
sleep 10

cd /bots
for dir in $(ls -p -1 | grep /)
do
    cd $dir
    if [ -e ./requirements.txt ]
    then
        pip install -r requirements.txt
    fi
    cd ..
done

cd /app 
# prepare init migration
python manage.py makemigrations myapp
# migrate db, so we have the latest db schema
python manage.py migrate
# collect static files
python manage.py collectstatic --no-input
# start development server on public ip interface, on port 8000
su - django -c "cd /app && uwsgi --socket :8000 --module mysite.wsgi"

## insecure way to run the server
# python manage.py runserver 0.0.0.0:8000
