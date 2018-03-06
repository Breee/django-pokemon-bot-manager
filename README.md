# Login with Discord Howto:

Install required packages:

``` pip install -r requirements.txt ```

Then migrate the Database:

``` manage.py migrate ```

and add a Superuser with manage.py

Go to the Admin site like `localhost:8000/admin`
There you need to add a "Site" and under "Social-Applikations" you need to add your Discord App.
In Discord App set the redirect URL to 

``` http://localhost:8000/accounts/discord/login/callback/ ```

