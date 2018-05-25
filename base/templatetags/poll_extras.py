from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime
register = template.Library()

# @register.filter
# @stringfilter
# def multiply(value, arg):
#     return int(value) * int(arg)


# @register.filter
# @stringfilter
# def get_other_user(users, my_user):
#     return [user for user in users.split(',') if user != my_user][0]
