from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from tasker.views import TaskListView, TaskDetailView, QuestionDetailView,\
                         TaskPlayView, TaskExportView, ExportListView


urlpatterns = (url(r'^$',
                   login_required(TaskListView.as_view()),
                   name='task-list'),
               url(r'^(?P<pk>(\d+))/$',
                   login_required(TaskDetailView.as_view()),
                   name='task-detail'),
               url(r'^(?P<pk>(\d+))/play$',
                   login_required(TaskPlayView.as_view()),
                   name='task-play'),
               url(r'^export/$',
                   login_required(TaskExportView.as_view()),
                   name='task-export'),
               url(r'^(?P<pk>(\d+))/export/$',
                   login_required(ExportListView.as_view()),
                   name='export-list'),
               url(r'^questions/(?P<slug>[\w-]+)/$',
                   login_required(QuestionDetailView.as_view()),
                   name='question-detail'))
