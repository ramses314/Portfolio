from django.shortcuts import render

# Create your views here.


def plakat(request):

    print(1111)

    return render(request, 'chats/plakat.html')