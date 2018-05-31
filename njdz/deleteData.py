 # -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "njdz.settings")

import django
if django.VERSION >= (1, 7):
    django.setup()





def main():
    from njdz_wechat.models import ChoiceQuestion, MultiChoiceQuestion, JudgeQuestion
    while MultiChoiceQuestion.objects.count():
		MultiChoiceQuestion.objects.all()[0].delete()
    while ChoiceQuestion.objects.count():
		ChoiceQuestion.objects.all()[0].delete()
 
if __name__ == "__main__":
    main()
    print('Done!')
	
