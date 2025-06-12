from django.urls import path
from . import views

urlpatterns = [
    path('', views.plusstore_main, name="plusstore_main"),
]
