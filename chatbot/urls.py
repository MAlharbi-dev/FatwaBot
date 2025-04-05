from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_page, name='chat'),
    path('getResponse/', views.get_fatwa, name='get_fatwa'),
]

