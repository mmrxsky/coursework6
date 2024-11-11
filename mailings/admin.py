from django.contrib import admin

from mailings.models import Client, Message, Mailing, Log


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
    )
    list_filter = ("name",)
    search_fields = (
        "name",
        "email",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("title",)
    list_filter = ("title",)
    search_fields = ("title",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "time_start",
        "time_end",
        "period",
        "status",
    )
    list_filter = ("time_start",)
    search_fields = ("time_start",)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = (
        "date_time",
        "status",
    )
    list_filter = ("date_time",)
    search_fields = ("date_time",)
