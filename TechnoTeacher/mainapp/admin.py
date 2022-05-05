from django.contrib import admin
from mainapp.models import Category, Course, Content, Task, Order

admin.site.register([Category, Course, Content, Task, Order])
