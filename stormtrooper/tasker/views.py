from django.views.generic.list import ListView
from tasker.models import Task, Question
from django.views.generic.detail import DetailView
from django.views.generic import View
from django.http.response import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse

class TaskListView(ListView):
    model = Task

    def get_queryset(self):
        if self.model.created_by is self.request.user:
            return self.model.objects.all_active()
        return self.model.objects.active()


class TaskDetailView(DetailView):
    model = Task


class TaskPlayView(View):

    def get(self, request, pk):
        try:
            task_obj = Task.objects.get(pk=pk)
            random_qn = task_obj.random_question(user=request.user)
            return HttpResponseRedirect(reverse('question-detail', kwargs={'slug': random_qn.slug}))
        except Task.DoesNotExist:
            return Http404


class QuestionDetailView(DetailView):
    model = Question
