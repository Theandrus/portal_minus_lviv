from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_shop, name='main_shop'),
    path('goods/<int:pk>/', views.goods, name='goods'),
    path('blurb-update/<int:pk>/', views.BlurbUpdate.as_view(), name="good-update"),
    path('add-to-selected/<int:pk>/', views.add_to_selected, name="add-to-selected"),
    path('is_business/<int:bool>/', views.gave_business_or_private, name='is_business'),
    path('add_good/', views.add_blurb, name="add_blurb"),
    path('lift-up/<int:pk>/', views.lift_up, name="lift-up"),
]
