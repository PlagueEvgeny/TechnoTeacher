from django.urls import path

import chatapp.views as chatapp

app_name = 'chatapp'

urlpatterns = [
    path('', chatapp.index, name='index'),
    path('dialog/show/<int:dialog_pk>/', chatapp.dialog_show, name='dialog_show'),
    path('user/dialog/create/<int:user_id>/', chatapp.user_dialog_create,
         name='user_dialog_create'),
    path('user/dialog/delete/<int:pk>/', chatapp.dialog_delete,
         name='dialog_delete'),

    path('dialog/member/<int:sender_pk>/message/create/',
         chatapp.DialogMessageCreate.as_view(),
         name='dialog_message_create'),

    path('user/dialog/new/messages/<int:dialog_pk>/',
         chatapp.dialog_new_messages,
         name='dialog_new_messages'),
]
