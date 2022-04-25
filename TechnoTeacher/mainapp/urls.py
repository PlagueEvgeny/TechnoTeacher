from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'


urlpatterns = [
    path('', mainapp.index, name='index'),
    path('<int:pk>', mainapp.all_category, name='category'),
]
