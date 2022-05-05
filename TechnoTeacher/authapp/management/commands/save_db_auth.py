import json

from django.core.management.base import BaseCommand
from authapp.models import UserProfile


class Command(BaseCommand):
    help = 'Makes reserve copy'

    def handle(self, *args, **options):
        items = UserProfile.objects.all()
        data_for_dump = []
        for item in items:
            data_for_dump.append({
                'username': item.username,
                'email': item.email,
                'last_name': item.last_name,
                'first_name': item.first_name,
                'role': item.role,
                'is_superuser': item.is_superuser,
                'is_staff': item.is_staff,
                'password': item.password,
            })
        with open('dump/authapp/profile.json', 'w', encoding='utf-8') as f:
            json.dump(data_for_dump, f)