import logging

from django.contrib import messages
from django.db.models import Q
from django.http.response import Http404, HttpResponseRedirect
from django.utils.encoding import force_text
from django.views.generic import View
from django.views.generic.base import ContextMixin
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import FormMixin, ProcessFormView, CreateView
from django.views.generic.list import ListView

from tasker.forms import TextAnswerForm, ChoiceAnswerForm, ExportForm
from tasker.models import Task, Question, Answer, Export


LOG = logging.getLogger(__name__)


class TaskListView(ListView):
    model = Task

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all_active()
        elif self.model.objects.filter(created_by=self.request.user).exists():
            return self.model.objects.all_active()\
                       .filter(Q(created_by=self.request.user) |
                               Q(is_closed=False))
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
                exclude = request.GET.get('exclude')
                random_qn = task_obj.random_question(user=request.user,
                                                     exclude=exclude)
                if random_qn:
                    return HttpResponseRedirect(random_qn.get_absolute_url())
                messages.add_message(self.request, messages.ERROR, "There are no more unanswered questions")
            return HttpResponseRedirect(task_obj.get_absolute_url())
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
        context['export_form'] = ExportForm(initial={'task': self.object})
        return context

    def get_queryset(self):
        return self.object.export_set.all()


class TaskExportView(CreateView):
    model = Export
    form_class = ExportForm

    def get_success_url(self):
        url = self.request.META.get('HTTP_REFERER',
                                    self.object.task.get_absolute_url())
        if self.object:
            messages.add_message(self.request, messages.INFO, "Your export has been queued")
            LOG.info("Export queued")
        return url

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(TaskExportView, self).form_valid(form)

    def form_invalid(self, form):
        if form.errors and form.errors.get('task'):
            for form_error in form.errors['task']:
                messages.add_message(self.request, level=messages.ERROR, message=form_error)
        return HttpResponseRedirect(form.task.get_absolute_url())


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
        context.update({'task': self.object.task,
                        'progress': self.object.task.progress(self.request.user)})
        return context

    def form_valid(self, form):
        if self.object:
            data = form.cleaned_data
            user = self.request.user
            task = self.object.task
            if task.is_multiple_choice:
                choice_obj = data.get('answer')
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
