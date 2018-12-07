from django.apps import AppConfig


class GameplayConfig(AppConfig):
    name = 'gameplay'

    def ready(self):
        import gameplay.signals
