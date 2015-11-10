from django.conf.urls import url
from course_management.views import course, enroll

urlpatterns = [
    url(r'^$', course.course, name='course'),
    url(r'^edit$', course.edit_course, name='edit-course'),
    url(r'^activate$', course.activate, name='activate-course'),
    url(r'^deactivate$', course.deactivate, name='deactivate-course'),
    url(r'^register$', enroll.add, name='register-course'),
    url(r'^unregister$', enroll.remove, name='unregister-course'),
    url(r'^register/done$', enroll.add_response, name='register-course-done'),
    url(r'^unregister/done$', enroll.remove_response, name='unregister-course-done'),
]
