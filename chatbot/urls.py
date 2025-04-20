from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_page, name='chat'),
    path('getResponse/', views.get_fatwa, name='get_fatwa'),
    path('get-random-question/', views.get_random_question, name='get_random_question'),
]

