from django.conf.urls import include, url
from django.contrib import admin
from .views import user, register, activate

urlpatterns = [
    url(r'^register$', register.register, name='register'),
    url(r'^edit$', user.modify, name='modify-user'),
    url(r'^profile', user.profile, name='user-profile'),
    url(r'^activate$', activate.activate, name='activate-user'),
    url('^', include('django.contrib.auth.urls')),
]
