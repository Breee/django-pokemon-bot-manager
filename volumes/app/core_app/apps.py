from django.apps import AppConfig


class MyappConfig(AppConfig):
    name = 'core_app'

    def ready(self):
        import core_app.signals
