from django.core.management import BaseCommand

from catalog.models import Product, Category

import psycopg2

import json


class Command(BaseCommand):

    def get_data_from_category(self):

        result_category_list = []
        with open('catalog/fixture/category_data.json', 'r', encoding='utf-8') as file:
            category_json = json.load(file)

            for item in category_json:
                result_category_list.append(item)
        return result_category_list

    def get_data_from_product(self):

        result_product_list = []
        with open('catalog/fixture/product_data.json', 'r', encoding='utf-8') as file:
            product_json = json.load(file)

            for item in product_json:
                result_product_list.append(item['fields'])
        return result_product_list

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
                            TRUNCATE TABLE catalog_product RESTART IDENTITY CASCADE;
                            TRUNCATE TABLE catalog_category RESTART IDENTITY CASCADE;
                        """)
        cur.close()
        conn.close()


        # Product.objects.all().delete()
        # Category.objects.all().delete()

        category_for_create = []

        for category_item in self.get_data_from_category():
            category_for_create.append(
                Category(pk=category_item["pk"],
                         name=category_item["fields"]["name"],
                         description=category_item["fields"]["description"])
                        )
        Category.objects.bulk_create(category_for_create)

        product_for_create = []

        for product_item in self.get_data_from_product():
            product_for_create.append(
                Product(name=product_item["name"],
                        description=product_item["description"],
                        image=product_item["image"],
                        category=Category.objects.get(pk=product_item["category"]),
                        price=product_item["price"])
                        )
        Product.objects.bulk_create(product_for_create)