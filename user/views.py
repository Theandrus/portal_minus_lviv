import random
import string

import pytz
from django.conf import settings
import requests
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from datetime import datetime

from liqpay import LiqPay

from user.models import Userprofile, UsersUserrating, FriendsFriendshipFriends, FriendsFriendship, \
    FriendsFriendshiprequest, UserActivitys, UserPost, UserStatus, Subscription
from minus_lviv.models import DjangoComments, ForumPost
from messanger.models import Channels
from album.models import PhotosPhotoalbum, PhotosPhoto
from minusstore.models import MinusstoreMinusauthor, MinusstoreMinusrecord
from main.models import ModeratorMessages
from shop.models import BlurbsBlurb, SelectedBlurb

from user.tokens import account_activation_token
from user.forms import UserCreateForm, EmailAuthenticationForm, AddUserPost, AddModeratorMessagesForm, AddPhotoForm
from user.serializers import UserSerializer

from rest_framework.response import Response
from rest_framework.views import APIView

import lxml.html
from datetime import datetime


def add_points(user_id, rating):
    with transaction.atomic():
        user_rating, created = UsersUserrating.objects.get_or_create(user_id=user_id)
        user_rating.rating += rating
        user_rating.save()


# Define functions for each action
def add_comment_like(user_id):
    add_points(user_id, 1)


def add_forum_thanks(user_id):
    add_points(user_id, 1)


def add_own_comment(user_id):
    add_points(user_id, 1)


def add_comment_like_by_others(user_id):
    add_points(user_id, 1)


def add_comment_dislike_by_others(user_id):
    add_points(user_id, -1)


def add_forum_reply(user_id):
    add_points(user_id, 2)


def add_forum_thanks_by_others(user_id):
    add_points(user_id, 10)


def add_ukrainian_content(user_id):
    add_points(user_id, 10)


def add_upload(user_id):
    add_points(user_id, 2)


def add_like(user_id):
    add_points(user_id, 2)


def add_vip(user_id):
    add_points(user_id, 3)


def add_gold(user_id):
    add_points(user_id, 5)


def add_moderator(user_id):
    add_points(user_id, 10)


def add_admin(user_id):
    add_points(user_id, 50)


def add_recording_quality_rating(user_id):
    add_points(user_id, 1)


def add_arrangement_rating(user_id):
    add_points(user_id, 1)


def add_top_rating(user_id):
    add_points(user_id, 10)


def add_top_week(user_id):
    add_points(user_id, 10)


def add_top_month(user_id):
    add_points(user_id, 50)


def add_top_year(user_id):
    add_points(user_id, 200)


@login_required
def user_page(request, pk):
    user = Userprofile.objects.get(user_id=pk)
    try:
        user_subscription = Subscription.objects.get(user_id=request.user.id)
    except Subscription.DoesNotExist:
        user_subscription = 0
    x = User.objects.get(id=request.user.id)
    try:
        friendship = FriendsFriendship.objects.get(user_id=user.user.id)
    except FriendsFriendship.DoesNotExist:
        friendship = 0

    # friendshipfriends = FriendsFriendshipFriends.objects.filter(from_friendship_id=friendship.id).order_by('-id')
    # friendship_id = friendshipfriends.values_list('to_friendship_id', flat=True)
    # friends = FriendsFriendship.objects.filter(id__in=friendship_id).order_by('-id')[:10]
    user.comments = DjangoComments.objects.filter(user_id=user.user_id).order_by('-id')[:10]
    user.forum = ForumPost.objects.filter(author_id=user.user_id).order_by('-id')[:10]
    for u_f in user.forum:
        u_f.body = lxml.html.fromstring(u_f.body).text_content()

    is_friend = 0
    add_post_form = AddUserPost(request.POST, request.FILES)
    if request.method == "POST":
        if add_post_form.is_valid():
            print("addING POST")
            add_post = add_post_form.save(request, commit=True)

    try:
        user.rating = UsersUserrating.objects.get(user_id=user.user.id)
    except UsersUserrating.DoesNotExist:
        user.rating = 0

    user_post = UserPost.objects.filter(userprofile_id=user.id).order_by('-pub_date')
    return render(request, 'user/index.html', {
        'user': user,
#         'friends': friends,
        'is_friend': is_friend,
        'posts': user_post,
        'add_post_form': add_post_form,
        'user_subscription': user_subscription,
        'x': x
    })


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Userprofile
    fields = ['gender', 'city', 'country', 'avatar', 'birthdate', 'icq', 'skype', 'website', 'about', 'instagram',
              'facebook']
    template_name_suffix = '_update_form'


@login_required
def all_friends(request, pk):
    try:
        friendship = FriendsFriendship.objects.get(user_id=pk)
    except FriendsFriendship.DoesNotExist:
        friendship = 0

    friendshipfriends = FriendsFriendshipFriends.objects.filter(from_friendship_id=friendship.id).order_by('-id')
    friendship_id = friendshipfriends.values_list('to_friendship_id', flat=True)
    friends = FriendsFriendship.objects.filter(id__in=friendship_id).order_by('-id')
    friends_request = FriendsFriendshiprequest.objects.filter(to_user_id=request.user.id)

    return render(request, 'user/all_friends.html', {
        'friends_request': friends_request,
        'users': friends,
    })


@login_required
def userlist(request):
    users = User.objects.all()
    paginator = Paginator(users, 25)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
        print('first')
    except PageNotAnInteger:
        users = paginator.page(1)
        print('second')
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
        print('third')

    return render(request, 'user/list.html', {'users': users})


class RegisterFormView(FormView):
    form_class = UserCreateForm
    success_url = "http://0.0.0.0:1761/user/success_registration/"
    template_name = "user/registration.html"

    def form_valid(self, form):
        form_data = form.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Активація акаунту minus.lviv.ua'
        message = render_to_string('user/succes_reg_true.html', {
            'user': form_data,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(form_data.id)),
            'token': account_activation_token.make_token(form_data),
        })

        to_email = form_data.email
        email = EmailMessage(mail_subject, message, to=[to_email])

        return super(RegisterFormView, self).form_valid(form)


def success_reg(request):
    return render(request, 'user/succes_reg_true.html')

@login_required
def advertisement(request):
    z = True
    selected_blurbs = SelectedBlurb.objects.filter(user_id=request.user.id)
    blurbs = BlurbsBlurb.objects.filter(user_id=request.user.id)
    paginator = Paginator(blurbs, 10)
    page = request.GET.get('page')
    try:
        blurbs = paginator.page(page)
        print('first')
    except PageNotAnInteger:
        blurbs = paginator.page(1)
        print('second')
    except EmptyPage:
        blurbs = paginator.page(paginator.num_pages)
        print('third')
    for g in blurbs:
        try:
            ph_a = PhotosPhotoalbum.objects.get(content_type_id=52, object_pk=g.id)
            g.photo = PhotosPhoto.objects.filter(album_id=ph_a.id)
            try:
                g.photo = g.photo[0].image
            except:
                g.photo = 'pass'
        except PhotosPhotoalbum.DoesNotExist:
            g.photo = "http://praktikaprava.ru/wp-content/uploads/2017/11/obmen-tovara-v-techenii-14-dnej.jpg"
    for g in selected_blurbs:
        try:
            ph_a = PhotosPhotoalbum.objects.get(content_type_id=52, object_pk=g.blurb.id)
            g.photo = PhotosPhoto.objects.filter(album_id=ph_a.id)
            try:
                g.photo = g.photo[0].image
            except:
                g.photo = 'pass'
        except PhotosPhotoalbum.DoesNotExist:
            g.photo = "http://praktikaprava.ru/wp-content/uploads/2017/11/obmen-tovara-v-techenii-14-dnej.jpg"
    return render(request, 'user/user_goods.html', {'blurbs': blurbs, 'selected_blurbs': selected_blurbs, 'z': z, })


class AddPhoto(LoginRequiredMixin, FormView):
    form_class = AddPhotoForm
    template_name = "user/add_photo.html"
    success_url = '/'

    def form_valid(self, form):
        photo_album = PhotosPhotoalbum.objects.get(content_type_id=20, user_id=self.request.user.id)
        form.instance.album = photo_album
        return super().form_valid(form)


@login_required
def delete_selected_blurbs(request, pk):
    selected_blurb = SelectedBlurb.objects.get(pk=pk).delete()
    return HttpResponseRedirect('/user/user-advertisement/')


class UserLoginView(LoginView):
    form_class = EmailAuthenticationForm
    template_name = 'user/succes_login.html'
    redirect_authenticated_user = True

    def post(self, request, *args, **kwargs):
        form = EmailAuthenticationForm(request, data=request.POST)

        if form.is_valid():
            print('Form is valid')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f'Username: {username}, Password: {password}')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                print(3)
                print(user)
                login(request, user)
                return self.form_valid(form)
            else:
                return HttpResponseRedirect('false_auth')
        else:
            print(4)
            print('Form is NOT valid')
            print(form.errors)
            return self.form_invalid(form)

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect('/')

    def form_invalid(self, form):
        return redirect('/')


def false_auth(request):
    return render(request, 'user/false_auth.html', {})


def success_login(request):
    return render(request, 'user/succes_login.html', {})


def logout_view(request):
    logout(request)
    return render(request, 'user/registration.html')


@login_required
def userminuses(request, user_id):
    user = request.user
    minuses = MinusstoreMinusrecord.objects.filter(user_id=user_id).order_by('-id')
    paginator = Paginator(minuses, 10)
    page = request.GET.get('page')
    try:
        minuses = paginator.page(page)
        print('first')
    except PageNotAnInteger:
        minuses = paginator.page(1)
        print('second')
    except EmptyPage:
        minuses = paginator.page(paginator.num_pages)
        print('third')
    return render(request, 'user/user_minuses.html', {'minus': minuses, 'user': user})


@login_required
def user_goods(request, user_id):
    blurbs = BlurbsBlurb.objects.filter(user_id=user_id)
    paginator = Paginator(blurbs, 10)
    page = request.GET.get('page')
    try:
        blurbs = paginator.page(page)
        print('first')
    except PageNotAnInteger:
        blurbs = paginator.page(1)
        print('second')
    except EmptyPage:
        blurbs = paginator.page(paginator.num_pages)
    for g in blurbs:
        try:
            ph_a = PhotosPhotoalbum.objects.get(content_type_id=52, object_pk=g.id)
            g.photo = PhotosPhoto.objects.filter(album_id=ph_a.id)
            try:
                g.photo = g.photo[0].image
            except:
                g.photo = 'pass'
        except PhotosPhotoalbum.DoesNotExist:
            g.photo = "http://praktikaprava.ru/wp-content/uploads/2017/11/obmen-tovara-v-techenii-14-dnej.jpg"
    return render(request, 'user/user_goods.html', {'blurbs': blurbs, })


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'user/succes_reg_true.html', {})
    else:
        return HttpResponse('Вибачте але лінк активації якийсь поганий(')


@login_required
def user_search(request):
    users = User.objects.filter(
        Q(first_name__startswith=request.GET['search']) | Q(last_name__startswith=request.GET['search']) | Q(
            username__startswith=request.GET['search']) | Q(email__startswith=request.GET['search'])
    )
    paginator = Paginator(users, 25)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
        print('first')
    except PageNotAnInteger:
        users = paginator.page(1)
        print('second')
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'user/list.html', {'users': users})


@login_required
def activities(request):
    last_forum = ForumPost.objects.order_by('-id')[:10]
    last_comments = DjangoComments.objects.order_by('-id')[:30]
    if request.user.is_authenticated:
        activities = UserActivitys.objects.filter(to_user_id=request.user.id)
        z = True
    else:
        activities = UserActivitys.objects.all()
        z = False
    return render(request, 'user/activities.html', {
        'activities': activities,
        'z': z,
        'last_forum': last_forum,
        'last_comments': last_comments,
    })


@login_required
def moderator_messages(request):
    if request.user.is_authenticated and request.user.is_staff:
        moderator_messages = ModeratorMessages.objects.all().order_by('-id')
        return render(request, 'user/moderator_messages.html', {'moderator_messages': moderator_messages, })


@login_required
def add_moderator_message(request, object_pk, content_id):
    form = AddModeratorMessagesForm(request.POST)
    if request.method == "POST":
        if request.user.is_authenticated:
            print("form prevalidation")
            if form.is_valid():
                print("form moderator_messages is valid")
                form = form.save(request, content_id, object_pk, commit=True)
    return render(request, 'user/add_moderator_messages.html', {'form': form, })


@login_required
def friends_requests(request, pk):
    if request.user.is_authenticated:
        friends_request = FriendsFriendshiprequest.objects.filter(to_user_id=request.user.id)
        return render(request, 'user/friends_requests.html', {'friends_request': friends_request, })


# API
class FriendsRequest(APIView):
    def get(self, request, to_user_id, format=None):
        print(to_user_id)
        friend_request = FriendsFriendshiprequest.objects.create(from_user_id=request.user.id, to_user_id=to_user_id,
                                                                 accepted=0)
        return Response('{"1":1}')


class GetUser(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk=pk)
        user = UserSerializer(user, many=False)
        return Response(user.data)


def status_checker(request):
    user = UserStatus.objects.get(user=request.user)
    time = User.objects.get(user=request.user)
    time_from_register = (datetime.now() - time.date_joined).days
    print(time_from_register)
    if time_from_register < 7:
        user.is_amateur = True
        user.save()
    elif time_from_register > 7:
        user.is_amateur = False
        user.is_user = True
        user.save()
    if user.points.rating >= 20000:
        user.is_user = False
        user.is_top_user = True
        user.save()
    if user.points.rating >= 200000:
        user.is_top_user = False
        user.is_vip_user = True
        user.save()
    if user.points.rating >= 250000:
        user.is_vip_user = False
        user.is_gold_user = True
        user.save()


def subscribe(request):
    x = User.objects.get(id=request.user.id)
    user = Userprofile.objects.get(user_id=request.user.id)

    # creating order id with random symbols for invoice
    characters = string.ascii_letters + string.digits
    order_id = ''.join(random.choice(characters) for _ in range(10))
    print(order_id)

    try:
        user_instance = User.objects.get(id=request.user.id)
        sub_delete = Subscription.objects.get(user=user_instance)
        sub_delete.delete()
        sub = Subscription(user=request.user, surname=request.POST['user_modal_form_input_surname'],
                            name=request.POST['user_modal_form_input_name'],
                            email=request.POST['user_modal_form_input_email'],
                            phone_number=request.POST['user_modal_form_input_phone'],
                            order_id=order_id)
        sub.save()
    except Subscription.DoesNotExist:
        sub = Subscription(user=request.user, surname=request.POST['user_modal_form_input_surname'],
                                    name=request.POST['user_modal_form_input_name'],
                                    email=request.POST['user_modal_form_input_email'],
                                    phone_number=request.POST['user_modal_form_input_phone'],
                                    order_id=order_id)
        sub.save()
    user_subscription = Subscription.objects.get(user_id=request.user.id)
    return render(request, 'user/index.html', {'user_subscription': user_subscription, 'user': user, 'x': x})


def admin_applications(request):
    subscriptions = Subscription.objects.filter(is_accepted=False)
    return render(request, 'user/applications_to_admin.html', {'subscriptions': subscriptions})


def admin_arrangers_list(request):
    arrangers = Subscription.objects.filter(is_paid=True, is_accepted=True)
    return render(request, 'user/arrangers_list.html', {'arrangers': arrangers})


def admin_accept(request, pk):
    liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    subscriptions = Subscription.objects.filter(is_accepted=False)

    current_datetime = datetime.now(pytz.utc)
    current_datetime_ua = pytz.timezone('Europe/Kiev')
    ua_now = current_datetime.astimezone(current_datetime_ua)
    formatted_datetime_ua = ua_now.strftime("%Y-%m-%d %H:%M:%S")
    if request.method == 'GET':
        sub = Subscription.objects.get(id=pk)
        params = liqpay.api("request", {
                "action": "invoice_send",
                "version": 3,
                "email": sub.email,
                "amount": 1,
                "currency": "UAH",
                'description': 'Оплата підписки на рік!',
                "order_id": sub.order_id,
                "phone": sub.phone_number,
                "action_payment": 'subscribe',
                "subscribe_date_start": formatted_datetime_ua,
                "subscribe_periodicity": "year",
                "language": 'uk'
        })
        print(params)

        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)
        params = {'data': data, 'signature': signature}

        res = requests.post(url='https://www.liqpay.ua/api/3/checkout/', data=params)
        if res.status_code == 200:
            user_subscription = Subscription.objects.get(id=pk)
            user_subscription.is_accepted = True
            user_subscription.save()
            print('chin-chin')
            return render(request, 'user/applications_to_admin.html', {'subscriptions': subscriptions})
        else:
            return render(request, 'user/applications_to_admin.html', {'subscriptions': subscriptions})


def admin_reject(request, pk):
    subscriptions = Subscription.objects.filter(is_accepted=False)

    if request.method == 'GET':
        sub = Subscription.objects.get(id=pk)
        sub.delete()
        return render(request, 'user/applications_to_admin.html', {'subscriptions': subscriptions})
    else:
        return render(request, 'user/applications_to_admin.html', {'subscriptions': subscriptions})
