from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from tasker.models import Export, Answer


class TextAnswerForm(forms.Form):
    answer = forms.CharField(widget=forms.TextInput)


class ChoiceAnswerForm(forms.Form):
    answer = forms.ModelChoiceField(queryset=None)

    def __init__(self, task, *args, **kwargs):
        super(ChoiceAnswerForm, self).__init__(*args, **kwargs)
        if task:
            qs = task.choices
            self.fields['answer'] = forms.ModelChoiceField(queryset=qs,
                                                           widget=forms.RadioSelect,
                                                           empty_label=None)


class ExportForm(forms.ModelForm):
    class Meta:
        model = Export
        fields = ['task']
        widgets = {'task': forms.HiddenInput()}

    def clean_task(self):
        self.task = self.cleaned_data['task']
        if not Answer.objects.filter(question__task=self.task).exists():
            raise ValidationError(_("Task does not have any answers to export"),
                                  code='invalid')
        return self.task
