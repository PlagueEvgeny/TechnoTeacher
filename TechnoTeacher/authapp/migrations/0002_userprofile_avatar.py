# Generated by Django 3.2.9 on 2022-04-23 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatar/default.png', upload_to='avatar/'),
        ),
    ]
