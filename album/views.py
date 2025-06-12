from django.shortcuts import render
from album.models import PhotosPhoto, PhotosPhotoalbum
from user.models import Userprofile
from django.contrib.auth.models import User


def user_album(request, pk):
    user = Userprofile.objects.get(user_id=User.objects.get(id=pk).id)
    photo_album = PhotosPhotoalbum.objects.filter(user_id=pk)
    photo_album_id = photo_album.values_list('id', flat=True)
    photos = PhotosPhoto.objects.filter(album_id__in=photo_album_id)

    return render(request, 'album/user_photos_and_video.html', {'photos': photos, 'photo_album': photo_album, 'user': user})
