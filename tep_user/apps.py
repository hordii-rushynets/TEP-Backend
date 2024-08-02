from django.apps import AppConfig


class TepUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tep_user'

    def ready(self):
        import tep_user.signals
