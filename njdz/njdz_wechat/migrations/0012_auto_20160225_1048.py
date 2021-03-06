# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-25 02:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('njdz_wechat', '0011_auto_20160116_1936'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_score', models.CharField(max_length=50)),
                ('rank_no', models.IntegerField()),
            ],
        ),
        migrations.RenameField(
            model_name='record',
            old_name='score',
            new_name='exam_score',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='phone',
            new_name='work_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='wechat',
        ),
        migrations.AddField(
            model_name='record',
            name='exam_month',
            field=models.IntegerField(default=1, verbose_name='Exam Month'),
        ),
        migrations.AddField(
            model_name='record',
            name='exam_quarter',
            field=models.IntegerField(default=1, verbose_name='Exam Quarter'),
        ),
        migrations.AddField(
            model_name='record',
            name='exam_type',
            field=models.CharField(default=datetime.datetime(2016, 2, 25, 2, 48, 28, 171000, tzinfo=utc), max_length=50, verbose_name='Exam Type'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='record',
            name='exam_week',
            field=models.IntegerField(default=1, verbose_name='Exam Week'),
        ),
        migrations.AddField(
            model_name='record',
            name='exam_year',
            field=models.IntegerField(default=1, verbose_name='Exam Year'),
        ),
        migrations.AddField(
            model_name='record',
            name='num_right',
            field=models.IntegerField(default=0, verbose_name='Right Number'),
        ),
        migrations.AddField(
            model_name='record',
            name='num_total',
            field=models.IntegerField(default=0, verbose_name='Total Number'),
        ),
        migrations.AddField(
            model_name='user',
            name='work_type',
            field=models.CharField(default=datetime.datetime(2016, 2, 25, 2, 48, 31, 394000, tzinfo=utc), max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='record',
            name='question_type',
            field=models.CharField(max_length=50, verbose_name='Question Type'),
        ),
        migrations.AddField(
            model_name='rank',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='njdz_wechat.User'),
        ),
    ]
