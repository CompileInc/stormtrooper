
from .models import Task, Export
from .utils import send_email_with_attachment
from channels import Channel
import logging

LOG = logging.getLogger(__name__)


def tasker_questions_create(message):
    task = Task.objects.get(id=message['task_id'])
    task.process(activate=True)


def tasker_export_send(message):
    export = Export.objects.get(id=message['export_id'])
    if export.status == Export.SUCCESS:
        user = export.created_by
        to_addr = [user.email]
        attachment = export.export_file.file.name
        data_dict = {'username': user.username,
                     'email': user.email}
        subject_template = 'email/export_subject.txt'
        email_template = 'email/export_email.txt'
        mail_dict = {'data_dict': data_dict,
                     'subject_template': subject_template,
                     'email_template': email_template}
        _result = send_email_with_attachment(to_addr, attachment, **mail_dict)
        LOG.info("sent mail")
    else:
        LOG.eror("Could not create CSV for export-id {}".format(export.pk))


def tasker_export_create(message):
    export = Export.objects.get(id=message['export_id'])
    export.export()
    message = {'export_id': export.pk}
    Channel('tasker-export-send').send(message)
