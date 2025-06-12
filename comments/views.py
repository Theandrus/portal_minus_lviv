from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from minus_lviv.models import DjangoComments, DjangoCommentFlags


@login_required
def add_comment(request):
    if request.method == 'POST':
        content_type_id = request.POST.get('content_type_id')
        object_pk = request.POST.get('object_pk')
        site_id = request.POST.get('site_id')
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        user_url = request.POST.get('user_url')
        comment_text = request.POST.get('comment_text')

        if content_type_id and object_pk and site_id and user_name and user_email and comment_text:
            comment = DjangoComments.objects.create(
                content_type_id=content_type_id,
                object_pk=object_pk,
                site_id=site_id,
                user=request.user,
                user_name=user_name,
                user_email=user_email,
                user_url=user_url,
                comment=comment_text,
                submit_date=timezone.now(),
                ip_address=request.META.get('REMOTE_ADDR'),
                is_public=1,
                is_removed=0,
            )
            comment.save()
    return redirect('comments:view_comments')


def view_comments(request):
    comments = DjangoComments.objects.all()
    return render(request, 'minusstore/minus.html', {'comments': comments})


@login_required
def interact_with_comment(request, comment_id, interaction_type):
    if interaction_type not in ['like', 'dislike']:
        return redirect('comments:view_comments')

    comment = get_object_or_404(DjangoComments, pk=comment_id)

    return redirect('comments:view_comments')


@login_required
def answer_comment(request, comment_id):
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text:
            comment = get_object_or_404(DjangoComments, pk=comment_id)
            answer = DjangoComments.objects.create(
                content_type_id=comment.content_type_id,
                object_pk=comment.object_pk,
                site_id=comment.site_id,
                user=request.user,
                user_name=request.user.username,
                user_email=request.user.email,
                comment=comment_text,
                submit_date=timezone.now(),
                ip_address=request.META.get('REMOTE_ADDR'),
                is_public=1,
                is_removed=0,
            )
            answer.save()
    return redirect('comments:view_comments')


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(DjangoComments, pk=comment_id)

    if request.user == comment.user and (timezone.now() - comment.submit_date).total_seconds() <= 300:
        if request.method == 'POST':
            comment_text = request.POST.get('comment_text')
            if comment_text:
                comment.comment = comment_text
                comment.save()

    return redirect('comments:view_comments')
