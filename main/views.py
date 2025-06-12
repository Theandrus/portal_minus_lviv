from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from minus_lviv.models import DjangoComments, CommentInteraction, CommentReply
from album.models import PhotosPhotoalbum, PhotosPhoto
from main.models import NewsNewsitem
from shop.models import BlurbsBlurb
from minusstore.models import MinusstoreMinusrecord
from django.contrib.auth.models import User
from user.models import Userprofile, UserActivitys, SubscribeOnComments
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic.edit import FormView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import AuthForm, AddNews, AddComments, CommentReplyForm
from django.core import serializers
from main.serializers import CommentSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
import json
from user.views import add_points


def main(request):
    news_objects = NewsNewsitem.objects.all().order_by('-id')
    user = request.user
    print(user)
    print(user.id)
    paginator = Paginator(news_objects, 10)
    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    for new in news:
        new.comments_count = DjangoComments.objects.filter(content_type_id=51, object_pk=new.id).count()

    return render(request, 'main/index.html', {
        'news': news,
        'user': user,
    })


def rules(request):
    return render(request, 'main/rules.html', {})


@login_required
def news_index(request, pk):
    new = get_object_or_404(NewsNewsitem, pk=pk)
    new_comments = DjangoComments.objects.filter(content_type_id=51, object_pk=pk)
    count = new_comments.count()

    for comment in new_comments:
        comment.replies = DjangoComments.objects.filter(comment=comment)

        comment.likes = CommentInteraction.objects.filter(comment=comment, reaction='like').count()
        comment.dislikes = CommentInteraction.objects.filter(comment=comment, reaction='dislike').count()

        if (timezone.now() - comment.submit_date).total_seconds() <= 300:
            comment.can_edit = True
        else:
            comment.can_edit = False

    add_comment_form = AddComments(request.POST or None)

    if request.method == "POST" and add_comment_form.is_valid():
        comment_text = add_comment_form.cleaned_data['comment']
        if comment_text.startswith('@'):
            comment_text = comment_text.split(' ')
            user = comment_text[0][1:]
            comment_id = user.split('#')[1]
            comment_text = ' '.join(comment_text[1:])
            comment = get_object_or_404(DjangoComments, pk=comment_id)
            DjangoComments.objects.create(user=request.user, comment=comment, reply=comment_text)
        else:
            DjangoComments.objects.create(
                content_type_id=51,
                object_pk=pk,
                user=request.user,
                user_first_name=request.user.first_name,
                user_last_name=request.user.last_name,
                comment=comment_text,
                submit_date=timezone.now(),
                ip_address=request.META.get('REMOTE_ADDR'),
                is_public=1,
                is_removed=0,
            )

    return render(request, 'main/news.html', {
        'count': count,
        'news': new,
        'add_comment_form': add_comment_form,
        'user_can_edit': (timezone.now() - new.submit_date).total_seconds() <= 300
    })


@login_required
def like_comment(request, pk):
    user = request.user

    comment = DjangoComments.objects.get(pk=pk)
    user_id = comment.user.id

    existing_interaction = CommentInteraction.objects.filter(
        user=request.user,
        comment=comment
    ).first()

    if existing_interaction:
        if existing_interaction.is_liked is True:
            existing_interaction.delete()
        else:
            existing_interaction.is_liked = True
            existing_interaction.save()
    else:
        CommentInteraction.objects.create(
            user=request.user,
            comment=comment,
            is_liked=True
        )
        add_points(user_id, 1)

    return render(request, 'main/index.html', {'user': user})


@login_required
def edit_comment(request, comment_id):
    user = request.user
    comment = get_object_or_404(DjangoComments, pk=comment_id)
    comments = DjangoComments.objects.filter(object_pk=comment_id)

    if comment.user.id == request.user.id:
        if request.method == 'POST':
            comment_text = request.POST.get('comment')
            if comment_text:
                comment.comment = comment_text
                comment.is_edited = 1
                comment.save()
    else:
        print('Ви не можете редагувати не свій коментар')

    redirect_url = request.META.get('HTTP_REFERER', reverse('news_index', kwargs={'pk': comment.object_pk, 'user': user}))
    return redirect(redirect_url)


@login_required
def add_comment_to_minus(request, pk):
    user = request.user
    minus = get_object_or_404(MinusstoreMinusrecord, pk=pk)
    if request.method == 'POST':
        form = AddComments(request.POST)
        if form.is_valid():
            comment = form.save(pk=minus.pk, request=request, content_type_id=51)
            comments = DjangoComments.objects.filter(object_pk=pk)
            user_id = request.user.id
            add_points(user_id, 1)
            return render(request, 'minusstore/minus.html', {'comments': comments, 'minus': minus})
    else:
        form = AddComments()

    redirect_url = request.META.get('HTTP_REFERER', reverse('news_index', kwargs={'pk': minus.pk, 'user': user}))
    return redirect(redirect_url)


def add_answer_to_comment(request, comment_id):
    parent_comment = get_object_or_404(DjangoComments, pk=comment_id)

    if request.method == 'POST':
        form = CommentReplyForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            CommentReply.objects.create(
                parent_comment=parent_comment,
                user=request.user,
                comment=comment
            )
            print(comment)
            redirect_url = request.META.get('HTTP_REFERER',
                                            reverse('news_index', kwargs={'pk': parent_comment.object_pk}))
            return redirect(redirect_url)
    else:
        form = CommentReplyForm()

    # redirect_url = request.META.get('HTTP_REFERER', reverse('news_index', kwargs={'pk': parent_comment.object_pk}))
    # return redirect(redirect_url)


class AddNewsView(FormView):
    form_class = AddNews
    template_name = "main/add_news.html"
    success_url = '/'

    def form_valid(self, form):
        print('add news valid')
        form.instance.user = self.request.user
        form_data = form.save()
        return super().form_valid(form)


class GetComments(APIView):

    def get_objects(self, pk):
        try:
            return DjangoComments.objects.filter(content_type_id=51, object_pk=pk)
        except DjangoComments.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        comments = self.get_objects(pk=pk)
        serializer_context = {
            'request': request,
        }
        comments = CommentSerializer(comments, many=True, context=serializer_context)
        return Response(comments.data)

# def likedislike(request, user_id, object_id, content_type_id, likeordislike):
#     try:
#         likeorodislike = Likedislike.objects.get(object_id=object_id, type_id=content_type_id, user_id=user_id)
#         user = User.objects.get(pk=user_id)
#         if content_type_id == '17':
#             minus = MinusstoreMinusrecord.objects.get(pk=object_id)
#         elif content_type_id == '52':
#             minus = BlurbsBlurb.objects.get(pk=object_id)
#         elif content_type_id == '45':
#             minus = DjangoComments.objects.get(pk=object_id)
#         if likeordislike == '1' and likeorodislike.likes is False:
#             likeorodislike.likes = 1
#             likeorodislike.save()
#             try:
#                 likes = Likedislike.objects.filter(type_id=content_type_id, object_id=object_id, likes=1).count()
#             except:
#                 likes = 0
#             dislikes = Likedislike.objects.filter(type_id=content_type_id, object_id=object_id, likes=0).count()
#             likeanddislike = json.dumps({'likes': likes, 'dislikes': dislikes})
#             UserActivitys.objects.filter(from_user=user, to_user_id=minus.user.id, type='d', activity_to=object_id).update(
#                 type='l')
#             return HttpResponse(likeanddislike)
#         elif likeordislike == '0' and likeorodislike.likes is True:
#             likeorodislike.likes = 0
#             likeorodislike.save()
#             likes = Likedislike.objects.filter(type_id=content_type_id, object_id=object_id, likes=1).count()
#             UserActivitys.objects.filter(from_user=user, to_user_id=minus.user.id, type='l', activity_to=object_id).update(
#                 type='d')
#             dislikes = Likedislike.objects.filter(type_id=content_type_id, object_id=object_id, likes=0).count()
#             likeanddislike = json.dumps({'likes': likes, 'dislikes': dislikes})
#             return HttpResponse(likeanddislike)
#         else:
#             return HttpResponse('figovo')
#
#     except Likedislike.DoesNotExist:
#         likedislike = Likedislike.objects.create(user_id=user_id, object_id=object_id, type_id=content_type_id,
#                                                  likes=likeordislike)
#         if content_type_id == '17':
#             minus = MinusstoreMinusrecord.objects.get(pk=object_id)
#         elif content_type_id == '52':
#             minus = BlurbsBlurb.objects.get(pk=object_id)
#         elif content_type_id == '45':
#             minus = DjangoComments.objects.get(pk=object_id)
#         user = User.objects.get(pk=user_id)
#         if likeordislike == '1':
#             UserActivitys.objects.create(from_user=user, to_user_id=minus.user.id, type='l', activity_to=object_id)
#         else:
#             UserActivitys.objects.create(from_user=user, to_user_id=minus.user.id, type='d', activity_to=object_id)
#         likes = Likedislike.objects.filter(type_id=content_type_id, object_id=object_id, likes=1).count()
#         dislikes = Likedislike.objects.filter(type_id=content_type_id, object_id=object_id, likes=0).count()
#         likeanddislike = {'likes': likes, 'dislikes': dislikes}
#         likeanddislike = json.dumps(likeanddislike)
#         return HttpResponse(likeanddislike)
