from __future__ import division, unicode_literals
from math import floor

from django.conf import settings
from django.core.validators import EMPTY_VALUES
from django.db import models, transaction

from jsonfield.fields import JSONField
from django.utils.functional import cached_property
import unicodecsv
from django.core.urlresolvers import reverse
import hashlib
from collections import Counter

from .plugins import initialize_plugins, get_plugin
initialize_plugins()


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
    csv = models.FileField(upload_to='tasks/%Y/%m/%d/')
    answer_label = models.CharField(max_length=30, default="Answer")

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    is_active = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    is_questions_created = models.BooleanField(default=False)
    is_best_of = models.BooleanField(default=False,
                                     help_text="Check this if you want to run best-of-n. Default: max-of-n")

    answer_plugin = models.CharField(max_length=5, blank=True, null=True)

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

    def answered(self, user=None):
        questions = self.questions
        base_qs = Answer.objects.filter(question__in=questions)
        if user:
            return base_qs.filter(answered_by=user).count()
        return base_qs.exclude(answered_by=None).count()

    def progress(self, user=None):
        if user:
            return floor(self.answered(user=user) / self.no_of_questions * 100)
        return None

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
            answered_qs = Answer.objects.filter(question__in=questions, answered_by=user).values_list('question__id', flat=True)
            questions = questions.exclude(id__in=answered_qs)
        return questions.order_by('?').first()

    @property
    def answers(self):
        answers = []
        for question in self.questions:
            row = question.question.copy()
            row.update(question.answer)
            answers.append(row)
        return answers


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

    def compute_answer(self, answers, is_best_of):
        if self.task.answer_plugin:
            answers = get_plugin(self.task.answer_plugin).process(answers)

        if len(answers) < Task.MIN_TO_ANSWER:
            answer = ""
        else:
            most_common = Counter(answers).most_common(1)
            if is_best_of:
                cutoff = max(len(answers) / 2 + 1, Task.MIN_TO_ANSWER)
                if most_common[1] >= cutoff:
                    answer = most_common[0]
                else:
                    answer = ""
            else:
                answer = most_common[0]
        return {'TASK_%s_ANSWER' % (self.task.id): answer}

    def get_absolute_url(self):
        return reverse('question-detail', args=[self.slug])

    @property
    def answer(self):
        answers = self.answer_set.all()
        answers = [a.data for a in answers]
        answers.insert(0, self.compute_answer(answers, self.task.is_best_of))
        return answers

    def __unicode__(self):
        return str(self.slug)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer = JSONField()
    answered_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        unique_together = ('question', 'answered_by')

    def __unicode__(self):
        choice_id = self.answer.get("choice_id")
        if choice_id and choice_id not in EMPTY_VALUES:
            return unicode(Choice.objects.get(task=self.question.task,
                                              id=int(choice_id)))

        return self.answer['verbose']

    @property
    def data(self):
        data = self.question.question
        data["USER_%s_ANSWER" % (self.answered_by.username)] = str(self)
