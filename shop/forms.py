from django.contrib.auth.models import User
from album.models import PhotosPhotoalbum, PhotosPhoto
from django import forms
from shop.models import BlurbsBlurb, BlurbsBlurbcategory


class BlurbForm(forms.ModelForm):
    first_photo = forms.FileField()
    second_photo = forms.FileField()
    third_photo = forms.FileField()

    class Meta:
        model = BlurbsBlurb
        fields = ['title', 'cost', 'buysell', 'description', 'category', 'georegion']

    def save(self, commit=True):
        blurb = super().save(commit=False)
        blurb.save()

        photo_album = PhotosPhotoalbum.objects.create(user=blurb.user, name=blurb.title,
                                                      slug="http://minus.lviv.ua/shop/", size=3, content_type_id=18,
                                                      object_pk=blurb.id)
        photo = PhotosPhoto.objects.create(title=blurb.title, image=self.cleaned_data['first_photo'], album=photo_album,
                                           is_cover=0)

        if self.cleaned_data['second_photo']:
            second_photo = PhotosPhoto.objects.create(title=blurb.title, image=self.cleaned_data['second_photo'],
                                                      album=photo_album, is_cover=0)

        if self.cleaned_data['third_photo']:
            third_photo = PhotosPhoto.objects.create(title=blurb.title, image=self.cleaned_data['third_photo'],
                                                     album=photo_album, is_cover=0)

        return blurb
