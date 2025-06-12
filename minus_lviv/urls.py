from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('main.urls')),
    path('shop/', include('shop.urls')),
    path('minusstore/', include('minusstore.urls')),
    path('user/', include('user.urls')),
    path('desks/', include('desks.urls')),
    path('messanger/', include('messanger.urls')),
    path('plusstore/', include('plusstore.urls')),
    path('albums/', include('album.urls')),
    path('comments/', include('comments.urls')),
]
