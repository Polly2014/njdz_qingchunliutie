 # -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "njdz.settings")

import django
if django.VERSION >= (1, 7):
    django.setup()





def main():
    from njdz_wechat.models import ChoiceQuestion, MultiChoiceQuestion, JudgeQuestion
    f = open('data_judge.txt')
    question_list = f.readlines()
    for question in question_list:
        #q, t, a, b, c, d, r = question.split('\t')
        q,t,r= question.split('\t')
        r = r.strip(' ').strip('\n').strip(' ')
        
        #r = int(r)
        print q,t,r
        #print q, t, a, b, c, d, r
        #ChoiceQuestion.objects.create(question=q,question_type=t,choice_A=a,choice_B=b,choice_C=c,choice_D=d,right_answer=r)
        #MultiChoiceQuestion.objects.create(question=q,question_type=t,choice_A=a,choice_B=b,choice_C=c,choice_D=d,right_answer=r)
        JudgeQuestion.objects.create(question=q,question_type=t,right_answer=r)
    f.close()
 
if __name__ == "__main__":
    main()
    print('Done!')