"""
URL configuration for fatwa_bot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from chatbot import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # شات الفتاوى
    path('', views.chat_page, name='chat'),
    path('chatbot/getResponse/', views.get_fatwa, name='get_fatwa'),
    path('chatbot/contact/', TemplateView.as_view(template_name='chatbot/includes/contact.html'), name='contact'),
    path('chatbot/get_quick_questions/', views.get_quick_questions, name='get_quick_questions'),
    path('chatbot/register/', views.register_view, name='register'),
    path('chatbot/login/', views.login_view, name='login'),
    path('chatbot/logout/', views.logout_view, name='logout'),
    path('chatbot/my_fatwas/', views.my_fatwas, name='my_fatwas'),  # ✅ جديد
    path('chatbot/get-random-question/', views.get_random_question, name='get_random_question'),

]
