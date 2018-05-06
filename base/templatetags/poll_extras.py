from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime
register = template.Library()


# def get_string_last_activity(last, now):
#     if last.date() == now.date():
#         return 'Заходил сегодня в %s:%s' % (last.hours, last.minute)
#     elif (now.date() - last.date()).days == 1:
#         return 'Заходил вчера в %s:%s' % (last.hours, last.minute)
#     else:
#         return 'Заходил %s в %s:%s' % (last.date, last.hours, last.minute)
#
#
# @register.filter
# @stringfilter
# def last_online(last):
#     now = datetime.now()
#     last = datetime.strptime(last, "%d/%m/%y %H:%M")
#     difference = (now - last).seconds
#     if difference > 600:
#         return get_string_last_activity(last, now)
#     else:
#         return 'online'
