from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic import View
from django.http.response import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse

from tasker.models import Task, Question
from tasker.forms import TextAnswerForm, ChoiceAnswerForm


class TaskListView(ListView):
    model = Task

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all_active()
        elif self.model.objects.filter(created_by=self.request.user).exists():
            return self.model.objects.all_active().filter(created_by=self.request.user)
        else:
            return self.model.objects.active()


class TaskDetailView(DetailView):
    model = Task


class TaskPlayView(View):

    def get(self, request, pk):
        try:
            task_obj = Task.objects.get(pk=pk)
            if not task_obj.is_closed:
                random_qn = task_obj.random_question(user=request.user)
                return HttpResponseRedirect(random_qn.get_absolute_url())
            return HttpResponseRedirect(reverse('task-list'))
        except Task.DoesNotExist:
            return Http404


class QuestionDetailView(DetailView, FormMixin):
    model = Question

    def get_form(self, form_class=None):
        question = self.get_object()
        task = question.task
        kwargs = self.get_form_kwargs()
        if form_class is None:
            if task.is_multiple_choice:
                return ChoiceAnswerForm(task=task, **kwargs)
            else:
                return TextAnswerForm(**kwargs)
        else:
            return form_class(**kwargs)
