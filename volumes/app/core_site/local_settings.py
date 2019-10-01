DATABASES = {
    'default': {
        'ENGINE'  : 'django.db.backends.postgresql_psycopg2',
        'NAME'    : 'postgres',
        'USER'    : 'postgres',
        'PASSWORD': 'changeme',
        'HOST'    : '127.0.0.1',
        'PORT'    : '5432',
    },
    'rocketdb': {
        'ENGINE'  : 'django.db.backends.mysql',
        'NAME'    : 'rocketdb',
        'USER'    : 'rocketdb',
        'PASSWORD': 'AnotherStrongPassword',
        'HOST'    : '127.0.0.1',
        'PORT'    : '3310',
    },
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG" : {
            "hosts": [("localhost", 6379)],
        },
    },
}

ALLOWED_HOSTS = ['*']
SECRET_KEY = 'changeme'
DEBUG = True

SITE_ID = 2

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

OSR_ROUTING = True
# get a openrouteservice token at https://openrouteservice.org/dev
OSR_TOKEN = '5b3ce3597851110001cf624823ca146158fb456582f26e4c53bc7173'
