from django.shortcuts import render
from django.http import HttpResponseRedirect
from minus_lviv.models import MessagesMessage
from django.contrib.auth.models import User
from django.db.models import Q
from messanger.models import NewMessagesChannels


def messanger(request):
    if request.user.is_authenticated:
        sender = MessagesMessage.objects.filter(Q(recipient_id=request.user.id) | Q(sender_id=request.user.id)).values('sender_id', 'recipient_id')
        sender = User.objects.filter(Q(id__in=sender.values('sender_id')) | Q(id__in=sender.values('recipient_id'))).order_by('-id')
        for i in sender:
            i.new = NewMessagesChannels.objects.filter(frm_user=i.id)
            print(i.new)
            print('messanger sender if exist new')
        return render(request, 'messanger/messanger.html', {'sender': sender})
    else:
        return HttpResponseRedirect('/')
