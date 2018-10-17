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

## Discord Oauth2 Config

For this you need:

* all packages from `requirements.txt`
* django superuser account
* discord account
* django sites configured to match your domain
  * The `SITE_ID` from your `settings.py`/`local_settings.py` must match the
   site id

First go to the Discord developers documentation and add a new app.
Set redirect to

```http://HOST[:PORT]/accounts/discord/login/callback/```

where `HOST` is the link to the `Django Pokemon Bot Manager` and `PORT` is
optional, e.g. when working on localhost:

``` http://localhost:8000/accounts/discord/login/callback/ ```

Then go to `Django Pokemon Bot Manager` admin panel (`/admin/`) and add a
`social application` with:

* `provider` : `discord`
* `name` : name of your coice
* `client id` : from discord developer app
* `client secret` : from discord developer app


## build static files
If you deploy without docker,  you have to do the following.
1. `apt get install npm`
2. `cd app/static/js/`
3. `npm install`
4. `cd app/static_dirs/js/`
5. `npm install`
6. run `manage.py` task and then execute `collectstatic`.

## OLD Login with Discord Howto

Install required packages:

``` pip install -r requirements.txt ```

Then migrate the Database:

``` manage.py migrate ```

and add a Superuser with manage.py

Go to the Admin site like `localhost:8000/admin`
There you need to add a "Site" and under "Social-Applikations" you need to add
your Discord App. In Discord App set the redirect URL to

``` http://localhost:8000/accounts/discord/login/callback/ ```

