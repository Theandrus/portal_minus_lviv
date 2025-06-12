from django.urls import path
from . import views

urlpatterns = [
    path('shame/', views.desk_of_shame, name='desk_of_shame'),
    path('respect/', views.desk_or_respect, name='desk_of_respect'),
]