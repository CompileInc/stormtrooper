from django.conf.urls import url
from tasker.views import TaskListView, TaskDetailView, QuestionDetailView, TaskPlayView


urlpatterns = (url(r'^$', TaskListView.as_view(), name='task-list'),
               url(r'^(?P<pk>(\d+))/$', TaskDetailView.as_view(), name='task-detail'),
               url(r'^(?P<pk>(\d+))/play$', TaskPlayView.as_view(), name='task-play'),
               url(r'^questions/(?P<slug>[\w-]+)/$', QuestionDetailView.as_view(), name='question-detail'),)
