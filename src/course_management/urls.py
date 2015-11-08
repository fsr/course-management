"""course_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from .views import index, register, subject, course, login, enroll, user, activate


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index.index, name='index'),
    url(r'^register$', register.register, name='register'),
    #url(r'^login$', login.login, name='login'),
    url(r'^subject/(?P<subjectname>\w+)$', subject.render_course_overview, name='subject'),
    url(r'^course/(?P<courseid>[0-9]+)$', course.render_course, name='course'),
    url(r'^enrollment/add/(?P<subject>)$', enroll.add, name='enrollment-add'),
    url(r'^enrollment/remove/(?P<subject>)$', enroll.remove, name='enrollment-remove'),
    url(r'^enrollment/add/(?P<subject>)/done$', enroll.add_response, name='enrollment-add-done'),
    url(r'^enrollment/remove/(?P<subject>)/done$', enroll.remove_response, name='enrollment-remove-done'),
    url(r'^accounts/edit$', user.modify, name='modify-user'),
    url(r'^accounts/profile', user.profile, name='user-profile'),
    url(r'^activate$', activate.activate, name='activate-user'),
    url('^', include('django.contrib.auth.urls')),
]
