from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^(?P<slug>[-\w]+)/process/$',
		view	= 'quiz.views.process_quiz',
		name	= 'process_quiz',
	),
	url(r'^(?P<slug>[-\w]+)/$',
		view	= 'quiz.views.quiz_detail',
		name	= 'quiz_detail',
	),
	url(r'^$',
		view	= 'quiz.views.quiz_dashboard',
		name	= 'quiz_dashboard',
	)
)