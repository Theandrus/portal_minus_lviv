from django.db import models
from django.contrib.auth.models import User


class NewsNewsitem(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField("Заголовок", max_length=150)
    img = models.ImageField("Зображення", upload_to='static/img/new-img/', null=True, blank=True)
    body = models.TextField("Текст новини")
    allow_comments = models.BooleanField("Заборонити коментарi до новини")
    pub_date = models.DateTimeField(auto_now_add=True)
    preview = models.TextField("Превью новини (те, що буде видно на головнiй сторiнцi)")

    class Meta:
        managed = True
        db_table = 'news_newsitem'


class ModeratorMessages(models.Model):
    attention_message = models.CharField(max_length=500)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    content_id = models.IntegerField()
    object_pk = models.IntegerField()

    class Meta:
        db_table = "moderator_messages"
        managed = True

    def __str__(self):
        return self.attention_message


class MainBanner(models.Model):
    html_code = models.TextField()

    class Meta:
        db_table = 'main_banner'
        managed = True


class LeftBanner(models.Model):
    html_code = models.TextField()

    class Meta:
        db_table = 'left_banner'
        managed = True


class RightBanner(models.Model):
    html_code = models.TextField()

    class Meta:
        db_table = 'right_banner'
        managed = True
