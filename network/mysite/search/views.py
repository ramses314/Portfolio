from django.contrib.auth.models import User
from django.shortcuts import render
from taggit.models import Tag

from account.models import Profile
from .forms import SearchForm


# Create your views here.


def users_search(request):

    users = User.objects.all().exclude(id=request.user.id)
    reserve_users = []

    if request.method == 'POST':
        form = SearchForm(request.POST)


        if form.is_valid():
            data = form.cleaned_data
            nickname = data['nickname']
            gender = data['gender']
            similar = data['similar']
            similar_tags = list(request.user.profile.tags.names())

            if nickname:
                users = User.objects.filter(username=nickname)
            if gender:
                users = User.objects.filter(username__in=list(users), profile__gender=gender)
            if similar:
                users = User.objects.filter(username__in=list(users), profile__tags__name__in=similar_tags)

            if len(users) == 0:
                reserve_users = User.objects.all().exclude(id=request.user.id)

            context = {
                    'form': form,
                     'users' : users,
                    'reserve_users' : reserve_users
                    }
            return render(request, 'search/user_search.html', context=context)

    else:
        form = SearchForm()

    context = {
        'users' : users,
        'form' : form,
        'reserve_users': reserve_users,
    }



    return render(request, 'search/user_search.html', context=context)