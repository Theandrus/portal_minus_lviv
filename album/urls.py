from django.urls import path
from . import views

urlpatterns = [
    path('user-album/<int:pk>/', views.user_album, name='user_album'),
]