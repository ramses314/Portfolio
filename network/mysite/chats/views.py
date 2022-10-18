from django.shortcuts import render

# Create your views here.


def plakat(request):
    return render(request, 'chats/plakat.html')