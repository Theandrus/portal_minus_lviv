from django.shortcuts import render
from user.models import Userprofile
import datetime


def desk_of_shame(request):
    banned_users = []
    users = Userprofile.objects.filter(banned=1)
    for u in users:
        if u.banned_until > datetime.date.today():
            banned_users.append(u)
    return render(request, 'desks/shame.html', {
        "users": banned_users,
    })


def desk_or_respect(request):
    banned_users = []
    users = Userprofile.objects.filter(banned=1)
    for u in users:
        if u.banned_until > datetime.date.today():
            banned_users.append(u)
    return render(request, 'desks/respect.html', {
        "users": banned_users,
    })

