 # -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "njdz.settings")

import django
if django.VERSION >= (1, 7):
    django.setup()

def main():
    from njdz_wechat.models import User
    f = open('data_userinfo.txt')
    user_list = f.readlines()
    for u in user_list:
        u_name, u_work_id = u.split('\t')
        u_work_id = u_work_id.strip(' ').strip('\n').strip(' ')

        tag = 5-len(u_work_id)

        u_work_id = "%s%s"%('0'*tag, u_work_id)

        print "%s\t%s"%(u_name, u_work_id)

        #q, t, a, b, c, d, r = question.split('\t')
        #q,t,r= question.split('\t')
        #r = r.strip(' ').strip('\n').strip(' ')
        
        #r = int(r)
        #print q,t,r
        #print q, t, a, b, c, d, r
        #ChoiceQuestion.objects.create(question=q,question_type=t,choice_A=a,choice_B=b,choice_C=c,choice_D=d,right_answer=r)
        #MultiChoiceQuestion.objects.create(question=q,question_type=t,choice_A=a,choice_B=b,choice_C=c,choice_D=d,right_answer=r)
        User.objects.create(name=u_name,work_id=u_work_id)
    f.close()
 
if __name__ == "__main__":
    main()
    print('Done!')