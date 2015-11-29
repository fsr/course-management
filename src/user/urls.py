from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls as auth_urls
from .views import user, register, activate, contact

urlpatterns = [
    url(r'^register/$', register.register, name='register'),
    url(r'^edit/$', user.modify, name='modify-user'),
    url(r'^profile/$', user.profile, name='user-profile'),
    url(r'^profile/(?P<user_id>[0-9]+)/$', user.profile, name='user-profile'),
    url(r'^activate/$', activate.activate, name='activate-user'),
    url(r'^student/verify/$', register.verify_student, name='student-verification'),
    url(r'^logout/$', auth_views.logout, {
        'template_name': 'registration/logout.html'
    }, name='logout'),
    url(r'^login/$', auth_views.login, {
        'template_name': 'registration/login.html'
    }, name='login'),
    url(r'contact/(?P<user_id>[0-9]+)/', contact.contact_form, name='contact-form'),
    url(r'^', include(auth_urls)),
]
