from django.conf.urls import include, url

from polls.views import tokens, polls

urlpatterns = [
    url(r'^$', polls.overview, name='poll-overview'),
    url(r'^create/$', polls.create, name='poll-create'),
    url(r'^poll/(?P<poll_name>[\w_\d-]+)/', include([
        url(r'^$', polls.view, name='poll-view'),
        url(r'^tokens/', include([
            url(r'^$', tokens.all, name='poll-token-overview'),
            url(r'^generate/$', tokens.generate, name='poll-generate-token'),
            #url(r'^generate/user/$', tokens.generate_user_token, name='generate-user-token')
        ])),
        url(r'^edit/', include([
            url(r'^question/(?P<question_id>[0-9]+)/', include([
                url(r'^add/$', polls.add_question, name='poll-add-question'),
                url(r'^(?P<qlink_id>[0-9]+)/', include([
                    url(r'^remove/$', polls.remove_question, name='poll-remove-question'),
                    url(r'^bump/', include([
                        url(r'^up/$', polls.bump_question, {'up': True}, name='poll-bump-question-up'),
                        url(r'^down/', polls.bump_question, {'up': False}, name='poll-bump-question-down'),
                    ])),
                ])),
            ])),
            url(r'^questions/$', polls.edit_questions, name='poll-edit-questions'),
        ])),
        url(r'^results/$', polls.results, name='poll-view-results'),
        url(r'^vote/$', polls.vote, name='poll-vote')
    ]))
]
