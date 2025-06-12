from .models import ForumPost, ForumThread
from minusstore.models import MinusstoreMinusweekstats, MinusstoreMinusrecord
from user.models import Userprofile, UsersUserrating
import lxml.html
from minus_lviv.models import DjangoComments


def top_minus_per_all_time():
    top_minus_per_all_time = []

    minus_record = MinusstoreMinusrecord.objects.order_by('-rating_score')[:10]

    for i in minus_record:
        top_minus_per_all_time.append(i)

    return top_minus_per_all_time


def top_minus_per_week():
    minus_week_stats = MinusstoreMinusweekstats.objects.order_by('-rate')[:10]
    mwk = [i.minus_id for i in minus_week_stats]

    top_minus_per_week = MinusstoreMinusrecord.objects.filter(pk__in=mwk)

    return top_minus_per_week


def top_users():
    users = UsersUserrating.objects.order_by('-rating')[:10]
    return users


def last_forum():
    post = ForumPost.objects.order_by('-id')[:10]

    for i in post:
        i.thread_text = ForumThread.objects.get(id=i.thread_id).title

        i.body = lxml.html.fromstring(i.body).text_content()
        i.body = i.body[:150] + '...'

    return post

def last_comments():
    comments = DjangoComments.objects.order_by('-id')[:30]
    return comments
