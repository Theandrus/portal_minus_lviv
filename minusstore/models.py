from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
import datetime
from django.dispatch import receiver


class MinusstoreCommentnotify(models.Model):
    comment_id = models.IntegerField(unique=True)
    user_id = models.IntegerField()
    is_seen = models.IntegerField()
    content_type_id = models.IntegerField()
    object_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'minusstore_commentnotify'


class MinusstoreFiletype(models.Model):
    type_name = models.CharField(max_length=15)
    display_name = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    filetype = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'minusstore_filetype'


class MinusstoreMinus(models.Model):
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'minusstore_minus'


class MinusstoreMinusauthorFiletypes(models.Model):
    minusauthor = models.IntegerField()
    filetype = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'minusstore_minusauthor_filetypes'


class MinusstoreMinuscategory(models.Model):
    name = models.CharField(max_length=50, default='null')
    display_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'minusstore_minuscategory'

    def __str__(self):
        return self.display_name


class Minusgenre(models.Model):
    name = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'minusstore_minusgenre'

    def __str__(self):
        return self.name


class Minusappointment(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'minusstore_minusappointment'

    def __str__(self):
        return self.name


class MinusstoreMinusplusrecord(models.Model):
    minus_id = models.IntegerField(unique=True, blank=True, null=True)
    user_id = models.IntegerField()
    file = models.FileField(upload_to="static/files/pluses/")

    class Meta:
        managed = True
        db_table = 'minusstore_minusplusrecord'


class MinusstoreMinusauthor(models.Model):
    name = models.CharField(max_length=255, default='null')

    class Meta:
        managed = True
        db_table = 'minusstore_minusauthor'

    def __str__(self):
        return self.name


class MinusstoreMinusrecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    file = models.FileField("Мінусовка", upload_to="static/files/minuses/", null=True, blank=True)
    title = models.CharField("Назва мінусовки", max_length=255)
    is_folk = models.IntegerField(default=0)
    author = models.ForeignKey(MinusstoreMinusauthor, on_delete=models.PROTECT, null=True, blank=True)
    arrangeuathor = models.CharField(max_length=50, blank=True, null=True)
    annotation = models.TextField()
    thematics = models.CharField(max_length=30, blank=True, null=True)
    tempo = models.CharField(max_length=10)
    staff = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    is_childish = models.IntegerField(default=0)
    is_amateur = models.IntegerField(default=0)
    is_ritual = models.IntegerField(default=0)
    minus_genre = models.ForeignKey(Minusgenre, on_delete=models.PROTECT)
    minus_appointment = models.ForeignKey(Minusappointment, on_delete=models.PROTECT)
    lyrics = models.TextField("Текст пісні", null=True, blank=True)
    plusrecord = models.FileField(upload_to="static/files/pluses/", blank=True, null=True)
    pub_date = models.DateTimeField()
    length = models.FloatField()
    bitrate = models.IntegerField()
    filesize = models.IntegerField()
    embed_video = models.TextField(blank=True, null=True)
    type_id = models.IntegerField()
    rating_votes = models.IntegerField()
    rating_score = models.IntegerField()
    alternative = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    price = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'minusstore_minusrecord'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/minusstore/minus/' + str(self.id) + '/'


class MinusPurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    minus_id = models.ForeignKey(MinusstoreMinusrecord, on_delete=models.PROTECT)
    order_id = models.CharField(max_length=15)
    email = models.EmailField(max_length=60, blank=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'minus_purchase'


class MoneyFromMinus(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    minus_id = models.ForeignKey(MinusstoreMinusrecord, on_delete=models.PROTECT)
    money_from_minus = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'money_from_minus'


class UserPoints(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField()


class MinusstoreMinusquality(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField()
    minus = models.ForeignKey(MinusstoreMinusrecord, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'minusstore_minusquality'


class MinusstoreMinusarrangement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField()
    minus = models.ForeignKey(MinusstoreMinusrecord, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'minusstore_minusarrangement'


class PreModerationRecord(models.Model):
    minus = models.ForeignKey(MinusstoreMinusrecord, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'pre_moderation_record'


@receiver(post_save, sender=MinusstoreMinusrecord)
def create_premoderationrecord(sender, instance, created, **kwargs):
    if created:
        PreModerationRecord.objects.create(minus=instance)


class MinusstoreMinusrecordCategories(models.Model):
    minusrecord = models.ForeignKey(MinusstoreMinusrecord, on_delete=models.CASCADE)
    minuscategory = models.ForeignKey(MinusstoreMinuscategory, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'minusstore_minusrecord_categories'
        unique_together = (('minusrecord', 'minuscategory'),)


class MinusstoreMinusstats(models.Model):
    date = models.DateField()
    rate = models.IntegerField()
    minus_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'minusstore_minusstats'


class MinusstoreMinusstopword(models.Model):
    word = models.CharField(max_length=30)
    blocked = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'minusstore_minusstopword'


class MinusstoreMinusweekstats(models.Model):
    rate = models.IntegerField()
    minus_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'minusstore_minusweekstats'


class MinusstoreMinusrecordScore(models.Model):
    minus = models.ForeignKey(MinusstoreMinusrecord, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.IntegerField()
    score = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'minusstore_minusrecord_score'
