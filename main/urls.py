from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('news/<int:pk>/', views.news_index, name='news_index'),
    path('add-new/', views.AddNewsView.as_view(), name='add_new'),
    path('comments/<int:pk>/', views.GetComments.as_view(), name='comments'),
    path('minus/add_comment/<int:pk>/', views.add_comment_to_minus, name='add_comment_to_minus'),
    path('comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('add_answer/<int:comment_id>/', views.add_answer_to_comment, name='add_answer_to_comment'),
    path('rules/', views.rules, name='rules'),
]

urlpatterns = format_suffix_patterns(urlpatterns)