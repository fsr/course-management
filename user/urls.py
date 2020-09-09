from django.urls import include, re_path, path

from django.contrib.auth import views as auth_views
from django.contrib.auth import urls as auth_urls
from .views import user, register, verify, contact

urlpatterns = [
    re_path(r'^register/$', register.register, name='register'),
    re_path(r'^edit/$', user.modify, name='modify-user'),
    re_path(r'^privacy-policy/$', user.privacy_consent, name='privacy-policy-updated'),
    re_path(r'^delete/$', user.delete_account, name='delete-account'),
    re_path(r'^profile/$', user.profile, name='user-profile'),
    re_path(r'^profile/(?P<user_id>[0-9]+)/$', user.profile, name='user-profile'),
    re_path(r'^verify/(?P<type_>[\w\d_-]+)/$', verify.verify, name='verify'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(template_name='new_ui_foo/registration/logout.html')),
    re_path(r'^login/$', auth_views.LoginView.as_view(template_name='new_ui_foo/registration/login.html')),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='new_ui_foo/user/change_pass.html')),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='new_ui_foo/user/change_pass_success.html')),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='new_ui_foo/registration/password-reset.html')),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='new_ui_foo/registration/password-reset-done.html')),
    re_path(r'^contact/(?P<user_id>[0-9]+)/',
        contact.contact_form, name='contact-form'),
    re_path(r'^', include(auth_urls)),
]
