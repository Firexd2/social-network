def online(request):
    if request.user.is_authenticated:
        user = request.user
        user.save()
    return {}
