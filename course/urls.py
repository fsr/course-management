from django.urls import include, path, re_path
from django.contrib import admin

from course.views import index, subject, course, enroll, time, news

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', index.index, name='index'),
    re_path(r'^subject/', include([
        # If you want to add new urls for subjects, you have to add them
        # before the generic subject url (last entry).
        # Also add the string in question to the SUBJECT_DISALLOWED_NAMES in
        # 'forms.py'.
        re_path(r'^overview/$', subject.subject_overview, name='subject-overview'),
        re_path(r'^new/$', subject.create, name='create-subject'),
        re_path(r'^(?P<subjectname>[^/?]+)/', include([
            re_path(r'^$', subject.course_overview, name='subject'),
            re_path(r'^edit/$', subject.edit, name='edit-subject'),
            re_path(r'^delete/$', subject.delete, name='delete-subject'),
        ]))
    ])),


    re_path(r'^course/new/$', course.create, name='create-course'),

    re_path(r'^course/(?P<course_id>[0-9]+)/', include([
        re_path(r'^$', course.course, name='course'),
        re_path(r'^edit/$', course.edit_course, name='edit-course'),
        re_path(r'^delete/$', course.delete, name='delete-course'),
        re_path(r'^activate/$', course.toggle,
            {'active': True}, name='activate-course'),
        re_path(r'^deactivate/$', course.toggle,
            {'active': False}, name='deactivate-course'),
        re_path(r'^participants/$', course.participants_list,
            name='course-participants'),
        re_path(r'^notify/', include([
            re_path(r'^$', course.notify, name='notify-course'),
            re_path(r'^done/$', course.notify_done, name='notify-course-done'),
        ])),
        re_path(r'^register/', include([
            re_path(r'^$', enroll.add, name='register-course'),
            re_path(r'^done/$', enroll.enroll_response,
                dict(action='register'), name='register-course-done'),
            re_path(r'^remove/', include([
                re_path(r'^$', enroll.remove, name='unregister-course'),
                re_path(r'^(?P<student_id>[0-9]+)/$',
                    course.remove_student, name='unregister-course'),
                re_path(r'^done/$', enroll.enroll_response,
                    dict(action='unregister'), name='unregister-course-done'),
            ])),
        ])),
        re_path(r'^schedule/', include([
            re_path(r'^edit/$', time.edit_slot, name='course-edit-slot'),
            re_path(r'^remove/(?P<slot_id>[0-9]+)/$',
                time.remove_slot, name='course-remove-slot'),
        ])),
        re_path(r'^teachers/', include([
            re_path(r'^add/$', course.add_teacher, name='add-teacher'),
            re_path(r'^remove/(?P<teacher_id>[0-9]+)/$',
                course.remove_teacher, name='remove-teacher'),
        ])),
        re_path(r'^attendee-list/$', course.attendee_list, name='attendee-list'),
    ])),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
    re_path(r'^accounts/', include('user.urls')),
    re_path(r'^news/create', news.create, name='create-news'),
    re_path(r'^news/overview', news.overview, name='overview-news'),
    re_path(r'^news/(?P<news_id>[0-9]+)/', include([
        re_path(r'^edit/$', news.edit, name='edit-news'),
        re_path(r'^delete/$', news.delete, name='delete-news')
    ])),
    re_path(r'^privacy-policy/', index.privacy_policy, name='privacy-policy')
]
