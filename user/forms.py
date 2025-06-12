import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.hashers import check_password
from main.models import ModeratorMessages
from album.models import PhotosPhotoalbum, PhotosPhoto
from .models import UserPost, Userprofile
from django.shortcuts import render, redirect
import datetime
from django.core.exceptions import ValidationError


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        print('G')
        user.is_active = True
        user.email = self.cleaned_data["email"]
        user.last_login = datetime.datetime.now()
        print('Uhuuu')

        if commit:
            user.save()
            print('Tusovkaaa')

        return user


class AddUserPost(forms.ModelForm):

    class Meta:
        model = UserPost
        fields = ('text','image')

    def save(self,request,commit=True):
        post = super(AddUserPost,self).save(commit=False)
        post.userprofile = Userprofile.objects.get(user_id = request.user.id)
        if commit:
            post.save()

        return post


class EmailAuthenticationForm(AuthenticationForm):
    # def clean_username(self):
        # if self.request.method == 'POST':
        #     print('aaa')
        #     username = self.request.POST["username"]
        #     password = self.request.POST["password"]
        #     print(username)
        #     print(password)
        #     user = authenticate(self.request, username=username, password=password)
        #     print(user)
        #     if user is not None:
        #         print('bbb')
        #         login(self.request, user)
        #         if self.request.user.is_authenticated:
        #             print('ccc')
        #             user = self.request.user
        #         return redirect('/', {'user': user})
        #     else:
        #         return redirect('authorization/')
        #
        # else:
        #     return render(self.request, 'user/succes_login.html', {})
    def clean(self):
        username = self.request.POST["username"]
        password = self.request.POST["password"]

        if username and password:  # Check if both fields are provided
            try:
                user = User.objects.get(email=username) if '@' in username else User.objects.get(username=username)
                if user.check_password(password):  # Use check_password to validate the password
                    print('auth success')
                    return self.cleaned_data
                else:
                    raise ValidationError('Invalid email/username or password.')
            except User.DoesNotExist:
                raise ValidationError('Invalid email/username or password.')
        else:
            raise ValidationError('Both email/username and password are required.')


class AddModeratorMessagesForm(forms.ModelForm):
    class Meta:
        model = ModeratorMessages
        fields = ('attention_message',)

    def save(self,request,content_type_id,object_pk,commit=True):
        post = super(AddModeratorMessagesForm,self).save(commit=False)
        post.user = request.user
        post.content_id = content_type_id
        post.object_pk = object_pk
        if commit:
            print("add moderator messages form presave")
            post.save()
            print("add moderator messages form save")

        return post


class AddPhotoForm(forms.ModelForm):
    class Meta:
        model = PhotosPhoto
        fields = ('title','image',)
