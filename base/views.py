from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from user.models import User


@csrf_exempt
def general_search(request):
    users = User.objects.all()
    request = request.POST['request'].lower()

    response = dict()

    for user in users:
        if request in user.last_name.lower() or request in user.first_name.lower():
            response[user.get_full_name()] = {'url': user.get_absolute_url(),
                                              'avatar': user.settings.avatar_thumbnail.url}

    return JsonResponse({'response': response})
