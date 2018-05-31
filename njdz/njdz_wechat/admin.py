from django.contrib import admin
from njdz_wechat.models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
	fieldsets = [('User Information',{'fields':['name', 'work_id']})]
	list_display = ('name', 'work_id')
	search_fields = ['name']

class ChoiceQuestionAdmin(admin.ModelAdmin):
	#fields = []
	fieldsets = [('Question Information',{'fields':['question', 'question_type', 'choice_A', 'choice_B', 'choice_C', 'choice_D', 'right_answer' ,'is_choice']})]
	list_display = ('question', 'question_type', 'choice_A', 'choice_B', 'choice_C', 'choice_D', 'right_answer', 'is_choice')
	list_filter = ['question_type']
	search_fields = ['question']
	#date_hidrarchy = ''

class MultiChoiceQuestionAdmin(admin.ModelAdmin):
	#fields = []
	fieldsets = [('Question Information',{'fields':['question', 'question_type', 'choice_A', 'choice_B', 'choice_C', 'choice_D', 'right_answer' ,'is_multichoice']})]
	list_display = ('question', 'question_type', 'choice_A', 'choice_B', 'choice_C', 'choice_D', 'right_answer', 'is_multichoice')
	list_filter = ['question_type']
	search_fields = ['question']

class JudgeQuestionAdmin(admin.ModelAdmin):
	#fields = []
	fieldsets = [('Question Information',{'fields':['question', 'question_type', 'right_answer', 'is_judge']})]
	list_display = ('question', 'question_type', 'right_answer', 'is_judge')
	#list_filter = ['question_type']
	search_fields = ['question']
	#date_hidrarchy = ''

class RecordAdmin(admin.ModelAdmin):
	#fields = []
	fieldsets = [
		('Record Information',{'fields':['user','department', 'work_type', 'exam_type', 'question_type', 'start_time', 'end_time', 'num_right', 'num_total', 'exam_score']}),	]
	list_display = ('id', 'user', 'department', 'work_type', 'exam_type', 'question_type', 'start_time', 'end_time', 'num_right', 'num_total', 'exam_score', 'get_year', 'get_quarter', 'get_month', 'get_week')
	#list_filter = ['question_type']
	#search_fields = ['question']

admin.site.register(Exam)
admin.site.register(QuestionType)
admin.site.register(User, UserAdmin)
admin.site.register(ChoiceQuestion, ChoiceQuestionAdmin)
admin.site.register(MultiChoiceQuestion, MultiChoiceQuestionAdmin)
admin.site.register(JudgeQuestion, JudgeQuestionAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Rank)
