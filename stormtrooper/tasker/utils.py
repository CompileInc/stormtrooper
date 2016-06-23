from django.core.mail import send_mail
from django.conf import settings
import html2text
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.text import normalize_newlines


def remove_newlines(text):
    """
    Removes all newline characters from a block of text.
    """
    # First normalize the newlines using Django's nifty utility
    normalized_text = normalize_newlines(text)
    # Then simply remove the newlines like so.
    return mark_safe(normalized_text.replace('\n', ' '))


def send_html_email(to_addr, **kwargs):
    data_dict = kwargs['data_dict']
    subject_template = kwargs['subject_template']
    email_template = kwargs['email_template']
    email_tag = settings.EMAIL_TAG
    subject = "{} {}".format(email_tag, remove_newlines(render_to_string(subject_template, data_dict)))
    html_body = render_to_string(email_template, data_dict)
    text_body = html2text.html2text(html_body)
    send_mail(subject=subject,
              message=text_body,
              from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=to_addr,
              fail_silently=True,
              html_message=html_body)
