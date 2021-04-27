from django.apps import AppConfig


class EquityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'equity'

    def ready(self):
    	from sharesUpdater import updater
    	updater.start()