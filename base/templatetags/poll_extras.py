from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime
register = template.Library()

# @register.filter
# @stringfilter
# def multiply(value, arg):
#     return int(value) * int(arg)

