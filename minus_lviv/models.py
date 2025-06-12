from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class AdminToolsDashboardPreferences(models.Model):
    user_id = models.IntegerField()
    data = models.TextField()
    dashboard_id = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'admin_tools_dashboard_preferences'
        app_label = 'minus_lviv'


class AdminToolsMenuBookmark(models.Model):
    user_id = models.IntegerField()
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'admin_tools_menu_bookmark'
        app_label = 'minus_lviv'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80,default='null')

    class Meta:
        managed = True
        db_table = 'auth_group'
        app_label = 'minus_lviv'


class AuthMessage(models.Model):
    user_id = models.IntegerField()
    message = models.TextField()

    class Meta:
        managed = True
        db_table = 'auth_message'
        app_label = 'minus_lviv'


class AuthPermission(models.Model):
    name = models.CharField(max_length=50,default='null')
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)
        app_label = 'minus_lviv'


class BannersBanner(models.Model):
    title = models.CharField(max_length=20, blank=True, null=True)
    key = models.CharField(unique=True, max_length=20)
    content = models.TextField()
    holder_id = models.IntegerField()
    ratio = models.SmallIntegerField()

    class Meta:
        managed = True
        db_table = 'banners_banner'
        app_label = 'minus_lviv'


class BannersPlaceholder(models.Model):
    title = models.CharField(max_length=35)
    key = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = True
        db_table = 'banners_placeholder'
        app_label = 'minus_lviv'


class CaptchaCaptchastore(models.Model):
    challenge = models.CharField(max_length=32)
    response = models.CharField(max_length=32)
    hashkey = models.CharField(unique=True, max_length=40)
    expiration = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'captcha_captchastore'
        app_label = 'minus_lviv'


class ChatChatroom(models.Model):
    user_id = models.IntegerField()
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'chat_chatroom'
        app_label = 'minus_lviv'


class ChunksChunk(models.Model):
    key = models.CharField(max_length=255)
    content = models.TextField()
    lang_code = models.CharField(max_length=5)
    site_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'chunks_chunk'
        unique_together = (('key', 'lang_code', 'site_id'),)
        app_label = 'minus_lviv'


class DeliveryMassmail(models.Model):
    subject = models.CharField(max_length=256)
    body = models.TextField()
    banner = models.TextField()
    date = models.DateTimeField()
    is_ready = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'delivery_massmail'
        app_label = 'minus_lviv'


class DeliverySubscriber(models.Model):
    email = models.CharField(unique=True, max_length=128)
    is_subscribed = models.IntegerField()
    frequency = models.CharField(max_length=12)
    date = models.DateTimeField()
    hash = models.CharField(max_length=128)

    class Meta:
        managed = True
        db_table = 'delivery_subscriber'
        app_label = 'minus_lviv'

# @receiver(post_save, sender=User)
# def create_user_subscribed(sender, instance, created, **kwargs):
#     if created:
#         UsersUserrating.objects.create(user=instance,rating = 0,average_minus_rating = 0)



class DeliverySubscribersmailsettings(models.Model):
    daily_title = models.CharField(max_length=256)
    daily_body = models.TextField()
    daily_banner = models.TextField(blank=True, null=True)
    weekly_title = models.CharField(max_length=256)
    weekly_body = models.TextField()
    weekly_banner = models.TextField(blank=True, null=True)
    weekly_2_title = models.CharField(max_length=256)
    weekly_2_body = models.TextField()
    weekly_2_banner = models.TextField(blank=True, null=True)
    monthly_title = models.CharField(max_length=256)
    monthly_body = models.TextField()
    monthly_banner = models.TextField(blank=True, null=True)
    happybirthday_title = models.CharField(max_length=256)
    happybirthday_body = models.TextField()
    happybirthday_banner = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'delivery_subscribersmailsettings'
        app_label = 'minus_lviv'



class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    user_id = models.IntegerField()
    content_type_id = models.IntegerField(blank=True, null=True)
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()

    class Meta:
        managed = True
        db_table = 'django_admin_log'
        app_label = 'minus_lviv'


class DjangoAuthopenidAssociation(models.Model):
    server_url = models.TextField()
    handle = models.CharField(max_length=255)
    secret = models.TextField()
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.TextField()

    class Meta:
        managed = True
        db_table = 'django_authopenid_association'
        app_label = 'minus_lviv'


class DjangoAuthopenidNonce(models.Model):
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=40)

    class Meta:
        managed = True
        db_table = 'django_authopenid_nonce'
        app_label = 'minus_lviv'


class DjangoAuthopenidUserassociation(models.Model):
    openid_url = models.CharField(primary_key=True, max_length=255)
    user_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'django_authopenid_userassociation'
        app_label = 'minus_lviv'


class DjangoCommentFlags(models.Model):
    user_id = models.IntegerField()
    comment_id = models.IntegerField()
    flag = models.CharField(max_length=30)
    flag_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'django_comment_flags'
        unique_together = (('user_id', 'comment_id', 'flag'),)
        app_label = 'minus_lviv'


class DjangoComments(models.Model):
    content_type_id = models.IntegerField()
    object_pk = models.TextField()
    site_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=50)
    user_email = models.CharField(max_length=75)
    user_url = models.CharField(max_length=200, blank=True, null=True)
    comment = models.TextField()
    submit_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=15, blank=True, null=True)
    is_public = models.IntegerField()
    is_removed = models.IntegerField()
    is_edited = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'django_comments'
        app_label = 'minus_lviv'


class CommentReply(models.Model):
    parent_comment = models.ForeignKey(DjangoComments, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

    class Meta:
        managed = True
        db_table = 'comment_replies'
        app_label = 'minus_lviv'


class CommentInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(DjangoComments, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)
    is_disliked = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'comment_interaction'
        app_label = 'minus_lviv'


class DjangoContentType(models.Model):
    name = models.CharField(max_length=100,default='null')
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)
        app_label = 'minus_lviv'


class DjangoFlatpage(models.Model):
    url = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    content = models.TextField()
    enable_comments = models.IntegerField()
    template_name = models.CharField(max_length=70)
    registration_required = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'django_flatpage'
        app_label = 'minus_lviv'


class DjangoFlatpageSites(models.Model):
    flatpage_id = models.IntegerField()
    site_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'django_flatpage_sites'
        unique_together = (('flatpage_id', 'site_id'),)
        app_label = 'minus_lviv'


class DjangoMessagesMessage(models.Model):
    subject = models.CharField(max_length=120)
    body = models.TextField()
    sender_id = models.IntegerField()
    recipient_id = models.IntegerField(blank=True, null=True)
    parent_msg_id = models.IntegerField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    read_at = models.DateTimeField(blank=True, null=True)
    replied_at = models.DateTimeField(blank=True, null=True)
    sender_deleted_at = models.DateTimeField(blank=True, null=True)
    recipient_deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'django_messages_message'
        app_label = 'minus_lviv'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255,default="migration")
    applied = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'django_migrations'
        app_label = 'minus_lviv'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'django_session'
        app_label = 'minus_lviv'


class DjangoSite(models.Model):
    domain = models.CharField(max_length=100)
    name = models.CharField(max_length=50,default='null')

    class Meta:
        managed = True
        db_table = 'django_site'
        app_label = 'minus_lviv'


class DjangobbForumAttachment(models.Model):
    post_id = models.IntegerField()
    size = models.IntegerField()
    content_type = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    name = models.TextField(default='null')
    hash = models.CharField(max_length=40)

    class Meta:
        managed = True
        db_table = 'djangobb_forum_attachment'
        app_label = 'minus_lviv'


class DjangobbForumBan(models.Model):
    user_id = models.IntegerField(unique=True)
    ban_start = models.DateTimeField()
    ban_end = models.DateTimeField(blank=True, null=True)
    reason = models.TextField()

    class Meta:
        managed = True
        db_table = 'djangobb_forum_ban'
        app_label = 'minus_lviv'


class DjangobbForumCategory(models.Model):
    name = models.CharField(max_length=80,default='null')
    position = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'djangobb_forum_category'
        app_label = 'minus_lviv'

class DjangobbForumCategoryGroups(models.Model):
    category_id = models.IntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'djangobb_forum_category_groups'
        unique_together = (('category_id', 'group_id'),)
        app_label = 'minus_lviv'


class DjangobbForumForum(models.Model):
    category_id = models.IntegerField()
    name = models.CharField(max_length=80,default='null')
    position = models.IntegerField()
    description = models.TextField()
    updated = models.DateTimeField()
    post_count = models.IntegerField()
    topic_count = models.IntegerField()
    last_post_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'djangobb_forum_forum'
        app_label = 'minus_lviv'


class DjangobbForumForumModerators(models.Model):
    forum_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'djangobb_forum_forum_moderators'
        unique_together = (('forum_id', 'user_id'),)
        app_label = 'minus_lviv'


class DjangobbForumPost(models.Model):
    topic_id = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    created = models.DateTimeField()
    updated = models.DateTimeField(blank=True, null=True)
    updated_by_id = models.IntegerField(blank=True, null=True)
    markup = models.CharField(max_length=15)
    body = models.TextField()
    body_html = models.TextField()
    user_ip = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'djangobb_forum_post'
        app_label = 'minus_lviv'


class DjangobbForumPosttracking(models.Model):
    user_id = models.IntegerField(unique=True)
    topics = models.TextField(blank=True, null=True)
    last_read = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'djangobb_forum_posttracking'
        app_label = 'minus_lviv'


class DjangobbForumProfile(models.Model):
    user_id = models.IntegerField(unique=True)
    status = models.CharField(max_length=30)
    site = models.CharField(max_length=200)
    jabber = models.CharField(max_length=80)
    icq = models.CharField(max_length=12)
    msn = models.CharField(max_length=80)
    aim = models.CharField(max_length=80)
    yahoo = models.CharField(max_length=80)
    location = models.CharField(max_length=30)
    signature = models.TextField()
    time_zone = models.FloatField()
    language = models.CharField(max_length=5)
    avatar = models.CharField(max_length=100)
    theme = models.CharField(max_length=80)
    show_avatar = models.IntegerField()
    show_signatures = models.IntegerField()
    privacy_permission = models.IntegerField()
    markup = models.CharField(max_length=15)
    post_count = models.IntegerField()
    show_smilies = models.IntegerField()
    signature_html = models.TextField()

    class Meta:
        managed = True
        db_table = 'djangobb_forum_profile'
        app_label = 'minus_lviv'


class DjangobbForumReport(models.Model):
    reported_by_id = models.IntegerField()
    post_id = models.IntegerField()
    zapped = models.IntegerField()
    zapped_by_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField()
    reason = models.TextField()

    class Meta:
        managed = True
        db_table = 'djangobb_forum_report'
        app_label = 'minus_lviv'


class DjangobbForumReputation(models.Model):
    from_user_id = models.IntegerField()
    to_user_id = models.IntegerField()
    post_id = models.IntegerField()
    time = models.DateTimeField()
    sign = models.IntegerField()
    reason = models.TextField()

    class Meta:
        managed = True
        db_table = 'djangobb_forum_reputation'
        unique_together = (('from_user_id', 'post_id'),)
        app_label = 'minus_lviv'


class DjangobbForumTopic(models.Model):
    forum_id = models.IntegerField()
    name = models.CharField(max_length=255,default='null')
    created = models.DateTimeField()
    updated = models.DateTimeField(blank=True, null=True)
    user_id = models.IntegerField()
    views = models.IntegerField()
    sticky = models.IntegerField()
    closed = models.IntegerField()
    post_count = models.IntegerField()
    last_post_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'djangobb_forum_topic'
        app_label = 'minus_lviv'


class DjangobbForumTopicSubscribers(models.Model):
    topic_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'djangobb_forum_topic_subscribers'
        unique_together = (('topic_id', 'user_id'),)
        app_label = 'minus_lviv'


class DjangoratingsScore(models.Model):
    content_type_id = models.IntegerField()
    object_id = models.IntegerField()
    key = models.CharField(max_length=32)
    score = models.IntegerField()
    votes = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'djangoratings_score'
        unique_together = (('content_type_id', 'object_id', 'key'),)
        app_label = 'minus_lviv'


class DjangoratingsVote(models.Model):
    content_type_id = models.IntegerField()
    object_id = models.IntegerField()
    key = models.CharField(max_length=32)
    score = models.IntegerField()
    user_id = models.IntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=15)
    date_added = models.DateTimeField()
    date_changed = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'djangoratings_vote'
        unique_together = (('content_type_id', 'object_id', 'key', 'user_id', 'ip_address'),)
        app_label = 'minus_lviv'


class ForumForum(models.Model):
    title = models.CharField(max_length=256)
    slug = models.CharField(max_length=256)
    parent_id = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    threads = models.IntegerField()
    posts = models.IntegerField()
    ordering = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'forum_forum'
        app_label = 'minus_lviv'


class ForumForumGroups(models.Model):
    forum_id = models.IntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'forum_forum_groups'
        unique_together = (('forum_id', 'group_id'),)
        app_label = 'minus_lviv'


class ForumPost(models.Model):
    thread_id = models.IntegerField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    body_html = models.TextField()
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'forum_post'
        app_label = 'minus_lviv'


class ForumSubscription(models.Model):
    author_id = models.IntegerField()
    thread_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'forum_subscription'
        unique_together = (('author_id', 'thread_id'),)
        app_label = 'minus_lviv'


class ForumThread(models.Model):
    forum_id = models.IntegerField()
    title = models.CharField(max_length=512)
    sticky = models.IntegerField()
    closed = models.IntegerField()
    posts = models.IntegerField()
    views = models.IntegerField()
    latest_post_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'forum_thread'
        app_label = 'minus_lviv'



class HitcountBlacklistIp(models.Model):
    ip = models.CharField(unique=True, max_length=40)

    class Meta:
        managed = True
        db_table = 'hitcount_blacklist_ip'
        app_label = 'minus_lviv'


class HitcountBlacklistUserAgent(models.Model):
    user_agent = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = True
        db_table = 'hitcount_blacklist_user_agent'
        app_label = 'minus_lviv'


class HitcountHit(models.Model):
    created = models.DateTimeField()
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40)
    user_agent = models.CharField(max_length=255)
    user_id = models.IntegerField(blank=True, null=True)
    hitcount_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'hitcount_hit'
        app_label = 'minus_lviv'


class HitcountHitCount(models.Model):
    hits = models.IntegerField()
    modified = models.DateTimeField()
    content_type_id = models.IntegerField()
    object_pk = models.TextField()

    class Meta:
        managed = True
        db_table = 'hitcount_hit_count'
        app_label = 'minus_lviv'


class JchatMessage(models.Model):
    room_id = models.IntegerField()
    type = models.CharField(max_length=1)
    author_id = models.IntegerField(blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'jchat_message'
        app_label = 'minus_lviv'


class JchatRoom(models.Model):
    content_type_id = models.IntegerField(blank=True, null=True)
    object_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField()
    comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'jchat_room'
        unique_together = (('content_type_id', 'object_id'),)
        app_label = 'minus_lviv'


class LinksFriendlink(models.Model):
    title = models.CharField(max_length=256)
    site = models.CharField(max_length=256)
    category_id = models.IntegerField()
    description = models.TextField()
    image_code = models.TextField(blank=True, null=True)
    banner_page = models.CharField(max_length=512, blank=True, null=True)
    email = models.CharField(max_length=128)
    is_approved = models.IntegerField()
    date_created = models.DateTimeField()
    date_approved = models.DateTimeField()
    is_notified = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'links_friendlink'
        app_label = 'minus_lviv'


class LinksFriendlinkcategory(models.Model):
    name = models.CharField(max_length=256,default='null')

    class Meta:
        managed = True
        db_table = 'links_friendlinkcategory'
        app_label = 'minus_lviv'


class MessagesMessage(models.Model):
    subject = models.CharField(max_length=120)
    body = models.TextField()
    sender_id = models.IntegerField()
    recipient_id = models.IntegerField(blank=True, null=True)
    parent_msg_id = models.IntegerField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    read_at = models.DateTimeField(blank=True, null=True)
    replied_at = models.DateTimeField(blank=True, null=True)
    sender_deleted_at = models.DateTimeField(blank=True, null=True)
    recipient_deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'messages_message'
        app_label = 'minus_lviv'



class RadioRadiojingle(models.Model):
    title = models.CharField(max_length=90, blank=True, null=True)
    file = models.CharField(max_length=2048)
    enabled = models.IntegerField()
    duration = models.TimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'radio_radiojingle'
        app_label = 'minus_lviv'


class RadioRadioplaylist(models.Model):
    title = models.CharField(max_length=90, blank=True, null=True)
    play_date = models.DateField(blank=True, null=True)
    play_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    play_in_time = models.IntegerField()
    added_by_id = models.IntegerField(blank=True, null=True)
    randomize = models.IntegerField()
    set_duration = models.IntegerField()
    duration = models.TimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'radio_radioplaylist'
        app_label = 'minus_lviv'


class RadioRadioplaylistJingles(models.Model):
    radioplaylist_id = models.IntegerField()
    radiojingle_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'radio_radioplaylist_jingles'
        unique_together = (('radioplaylist_id', 'radiojingle_id'),)
        app_label = 'minus_lviv'


class RadioRadiosong(models.Model):
    title = models.CharField(max_length=90, blank=True, null=True)
    file = models.CharField(max_length=2048)
    enabled = models.IntegerField()
    duration = models.TimeField(blank=True, null=True)
    playlist_id = models.IntegerField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    content_type_id = models.IntegerField(blank=True, null=True)
    object_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'radio_radiosong'
        app_label = 'minus_lviv'


class RegistrationRegistrationprofile(models.Model):
    user_id = models.IntegerField(unique=True)
    activation_key = models.CharField(max_length=40)

    class Meta:
        managed = True
        db_table = 'registration_registrationprofile'
        app_label = 'minus_lviv'


class SouthMigrationhistory(models.Model):
    app_name = models.CharField(max_length=255)
    migration = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'south_migrationhistory'
        app_label = 'minus_lviv'


class TastypieApiaccess(models.Model):
    identifier = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    request_method = models.CharField(max_length=10)
    accessed = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'tastypie_apiaccess'
        app_label = 'minus_lviv'


class TastypieApikey(models.Model):
    user_id = models.IntegerField(unique=True)
    key = models.CharField(max_length=256)
    created = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'tastypie_apikey'
        app_label = 'minus_lviv'


class VideosVideo(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField()
    embed_video = models.TextField()
    video_album_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'videos_video'
        app_label = 'minus_lviv'


class VideosVideoalbum(models.Model):
    user_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=128,default='null')
    slug = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField()
    videos_count = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'videos_videoalbum'
        app_label = 'minus_lviv'


class VocalContestRealvocalcontestguest(models.Model):
    user_id = models.IntegerField()
    contest_id = models.IntegerField()
    places = models.IntegerField()
    is_payed = models.IntegerField()
    pub_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'vocal_contest_realvocalcontestguest'
        app_label = 'minus_lviv'


class VocalContestRealvocalcontestparticipant(models.Model):
    user_id = models.IntegerField()
    contest_id = models.IntegerField()
    places = models.IntegerField()
    is_payed = models.IntegerField()
    category_id = models.IntegerField()
    info = models.TextField(blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)
    pub_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'vocal_contest_realvocalcontestparticipant'
        app_label = 'minus_lviv'


class VocalContestVocalcontest(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField()
    rules_id = models.IntegerField(blank=True, null=True)
    start_date = models.DateField()
    registration_end_date = models.DateField()
    end_date = models.DateField()
    is_real = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'vocal_contest_vocalcontest'
        app_label = 'minus_lviv'


class VocalContestVocalcontestcategory(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField()
    contest_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'vocal_contest_vocalcontestcategory'
        app_label = 'minus_lviv'


class VocalContestVocalcontestparticipant(models.Model):
    user_id = models.IntegerField()
    contest_id = models.IntegerField()
    title = models.CharField(max_length=120)
    category_id = models.IntegerField()
    file = models.CharField(max_length=2048)
    description = models.TextField()
    pub_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'vocal_contest_vocalcontestparticipant'
        app_label = 'minus_lviv'


class Votes(models.Model):
    user_id = models.IntegerField()
    content_type_id = models.IntegerField()
    object_id = models.IntegerField()
    vote = models.SmallIntegerField()

    class Meta:
        managed = True
        db_table = 'votes'
        unique_together = (('user_id', 'content_type_id', 'object_id'),)
        app_label = 'minus_lviv'
