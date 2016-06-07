from django import forms
from django.contrib import admin, messages
from django.db.models.fields import BLANK_CHOICE_DASH
from tasker.models import Task, Choice, Question, Answer
from plugins import ALL_PLUGIN_CHOICES


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('task', 'name')
    raw_id_fields = ('task', )


class ChoiceInline(admin.TabularInline):
    model = Choice


class TaskAdminForm(forms.ModelForm):
    answer_plugin = forms.ChoiceField(choices=BLANK_CHOICE_DASH + ALL_PLUGIN_CHOICES, required=False)


class TaskAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    exclude = ('created_by', )
    list_display = ('title', 'id', 'created_by', 'is_active', 'is_closed')
    list_filter = ('is_active', 'is_closed', 'created_on')
    inlines = (ChoiceInline, )
    actions = ['generate_questions']
    form = TaskAdminForm

    def save_model(self, request, obj, form, change):
        user = request.user
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = user
        if change and form.is_valid():
            if 'is_closed' in form.changed_data:
                is_closed = form.cleaned_data['is_closed']
                if user.is_superuser or (user == obj.created_by and is_closed):
                    obj.is_closed = is_closed
                else:
                    obj.is_closed = not is_closed
                    message = "You don't have permission to change task status"
                    self.message_user(request, message, level=messages.ERROR)
        obj.save()

    def generate_questions(self, request, queryset):
        for q in queryset:
            q.process()
        questions = Question.objects.filter(task__in=queryset)
        message = "%s tasks processed to %s questions in total." % (queryset.count(), questions.count())
        self.message_user(request, message)

    generate_questions.short_description = "Generate questions"


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('slug', 'task', 'question')
    raw_id_fields = ('task',)
    readonly_fields = ('task', 'question', 'slug')

admin.site.register(Task, TaskAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
