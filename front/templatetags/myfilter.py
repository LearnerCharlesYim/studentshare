# -*- coding:utf-8 -*-
# @Time   :2021/5/10 16:05
# @Author :CharlesYim
# @File   :myfilter.py
from django import template

register = template.Library()
@register.filter(name='get_range')
def get_range(value):
    return range(value)