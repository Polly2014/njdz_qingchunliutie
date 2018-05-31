 # -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "njdz.settings")

import django
if django.VERSION >= (1, 7):
    django.setup()


def main():
    from njdz_wechat.models import Record
    records = Record.objects.all()

    for r in records:
        if r.num_total==300:
            exam_time = (r.end_time - r.start_time).seconds
            print exam_time
            if exam_time<60:
                r.delete()
                print 'less than 1s:%s'%r.user.name

if __name__ == "__main__":
    main()
    print('Done!')
