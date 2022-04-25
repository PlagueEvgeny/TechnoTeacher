from django.shortcuts import render
from mainapp.models import Category, Course, Task


def index(request):
    category = Category.objects.all()[0:10]

    context = {
        'category': category,
        'title': 'TechnoTeacher'
    }

    return render(request, "mainapp/index.html", context)


def all_category(request, pk):
    category = Category.objects.filter(id=pk)
    categories = Category.objects.all()[0:10]

    if 'search' in request.GET:
        title_course = request.GET['search']
        course = Course.objects.filter(name__icontains=title_course, category_id=pk)
    else:
        course = Course.objects.filter(category_id=pk)

    context = {
        'category': category,
        'categories': categories,
        'course': course,
    }

    return render(request, "mainapp/category.html", context)
