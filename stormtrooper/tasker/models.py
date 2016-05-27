from __future__ import unicode_literals

from django.conf import settings
from django.core.validators import EMPTY_VALUES
from django.db import models, transaction

from jsonfield.fields import JSONField
from django.utils.functional import cached_property
import unicodecsv


class TaskQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True,
                           is_closed=False)

    def closed(self):
        return self.filter(is_closed=True)


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    csv = models.FileField(upload_to='tasks/%Y/%m/%d/')
    answer_label = models.CharField(max_length=30, default="Answer")

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    is_active = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    closed_on = models.DateTimeField(blank=True, null=True)

    is_questions_created = models.BooleanField(default=False)

    objects = TaskQuerySet.as_manager()

    def __unicode__(self):
        return self.title

    @cached_property
    def no_of_questions(self):
        return self.question_set.all().count()

    @cached_property
    def choices(self):
        return self.choice_set.all()

    @cached_property
    def is_multiple_choice(self):
        if len(self.choices) > 0:
            return True
        return False

    @transaction.atomic
    def process(self):
        if not self.is_questions_created:
            data = list(unicodecsv.DictReader(self.csv.file))
            for d in data:
                Question.objects.create(task=self,
                                        question=d)
            self.is_questions_created = True
            self.save()


class Choice(models.Model):
    task = models.ForeignKey(Task)
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class Question(models.Model):
    task = models.ForeignKey(Task)
    question = JSONField()

    def __unicode__(self):
        return str(self.question)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer = JSONField()
    answered_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        unique_together = ('question', 'answered_by')

    def __unicode__(self):
        if self.answer['choice_id'] not in EMPTY_VALUES:
            return Choice.objects.get(task=self.question.task,
                                      id=int(self.answer['choice_id']))

        return self.answer['verbose']

    def exportable_data(self):
        data = self.question.question
        data["answer_%s" % (self.answered_by.username)] = str(self)
