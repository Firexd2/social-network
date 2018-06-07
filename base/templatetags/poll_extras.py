from django import template

register = template.Library()


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
