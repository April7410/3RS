from django.urls import path
from django.conf.urls import url
from django.contrib.auth.views import login, logout
from .views import register, LoginView#, LogoutView

app_name = 'account'

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'login.html'}),
    url(r'^logout/$', logout, {'template_name': 'logout.html'}),
    path('register/', register, name='register'),
]