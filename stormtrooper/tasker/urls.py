from django.conf.urls import url
from tasker.views import TaskListView


urlpatterns = (url(r'^$', TaskListView.as_view(), name='task-list'),)
