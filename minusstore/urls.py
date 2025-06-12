from django.urls import path
from . import views

urlpatterns = [
    path('', views.minusstore_main, name="minusstore_main"),
    path('minus/<int:pk>/', views.minusstore_minus, name="minus"),
    path('add_minus/', views.add_minus, name="add_minus"),
    path('if-minus-correct/<int:pk>/', views.if_minus_correct, name="if_minus_correct"),
    path('generete_pdf/<int:pk>/', views.pdf_generete, name="generete_pdf"),
    path('letters-filter/<str:letter>/', views.letters_filter, name="letter_filter"),
    path('give/<int:author_id>/', views.gave, name="gave_minus"),
    path('subscribe/', views.subscribe, name="subscribe"),
    path('minus-archiv/<int:day>/', views.archiv_of_minuses, name="archiv_of_minuses"),
    path('minus-search/', views.minus_search, name="minus-search"),
    path('get_authors/<str:letter>/', views.MinusAuthor.as_view(), name="get_minus_author"),
    path('all-minuses-by-date/', views.all_minuses_by_date, name="all-minuses-by-date"),
    path('minus-update/<int:pk>/', views.MinusRecordUpdate.as_view(), name="minus-update"),
    path('minus-arrangement-assessment/<int:user_id>/<int:minus_id>/<int:assessment>/', views.minusarrangement, name="minus_arrangement"),
    path('minus-quality-assessment/<int:user_id>/<int:minus_id>/<int:assessment>/', views.minusquality, name="minus_quality"),
    path('comment/<int:pk>/dislike/', views.dislike_comment, name='dislike_comment'),
    path('minus/buy/<int:pk>', views.payment_for_minus, name='payment_for_minus')
]
