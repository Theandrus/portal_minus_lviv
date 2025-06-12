from django.db import models
from django.contrib.auth.models import User


class AlbumsAudio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, blank=True, null=True)
    pub_date = models.DateTimeField()
    order = models.IntegerField()
    file = models.CharField(max_length=256)
    rating_votes = models.IntegerField()
    rating_score = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    album_id = models.IntegerField(blank=True, null=True)
    downloadable = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'albums_audio'


class AlbumsAudioalbum(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type_id = models.IntegerField(blank=True, null=True)
    object_pk = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=128, default='null')
    slug = models.CharField(unique=True, max_length=150)
    description = models.TextField(blank=True, null=True)
    pub_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'albums_audioalbum'


class PhotosPhotoalbum(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=128, default='null')
    slug = models.CharField(unique=True, max_length=150)
    description = models.TextField(blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    size = models.IntegerField()
    content_type_id = models.IntegerField(blank=True, null=True)
    object_pk = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'photos_photoalbum'


class PhotosPhoto(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="static/files/userphotos/")
    album = models.ForeignKey(PhotosPhotoalbum, on_delete=models.CASCADE)
    is_cover = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'photos_photo'
