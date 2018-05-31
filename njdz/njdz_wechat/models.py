# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
'''
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __unicode__(self):              # __unicode__ on Python 2
        return self.question_text
'''

class Exam(models.Model):
    type = models.CharField('Exam Type', max_length=50)
    url = models.CharField('Exam URL', max_length=20)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.type

class QuestionType(models.Model):
    type = models.CharField(max_length=50)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.type

class User(models.Model):
    name = models.CharField(max_length=200)
    '''
    department = models.CharField(max_length=200)
    work_type = models.CharField(max_length=100)
    '''
    work_id = models.CharField(max_length=20)
    '''
    phone = models.CharField(max_length=20)
    wechat = models.CharField(max_length=20)
    '''
    def __unicode__(self):              # __unicode__ on Python 2
        return self.name

class ChoiceQuestion(models.Model):
    question = models.TextField('Question')
    #question_type = models.BooleanField('IsMultiChoice', default=False)
    question_type = models.IntegerField('Question Type (1-6)', default=1)
    #question_type = models.ForeignKey(QuestionType)
    choice_A = models.CharField(max_length=200)
    choice_B = models.CharField(max_length=200)
    choice_C = models.CharField(max_length=200)
    choice_D = models.CharField(max_length=200)
    right_answer = models.CharField(max_length=20)
    is_choice = models.BooleanField('Is ChoiceQuestion', default=True)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.question

class MultiChoiceQuestion(models.Model):
    question = models.TextField('Question')
    question_type = models.IntegerField('Question Type (1-6)', default=1)
    choice_A = models.CharField(max_length=200)
    choice_B = models.CharField(max_length=200)
    choice_C = models.CharField(max_length=200)
    choice_D = models.CharField(max_length=200)
    right_answer = models.CharField(max_length=20)
    is_multichoice = models.BooleanField('Is MultiChoiceQuestion', default=True)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.question

class JudgeQuestion(models.Model):
    question = models.TextField('Question')
    question_type = models.IntegerField('Question Type (1-6)', default=1)
    right_answer = models.BooleanField('Right Or False', default=False)
    is_judge = models.BooleanField('Is JudgeQuestion', default=True)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.question
'''
class WeekRecordManager(models.Manager):
    def get(self, week):
        return super(WeekRecordManager, self).all().filter(get_week=week)
'''
class Record(models.Model):
    user = models.ForeignKey(User)
    department = models.CharField('Department', max_length=200)
    work_type = models.CharField('Work Type', max_length=100)
    exam_type = models.CharField('Exam Type', max_length=50)
    question_type = models.CharField('Question Type', max_length=50)
    start_time = models.DateTimeField('Start Time')
    end_time = models.DateTimeField('End Time')
    num_right = models.IntegerField('Right Number', default=0)
    num_total = models.IntegerField('Total Number', default=0)
    exam_score = models.CharField(max_length=50, default='0')

    def get_week(self):
        return self.end_time.strftime('%W')
    def get_month(self):
        return self.end_time.strftime('%m')
    def get_quarter(self):
        month = self.end_time.strftime('%m')
        if month=='01' or month=='02' or month=='03':
            return '01'
        elif month=='04' or month=='05' or month=='06':
            return '02'
        elif month=='07' or month=='08' or month=='09':
            return '03'
        else:
            return '04'
    def get_year(self):
        return self.end_time.strftime('%Y')
    get_week.short_description = 'Exam Week'
    get_month.short_description = 'Exam Month'
    get_quarter.short_description = 'Exam Quarter'
    get_year.short_description = 'Exam Year'
    def __unicode__(self):              # __unicode__ on Python 2
        return self.user.name

class Rank(models.Model):
    user = models.ForeignKey(User)
    exam_score = models.CharField(max_length=50)
    rank_no = models.IntegerField()

    def __unicode__(self):              # __unicode__ on Python 2
        return self.user.name

'''
class config(models.Model):
    start_time = models.DateTimeField('Start Time')
    end_time = models.DateTimeField('End Time')
    def __unicode__(self):              # __unicode__ on Python 2
        return self.question
'''
