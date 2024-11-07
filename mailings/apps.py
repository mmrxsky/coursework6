from django.apps import AppConfig


class MailingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mailings"

    # def ready(self):
    #     from mailings.management.commands import runapscheduler
    #     sleep(2)
    #     runapscheduler()
