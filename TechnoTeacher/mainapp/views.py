from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from mainapp.models import Category, Course, Order, Task, Event, Content
from mainapp.forms import CourseForm, ContentForm, TaskForm, CodeForm, ContactEventForm


def index(request):
    category = Category.objects.all()[0:10]
    event = Event.objects.all()[0:2]
    if 'filter' in request.GET:
        filter_title = request.GET['filter']
        course = Course.objects.filter(category__name__icontains=filter_title, is_active=True)
    else:
        category = Category.objects.all()[0:10]

    context = {
        'category': category,
        'event': event,
        'title': 'TechnoTeacher'
    }

    return render(request, "mainapp/index.html", context)


def events(request):
    events = get_list_or_404(Event)

    context = {
        "events": events,
        "title": "Мероприятия"
    }

    return render(request, "mainapp/events.html", context)


def events_detail(request, pk):
    events = Event.objects.get(id=pk)
    if request.method == 'POST':
        form = ContactEventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно записались на мероприятие')
            return HttpResponseRedirect(reverse('main:events'))
    form = ContactEventForm()

    context = {
        "form": form,
        "events": events,
        "title": f"{events.name}"
    }

    return render(request, "mainapp/events_detail.html", context)


def all_category(request):
    categories = Category.objects.all()[0:10]
    course = Course.objects.filter(is_active=True)

    if 'search' in request.GET:
        title_course = request.GET['search']
        course = Course.objects.filter(name__icontains=title_course, is_active=True)
    elif 'filter' in request.GET:
        filter_title = request.GET['filter']
        course = Course.objects.filter(category__name__icontains=filter_title, is_active=True)
    elif "all" in request.GET:
        course = Course.objects.filter(is_active=True)

    context = {
        'categories': categories,
        'course': course,
        'title': f"Онлайн курсы"
    }

    return render(request, "mainapp/category.html", context)


def about(request):
    context = {
        'title': "О TechnoTeacher"
    }
    return render(request, 'mainapp/about.html', context)


@login_required
def course_detail(request, pk, course):
    category = Category.objects.filter(id=pk)
    course = get_object_or_404(Course, slug=course)
    content = Content.objects.filter(course=course)

    if request.user.is_anonymous:
        order = None
    else:
        try:
            order = Order.objects.get(user=request.user, course=course)
        except:
            order = None

    context = {
        'category': category,
        'course': course,
        'content': content,
        'title': f"{course.name}",
    }

    try:
        if order.course.name in course.name:
            return HttpResponseRedirect(reverse('main:course_order', kwargs={'course': course.slug}))
    except:
        return render(request, 'mainapp/course.html', context)


@login_required
def course_teacher(request):
    if 'search' in request.GET:
        title_course = request.GET['search']
        course = Course.objects.filter(name__icontains=title_course, teachers=request.user, is_active=True)
    else:
        course = Course.objects.filter(teachers=request.user, is_active=True)

    context = {
        "title": "Ваши курсы",
        "course": course,
    }

    return render(request, 'mainapp/teacher/course_teacher.html', context)


@login_required
def course_teacher_detail(request, course):
    course = get_object_or_404(Course, slug=course)
    content = Content.objects.filter(course=course)

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        form_content = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изменения вступили в силу!')
            return HttpResponseRedirect(reverse('main:course_teacher_detail', kwargs={'course': course.slug}))
        elif form_content.is_valid():
            form_content.save()
            messages.success(request, 'Пункт меню добавлен')
            return HttpResponseRedirect(reverse('main:course_teacher_detail', kwargs={'course': course.slug}))
    else:
        form = CourseForm(instance=course)
        form_content = ContentForm()

    context = {
        'course': course,
        'content': content,
        'form': form,
        'form_content': form_content,
        'title': f"{course.name}"
    }

    return render(request, "mainapp/teacher/course_teacher_detail.html", context)


@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Курс создан')
            return HttpResponseRedirect(reverse('auth:profile'))
    else:
        form = CourseForm()
    context = {
        'title': 'Добавить курс',
        'form': form,
    }

    return render(request, 'mainapp/teacher/course_create.html', context)


@login_required
def course_remove(request, course):
    course = Course.objects.get(slug=course)
    course.delete()
    messages.success(request, 'Курс удален')
    return HttpResponseRedirect(reverse('main:course_teacher'))


@login_required
def task_detail(request, pk):
    task = Task.objects.get(id=pk)
    form = CodeForm()
    form.initial['task'] = task.id
    if request.method == "POST":
        form = CodeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('main:task_detail', kwargs={'pk': task.id}))

    context = {
        'title': f'{task.name}',
        'task': task,
        'form': form,
    }

    return render(request, 'mainapp/task.html', context)

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача создан')
            return HttpResponseRedirect(reverse('main:course_teacher'))
    else:
        form = TaskForm()
    context = {
        'title': 'Задача',
        'form': form,
    }

    return render(request, 'mainapp/teacher/task_create.html', context)



@login_required
def task_edit(request, pk):
    task = Task(Task, id=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изменения вступили в силу!')
            return HttpResponseRedirect(reverse('main:course_teacher'))
    else:
        form = TaskForm(instance=task)
    context = {
        'title': f'Изменить курс {task.name}',
        'form': form,
    }
    return render(request, 'mainapp/teacher/task_edit.html', context)


@login_required
def task_remove(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    messages.success(request, 'Курс удален')
    return HttpResponseRedirect(reverse('main:course_teacher'))


@login_required
def content_remove(request, pk):
    content = Content.objects.get(id=pk)
    content.delete()
    messages.success(request, 'Пункт удален')
    return HttpResponseRedirect(reverse('main:course_teacher'))


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


@login_required
def course_order(request, course):
    course = get_object_or_404(Course, slug=course, is_active=True)
    content = Content.objects.filter(course=course)
    task = Task.objects.filter(course=course)

    if request.user.is_anonymous:
        order = None
    else:
        try:
            order = Order.objects.get(user=request.user, course=course)
        except:
            order = None

    context = {
        "course": course,
        'content': content,
        'task': task,
        "title": f"{course.name}",
    }

    if order.course.name in course.name:
        return render(request, 'mainapp/course_order.html', context)


@login_required
def task_finish(request, pk):
    task = Task.objects.get(id=pk)
    task.finish()
    messages.success(request, 'Задача выполена')
    return HttpResponseRedirect(reverse('main:course_order', kwargs={'course': task.course.slug}))
