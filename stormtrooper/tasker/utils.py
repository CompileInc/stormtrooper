from django.utils.safestring import mark_safe
from django.utils.text import normalize_newlines
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import urllib


def remove_newlines(text):
    """
    Removes all newline characters from a block of text.
    """
    # First normalize the newlines using Django's nifty utility
    normalized_text = normalize_newlines(text)
    # Then simply remove the newlines like so.
    return mark_safe(normalized_text.replace('\n', ' '))


def send_email_with_attachment(to_addr, attachment, **kwargs):
    data_dict = kwargs['data_dict']
    subject_template = kwargs['subject_template']
    email_template = kwargs['email_template']
    subject = remove_newlines(render_to_string(subject_template, data_dict))
    body = render_to_string(email_template, data_dict)
    email = EmailMessage(
                         subject = subject,
                         body = body,
                         to=to_addr
                         )
    email.attach_file(attachment)
    email.send(fail_silently=True)


def url_with_params(url, **kwargs):
    return "{}?{}".format(url, urllib.urlencode(kwargs))