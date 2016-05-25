from django.conf.urls import url
from tasker.views import TaskListView, TaskDetailView


urlpatterns = (url(r'^$', TaskListView.as_view(), name='task-list'),
               url(r'^(?P<pk>(\d+))/$', TaskDetailView.as_view(), name='task-detail'),
               url(r'^(?P<pk>(\d+))/play$', TaskDetailView.as_view(), name='task-play'),
               )
