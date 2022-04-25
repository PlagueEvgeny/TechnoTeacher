from django import template  
from chatapp.models import Dialog, DialogMembers, Message
from django.shortcuts import render, get_object_or_404
from authapp.models import UserProfile
  
  
register = template.Library()  

@register.simple_tag  
def dialog_create(request):
    dialogues = request.user.dialogs.select_related('dialog').all(). \
        values_list('dialog_id', flat=True)
    interlocutors = DialogMembers.objects.filter(dialog__in=dialogues). \
        values_list('member_id', flat=True)
    new_interlocutors = UserProfile.objects.exclude(pk__in=interlocutors)

    context = {
        'page_title': 'новый диалог',
        'new_interlocutors': new_interlocutors,
    }
    return context