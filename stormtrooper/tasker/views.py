from django.views.generic.list import ListView
from tasker.models import Task
from django.views.generic.detail import DetailView


class TaskListView(ListView):
    model = Task

    def get_queryset(self):
        return self.model.objects.active()


class TaskDetailView(DetailView):
    model = Task
