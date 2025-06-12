from django import template
from minus_lviv.new_minuses import *
from minus_lviv.tops_functions import *
import datetime
from django.contrib.auth.models import User
from main.models import ModeratorMessages,MainBanner, LeftBanner, RightBanner
from user.models import UsersUserrating,Userprofile,UserActivitys, FriendsFriendshiprequest
from main.forms import AuthForm

from minusstore.models import MinusstoreMinusrecord,PreModerationRecord
from django.views.decorators.cache import cache_page
from messanger.models import Channels,NewMessagesChannels

register = template.Library()


@register.inclusion_tag('mytags/minus_per_all_time.html')
def minus_per_all_time():
	return {'minus_top_all_time' : top_minus_per_all_time() }


@register.inclusion_tag('mytags/minus_per_week.html')
def minus_per_week():
	return {'minus_top_week' : top_minus_per_week()}


@register.inclusion_tag('mytags/top_user.html')
def top_u():
	users = top_users()

	return {
		'top_users' : users,
		# 'rating' : rate,
	}


@register.simple_tag
def main_banner():
	try:
		banner = MainBanner.objects.all().reverse()[0].html_code
	except:
		banner = "<p>hello hello hello</p>"
	return banner

@register.simple_tag
def left_banner():
	try:
		banner = LeftBanner.objects.all().reverse()[0].html_code
	except:
		banner = "<p>hello hello hello</p>"
	return banner


@register.simple_tag
def right_banner():
	try:
		banner = RightBanner.objects.all().reverse()[0].html_code
	except:
		banner = "<p>hello hello hello</p>"
	return banner


@register.simple_tag
def count_friend_request(pk):
	friends_request = FriendsFriendshiprequest.objects.filter(to_user_id=pk).count()
	return friends_request


@register.inclusion_tag('mytags/new_m.html')
def new_m():
	pre_moderation_minus = PreModerationRecord.objects.all()
	return {'new_m': pre_moderation_minus}

@register.inclusion_tag('mytags/last_minuses.html')
def last_minuses():
	return {'new_m':new_minuses()}


@register.inclusion_tag('mytags/last_minus_another.html')
def last_minuses_another():
	new_m = MinusstoreMinusrecord.objects.filter(alternative = 1)[:10]
	return {'new_m':new_m}


@register.inclusion_tag('mytags/last_forum.html')
def last_f():
	return {'forum' : last_forum()}

@register.inclusion_tag('mytags/last_comment.html')
def last_c():
	return {'comments' : last_comments()}

@register.inclusion_tag('mytags/login.html')
def login():
	form = AuthForm()
	return 	{'form':form }

@register.inclusion_tag('mytags/letters.html')
def letters():
	pass

@register.simple_tag
def avatar(pk):
	avatar = Userprofile.objects.get(user_id = pk).avatar
	return avatar


@register.simple_tag
def count_moderators_message():
	count = ModeratorMessages.objects.all().count()
	return count

@register.inclusion_tag('mytags/len_shame.html')
def count_shame():
	banned_users = []
	users = Userprofile.objects.filter(banned=1)
	for u in users:
		if u.banned_until>datetime.date.today():
			banned_users.append(u)
	return {'len':len(banned_users)}



@register.inclusion_tag('mytags/user_online.html')
def user_online():
	users = Channels.objects.filter(is_active=1)
	count = users.count()
	users = Userprofile.objects.filter(user_id__in=users.values_list('user_id'))
	return {'users_online': users, 'len': 0, 'count': count}


@register.inclusion_tag('mytags/users_menu.html')
def user_menu(user_id):
	new_messages = NewMessagesChannels.objects.filter(to_user=user_id).count()
	# activitys = UserActivitys.objects.filter(to_user_id = user_id)
	print(new_messages)
	print('yakbu vse bulo')
	return {'count_new_messages': new_messages,}


@register.inclusion_tag('mytags/get_activitys.html')
def get_activitys(user_id):
	activitys = UserActivitys.objects.filter(to_user_id = user_id)[:20]
	return {'activitys':activitys}


@register.inclusion_tag('mytags/last_minuses_for_user.html')
def last_minuses_for_user(user_id):
	try:
		user = User.objects.get(id = user_id)
	except User.DoesNotExist:
		pass
	minuses = MinusstoreMinusrecord.objects.filter(pub_date__range=(user.last_login,datetime.datetime.now()))[:20]
	return {'last_minuses_for_user':minuses}

