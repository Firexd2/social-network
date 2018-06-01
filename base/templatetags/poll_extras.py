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

@register.filter
def previous(all_messages, counter):
    try:
        current_message = all_messages[counter]
        prev_message = all_messages[counter - 1]

        difference_time = current_message.datetime - prev_message.datetime

        if current_message.author.id == prev_message.author.id and difference_time.seconds < 300:
            return False
        else:
            return True
    except AssertionError:
        return True
