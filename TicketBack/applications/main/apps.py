from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'applications.main'
    verbose_name = 'Backend Settings'

    scheduler = BackgroundScheduler()

    def ready(self):
        from jobs import updater
        updater.start(self.scheduler)
