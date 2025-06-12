from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('', views.view_comments, name='view_comments'),
    # path('add/', views.add_comment, name='add_comment'),
    # path('interact/<int:comment_id>/<str:reaction_type>/', views.interact_with_comment, name='interact_with_comment'),
    # path('reply/<int:comment_id>/', views.reply_to_comment, name='reply_to_comment'),
]