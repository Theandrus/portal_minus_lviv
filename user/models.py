from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class FriendsFriendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'friends_friendship'


class FriendsFriendshipFriends(models.Model):
    from_friendship_id = models.IntegerField()
    to_friendship_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'friends_friendship_friends'
        unique_together = (('from_friendship_id', 'to_friendship_id'),)


class FriendsFriendshiprequest(models.Model):
    from_user_id = models.IntegerField()
    to_user_id = models.IntegerField()
    message = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    accepted = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'friends_friendshiprequest'
        unique_together = (('to_user_id', 'from_user_id'),)


class FriendsUserblocks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'friends_userblocks'


class FriendsUserblocksBlocks(models.Model):
    userblocks_id = models.IntegerField()
    user_id = models.IntegerField(unique=True)

    class Meta:
        managed = True
        db_table = 'friends_userblocks_blocks'
        unique_together = (('userblocks_id', 'user_id'),)


class UserActivitys(models.Model):
    activity_type = (
        ('l', 'like'),
        ('d', 'dislike'),
        ('c', 'comment'),
        ('s', 'subscribe')
    )

    type = models.CharField(choices=activity_type, null=True, max_length=255)
    from_user = models.ForeignKey(User, on_delete=models.PROTECT)
    to_user_id = models.IntegerField()
    activity_to = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'useractivitys'


class SubscribeOnComments(models.Model):
    content_type_id = models.IntegerField()
    object_pk = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'subscribed_on_comments'


class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=6, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)
    avatar = models.ImageField(upload_to='static/img/avatars/', blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    hide_birthdate = models.IntegerField(blank=True, null=True)
    icq = models.CharField(max_length=10, blank=True, null=True)
    jabber = models.CharField(max_length=128, blank=True, null=True)
    skype = models.CharField(max_length=128, blank=True, null=True)
    instagram = models.CharField(max_length=128, blank=True, null=True)
    facebook = models.CharField(max_length=128, blank=True, null=True)
    website = models.CharField(max_length=128, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    is_admin_subscribed = models.IntegerField()
    status_title = models.CharField(max_length=20, blank=True, null=True)
    status_css = models.CharField(max_length=20, blank=True, null=True)
    banned = models.IntegerField()
    banned_until = models.DateField(blank=True, null=True)
    seen_rules = models.IntegerField()
    is_business = models.BooleanField(default=False)
    is_user_online = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'userprofile'

    def get_absolute_url(self):
        return "/user/user/%i/" % self.user_id


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Userprofile.objects.create(
            user=instance,
            banned=0,
            hide_birthdate=0,
            is_admin_subscribed=0,
            seen_rules=0,
            is_business=False,
            is_user_online=False
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class UsersStaffticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    content_type_id = models.IntegerField()
    object_id = models.IntegerField()
    url = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    pub_date = models.DateTimeField()
    is_done = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'users_staffticket'


class UsersUseractivity(models.Model):
    last_activity_ip = models.CharField(max_length=15)
    last_activity_date = models.DateTimeField()
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'users_useractivity'


class UsersUserrating(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    rating = models.IntegerField()
    average_minus_rating = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'users_userrating'


class UserPost(models.Model):
    userprofile = models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="static/img/user-post-img/", blank=True, null=True)


@receiver(post_save, sender=User)
def create_user_rating(sender, instance, created, **kwargs):
    if created:
        UsersUserrating.objects.create(user=instance, rating=0, average_minus_rating=0)


class UserStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.ForeignKey(UsersUserrating, on_delete=models.CASCADE)
    is_guest = models.BooleanField(default=False)
    is_amateur = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_top_user = models.BooleanField(default=False)
    is_vip_user = models.BooleanField(default=False)
    is_gold_user = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.points.rating}"


class UserRank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_volunteer = models.BooleanField(default=False)
    is_amateur = models.BooleanField(default=False)
    is_arranger = models.BooleanField(default=False)
    is_patron_of_the_portal = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_honorary_forum_member = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=15)
    surname = models.CharField(max_length=60, blank=True)
    name = models.CharField(max_length=60, blank=True)
    email = models.EmailField(max_length=60, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    exclusive = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'subscription'

    def __str__(self):
        return f"{self.id}"
