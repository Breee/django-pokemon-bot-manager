# Django Pokemon Bot Manager

## deploy with docker

* copy `docker-compose.yml.dist` to `docker-compose.yml` and configure
  environment variables.

* copy `volumes/app/mysite/local_settings.py.dist` to
  `volumes/app/mysite/local_settings.py` and configure it. You can
   overwrite all settings made in settings.py

* build and start it with `docker-compose up -d`

## configure rest api with token auth

Go `admin/authtoken/token/` panel and create tokens

In your client add it like
`Authorization: Token 53f5dea10a90204376a3786eaeb67f02c3c1d6cb`
to your headers.

POST requests are done by json in body.

## Login with Discord Howto

Install required packages:

``` pip install -r requirements.txt ```

Then migrate the Database:

``` manage.py migrate ```

and add a Superuser with manage.py

Go to the Admin site like `localhost:8000/admin`
There you need to add a "Site" and under "Social-Applikations" you need to add
your Discord App. In Discord App set the redirect URL to

``` http://localhost:8000/accounts/discord/login/callback/ ```

