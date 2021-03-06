from __future__ import division, unicode_literals
from collections import Counter
import logging
from math import floor
import StringIO
import datetime
import hashlib
import random
import string
import urllib

from django.core.files.base import ContentFile
from django.conf import settings
from django.core.validators import EMPTY_VALUES
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField
from django.utils.functional import cached_property
from django.core.urlresolvers import reverse

from channels import Channel
from el_pagination.paginators import BasePaginator
import unicodecsv as csv

from .plugins import initialize_plugins, get_plugin

LOG = logging.getLogger(__name__)

initialize_plugins()

# Remove me when el_pagination has proper support for 1.10


def basepaginator__init__(self, object_list, per_page, **kwargs):
    # Hack to support django 1.10 in django-el-pagination
    self._num_pages = None
    if 'first_page' in kwargs:
        self.first_page = kwargs.pop('first_page')
    else:
        self.first_page = per_page
    super(BasePaginator, self).__init__(object_list, per_page, **kwargs)
BasePaginator.__init__ = basepaginator__init__


class TaskQuerySet(models.QuerySet):
    def active(self):
        '''Normal users'''
        return self.filter(is_active=True,
                           is_closed=False)

    def all_active(self):
        '''Admin users'''
        return self.filter(is_active=True)

    def closed(self):
        return self.filter(is_closed=True)


class Task(models.Model):
    MIN_TO_ANSWER = 2

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    csv = models.FileField(upload_to='tasks/%Y/%m/%d/%H%M%S%f/')
    answer_label = models.CharField(max_length=30, default="Answer")

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    is_active = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    is_multiple_choice = models.BooleanField(default=False)
    is_questions_created = models.BooleanField(default=False)
    is_best_of = models.BooleanField(default=False,
                                     help_text="Check this if you want to run best-of-n. Default: max-of-n")

    answer_plugin = models.CharField(max_length=5, blank=True, null=True)

    objects = TaskQuerySet.as_manager()

    class Meta:
        ordering = ['-created_on']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task-detail', args=[self.id])

    def get_task_play_url(self, exclude=None):
        url = reverse('task-play', args=[self.id])
        if exclude:
            return "{}?{}".format(url, urllib.urlencode(exclude))
        return url

    def get_task_export_url(self):
        return reverse('task-export', args=[self.id])

    @cached_property
    def questions(self):
        return self.question_set.all()

    @property
    def exports(self):
        return self.export_set.all()

    @property
    def has_exports(self):
        exports = self.exports
        return exports.exists()

    @cached_property
    def no_of_questions(self):
        return self.questions.count()

    @cached_property
    def question_template(self):
        questions = self.questions
        try:
            template = questions[0].question.keys()
        except IndexError:
            template = {}
        return template

    @cached_property
    def choices(self):
        return self.choice_set.all()

    @cached_property
    def no_of_choices(self):
        return self.choice_set.all().count()

    def answered(self, user=None):
        questions = self.questions
        base_qs = Answer.objects.filter(question__in=questions)
        if user:
            return base_qs.filter(answered_by=user).count()
        return base_qs.exclude(answered_by=None).count()

    def progress(self, user=None):
        if user and self.no_of_questions > 0:
            return floor(self.answered(user=user) / self.no_of_questions * 100)
        return None

    @transaction.atomic
    def process(self, activate=False):
        if not self.is_questions_created:
            data = list(csv.DictReader(self.csv.file))
            for d in data:
                Question.objects.create(task=self,
                                        question=d)
            self.is_questions_created = True

            if activate:
                self.is_active = True

            self.save()

    def random_question(self, user=None, exclude=None):
        '''
        Responds with a random un-answered question for that user
        if user is None, returns a random question.
        '''
        from .models import Answer

        questions = self.questions
        if user:
            answered = Answer.objects.filter(question__in=questions.values_list('id', flat=True),
                                            answered_by=user)\
                                    .values_list('question_id', flat=True)
            questions = questions.exclude(id__in=answered)
            if exclude:
                questions = questions.exclude(slug=exclude)

        return questions.order_by('?').first()

    @property
    def answers(self):
        answers = []
        for question in self.questions:
            row = question.question.copy()
            row.update(question.answer)
            answers.append(row)
        return answers

    def save(self, *args, **kwargs):
        if len(self.choices) > 0:
            self.is_multiple_choice = True
        return super(Task, self).save(*args, **kwargs)


class Choice(models.Model):
    task = models.ForeignKey(Task)
    name = models.CharField(max_length=120)

    def __unicode__(self):
        return self.name


class Question(models.Model):
    task = models.ForeignKey(Task)
    question = JSONField(default=dict({'key1': 'value1',
                                       'key2': 'value2'}))
    slug = models.SlugField(null=True, blank=True)

    def __unicode__(self):
        return str(self.slug)

    def save(self, *args, **kwargs):
        if self.slug in EMPTY_VALUES:
            rs = ''.join(random.choice(string.lowercase) for i in range(10))
            content = "{}{}".format(str(self.question),
                                    str(rs))
            self.slug = hashlib.sha1(content).hexdigest()

        return super(Question, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('question-detail', args=[self.slug])

    def compute_answer(self, answers, is_best_of):
        answer = None
        votes = None
        computed = False
        if self.task.answer_plugin:
            plugin = get_plugin(self.task.answer_plugin)
            if plugin.COMPUTE_ANSWER:
                # Plugins should return answers and votes because if a plugin
                # performs a transformation on answers, that info would be lost when
                # trying to count votes separately
                answer, votes = plugin.process(answers)
                computed = True
            else:
                answers = [ans for ans in get_plugin(self.task.answer_plugin).process(answers) if ans not in EMPTY_VALUES]
        if not answer and not votes and not computed:
            if len(answers) < Task.MIN_TO_ANSWER:
                answer = ""
            else:
                most_common = Counter(answers).most_common(1)[0]
                votes = most_common[1]
                if is_best_of:
                    cutoff = max(len(answers) // 2, Task.MIN_TO_ANSWER)
                    if votes >= cutoff:
                        answer = most_common[0]
                    else:
                        votes = None
                        answer = ""
                else:
                    answer = most_common[0]
        return {'ST_TASK_%s_ANSWER' % (self.task.id): answer,
                'ST_TASK_%s_VOTES' % (self.task.id): votes}

    @property
    def answer(self):
        answer_set = self.answer_set.all()
        answers = {}
        for a in answer_set:
            answers.update(a.data)
        answers.update(self.compute_answer(answers.values(),
                                           self.task.is_best_of))
        return answers


class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer = JSONField(default=dict({'choice_id': None,
                                     'verbose': 'Default Answer'}))
    answered_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_on = models.DateTimeField(auto_now_add=True)

    '''Use this field in future to mark if this answer was chosen.'''
    # is_voted_answer = models.BooleanField(default=False)

    class Meta:
        unique_together = ('question', 'answered_by')

    def __unicode__(self):
        answer = self.answer
        try:
            choice_id = self.answer.get("choice_id")
            if choice_id and choice_id not in EMPTY_VALUES:
                answer = unicode(Choice.objects.get(task=self.question.task,
                                                    id=int(choice_id)))
            else:
                answer = self.cleaned_answer()
        except AttributeError:
            pass
        return answer

    @property
    def data(self):
        return {"ST_USER_%s_ANSWER" % (self.answered_by.username): str(self)}

    def cleaned_answer(self):
        choice_id = self.answer.get("choice_id")
        if not choice_id or choice_id in EMPTY_VALUES:
            answer = self.answer['verbose']
            # remove multiple spaces
            return ' '.join(answer.split())
        return str(self)


class Export(models.Model):
    PROCESSING = 'PS'
    FAILURE = 'FR'
    SUCCESS = 'SS'
    STATUS_CHOICES = ((PROCESSING, "Processing"),
                      (FAILURE, "Failure"),
                      (SUCCESS, "Success"))

    task = models.ForeignKey(Task)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    export_file = models.FileField(upload_to='exports/%Y/%m/%d/%H%M%S%f/',
                                   blank=True, null=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES,
                              default=PROCESSING)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __unicode__(self):
        return unicode(self.task)

    def export(self, file_handle=None):
        '''
        exports the task questions and answers as a CSV
        '''
        try:
            if not file_handle:
                file_handle = StringIO.StringIO()
            data = self.task.answers
            # http://stackoverflow.com/a/11399424
            # getting the union of all keys in all of the answer rows
            headers = list(set().union(*(i.keys() for i in data)))
            writer = csv.DictWriter(file_handle, fieldnames=headers)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
            export_file = ContentFile(file_handle.getvalue())
            export_filename = "ST_TASK_{task_id}_EXPORT_{date}.csv".format(task_id=self.task.id,
                                                                           date=str(datetime.date.today()))
            self.export_file.save(name=export_filename, content=export_file, save=False)
            self.status = self.SUCCESS
        except Exception as e:
            LOG.exception(e)
            self.status = self.FAILURE
        self.save()


@receiver(post_save, sender=Export)
def export_post_save(sender, instance, created=False, *args, **kwargs):
    if instance.status == Export.PROCESSING:
        message = {'export_id': instance.pk}
        Channel('tasker-export-create').send(message)
