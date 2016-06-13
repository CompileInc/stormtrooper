from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import FormMixin, ProcessFormView, CreateView
from django.views.generic import View
from django.views.generic.base import ContextMixin
from django.http.response import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.encoding import force_text
from django.contrib import messages
from channels import Channel

from tasker.models import Task, Question, Answer, Export
from tasker.forms import TextAnswerForm, ChoiceAnswerForm, ExportForm
import logging

LOG = logging.getLogger(__name__)


class TaskListView(ListView):
    model = Task

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all_active()
        elif self.model.objects.filter(created_by=self.request.user).exists():
            return self.model.objects.all_active().filter(created_by=self.request.user)
        else:
            return self.model.objects.active()


class TaskDetailView(DetailView, ContextMixin):
    model = Task

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        task_obj = self.get_object()
        export_form = ExportForm(initial={'task': task_obj})
        user = self.request.user
        context.update({'export_form': export_form,
                        'answered': task_obj.answered(user),
                        'progress': task_obj.progress(user)})
        return context


class TaskPlayView(View):

    def get(self, request, pk):
        try:
            task_obj = Task.objects.get(pk=pk)
            if not task_obj.is_closed:
                random_qn = task_obj.random_question(user=request.user)
                if random_qn:
                    return HttpResponseRedirect(random_qn.get_absolute_url())
                messages.add_message(self.request, messages.ERROR, "There are no more unanswered questions")
            return HttpResponseRedirect(reverse('task-list'))
        except Task.DoesNotExist:
            return Http404


class ExportListView(ListView, SingleObjectMixin):
    template = 'tasker/export_list.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Task.objects.all())
        return super(ExportListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ExportListView, self).get_context_data(**kwargs)
        context['task'] = self.object
        return context

    def get_queryset(self):
        return self.object.export_set.all()


class TaskExportView(CreateView):
    model = Export
    form_class = ExportForm

    def get_success_url(self):
        if self.object:
            messages.add_message(self.request, messages.INFO, "Your export has been queued")
            LOG.info("Export queued")
        return force_text(self.object.task.get_absolute_url())

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskExportView, self).form_valid(form)


class QuestionDetailView(DetailView, FormMixin, ProcessFormView):
    model = Question

    def get_success_url(self):
        if self.object:
            return force_text(self.object.task.get_task_play_url())

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

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['task'] = self.object.task
        return context

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
            _ans_obj, _created = Answer.objects.get_or_create(question=self.object,
                                                              answered_by=user,
                                                              defaults=defaults)
        return super(QuestionDetailView, self).form_valid(form)
