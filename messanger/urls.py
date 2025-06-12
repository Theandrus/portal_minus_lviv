from django.urls import path
from . import views, api_views

urlpatterns = [
    path('', views.messanger, name='messanger'),
    path('api/message-list/', api_views.ListMessages.as_view(), name="listMessages"),
]