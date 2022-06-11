from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path("events/", mainapp.events, name="events"),
    path("events/detail/<int:pk>/", mainapp.events_detail, name="events_detail"),
    path('about/', mainapp.about, name='about'),
    # Категории
    path('category/', mainapp.all_category, name='category'),
    # Курсы
    path('course/<int:pk>/<slug:course>/', mainapp.course_detail, name='course'),
    path('course/education/<slug:course>/', mainapp.course_order, name='course_order'),
    # Преподавание
    path('course/teacher/', mainapp.course_teacher, name='course_teacher'),
    path('course/teacher/create/', mainapp.course_create, name='course_create'),
    path('course/teacher/<slug:course>/', mainapp.course_teacher_detail, name='course_teacher_detail'),
    path('course/teacher/<slug:course>/remove/', mainapp.course_remove, name='course_remove'),
    # Содержание
    path('course/teacher/content/<int:pk>/remove/', mainapp.content_remove, name='content_remove'),
    # Покупка товаров
    path('course/add/<int:pk>/', mainapp.add_order, name='add_order'),
    # Задачи
    path("course/task/<int:pk>/", mainapp.task_detail, name='task_detail'),
    path("course/teacher/task/create/", mainapp.task_create, name='task_create'),
    path("course/teacher/task/<int:pk>/remove/", mainapp.task_remove, name='task_remove'),
    path("course/task/finish/<int:pk>/", mainapp.task_finish, name="task_finish"),

]
