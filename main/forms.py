from django import forms
from django.contrib.auth.models import User
from main.models import NewsNewsitem
from minus_lviv.models import DjangoComments, CommentReply


class AuthForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', )


class AddNews(forms.ModelForm):
    class Meta:
        model = NewsNewsitem
        fields = ('title', 'preview', 'body', 'img', 'allow_comments')


class AddComments(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = DjangoComments
        fields = ('comment',)

    def save(self, pk, request, content_type_id, commit=True):
        comment = super().save(commit=False)
        comment.content_type_id = content_type_id
        comment.object_pk = pk
        comment.user = request.user
        comment.user_name = request.user.username
        comment.user_email = request.user.email
        comment.site_id = pk
        comment.user_url = '/user/user/' + str(request.user.id) + '/'
        comment.is_public = True
        comment.is_removed = False
        if commit:
            comment.save()
        return comment


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = CommentReply
        fields = ('comment',)
