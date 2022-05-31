import json

from django.core.management.base import BaseCommand
from mainapp.models import Course, Category, Task, Order, Content


class Command(BaseCommand):
    help = 'Makes reserve copy'

    def handle(self, *args, **options):
        with open('dump/mainapp/category.json', 'r', encoding='utf-8') as f:
            data_for_resore = json.load(f)

        for item in data_for_resore:
            Category.objects.create(**{
                'name': item['name'],
                'desc': item['desc'],
                'slug': item['slug'],
                'is_active': item['is_active'],
            })

