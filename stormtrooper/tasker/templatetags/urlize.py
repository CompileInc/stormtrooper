from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import urlize as urlize_impl
from django.utils.safestring import mark_safe
register = template.Library()


@register.filter(is_safe=True, needs_autoescape=True)
@stringfilter
def urlize_target_blank(value, limit=None, autoescape=None):
    if not limit:
        limit = len(value)
    return mark_safe(urlize_impl(value, trim_url_limit=int(limit),
                                 nofollow=True, autoescape=autoescape).replace('<a', '<a target="_blank"'))
