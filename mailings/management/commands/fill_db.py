from django.core.management import BaseCommand

from mailings.models import Mailing, Client, Message

import psycopg2

import json


class Command(BaseCommand):

    def get_data_from_mailings(self):

        result_mailings_list = []
        with open('mailings/fixtures/mailing.json', 'r', encoding='utf-8') as file:
            mailing_json = json.load(file)

            for item in mailing_json:
                result_mailings_list.append(item)
        return result_mailings_list

    def get_data_from_client(self):

        result_client_list = []
        with open('mailings/fixtures/client.json', 'r', encoding='utf-8') as file:
            client_json = json.load(file)

            for item in client_json:
                result_client_list.append(item['fields'])
        return result_client_list

    def get_data_from_message(self):

        result_message_list = []
        with open('mailings/fixtures/message.json', 'r', encoding='utf-8') as file:
            message_json = json.load(file)

            for item in message_json:
                result_message_list.append(item['fields'])
        return result_message_list

    def handle(self, *args, **options):

        conn = psycopg2.connect(
            host="localhost",
            database="course_6",
            user="postgres",  # Введите ИМЯ ПОЛЬЗОВАТЕЛЯ
            password="2468"  # Введите ПАРОЛЬ
        )
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute("""
                            TRUNCATE TABLE mailings_mailing RESTART IDENTITY CASCADE;
                            TRUNCATE TABLE mailings_client RESTART IDENTITY CASCADE;
                            TRUNCATE TABLE mailings_message RESTART IDENTITY CASCADE;
                        """)
        cur.close()
        conn.close()

        client_for_create = []

        for client_item in self.get_data_from_client():
            client_for_create.append(
                Client(name=client_item["name"],
                       email=client_item["email"],
                       comment=client_item["comment"]),
            )
        Client.objects.bulk_create(client_for_create)

        message_for_create = []

        for message_item in self.get_data_from_message():
            message_for_create.append(
                Message(title=message_item["title"],
                        message=message_item["message"]),
            )
        Message.objects.bulk_create(message_for_create)

        mailings_for_create = []

        for mailings_item in self.get_data_from_mailings():
            mailings_for_create.append(
                Mailing(pk=mailings_item["pk"],
                        time_start=mailings_item['fields']["time_start"],
                        time_end=mailings_item['fields']["time_end"],
                        period = mailings_item['fields']["period"],
                        message=Message.objects.get(pk=mailings_item['fields']['message']),

                        clients=Client.objects.get(pk=mailings_item['fields']["clients"][0])),
                        )
        Mailing.objects.bulk_create(mailings_for_create)