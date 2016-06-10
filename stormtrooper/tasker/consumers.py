def tasker_questions_create(message):
    from .models import Task
    task = Task.objects.get(id=message['task_id'])
    task.process(activate=True)
