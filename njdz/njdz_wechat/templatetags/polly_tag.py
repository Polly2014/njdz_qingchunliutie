 # -*- coding: utf-8 -*-

from django import template

register = template.Library()
@register.filter(name='clear')
def clear(value):
	return value.strip('\n')

@register.filter(name='toBool')
def toBool(value):
	if value:
		return 1
	else:
		return 0