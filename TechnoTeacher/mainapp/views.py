from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from mainapp.models import Category, Course, Order, Task



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
    
    if request.user.is_anonymous == True:
    	order = None
    else:
    	order = Order.objects.filter(user=request.user)


    if 'search' in request.GET:
        title_course = request.GET['search']
        course = Course.objects.filter(name__icontains=title_course, category_id=pk)
    else:
        course = Course.objects.filter(category_id=pk)


    context = {
        'category': category,
        'categories': categories,
        'course': course,
        'order': order,
        'title': f"Онлайн курсы {Category.objects.get(id=pk)}"
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

@login_required
def add_order(request, pk):
    course = get_object_or_404(Course, id=pk)
    Order.objects.get_or_create(
        user=request.user,
        course=course,
    )
    messages.success(request, 'Вы успешно заказали товар!')
    return HttpResponseRedirect(
        reverse('auth:profile')
    )



