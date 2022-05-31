import json

from django.core.management.base import BaseCommand
from mainapp.models import Category, Course


class Command(BaseCommand):
    help = 'Makes reserve copy'

    def handle(self, *args, **options):
        category = Category.objects.all()
        data_for_dump = []
        for item in category:
            data_for_dump.append({
                'name': item.name,
                'desc': item.desc,
                'slug': item.slug,
                'is_active': item.is_active,
            })
        with open('dump/mainapp/category.json', 'w', encoding='utf-8') as f:
            json.dump(data_for_dump, f)


        course = Course.objects.all()
        data_for_dump = []
        for item in course:
            data_for_dump.append({
                'category': item.category.id,
                'name': item.name,
                'desc': item.desc,
                'slug': item.slug,
                'status': item.status,
                'is_active': item.is_active,
            })
        with open('dump/mainapp/course.json', 'w', encoding='utf-8') as f:
            json.dump(data_for_dump, f)