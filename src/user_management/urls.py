from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls as auth_urls
from .views import user, register, activate
from course_management.models import subject

urlpatterns = [
    url(r'^register/$', register.register, name='register'),
    url(r'^edit/$', user.modify, name='modify-user'),
    url(r'^profile/$', user.profile, name='user-profile'),
    url(r'^activate/$', activate.activate, name='activate-user'),
    url(r'^logout/$', auth_views.logout, {
        'template_name': 'registration/logout.html',
        'extra_context': {
            'active_subjects': subject.Subject.get_active
        }
    }, name='logout'),
    url(r'^login/$', auth_views.login, {
        'template_name': 'registration/login.html',
        'extra_context': {
            'active_subjects': subject.Subject.get_active
        }
    }, name='login'),
    url('^', include(auth_urls)),
]
