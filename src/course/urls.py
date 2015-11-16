from django.conf.urls import include, url
from django.contrib import admin

from course.models.subject import Subject
from course.views import index, subject, course, enroll, time


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index.index, name='index'),
    url(r'subject/', include([
        # If you want to add new urls for subjects, you have to add them
        # before the generic subject url (last entry).
        # Also add the string in question to the SUBJECT_DISALLOWED_NAMES in
        # 'forms.py'.
        url(r'^overview/$', subject.subject_overview, name='subject-overview'),
        url(r'^new/$', subject.create, name='create-subject'),
        url(r'^(?P<subjectname>[^/?]+)/', include([
            url(r'^$', subject.course_overview, name='subject'),
            url(r'^edit/$', subject.edit, name='edit-subject'),
            url(r'^delete/$', subject.delete, name='delete-subject'),
        ]))
    ])),


    url(r'^course/new/$', course.create, name='create-course'),

    url(r'^course/(?P<course_id>[0-9]+)/', include([
        url(r'^$', course.course, name='course'),
        url(r'^edit/$', course.edit_course, name='edit-course'),
        url(r'^delete/$', course.delete, name='delete-course'),
        url(r'^activate/$', course.toggle, {'active': True}, name='activate-course'),
        url(r'^deactivate/$', course.toggle, {'active': False}, name='deactivate-course'),
        url(r'^notify/$', course.notify, name='notify-course'),
        url(r'^notify/done/$', course.notify_done, name='notify-course-done'),
        url(r'^register/$', enroll.add, name='register-course'),
        url(r'^register/done/$', enroll.enroll_response, dict(action='register'), name='register-course-done'),
        url(r'^unregister/$', enroll.remove, name='unregister-course'),
        url(r'^unregister/done/$', enroll.enroll_response, dict(action='unregister'), name='unregister-course-done'),
        url(r'^schedule/edit/$', time.edit_slot, name='course-edit-slot'),
        url(r'^schedule/remove/(?P<slot_id>[0-9]+)/$', time.remove_slot, name='course-remove-slot'),
        url(r'^teachers/$', course.add_teacher, name='add-teacher'),
        url(r'^teachers/remove/(?P<teacher_id>[0-9]+)/$', course.remove_teacher, name='remove-teacher'),
    ])),
    url(r'^accounts/', include('user.urls'), {
            'extra_context': {
                'active_subjects': lambda: Subject.get_active()
            }
    })
]
