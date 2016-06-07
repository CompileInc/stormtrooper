from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin, ProcessFormView
from django.views.generic import View
from django.http.response import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.encoding import force_text

from tasker.models import Task, Question, Answer
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
                if random_qn:
                    return HttpResponseRedirect(random_qn.get_absolute_url())
                #TODO show message saying no more unanswered questions
            return HttpResponseRedirect(reverse('task-list'))
        except Task.DoesNotExist:
            return Http404


class QuestionDetailView(DetailView, FormMixin, ProcessFormView):
    model = Question

    def get_success_url(self):
        # TODO: redirect to next unanswered question
        if self.object:
            return force_text(self.object.get_absolute_url())

    def get_form(self, form_class=None):
        # TODO: notify if question has already been answered
        self.object = self.get_object()
        task = self.object.task
        kwargs = self.get_form_kwargs()
        if form_class is None:
            if task.is_multiple_choice:
                return ChoiceAnswerForm(task=task, **kwargs)
            else:
                return TextAnswerForm(**kwargs)
        else:
            return form_class(**kwargs)

    def form_valid(self, form):
        if self.object:
            data = form.cleaned_data
            user = self.request.user
            task = self.object.task
            if task.is_multiple_choice:
                choice_obj = data.get('answer_choice')
                choice_id = choice_obj.pk
                choice_verbose = choice_obj.name
                answer = {'choice_id': choice_id,
                          'verbose': choice_verbose}
            else:
                answer = {'verbose': data.get('answer')}
            defaults = {'answer': answer}
            _ans_obj, _created = Answer.objects.get_or_create(question=self.object, answered_by=user, defaults=defaults)
        return super(QuestionDetailView, self).form_valid(form)
