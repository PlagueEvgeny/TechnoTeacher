from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'


urlpatterns = [
    path('', mainapp.index, name='index'),
    path('<int:pk>/<slug:category>', mainapp.all_category, name='category'),
    path('course/<int:pk>/<slug:course>', mainapp.course_detail, name='course'),
]
