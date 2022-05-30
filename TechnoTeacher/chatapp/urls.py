from django.urls import path

import chatapp.views as chatapp

app_name = 'chatapp'

urlpatterns = [
    path('', chatapp.rooms, name='rooms'),
    path('<slug:slug>/', chatapp.room, name='room'),
]
