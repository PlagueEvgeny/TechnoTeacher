from django.contrib.auth.decorators import login_required
from authapp.models import UserProfile
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView
from django.contrib import messages
from chatapp.forms import DialogMessageForm
from chatapp.models import Dialog, DialogMembers, Message


def index(request):
    dialogues = request.user.dialogs.select_related('dialog').all()
    dialog = request.user.dialogs.select_related('dialog').all(). \
        values_list('dialog_id', flat=True)
    interlocutors = DialogMembers.objects.filter(dialog__in=dialog). \
        values_list('member_id', flat=True)
    new_interlocutors = UserProfile.objects.exclude(pk__in=interlocutors)
    context = {
        'page_title': 'диалоги',
        'dialogues': dialogues,
        'new_interlocutors': new_interlocutors,
    }

    return render(request, 'chatapp/index.html', context)

class DialogMessageCreate(CreateView):
    model = Message
    form_class = DialogMessageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context['form']
        sender_pk = self.request.resolver_match.kwargs['sender_pk']
        # print(context)
        # print(form.fields['sender'].initial)
        # print(dir(form.fields['sender']))
        # print(sender_pk)
        # print(form.initial)
        # form.fields['sender'].initial = sender_pk
        form.initial['sender'] = sender_pk

        return context

    def get_success_url(self):
        # print(self.object.sender.dialog_id)
        # return reverse('main:index')
        return reverse(
            'chat:dialog_show',
            kwargs={'dialog_pk': self.object.sender.dialog_id}
        )

    def get_success_url(self):
        return reverse(
            'chat:dialog_show',
            kwargs={'dialog_pk': self.object.sender.dialog_id}
        )


def dialog_show(request, dialog_pk):
    dialogs = get_object_or_404(Dialog, pk=dialog_pk)
    sender = dialogs.get_sender(request.user.pk)
    

    context = {
        'page_title': 'диалог',
        'dialogs': dialogs,
        'sender': sender,
    }

    return render(request, 'chatapp/dialog_show.html', context)


def user_dialog_create(request, user_id):
    interlocutor = UserProfile.objects.get(pk=user_id)
    dialog = Dialog.objects.create(
        name=interlocutor.username
    )
    DialogMembers.objects.create(
        dialog=dialog,
        member=request.user,
        role=DialogMembers.CREATOR
    )
    DialogMembers.objects.create(
        dialog=dialog,
        # member_id=user_id,
        member=interlocutor,
        role=DialogMembers.INTERLOCUTOR
    )

    return HttpResponseRedirect(
        reverse('chat:dialog_show', kwargs={'dialog_pk': dialog.pk})
    )

# CBV
def dialog_delete(request, pk):
    instance = get_object_or_404(Dialog, pk=pk)
    instance.delete()
    return HttpResponseRedirect(reverse('chat:index'))


def dialog_new_messages(request, dialog_pk):
    if request.is_ajax():
        dialog = Dialog.objects.filter(pk=dialog_pk).first()
        status = False
        new_messages = None
        if dialog:
            status = True
            _new_messages = dialog.get_messages_new(request.user.pk)
            new_messages = [{'pk': el.pk,
                             'username': el.sender.member.username,
                             'created': el.created.strftime('%Y.%m.%d %H:%M'),
                             'text': el.text}
                            for el in _new_messages]
        return JsonResponse({
            'status': status,
            'new_messages': new_messages,
        })
    return HttpResponseRedirect(reverse('chatapp:index'))