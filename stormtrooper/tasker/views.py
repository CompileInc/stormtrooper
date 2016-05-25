from django.views.generic.list import ListView
from tasker.models import Task


class TaskListView(ListView):
    model = Task

    def get_queryset(self):
        return self.model.objects.active()

