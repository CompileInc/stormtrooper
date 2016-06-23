from __future__ import unicode_literals
import hashlib
import urllib

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.functional import cached_property


class Trooper(AbstractUser):

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def profile_pic(self):
        email_hash = hashlib.md5(self.email.lower()).hexdigest()
        keys = {'d': settings.DEFAULT_AVATAR}
        keys = urllib.urlencode(keys)
        return "https://www.gravatar.com/avatar/{hash}?{query}".format(hash=email_hash,
                                                                       query=keys)

    @cached_property
    def recently_created_tasks(self):
        return self.task_set.all()

    @cached_property
    def recently_answered_tasks(self):
        from tasker.models import Task
        answer_ids = self.recent_answers.values_list('id', flat=True)
        return Task.objects.filter(id__in=answer_ids).distinct()

    @cached_property
    def recent_answers(self):
        return self.answer_set.all().prefetch_related('question__task')
