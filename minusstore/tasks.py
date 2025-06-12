import datetime
from django.core.mail import send_mail
from minus_lviv.celery import app
from minusstore.models import MinusstoreMinusrecord
from celery.schedules import crontab


@app.task
def minus_send_new():
    m = []
    minuses = list(MinusstoreMinusrecord.objects.filter(pub_date__gte=datetime.datetime.now() - datetime.timedelta(days=7)))
    for i in minuses:
        m.append(i.title)

    m = ', '.join(m)
    send_mail('celery', f'Доброго дня! Шановний користувач. За останній тиждень добавились такі мінусовки: {m}', 'minuslviv@gmail.com', ['turupuru8@gmail.com'])

