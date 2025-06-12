from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core import serializers
from shop.models import BlurbsBlurb, BlurbsGeoregion, SelectedBlurb
from minus_lviv.models import DjangoComments, CommentInteraction
from album.models import PhotosPhotoalbum, PhotosPhoto
from user.models import Userprofile, UserActivitys, SubscribeOnComments
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import FormView, UpdateView
from shop.forms import BlurbForm
from main.forms import AddComments
from django.utils import timezone


def main_shop(request):
    if request.method == "GET":
        goods = BlurbsBlurb.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        georegion = BlurbsGeoregion.objects.all()
        paginator = Paginator(goods, 40)
        page = request.GET.get('page')
        try:
            goods = paginator.page(page)
        except PageNotAnInteger:
            goods = paginator.page(1)
        except EmptyPage:
            goods = paginator.page(paginator.num_pages)
        for g in goods:
            try:
                ph_a = PhotosPhotoalbum.objects.get(content_type_id=52, object_pk=g.id)
                g.photo = PhotosPhoto.objects.filter(album_id=ph_a.id)
                try:
                    g.photo = g.photo[0].image
                except:
                    g.photo = 'pass'
            except PhotosPhotoalbum.DoesNotExist:
                g.photo = "http://praktikaprava.ru/wp-content/uploads/2017/11/obmen-tovara-v-techenii-14-dnej.jpg"
        return render(request, 'shop/index.html', {
            'goods': goods,
            'georegion': georegion,
        })
    else:
        pass


def goods(request, pk):
    good = get_object_or_404(BlurbsBlurb, pk=pk)
    try:
        photo_album = PhotosPhotoalbum.objects.get(content_type_id=52, object_pk=good.id)
    except PhotosPhotoalbum.DoesNotExist:
        raise Http404
    photos = PhotosPhoto.objects.filter(album_id=photo_album.id)
    good.comments = DjangoComments.objects.filter(content_type_id=52, object_pk=pk)
    for c in good.comments:
        c.answer = DjangoComments.objects.filter(object_pk=c.id, content_type_id=45)
        c.likes = CommentInteraction.objects.filter(type_id=45, object_id=c.pk, likes=1).count()
        c.dislikes = CommentInteraction.objects.filter(type_id=45, object_id=c.pk, likes=0).count()
    count = DjangoComments.objects.filter(content_type_id=52, object_pk=pk).count()
    add_comment_form = AddComments(request.POST)
    likes = CommentInteraction.objects.filter(type_id=52, object_id=good.pk, likes=1).count()
    dislikes = CommentInteraction.objects.filter(type_id=52, object_id=good.pk, likes=0).count()
    next_good = BlurbsBlurb.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date').values_list('id')
    len_n = len(next_good)
    for i in range(len_n):
        if next_good[i][0] == good.id:
            if i == 0:
                previus_good = next_good[len_n - 1][0]
            else:
                previus_good = next_good[i - 1][0]
            if i == len_n - 1:
                next_good = next_good[0][0]
            else:
                next_good = next_good[i + 1][0]
            break
    if request.user.is_authenticated:
        print('user is authenticated')
        if request.method == "POST":
            if add_comment_form.is_valid():
                print('form is valid')
                comment = add_comment_form.cleaned_data['comment']
                if comment[0] == "@":
                    print('new level')
                    comment = comment.split(" ")
                    user = comment[0]
                    comment_id = user.split('#')
                    comment_id = comment_id[1]
                    comment = user[0]
                    add_comment = add_comment_form.save(commit=True, pk=comment_id, request=request,
                                                      content_type_id=45)
                else:
                    add_comment = add_comment_form.save(commit=True, pk=pk, request=request, content_type_id=52)
                if request.POST.get('subscribe'):
                    for subscriber in SubscribeOnComments.objects.filter(content_type_id=51, object_pk=pk):
                        UserActivitys.objects.create(from_user=request.user, type='s', to_user_id=subscriber.user.id,
                                                     activity_to=pk)
                    try:
                        SubscribeOnComments.objects.get(content_type_id=51, object_pk=pk, user=request.user)
                    except SubscribeOnComments.DoesNotExist:
                        SubscribeOnComments.objects.create(
                            content_type_id=51,
                            object_pk=pk,
                            user=request.user
                        )
                    return render(request, 'minusstore/minus.html', {
                        'likes': likes,
                        'dislikes': dislikes,
                        'minus': minus,
                        'author': author,
                        'minus_user': minus_user,
                        'upload_minuses': upload_minuses_from_user,
                        'add_comment_form': add_comment_form,
                    })

    return render(request, 'shop/goods.html', {
        'good': good,
        'photos': photos,
        'count': count,
        'add_comment_form': add_comment_form,
        'next_good': next_good,
        'previus_good': previus_good,
        'likes': likes,
        'dislikes': dislikes,
    })


class BlurbUpdate(UpdateView):
    model = BlurbsBlurb
    fields = ['title', 'category', 'description', 'cost', 'georegion']
    template_name_suffix = '_update_form'


def add_to_selected(request, pk):
    if request.user.is_authenticated:
        selected = SelectedBlurb.objects.create(user=request.user, blurb_id=pk)
    return HttpResponseRedirect('/shop/goods/' + pk + '/')


def lift_up(request, pk):
    if request.user.is_authenticated:
        blurb = BlurbsBlurb.objects.get(pk=pk)
        blurb.pub_date = timezone.now()
        blurb.save()
        return HttpResponseRedirect('/shop/')


def gave_business_or_private(request, bool):
    if bool == '1':
        goods = BlurbsBlurb.objects.filter(is_user_business=1)
        paginator = Paginator(goods, 40)
        page = request.GET.get('page')
        try:
            goods = paginator.page(page)
        except PageNotAnInteger:
            goods = paginator.page(1)
        except EmptyPage:
            goods = paginator.page(paginator.num_pages)
        return render(request, 'shop/index.html', {
            'goods': goods,
            'z': True,
        })
    else:
        goods = BlurbsBlurb.objects.filter(is_user_business=0)
        paginator = Paginator(goods, 40)
        page = request.GET.get('page')
        try:
            goods = paginator.page(page)
        except PageNotAnInteger:
            goods = paginator.page(1)
        except EmptyPage:
            goods = paginator.page(paginator.num_pages)
        return render(request, 'shop/index.html', {
            'goods': goods,
            'f': True,
        })


def add_blurb(request):
    if request.user.is_authenticated:
        blurb_form = BlurbForm(request.POST or None, request.FILES or None)
        if request.method == 'POST':
            if blurb_form.is_valid():
                blurb_form_s = blurb_form.save(commit=False)
                blurb_form_s.user = request.user
                blurb_form_s.is_user_business = Userprofile.objects.get(user_id=request.user.id).is_business
                blurb_form_s.category_id = request.POST.get('category')
                blurb_form_s.title = request.POST.get('title')
                blurb_form_s.buysell = request.POST.get('buysell')
                blurb_form_s.description = request.POST.get('description')
                blurb_form_s.georegion_id = request.POST.get('georegion')
                blurb_form_s.cost = request.POST.get('cost')
                try:
                    blurb_form_s.first_photo = request.FILES.get('first_photo')
                    blurb_form_s.second_photo = request.FILES.get('second_photo')
                    blurb_form_s.third_photo = request.FILES.get('third_photo')
                except:
                    print('error with files')
                blurb_form_s.save()
        return render(request, 'shop/add_blurb.html', {
            'form': blurb_form,
        })
    else:
        return HttpResponseRedirect('../')
