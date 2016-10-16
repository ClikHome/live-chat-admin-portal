from django.shortcuts import render


def index(request):
    return render(request, 'portal/channels/list.html', {})
