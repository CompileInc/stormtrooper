from django.contrib.auth import get_user_model
from .models import Task
from .utils import send_email_with_attachment
def tasker_questions_create(message):
    task = Task.objects.get(id=message['task_id'])
    task.process(activate=True)

def tasker_export_create(message):
    task = Task.objects.get(id=message['task_id'])
    user_model = get_user_model()
    user = user_model.objects.get(id=message['user_id'])
    to_addr = [user.email]
    export = task.export()
    attachment = export.export_file.file.name
    data_dict = {'username': user.username,
                 'email': user.email}
    subject_template = 'email/export_subject.txt'
    email_template = 'email/export_email.txt'
    mail_dict = {'data_dict': data_dict,
                 'subject_template': subject_template,
                 'email_template': email_template}
    _result = send_email_with_attachment(to_addr, attachment, **mail_dict)
    # log the result
