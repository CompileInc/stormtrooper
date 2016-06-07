from django import forms

class TextAnswerForm(forms.Form):
    answer = forms.CharField()

class ChoiceAnswerForm(forms.Form):
    answer_choice = forms.ModelChoiceField(queryset=None)

    def __init__(self, task, *args, **kwargs):
        super(ChoiceAnswerForm, self).__init__(*args, **kwargs)
        if task:
            qs = task.choices
            self.fields['answer_choice'] = forms.ModelChoiceField(queryset=qs)
