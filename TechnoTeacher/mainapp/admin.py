from django.contrib import admin
from mainapp.models import Category, Course, Task, Order

admin.site.register([Category, Course, Task, Order])
