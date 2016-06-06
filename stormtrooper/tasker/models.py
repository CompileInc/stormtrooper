from __future__ import unicode_literals

from django.conf import settings
from django.core.validators import EMPTY_VALUES
from django.db import models, transaction

from jsonfield.fields import JSONField
from django.utils.functional import cached_property
import unicodecsv
from django.core.urlresolvers import reverse
from django.utils.text import slugify
import hashlib


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
    is_questions_created = models.BooleanField(default=False)

    objects = TaskQuerySet.as_manager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task-detail', args=[self.id])

    @cached_property
    def questions(self):
        return self.question_set.all()

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
    def is_multiple_choice(self):
        if len(self.choices) > 0:
            return True
        return False

    @transaction.atomic
    def process(self, activate=False):
        if not self.is_questions_created:
            data = list(unicodecsv.DictReader(self.csv.file))
            for d in data:
                Question.objects.create(task=self,
                                        question=d)
            self.is_questions_created = True

            if activate:
                self.is_active = True

            self.save()

    def random_question(self, user=None):
        '''
        Responds with a random un-answered question for that user
        if user is None, returns a random question.
        '''
        questions = self.questions
        if user:
            answered_qs = self.answer_set.filter(answered_by=user).values_id('question')
            questions = questions.exclude(id__in=answered_qs)
        return questions.order_by('?').first()


class Choice(models.Model):
    task = models.ForeignKey(Task)
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class Question(models.Model):
    task = models.ForeignKey(Task)
    question = JSONField()
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.slug in EMPTY_VALUES:
            self.slug = hashlib.sha1(str(self.question)).hexdigest()

        return super(Question, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.slug)


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
