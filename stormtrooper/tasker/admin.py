from django.contrib import admin
from tasker.models import Task, Choice, Question, Answer


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('task', 'name')
    raw_id_fields = ('task', )


class ChoiceInline(admin.TabularInline):
    model = Choice


class TaskAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    exclude = ('created_by', )
    list_display = ('title', 'id', 'created_by', 'is_active', 'is_closed')
    list_filter = ('is_active', 'is_closed', 'created_on', 'closed_on')
    inlines = (ChoiceInline, )
    actions = ['generate_questions']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()

    def generate_questions(self, request, queryset):
        for q in queryset:
            q.process()
        questions = Question.objects.filter(task__in=queryset)
        message = "%s tasks processed to %s questions in total." % (queryset.count(), questions.count())
        self.message_user(request, message)

    generate_questions.short_description = "Generate questions"


class QuestionAdmin(admin.ModelAdmin):
    raw_id_fields = ('task',)

admin.site.register(Task, TaskAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
