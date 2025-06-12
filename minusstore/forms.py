from minusstore.models import MinusstoreMinusrecord, Minusgenre, Minusappointment
from django.contrib.auth.models import User
from django import forms
from mutagen.mp3 import MP3
import datetime


class AddMinusForm(forms.ModelForm):
    class Meta:
        model = MinusstoreMinusrecord
        fields = ['file', 'author', 'title', 'lyrics', 'plusrecord', 'embed_video']

    def save(self, commit=True):
        minus = super().save(commit=False)
        f = MP3(self.cleaned_data['file'])
        minus.title = self.cleaned_data['title']
        minus.bitrate = f.info.bitrate // 1000
        minus.length = f.info.length // 100
        print(minus.length)
        minus.pub_date = datetime.datetime.now()
        minus.genre = self.cleaned_data.get('genre')
        minus.specifik = self.cleaned_data.get('specifik')
        minus.filesize = 1
        minus.type_id = 1
        minus.rating_votes = 1
        minus.rating_score = 1
        minus.alternative = 1
        # minus.price = self.cleaned_data['price']
        if commit:
            minus.save()
        return minus
