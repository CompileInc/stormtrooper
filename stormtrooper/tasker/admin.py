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

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()

admin.site.register(Task, TaskAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Question)
admin.site.register(Answer)
