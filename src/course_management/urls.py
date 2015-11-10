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

from course_management.views import index, subject, course, enroll
import user_management


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index.index, name='index'),
    #url(r'^login$', login.login, name='login'),
    url(r'^subject/(?P<subjectname>\w+)$', subject.course_overview, name='subject'),

    url(r'^course/(?P<course_id>[0-9]+)/', include([
        url(r'^$', course.course, name='course'),
        url(r'^edit$', course.edit_course, name='edit-course'),
        url(r'^activate$', course.activate, name='activate-course'),
        url(r'^deactivate$', course.deactivate, name='deactivate-course'),
        url(r'^register$', enroll.add, name='register-course'),
        url(r'^unregister$', enroll.remove, name='unregister-course'),
        url(r'^register/done$', enroll.enroll_response, dict(action='register'), name='register-course-done'),
        url(r'^unregister/done$', enroll.enroll_response, dict(action='unregister'), name='unregister-course-done'),
    ])),
    url('^', include(user_management.urls))
]
