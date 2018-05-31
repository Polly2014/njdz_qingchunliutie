 # -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "njdz.settings")

import django
if django.VERSION >= (1, 7):
    django.setup()





def main():
    from njdz_wechat.models import Record
    records = Record.objects.all()
    records_bak = Record.objects.all()

#     r = records[1]
#           
#     for i in range(5):
#         p = Record(user=r.user, department=r.department, work_type=r.work_type,
#     exam_type=r.exam_type, question_type=r.question_type, start_time=r.start_time,
#     end_time=r.end_time, num_right=r.num_right, num_total=r.num_total,
#     exam_score=r.exam_score)
#         p.save()




    for r in records:
        rcds = records_bak.filter(user=r.user, department=r.department, work_type=r.work_type,
exam_type=r.exam_type, question_type=r.question_type, start_time=r.start_time, num_right=r.num_right, num_total=r.num_total,
exam_score=r.exam_score)
        num = rcds.count()
        while num > 1:
            print "There are %s item: %s"%(num,rcds[0])
            try:
                rcds[1].delete()
                print "delete item"
            except:
                print "Finished same items delete!"
                break
        else:
            print "Only one item: %s"%rcds


    '''	
    while MultiChoiceQuestion.objects.count():
		MultiChoiceQuestion.objects.all()[0].delete()
    while ChoiceQuestion.objects.count():
		ChoiceQuestion.objects.all()[0].delete()
 	'''

if __name__ == "__main__":
    main()
    print('Done!')
	
