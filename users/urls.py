# users/urls.py
from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
]
