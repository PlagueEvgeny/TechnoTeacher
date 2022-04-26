from django.shortcuts import render, get_object_or_404 
from mainapp.models import Category, Course, Task


def index(request):
    category = Category.objects.all()[0:10]

    context = {
        'category': category,
        'title': 'TechnoTeacher'
    }

    return render(request, "mainapp/index.html", context)


def all_category(request, category, pk):
    category = Category.objects.filter(slug=category)
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
        'title': f"Оналайн курсы '{Category.objects.get(id=pk)}'"
    }

    return render(request, "mainapp/category.html", context)

def course_detail(request, pk, course):
    category = Category.objects.filter(id=pk)
    course = get_object_or_404(Course, slug=course)

    context = {
        'category': category,
        'course':course,
        'title': 'TechnoTeacher'
    }

    return render(request, "mainapp/course.html", context)



