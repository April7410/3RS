from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from account.views import login_redirect

urlpatterns = [
    url(r'^$', login_redirect, name='login_redirect'),
    #path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('account/', include('account.urls')),
    path('buildings/', include('reservation.urls')),
    path('admin/', admin.site.urls),
]
