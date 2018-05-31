 # -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "njdz.settings")

import django
import xlwt

if django.VERSION >= (1, 7):
    django.setup()





def main():
    from njdz_wechat.models import Record

    records = Record.objects.all()
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('比赛日志')
    ws.write(0, 0, '姓名')
    ws.write(0, 1, '工号')
    ws.write(0, 2, '部门')
    ws.write(0, 3, '工种')
    ws.write(0, 4, '比赛类型')
    ws.write(0, 5, '题库类型')
    ws.write(0, 6, '开始时间')
    ws.write(0, 7, '结束时间')
    ws.write(0, 8, '正确题数')
    ws.write(0, 9, '总题数')
    ws.write(0, 10, '得分')
    excel_row = 1
    for r in records:
        ws.write(excel_row, 0, r.user.name)
        ws.write(excel_row, 1, r.user.work_id)
        ws.write(excel_row, 2, r.department)
        ws.write(excel_row, 3, r.work_type)
        ws.write(excel_row, 4, r.exam_type)
        ws.write(excel_row, 5, r.question_type)
        ws.write(excel_row, 6, str(r.start_time))
        ws.write(excel_row, 7, str(r.end_time))
        ws.write(excel_row, 8, r.num_right)
        ws.write(excel_row, 9, r.num_total)
        ws.write(excel_row, 10, r.exam_score)
        excel_row = excel_row + 1
    # ------ 开始：这段代码可以用下面注释段替代，都是本应保存为文件格式的改成保存为数据流，以便返回前端下载
    wb.save('recordsHistory.xls')





 

if __name__ == "__main__":
    main()
    print('Done!')

