from django.urls import path
from . import views

urlpatterns = [
    path('user/<int:pk>/', views.user_page, name="user_page"),
    path('reg/', views.RegisterFormView.as_view(), name="registration_page"),
    path('success_registration/', views.success_reg, name="success_reg"),
    path('success_login/', views.success_login, name="success_login"),
    path('login/', views.UserLoginView.as_view(), name="signin"),
    path('update-profile/<int:pk>/', views.ProfileUpdate.as_view(), name="profile_update"),
    path('logout/', views.logout_view, name="logout"),
    path('userlist/', views.userlist, name="userlist"),
    path('userminuses/<int:user_id>/', views.userminuses, name="userminuses"),
    path('user-goods/<int:user_id>/', views.user_goods, name="user_goods"),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('search/', views.user_search, name="user_search"),
    path('activities/', views.activities, name="activities"),
    path('false_auth/', views.false_auth, name="false_auth"),
    path('moderator-messages/', views.moderator_messages, name="moderator_messages"),
    path('add_moderator_message/<int:object_pk>/<int:content_id>/', views.add_moderator_message, name="add_moderator_message"),
    path('get_user/<int:pk>/', views.GetUser.as_view(), name="GetUser"),
    path('friend_request/<int:to_user_id>/', views.FriendsRequest.as_view(), name="friend_request"),
    path('user-friends-requests/', views.friends_requests, name="user_friend_request"),
    path('all-friends/<int:pk>/', views.all_friends, name="all_friends"),
    path('user-advertisement/', views.advertisement, name="advertisement"),
    path('delete-selected-blurbs/<int:pk>/', views.delete_selected_blurbs, name="delete-selected-blurbs"),
    path('add-photo/', views.AddPhoto.as_view(), name="add_photo"),
    path('subscription/', views.subscribe, name='subscribe'),
    path('applications-to-admin/', views.admin_applications, name='applications'),
    path('arrangers-list/', views.admin_arrangers_list, name='arrangers_list'),
    path('applications-to-admin/accept/<int:pk>', views.admin_accept, name='admin_accept'),
    path('applications-to-admin/reject/<int:pk>', views.admin_reject, name='admin_reject'),
    path('button_checker/', views.button_checker, name='button_checker')

]
