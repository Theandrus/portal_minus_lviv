import random
import string
from json import JSONDecodeError

import requests
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.db.models import Sum, Count, Case, When, IntegerField, OuterRef, Subquery, Q
from django.contrib.auth.models import User
from liqpay import LiqPay
from rest_framework.response import Response
from rest_framework.views import APIView
from main.forms import AuthForm, AddComments

from django.core import serializers

from user.models import Subscription
from .models import (
    MinusstoreMinusauthor, MinusstoreMinusrecord, MinusstoreMinuscategory, MinusstoreMinusplusrecord,
    MinusstoreMinusquality, MinusstoreMinusarrangement, MinusstoreFiletype, MinusPurchase
)
from minus_lviv.models import DjangoComments, CommentInteraction, DeliverySubscriber, CommentReply
from minusstore.forms import AddMinusForm
from minusstore.serializers import MinusAuthorSerializer
import datetime
import pdfkit


def minusstore_main(request):
    # Операції з фільтрацією категорій
    if 'category' in request.GET:
        selected_categories = request.POST.getlist('categories')
        filtered_items = MinusstoreMinusrecord.objects.filter(category__in=selected_categories)
        # Додайте код для обробки відфільтрованих категорій

    # Отримання списку авторів та фольк-мінусів
    authors = MinusstoreMinusauthor.objects.filter(name__istartswith='А') | MinusstoreMinusauthor.objects.filter(name__istartswith='a')
    folk_minus = MinusstoreMinusrecord.objects.filter(title__istartswith='А', is_folk=1) | MinusstoreMinusrecord.objects.filter(title__istartswith='a', is_folk=1)

    # user = request.user.id
    # try:
    #     exc_minus = MinusstoreMinusrecord.objects.get(user=user)
    # except MinusstoreMinusrecord.DoesNotExist:
    #     exc_minus = None
    # try:
    #     sub = Subscription.objects.filter(user_id=exc_minus.user.id)
    #     print(sub)
    # except Subscription.DoesNotExist:
    #     sub = None

    return render(request, 'minusstore/index.html', {
        'authors': authors,
        'folk_minus': folk_minus,
    })


def minusstore_minus(request, pk):
    user = request.user
    minus = get_object_or_404(MinusstoreMinusrecord, pk=pk)
    author = get_object_or_404(MinusstoreMinusauthor, pk=minus.author_id)
    quality_rate = MinusstoreMinusquality.objects.filter(minus_id=minus.id)
    count_quality_rate = quality_rate.count()
    arrangement_rate = MinusstoreMinusarrangement.objects.filter(minus_id=minus.id)
    count_arrangement_rate = arrangement_rate.count()
    sum_q_rate = quality_rate.aggregate(Sum('rate'))['rate__sum'] or 0
    try:
        quality_rate = sum_q_rate / count_quality_rate
    except ZeroDivisionError:
        quality_rate = 0
    sum_a_rate = arrangement_rate.aggregate(Sum('rate'))['rate__sum'] or 0
    try:
        arrangement_rate = sum_a_rate / count_arrangement_rate
    except ZeroDivisionError:
        arrangement_rate = 0
    comments = DjangoComments.objects.filter(object_pk=pk)
    for comment in comments:
        comment.replies = CommentReply.objects.filter(parent_comment=comment)
    minus.all_rate = (quality_rate + arrangement_rate) / 2
    minus.comments = DjangoComments.objects.filter(object_pk=minus.pk, content_type_id=17)
    # Додайте код для отримання інформації про коментарі та лайки/дизлайки

    print(request.user)
    existing_interaction = CommentInteraction.objects.all()
    com = DjangoComments.objects.all()

    return render(request, 'minusstore/minus.html', {
        'minus': minus,
        'author': author,
        'user': user,
        'comments': comments,
        'existing_interacrion': existing_interaction
    })


def dislike_comment(request, pk):
    comment = DjangoComments.objects.get(id=pk)
    user = request.user.id
    comments = DjangoComments.objects.filter(object_pk=pk)
    user_instance = User.objects.get(id=user)
    if request.method == 'GET':
        try:
            com = CommentInteraction.objects.get(user=user_instance, comment=comment)
            if com.is_disliked is True:
                com.is_disliked = False
                com.save()
            else:
                com.is_disliked = True
                com.save()
        except CommentInteraction.DoesNotExist:
            CommentInteraction.objects.create(
                user=user_instance,
                comment=comment,
                is_disliked=True
            )
    return redirect(minusstore_minus, {'user': user, 'comments': comments})


def if_minus_correct(request, pk):
    form = AuthForm(request.POST)
    minus = get_object_or_404(MinusstoreMinusrecord, pk=pk)
    # Отримання інформації про мінус та категорію

    return render(request, 'minusstore/look_on_minus_correct.html', {
        'minus': minus, 'form': form
        # Додайте інші змінні, які необхідні для відображення сторінки
    })


def pdf_generete(request, pk):
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': 'UTF-8',
    }
    minus = get_object_or_404(MinusstoreMinusrecord, pk=pk)
    text = "<h1>" + minus.lyrics + "</h1>"

    pdf = pdfkit.from_string(text, 'micro.pdf', options=options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="micro.pdf"'
    return response


def letters_filter(request, letter):
    author = MinusstoreMinusauthor.objects.filter(name__istartswith=letter)
    minus_folk = MinusstoreMinusrecord.objects.filter(title__istartswith=letter, is_folk=1)

    return render(request, 'minusstore/index.html', {
        'author': author,
        'letter': letter,
        'minus_folk': minus_folk,
    })


def gave(request, author_id):
    minuses = MinusstoreMinusrecord.objects.filter(author_id=author_id)
    minuses = serializers.serialize("json", minuses)
    return HttpResponse(minuses)


def archiv_of_minuses(request, day):
    date = datetime.date.today()
    minuses = MinusstoreMinusrecord.objects.filter(pub_date__year=date.year, pub_date__month=date.month, pub_date__day=day)
    paginator = Paginator(minuses, 10)
    page = request.GET.get('page')
    try:
        minuses = paginator.page(page)
    except PageNotAnInteger:
        minuses = paginator.page(1)
    except EmptyPage:
        minuses = paginator.page(paginator.num_pages)

    return render(request, 'user/user_minuses.html', {
        'minus': minuses,
        'z': day,
    })


def subscribe(request):
    if request.user.is_authenticated:
        subscriber = DeliverySubscriber.objects.create(email=request.user.email, is_subscribed=1, frequency='weekly', hash="214213a", date=datetime.datetime.now())
        subscriber.save()
        z = "Вітаємо ви підписались на оновлення мінусовок!!"
        k = "Тепер кожного тижня вам на пошту будуть приходити списки нових мінусовок"
        return render(request, 'minusstore/subscribed.html', {
            'z': z,
            'k': k,
        })
    else:
        z = "Вибачте, щоб підписати на оновлення вам потрібно увійти"
        k = "Щоб увійти перейдіть у 'Закуліси'"

        return render(request, 'minusstore/subscribed.html', {
            'z': z,
            'k': k,
        })


def all_minuses_by_date(request):
    minuses = MinusstoreMinusrecord.objects.order_by('-pub_date')
    paginator = Paginator(minuses, 40)
    page = request.GET.get('page')
    try:
        minuses = paginator.page(page)
    except PageNotAnInteger:
        minuses = paginator.page(1)
    except EmptyPage:
        minuses = paginator.page(paginator.num_pages)

    return render(request, 'user/user_minuses.html', {
        'minus': minuses,
        'all_minuses': True,
    })


def add_minus(request):
    user = request.user
    try:
        user_arranger = Subscription.objects.get(user=user.id)
    except Subscription.DoesNotExist:
        user_arranger = 0
    if request.user.is_authenticated:
        minuscategory = MinusstoreMinuscategory.objects.all()[::20]
        minustype = MinusstoreFiletype.objects.all()

        if request.method == "POST":
            form_add_minus = AddMinusForm(request.POST, request.FILES)
            print(1)
            if form_add_minus.is_valid():
                print(2)
                minusrecord = form_add_minus.save(commit=False)
                z = False
                for author in MinusstoreMinusauthor.objects.all():

                    if minusrecord.author and minusrecord.author.lower() == author.name.lower():
                        print(4)
                        minusrecord.author = author
                        z = True
                        break

                if request.POST.get('subscribe'):
                    print(1111)
                    minusrecord.is_paid = True
                    minusrecord.price = True
                    pass
                else:
                    print('fuck')
                    pass

                if not z:
                    print(5)
                    minus_author = MinusstoreMinusauthor.objects.create(name=request.POST.get('surname'))
                    minusrecord.author = minus_author

                minusrecord.user = request.user

                minusrecord.save()
                minuses = MinusstoreMinusrecord.objects.filter(user_id=request.user.id).order_by('-id')
                if 'plus' in request.FILES:
                    print(6)
                    MinusstoreMinusplusrecord.objects.create(minus_id=minusrecord.id, user_id=request.user.id, file=request.FILES['plus'])
                    print('2872')

                return render(request, 'user/user_minuses.html', {
                    'minus': minuses,
                    'user': user
                })

            else:
                print("NOT VALID !!! NOT VALID !!!")
        else:
            form_add_minus = AddMinusForm()

        return render(request, 'minusstore/add_minus.html', {
            'user_arranger': user_arranger,
            'form_add_minus': form_add_minus,
            'minuscategory': minuscategory,
            'minustype': minustype,
            'user': user,
        })
    else:
        return HttpResponseRedirect('../../')


class MinusRecordUpdate(UpdateView):
    model = MinusstoreMinusrecord
    fields = ['title', 'file', 'annotation', 'minus_genre', 'minus_appointment', 'lyrics', 'plusrecord']
    template_name_suffix = '_update_form'


def minus_search(request):
    search_query = request.GET.get('search', '')
    minuses = MinusstoreMinusrecord.objects.filter(title__istartswith=search_query)
    paginator = Paginator(minuses, 40)
    page = request.GET.get('page')
    try:
        minuses = paginator.page(page)
    except PageNotAnInteger:
        minuses = paginator.page(1)
    except EmptyPage:
        minuses = paginator.page(paginator.num_pages)

    return render(request, 'user/user_minuses.html', {
        'minus': minuses,
        'k': True,
    })


def minusarrangement(request, user_id, minus_id, assessment):
    try:
        minus_arrangement = MinusstoreMinusarrangement.objects.get(minus_id=minus_id, user_id=user_id)
        minus_arrangement.rate = assessment
        minus_arrangement.save()
        return HttpResponse(assessment)
    except MinusstoreMinusarrangement.DoesNotExist:
        minus_arrangement = MinusstoreMinusarrangement.objects.create(minus_id=minus_id, user_id=user_id, rate=assessment)
        minus_arrangement.save()
        return HttpResponse(assessment)


def minusquality(request, user_id, minus_id, assessment):
    try:
        minus_quality = MinusstoreMinusquality.objects.get(minus_id=minus_id, user_id=user_id)
        minus_quality.rate = assessment
        minus_quality.save()
        return HttpResponse(assessment)
    except MinusstoreMinusquality.DoesNotExist:
        minus_quality = MinusstoreMinusquality.objects.create(minus_id=minus_id, user_id=user_id, rate=assessment)
        minus_quality.save()
        return HttpResponse(assessment)


class MinusAuthor(APIView):
    def get_objects(self, letter):
        return MinusstoreMinusauthor.objects.filter(name__istartswith=letter)

    def get(self, request, letter='А', format=None):
        authors = self.get_objects(letter)
        paginator = Paginator(authors, 40)
        page = self.request.GET.get('page')
        try:
            authors = paginator.page(page)
        except PageNotAnInteger:
            authors = paginator.page(1)
        except EmptyPage:
            authors = paginator.page(paginator.num_pages)

        serializer_context = {
            'request': request,
        }
        authors = MinusAuthorSerializer(authors, many=True, context=serializer_context)
        return Response(authors.data)


def payment_for_minus(request, pk):
    liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    minus = MinusstoreMinusrecord.objects.get(id=pk)
    minus_price = minus.price

    # creating order id with random symbols for invoice
    characters = string.ascii_letters + string.digits
    order_id = ''.join(random.choice(characters) for _ in range(10))
    print(order_id)

    params = liqpay.api("request", {
        "action": "invoice_send",
        "version": "3",
        "email": request.user.email,
        "amount": "1",
        "currency": "UAH",
        "order_id": order_id,
        "description": 'Купівля мінусівки',
        "action_payment": "pay",
        "language": 'uk',
    })

    signature = liqpay.cnb_signature(params)
    data = liqpay.cnb_data(params)
    params = {'data': data, 'signature': signature}

    res = requests.post(url='https://www.liqpay.ua/api/3/checkout/', data=params)

    if res.status_code == 200:
        # MinusPurchase.objects.create(user=request.user, minus_id=pk, order_id=order_id, email=request.user.email,
        #                              is_paid=False)
        return redirect(res.url, {'minus': minus})
    else:
        return render(request, 'minusstore/index.html')

