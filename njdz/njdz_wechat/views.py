# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
#from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from njdz_wechat.models import *

from random import shuffle

import datetime
import time
import json
import xlwt

ISOTIMEFORMAT = '%Y-%m-%d %X'
WEEKFORMAT = '%W'

# Create your views here.
question_list = []

def get_quarter(dt):
    month = dt.strftime('%m')
    if month=='01' or month=='02' or month=='03':
        return '01'
    elif month=='04' or month=='05' or month=='06':
        return '02'
    elif month=='07' or month=='08' or month=='09':
        return '03'
    else:
        return '04'

def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    return render_to_response('index.html',{'request':request})

def selectexamtype(request):
    #return HttpResponse("Hello, world!")
    exams = Exam.objects.all()
    return render_to_response('select_exam.html',{'exams':exams})

def selectquestiontype(request, examType):
    libs = QuestionType.objects.all()
    return render_to_response('select_lib.html',{'libs':libs})

def showrule(request, examType, questionType):
    question_url = "/%s/%s/exam"%(examType, questionType)
    if examType=='thzh':
        img_url = '/static/images/rule_thzh.png'
    elif examType=='zfdm':
        img_url = '/static/images/rule_zfdm.png'
    elif examType=='yzdd':
        img_url = '/static/images/rule_yzdd.png'
    else:
        img_url = '/static/images/rule_zjtz.png'

    request.session['tag_submited'] = 0
    request.session['tag_answerded'] = 0
    return render_to_response('rules.html',{'question_url':question_url, 'img_url':img_url})

def answerquestion(request, examType, questionType):

    choicequestions = list(ChoiceQuestion.objects.filter(question_type = questionType))
    multichoicequestions = list(MultiChoiceQuestion.objects.filter(question_type = questionType))
    judgequestions = list(JudgeQuestion.objects.filter(question_type = questionType))
    question_list = choicequestions + multichoicequestions + judgequestions
    shuffle(question_list)

    if examType=='zfdm':
        question_list = question_list[:30]
    else:
        question_list = question_list[:300]
    request.session['start_time'] = time.strftime(ISOTIMEFORMAT, time.localtime())    
    
    #request.session['start_time'] = json.dumps(time.localtime())
    request.session['exam_type'] = examType
    request.session['question_type'] = questionType
    request.session['start_question_no'] = 1
    request.session['score'] = 0
    request.session['total_length'] = len(question_list)
    
    request.session['num_right'] = 0
    request.session['num_total'] = 0
    request.session['tag_answerded'] = 0
    pre_info_url = "/%s/%s/"%(examType, questionType)
    file_template = "%s.html"%examType
    try:
        if request.session['tag_submited']:
            print "tag_submited=1"
            return HttpResponseRedirect('/polly/')
        else:
            print "tag_submited=0"
            return render_to_response(file_template, {'question_list':question_list,'request':request,'pre_info_url':pre_info_url})
    except:
        return HttpResponseRedirect('/result/')
@csrf_exempt
def inputUserInfo(request):
    try:
        if request.session['tag_submited']:
            return render_to_response('info.html',{'request':request, 'user_list':user_list})
        if request.session['tag_answerded']:
            print 'User has answerded'
            request.session.clear()
            return HttpResponseRedirect('/result/')
        else:
            request.session['tag_answerded'] = 1
    except:
        return HttpResponseRedirect('/result/')
    #if request.session['tag_submited']==1:
    #    return HttpResponseRedirect('/index/')
    request.session['end_time'] = time.strftime(ISOTIMEFORMAT, time.localtime())
    right_num = request.POST.get('right_num', '0')
    total_num = request.POST.get('total_num', '0')
    
    try:
        start_time = time.mktime(time.strptime(request.session['start_time'], ISOTIMEFORMAT))
    except:
        request.session['score'] = 0
        return HttpResponseRedirect('/polly/')
    
    #start_time = time.mktime(time.strptime(request.session['start_time'], ISOTIMEFORMAT))
    end_time = time.mktime(time.strptime(request.session['end_time'], ISOTIMEFORMAT))
    exam_time = end_time - start_time
    request.session['exam_time'] = exam_time

    request.session['num_right'] = right_num
    request.session['num_total'] = total_num
    examType = request.session['exam_type']
    if examType=='thzh':
        request.session['score'] = int(right_num)
    elif examType=='zfdm':
        request.session['score'] = int(5000*(float(right_num)/float(total_num))*(1/float(exam_time)))
    elif examType=='yzdd':
        right_num = int(right_num)
        if right_num<=20:
            request.session['score'] = right_num
        elif right_num<=50:
            request.session['score'] = 20 + (right_num-20)*2
        elif right_num<=100:
            request.session['score'] = 20 + 60 + (right_num-30)*3
        else:
            request.session['score'] = 20 + 60 + 150 + (right_num-100)*5
    elif examType=='zjtz':
        right_num = int(right_num)
        request.session['score'] = int(right_num)

    request.session['department'] = str(QuestionType.objects.get(id = request.session['question_type']))
    user_list = User.objects.all()
    print request.POST
    return render_to_response('info.html',{'request':request, 'user_list':user_list})

def inputuserinfo(request, examType, questionType, right_num, total_num):
    #return HttpResponse("Hello, world!")
    request.session['end_time'] = time.strftime(ISOTIMEFORMAT, time.localtime())
    request.session['exam_type'] = examType
    request.session['question_type'] = questionType
    '''
    request.session['exam_week'] = time.strftime(WEEKFORMAT, time.localtime())
    request.session['exam_month'] = time.strftime('%m')
    if request.session['exam_month'] in '123':
        request.session['exam_quarter'] = '1'
    elif request.session['exam_month'] in '456':
        request.session['exam_quarter'] = '2'
    elif request.session['exam_month'] in '789':
        request.session['exam_quarter'] = '3'
    else:
        request.session['exam_quarter'] = '4'
    request.session['exam_year'] = time.strftime('%Y')
    '''
    request.session['num_right'] = right_num
    request.session['num_total'] = total_num



    start_time = time.mktime(time.strptime(request.session['start_time'], ISOTIMEFORMAT))
    end_time = time.mktime(time.strptime(request.session['end_time'], ISOTIMEFORMAT))
    exam_time = end_time - start_time
    request.session['exam_time'] = exam_time
    print exam_time
    print examType
    if examType=='thzh':
        request.session['score'] = int(right_num)
    elif examType=='zfdm':
        request.session['score'] = int(5000*(float(right_num)/float(total_num))*(1/float(exam_time)))
    elif examType=='yzdd':
        right_num = int(right_num)
        if right_num<=20:
            request.session['score'] = right_num
        elif right_num<=50:
            request.session['score'] = 20 + (right_num-20)*2
        elif right_num<=100:
            request.session['score'] = 20 + 60 + (right_num-30)*3
        else:
            request.session['score'] = 20 + 60 + 150 + (right_num-100)*5
    elif examType=='zjtz':
        right_num = int(right_num)
        request.session['score'] = int(right_num)
        
    print request.session['score']

    #request.session['end_time'] = time.localtime()
    #request.session['exam_week'] = time.strftime(WEEKFORMAT, time.localtime())
    #request.session['score'] = scoreFinal
    #print dir(QuestionType.objects.filter(id = questionType))
    request.session['department'] = str(QuestionType.objects.get(id = questionType))
    user_list = User.objects.all()
    return render_to_response('info.html',{'request':request, 'user_list':user_list})

@csrf_exempt
def result(request):
    u_name = request.POST.get('HiddenField1', u'匿名')
    u_work_id = request.POST.get('HiddenField4', u'000000')
    request.session['department'] = request.POST.get('HiddenField2', u'无')
    request.session['work_type'] = request.POST.get('HiddenField3', u'无')
    try:
        u = User.objects.filter(work_id=u_work_id, name=u_name)[0]
    except:
        return render_to_response('result.html',{'request':request})

    if not u_name=='匿名':
        r_user = u
        r_department = request.session['department']
        r_work_type = request.session['work_type']
        r_exam_type = request.session['exam_type']
        r_question_type = request.session['question_type']
        r_start_time = datetime.datetime.strptime(request.session['start_time'], ISOTIMEFORMAT)
        r_end_time = datetime.datetime.strptime(request.session['end_time'], ISOTIMEFORMAT)
        r_num_right = request.session['num_right']
        r_num_total = request.session['num_total']
        r_exam_score = request.session['score']
        #if Record.objects.filter(user=r_user, department=r_department, work_type=r_work_type, exam_type=r_exam_type, question_type=r_question_type, start_time=r_start_time, num_right=r_num_right, num_total=r_num_total, exam_score=r_exam_score):
        #    request.session['tag_submited'] = 1
        #    return render_to_response('result.html',{'request':request})
        #else:
        #    r = Record(user=r_user, department=r_department, work_type=r_work_type, exam_type=r_exam_type, question_type=r_question_type, start_time=r_start_time, end_time=r_end_time, num_right=r_num_right, num_total=r_num_total, exam_score=r_exam_score)
        #    r.save()
        if request.session['tag_submited']==0:
            r = Record(user=r_user, department=r_department, work_type=r_work_type, exam_type=r_exam_type, question_type=r_question_type, start_time=r_start_time, end_time=r_end_time, num_right=r_num_right, num_total=r_num_total, exam_score=r_exam_score)
            r.save()
            request.session['tag_submited'] = 1
            #del request.session['start_time']
        # else:
        #     return HttpResponseRedirect('/result/')
            
    '''
    u_name = request.GET.get('HiddenField1', '匿名')
    u_department = request.GET.get('HiddenField2', '无')
    u_work_type = request.GET.get('HiddenField3', '无')
    u_work_id = request.GET.get('HiddenField4', '000000')

    if not u_name=='匿名':
        if User.objects.filter(work_id=u_work_id, name=u_name):
            u = User.objects.filter(work_id=u_work_id, name=u_name)[0]
        else:
            u = User(name=u_name, department=u_department, work_type=u_work_type, work_id=u_work_id)
            u.save()

        r_user = u
        r_exam_type = request.session['exam_type']
        r_question_type = request.session['question_type']
        r_start_time = datetime.datetime.strptime(request.session['start_time'], ISOTIMEFORMAT)
        r_end_time = datetime.datetime.strptime(request.session['end_time'], ISOTIMEFORMAT)
        r_num_right = request.session['num_right']
        r_num_total = request.session['num_total']
        r_exam_score = request.session['score']
        r = Record(user=r_user, exam_type=r_exam_type, question_type=r_question_type, start_time=r_start_time, end_time=r_end_time, num_right=r_num_right, num_total=r_num_total, exam_score=r_exam_score)
        r.save()
    '''
    return render_to_response('result.html',{'request':request})    

def ranklistselect(request):
    try:
        request.session.clear()
    except:
        pass
    return render_to_response('ranklist_select.html',{})

def ranlistresult(request, tag):
    rank_dict = {}

    dt = datetime.datetime.now()
    records = Record.objects.distinct()

    if tag=='week':
        title = '业务达人周排行榜'
        week = dt.strftime("%W")
        week_tag = 0
        for r in records:
            if r.get_week()==week:
                if r.user.work_id not in rank_dict.keys():
                    rank_dict[r.user.work_id] = [r.user.name, r.work_type, 0, 0, 0, 0]
                #else:
                if r.exam_type=='thzh':
                    if rank_dict[r.user.work_id][2]==0:
                        rank_dict[r.user.work_id][2] = int(r.exam_score)
                    else:
                        rank_dict[r.user.work_id][2] = rank_dict[r.user.work_id][2] + int(r.exam_score)
                    rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                elif r.exam_type=='zfdm':
                    if rank_dict[r.user.work_id][3]==0:
                        rank_dict[r.user.work_id][3] = int(r.exam_score)
                        rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                        week_tag = int(r.get_week())
                    else:
                        if not int(r.get_week())==week_tag:
                            rank_dict[r.user.work_id][3] = int(r.exam_score)
                            rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                            week_tag = int(r.get_week())
                elif r.exam_type=='yzdd':
                    if rank_dict[r.user.work_id][4]==0:
                        rank_dict[r.user.work_id][4] = int(r.exam_score)
                        rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                        week_tag = int(r.get_week())
                    else:
                        if not int(r.get_week())==week_tag:
                            #print "The Different Week:%s->%s"%(week_tag, int(r.get_week()))
                            rank_dict[r.user.work_id][4] = int(r.exam_score)
                            rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                            week_tag = int(r.get_week())
        rank_dict[r.user.work_id][1] = r.work_type
    elif tag=='month':
        title = '业务达人月排行榜'
        month = dt.strftime("%m")
        week_tag = 0
        for r in records:
            if r.get_month()==month:
                if r.user.work_id not in rank_dict.keys():
                    rank_dict[r.user.work_id] = [r.user.name, r.work_type, 0, 0, 0, 0]
                #else:
                if r.exam_type=='thzh':
                    if rank_dict[r.user.work_id][2]==0:
                        rank_dict[r.user.work_id][2] = int(r.exam_score)
                    else:
                        rank_dict[r.user.work_id][2] = rank_dict[r.user.work_id][2] + int(r.exam_score)
                    rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                elif r.exam_type=='zfdm':
                    if rank_dict[r.user.work_id][3]==0:
                        rank_dict[r.user.work_id][3] = int(r.exam_score)
                        rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                        week_tag = int(r.get_week())
                    else:
                        if not int(r.get_week())==week_tag:
                            #print "The Different Week:%s->%s"%(week_tag, int(r.get_week()))
                            rank_dict[r.user.work_id][3] = int(r.exam_score)
                            rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                            week_tag = int(r.get_week())
                elif r.exam_type=='yzdd':
                    if rank_dict[r.user.work_id][4]==0:
                        rank_dict[r.user.work_id][4] = int(r.exam_score)
                        rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                        week_tag = int(r.get_week())
                    else:
                        if not int(r.get_week())==week_tag:
                            #print "The Different Week:%s->%s"%(week_tag, int(r.get_week()))
                            rank_dict[r.user.work_id][4] = int(r.exam_score)
                            rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                            week_tag = int(r.get_week())
        rank_dict[r.user.work_id][1] = r.work_type
    elif tag=='quarter':
        title = '业务达人季度排行榜'
        quarter = get_quarter(dt)
        week_tag = 0
        for r in records:
            if r.get_quarter()==quarter:
                if r.user.work_id not in rank_dict.keys():
                    rank_dict[r.user.work_id] = [r.user.name, r.work_type, 0, 0, 0, 0]
                #else:
                if r.exam_type=='thzh':
                    if rank_dict[r.user.work_id][2]==0:
                        rank_dict[r.user.work_id][2] = int(r.exam_score)
                    else:
                        rank_dict[r.user.work_id][2] = rank_dict[r.user.work_id][2] + int(r.exam_score)
                    rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                elif r.exam_type=='zfdm':
                    if rank_dict[r.user.work_id][3]==0:
                        rank_dict[r.user.work_id][3] = int(r.exam_score)
                        rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                        week_tag = int(r.get_week())
                    else:
                        if not int(r.get_week())==week_tag:
                            #print "The Different Week:%s->%s"%(week_tag, int(r.get_week()))
                            rank_dict[r.user.work_id][3] = int(r.exam_score)
                            rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                            week_tag = int(r.get_week())
                elif r.exam_type=='yzdd':
                    if rank_dict[r.user.work_id][4]==0:
                        rank_dict[r.user.work_id][4] = int(r.exam_score)
                        rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                        week_tag = int(r.get_week())
                    else:
                        if not int(r.get_week())==week_tag:
                            #print "The Different Week:%s->%s"%(week_tag, int(r.get_week()))
                            rank_dict[r.user.work_id][4] = int(r.exam_score)
                            rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                            week_tag = int(r.get_week())
        rank_dict[r.user.work_id][1] = r.work_type
    elif tag=='year':
        title = '业务达人年度排行榜'
        year = dt.strftime("%Y")
        week_tag = 0
        for r in records:
            if r.get_year()==year:
                if r.user.work_id not in rank_dict.keys():
                    rank_dict[r.user.work_id] = [r.user.name, r.work_type, 0, 0, 0, 0]
                #else:
                if r.exam_type=='thzh':
                    if rank_dict[r.user.work_id][2]==0:
                        rank_dict[r.user.work_id][2] = int(r.exam_score)
                    else:
                        rank_dict[r.user.work_id][2] = rank_dict[r.user.work_id][2] + int(r.exam_score)
                    rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                elif r.exam_type=='zfdm':
                    if rank_dict[r.user.work_id][3]==0:
                        rank_dict[r.user.work_id][3] = int(r.exam_score)
                        rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                        week_tag = int(r.get_week())
                    else:
                        if not int(r.get_week())==week_tag:
                            #print "The Different Week:%s->%s"%(week_tag, int(r.get_week()))
                            rank_dict[r.user.work_id][3] = int(r.exam_score)
                            rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                            week_tag = int(r.get_week())
                elif r.exam_type=='yzdd':
                    if rank_dict[r.user.work_id][4]==0:
                        rank_dict[r.user.work_id][4] = int(r.exam_score)
                        rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                        week_tag = int(r.get_week())
                    else:
                        if not int(r.get_week())==week_tag:
                            #print "The Different Week:%s->%s"%(week_tag, int(r.get_week()))
                            rank_dict[r.user.work_id][4] = int(r.exam_score)
                            rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                            week_tag = int(r.get_week())
        rank_dict[r.user.work_id][1] = r.work_type

    '''
    if tag=='week':
        title = '业务达人周排行榜'
        week = dt.strftime("%W")
        week_tag = 0
        for r in records:
            if r.get_week()==week:
                if r.user.work_id not in rank_dict.keys():
                    rank_dict[r.user.work_id] = [r.user.name, r.user.work_type, 0, 0, 0, 0]
                #else:
                if r.exam_type=='thzh':
                    if rank_dict[r.user.work_id][2]==0:
                        rank_dict[r.user.work_id][2] = int(r.exam_score)
                    else:
                        rank_dict[r.user.work_id][2] = rank_dict[r.user.work_id][2] + int(r.exam_score)
                    rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                elif r.exam_type=='zfdm':
                    if rank_dict[r.user.work_id][3]==0:
                        rank_dict[r.user.work_id][3] = int(r.exam_score)
                        rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                        week_tag = int(r.get_week())
                    else:
                        if not int(r.get_week())==week_tag:
                            rank_dict[r.user.work_id][3] = int(r.exam_score)
                            rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                            week_tag = int(r.get_week())
                elif r.exam_type=='yzdd':
                    if rank_dict[r.user.work_id][4]==0:
                        rank_dict[r.user.work_id][4] = int(r.exam_score)
                        rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                        week_tag = int(r.get_week())
                    else:
                        if not int(r.get_week())==week_tag:
                            #print "The Different Week:%s->%s"%(week_tag, int(r.get_week()))
                            rank_dict[r.user.work_id][4] = int(r.exam_score)
                            rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                            week_tag = int(r.get_week())
    elif tag=='month':
        title = '业务达人月排行榜'
        month = dt.strftime("%m")
        week_tag = 0
        for r in records:
            if r.get_month()==month:
                if r.user.work_id not in rank_dict.keys():
                    rank_dict[r.user.work_id] = [r.user.name, r.user.work_type, 0, 0, 0, 0]
                #else:
                if r.exam_type=='thzh':
                    if rank_dict[r.user.work_id][2]==0:
                        rank_dict[r.user.work_id][2] = int(r.exam_score)
                    else:
                        rank_dict[r.user.work_id][2] = rank_dict[r.user.work_id][2] + int(r.exam_score)
                    rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                elif r.exam_type=='zfdm':
                    if rank_dict[r.user.work_id][3]==0:
                        rank_dict[r.user.work_id][3] = int(r.exam_score)
                        rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                        week_tag = int(r.get_week())
                    else:
                        if not int(r.get_week())==week_tag:
                            #print "The Different Week:%s->%s"%(week_tag, int(r.get_week()))
                            rank_dict[r.user.work_id][3] = int(r.exam_score)
                            rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                            week_tag = int(r.get_week())
                elif r.exam_type=='yzdd':
                    if rank_dict[r.user.work_id][4]==0:
                        rank_dict[r.user.work_id][4] = int(r.exam_score)
                        rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                        week_tag = int(r.get_week())
                    else:
                        if not int(r.get_week())==week_tag:
                            #print "The Different Week:%s->%s"%(week_tag, int(r.get_week()))
                            rank_dict[r.user.work_id][4] = int(r.exam_score)
                            rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                            week_tag = int(r.get_week())
    elif tag=='quarter':
        title = '业务达人季度排行榜'
        quarter = get_quarter(dt)
        week_tag = 0
        for r in records:
            if r.get_quarter()==quarter:
                if r.user.work_id not in rank_dict.keys():
                    rank_dict[r.user.work_id] = [r.user.name, r.user.work_type, 0, 0, 0, 0]
                #else:
                if r.exam_type=='thzh':
                    if rank_dict[r.user.work_id][2]==0:
                        rank_dict[r.user.work_id][2] = int(r.exam_score)
                    else:
                        rank_dict[r.user.work_id][2] = rank_dict[r.user.work_id][2] + int(r.exam_score)
                    rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                elif r.exam_type=='zfdm':
                    if rank_dict[r.user.work_id][3]==0:
                        rank_dict[r.user.work_id][3] = int(r.exam_score)
                        rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                        week_tag = int(r.get_week())
                    else:
                        if not int(r.get_week())==week_tag:
                            #print "The Different Week:%s->%s"%(week_tag, int(r.get_week()))
                            rank_dict[r.user.work_id][3] = int(r.exam_score)
                            rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                            week_tag = int(r.get_week())
                elif r.exam_type=='yzdd':
                    if rank_dict[r.user.work_id][4]==0:
                        rank_dict[r.user.work_id][4] = int(r.exam_score)
                        rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                        week_tag = int(r.get_week())
                    else:
                        if not int(r.get_week())==week_tag:
                            #print "The Different Week:%s->%s"%(week_tag, int(r.get_week()))
                            rank_dict[r.user.work_id][4] = int(r.exam_score)
                            rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                            week_tag = int(r.get_week())
    elif tag=='year':
        title = '业务达人年度排行榜'
        year = dt.strftime("%Y")
        week_tag = 0
        for r in records:
            if r.get_year()==year:
                if r.user.work_id not in rank_dict.keys():
                    rank_dict[r.user.work_id] = [r.user.name, r.user.work_type, 0, 0, 0, 0]
                #else:
                if r.exam_type=='thzh':
                    if rank_dict[r.user.work_id][2]==0:
                        rank_dict[r.user.work_id][2] = int(r.exam_score)
                    else:
                        rank_dict[r.user.work_id][2] = rank_dict[r.user.work_id][2] + int(r.exam_score)
                    rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                elif r.exam_type=='zfdm':
                    if rank_dict[r.user.work_id][3]==0:
                        rank_dict[r.user.work_id][3] = int(r.exam_score)
                        rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                        week_tag = int(r.get_week())
                    else:
                        if not int(r.get_week())==week_tag:
                            #print "The Different Week:%s->%s"%(week_tag, int(r.get_week()))
                            rank_dict[r.user.work_id][3] = int(r.exam_score)
                            rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                            week_tag = int(r.get_week())
                elif r.exam_type=='yzdd':
                    if rank_dict[r.user.work_id][4]==0:
                        rank_dict[r.user.work_id][4] = int(r.exam_score)
                        rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                        week_tag = int(r.get_week())
                    else:
                        if not int(r.get_week())==week_tag:
                            #print "The Different Week:%s->%s"%(week_tag, int(r.get_week()))
                            rank_dict[r.user.work_id][4] = int(r.exam_score)
                            rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                            week_tag = int(r.get_week())

                if r.exam_type=='thzh':
                    if rank_dict[r.user.work_id][2]==0:
                        rank_dict[r.user.work_id][2] = int(r.exam_score)
                    else:
                        rank_dict[r.user.work_id][2] = rank_dict[r.user.work_id][2] + int(r.exam_score)
                elif r.exam_type=='zfdm':
                    rank_dict[r.user.work_id][3] = int(r.exam_score)
                elif r.exam_type=='yzdd':
                    rank_dict[r.user.work_id][4] = int(r.exam_score)
                rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                '''

    rank_list = sorted(rank_dict.items(), key=lambda d: d[1][5], reverse=True)

    return render_to_response('ranklist_result.html',{'rank_list':rank_list, 'title':title})

def download(request):
    dt = datetime.datetime.now()
    week = dt.strftime("%W")
    month = dt.strftime("%m")
    year = dt.strftime("%Y")

    year_list = range(2016, int(year)+1)
    month_list = range(1, int(month)+1)
    week_list = range(1, int(week)+1)
        
    return render_to_response('download.html',{'year_list':year_list, 'month_list':month_list, 'week_list':week_list})

def send_excle_file(request, tag, year, mw):
    rank_dict = {}
    filename = ''

    records = Record.objects.all()

    if tag=='week':
        if len(mw)==1:
            week = "0%s"%mw
        else:
            week = mw
        filename = 'weekrank(%s-%s)'%(year,week)
        print week
        for r in records:
            if r.get_year()==year and r.get_week()==week:
                if r.user.work_id not in rank_dict.keys():
                    rank_dict[r.user.work_id] = [r.user.name, r.work_type, 0, 0, 0, 0, r.department]
                #else:
                if r.exam_type=='thzh':
                    if rank_dict[r.user.work_id][2]==0:
                        rank_dict[r.user.work_id][2] = int(r.exam_score)
                    else:
                        rank_dict[r.user.work_id][2] = rank_dict[r.user.work_id][2] + int(r.exam_score)
                    rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                elif r.exam_type=='zfdm':
                    if rank_dict[r.user.work_id][3]==0:
                        rank_dict[r.user.work_id][3] = int(r.exam_score)
                        rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                elif r.exam_type=='yzdd':
                    if rank_dict[r.user.work_id][4]==0:
                        rank_dict[r.user.work_id][4] = int(r.exam_score)
                        rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
    elif tag=='month':
        if len(mw)==1:
            month = "0%s"%mw
        else:
            month = mw
        filename = 'monthrank(%s-%s)'%(year,month)
        for r in records:
            if r.get_year()==year and r.get_month()==month:
                if r.user.work_id not in rank_dict.keys():
                    rank_dict[r.user.work_id] = [r.user.name, r.work_type, 0, 0, 0, 0, r.department]
                #else:
                if r.exam_type=='thzh':
                    if rank_dict[r.user.work_id][2]==0:
                        rank_dict[r.user.work_id][2] = int(r.exam_score)
                    else:
                        rank_dict[r.user.work_id][2] = rank_dict[r.user.work_id][2] + int(r.exam_score)
                    rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                elif r.exam_type=='zfdm':
                    if rank_dict[r.user.work_id][3]==0:
                        rank_dict[r.user.work_id][3] = int(r.exam_score)
                        rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
                elif r.exam_type=='yzdd':
                    if rank_dict[r.user.work_id][4]==0:
                        rank_dict[r.user.work_id][4] = int(r.exam_score)
                        rank_dict[r.user.work_id][5] = rank_dict[r.user.work_id][5]+int(r.exam_score)
    
    rank_list = sorted(rank_dict.items(), key=lambda d: d[1][5], reverse=True)
    #print rank_list


    # 创建 Workbook 时，如果需要写入中文，请使用 utf-8 编码，默认是 unicode 编码。
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('比赛记录')
    ws.write(0, 0, '名次')
    ws.write(0, 1, '姓名')
    ws.write(0, 2, '部门')
    ws.write(0, 3, '车间(站)')
    ws.write(0, 4, '工号')
    ws.write(0, 5, '得分')
    excel_row = 1
    for r in rank_list:
        ws.write(excel_row, 0, excel_row)
        ws.write(excel_row, 1, r[1][0])
        ws.write(excel_row, 2, r[1][6])
        ws.write(excel_row, 3, r[1][1])
        ws.write(excel_row, 4, r[0])
        ws.write(excel_row, 5, r[1][5])
        excel_row = excel_row + 1
    # ------ 开始：这段代码可以用下面注释段替代，都是本应保存为文件格式的改成保存为数据流，以便返回前端下载
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s.xls'%filename
    wb.save(response)
    return response
    # ------ 结束
    """
    sio = StringIO.StringIO()
    wb.save(sio)
    response = HttpResponse(sio.getvalue(),content_type='application/vnd.ms-excel') 
    response['Content-Disposition'] = 'attachment; filename=test.xls'          
    return response
    """ 









'''
def showrule(request, examType, questionType):
    global question_list
    question_url = "/%s/%s/1"%(examType, questionType)
    choicequestions = list(ChoiceQuestion.objects.filter(question_type = questionType))
    multichoicequestions = list(MultiChoiceQuestion.objects.filter(question_type = questionType))
    judgequestions = list(JudgeQuestion.objects.filter(question_type = questionType))
    question_list = choicequestions + multichoicequestions + judgequestions
    shuffle(question_list)
    return render_to_response('rules.html',{'question_url':question_url})

def answerquestion(request, examType, questionType, questionNo):
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    request.session['start_time'] = time.strftime(ISOTIMEFORMAT, time.localtime())
    global question_list
    question_url = "/%s/%s/%s"%(examType, questionType, questionNo)
    next_question_url = "/%s/%s/%s"%(examType, questionType, int(questionNo)+1)
    question = question_list[int(questionNo)-1]
    return render_to_response('answer_question.html',{'question':question, 'questionNo':questionNo, 'question_url':question_url, 'next_question_url':next_question_url, 'start_time':request.session['start_time']})
'''
def ruletongyong(request):
    #return HttpResponse("Hello, world!")
    return render_to_response('ruletongyong.html',{})

def tihaizongheng(request):
    #return HttpResponse("Hello, world!")

    choicequestions = ChoiceQuestion.objects.all()
    '''
    for choicequestion in choicequestions:
        question = choicequestion.question
        questionType = choicequestion.questionType
        choice_A = choicequestion.choice_A
        choice_B = choicequestion.choice_B
        choice_C = choicequestion.choice_C
        choice_D = choicequestion.choice_D
        right_answer = choicequestion.right_answer
    '''
    multichoicequestions = MultiChoiceQuestion.objects.all()
    judgequestions = JudgeQuestion.objects.all()
    return render_to_response('tihaizongheng.html',{'choicequestions':choicequestions, 'multichoicequestion':multichoicequestions, 'judgequestions':judgequestions})

def info(request):
    #return HttpResponse("Hello, world!")

    return render_to_response('info.html',{})

def score(request):
    '''
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    request.session['end_time'] = time.strftime(ISOTIMEFORMAT, time.localtime())
    start_time = request.session.get('start_time',default=None)
    '''
    #return HttpResponse("Hello, world!")
    return render_to_response('score.html',{})

def ajax_list(request):
    question_list = []
    for i in ChoiceQuestion.objects.all():
        question = {}
        question['question'] = i.question
        question['questionType'] = i.question_type
        question['choice_A'] = i.choice_A
        question['choice_B'] = i.choice_B
        question['choice_C'] = i.choice_C
        question['choice_D'] = i.choice_D
        question['right_answer'] = i.right_answer
        print "The Question Is: %s|%s"%(i.question,question['question'])
        question_list.append(question)
    shuffle(question_list)
    return JsonResponse(question_list, safe=False)

def ajax_dict(request):
    question_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
    return JsonResponse(question_dict)

@csrf_exempt
def polly(request):
    return HttpResponse("Hello, world!")
    #print request.POST
    #return render_to_response('polly.html', {'request':request})

def formTest(request):

    return render_to_response('formTest.html', {'request':request})
    #return HttpResponse('Done!')