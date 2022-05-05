import json

from django.core.management.base import BaseCommand
from authapp.models import UserProfile


class Command(BaseCommand):
    help = 'Makes reserve copy'

    def handle(self, *args, **options):
        with open('dump/authapp/profile.json', 'r', encoding='utf-8') as f:
            data_for_resore = json.load(f)

        for item in data_for_resore:
            UserProfile.objects.create(**{
                'username': item['username'],
                'email': item['email'],
                'role': item['role'],
                'is_superuser': item['is_superuser'],
                'is_staff': item['is_staff'],
                'last_name': item['last_name'],
                'first_name': item['first_name'],
                'password': item['password'],
            })
