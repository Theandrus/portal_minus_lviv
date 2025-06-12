from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class BlurbsBlurbcategory(models.Model):
    title = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)

    class Meta:
        managed = True
        db_table = 'blurbs_blurbcategory'

    def __str__(self):
        return self.title


class BlurbsGeocity(models.Model):
    title = models.CharField(max_length=30)
    region_id = models.IntegerField()
    is_city = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'blurbs_geocity'


class BlurbsGeoregion(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        managed = True
        db_table = 'blurbs_georegion'

    def __str__(self):
        return self.title


class BlurbsBlurb(models.Model):
    buy_or_sell = [
        ('B', 'Куплю'),
        ('S', 'Продам'),
    ]
    title = models.CharField('Назва', max_length=120)
    description = models.TextField('Опис товару')
    buysell = models.CharField('Куплю/Продам', choices=buy_or_sell, max_length=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(BlurbsBlurbcategory, on_delete=models.PROTECT)
    pub_date = models.DateTimeField(auto_now_add=True)
    georegion = models.ForeignKey(BlurbsGeoregion, on_delete=models.PROTECT)
    is_user_business = models.BooleanField(default=False)
    cost = models.CharField('Ціна', max_length=255, default="Договірна")

    class Meta:
        managed = True
        db_table = 'blurbs_blurb'

    def __str__(self):
        return self.title


class SelectedBlurb(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blurb = models.ForeignKey(BlurbsBlurb, on_delete=models.PROTECT)

    class Meta:
        db_table = "selected_blurb"
