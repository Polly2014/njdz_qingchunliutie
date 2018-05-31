# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-26 08:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('njdz_wechat', '0012_auto_20160225_1048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='exam_month',
        ),
        migrations.RemoveField(
            model_name='record',
            name='exam_quarter',
        ),
        migrations.RemoveField(
            model_name='record',
            name='exam_week',
        ),
        migrations.RemoveField(
            model_name='record',
            name='exam_year',
        ),
        migrations.AlterField(
            model_name='choicequestion',
            name='question_type',
            field=models.IntegerField(default=1, verbose_name='Question Type (1-6)'),
        ),
        migrations.AlterField(
            model_name='judgequestion',
            name='question_type',
            field=models.IntegerField(default=1, verbose_name='Question Type (1-6)'),
        ),
        migrations.AlterField(
            model_name='multichoicequestion',
            name='question_type',
            field=models.IntegerField(default=1, verbose_name='Question Type (1-6)'),
        ),
        migrations.AlterField(
            model_name='record',
            name='exam_score',
            field=models.CharField(default='0', max_length=50),
        ),
    ]
