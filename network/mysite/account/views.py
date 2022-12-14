from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from posts.forms import CommentCreateForm
from posts.models import Post, Comment
# Create your views here.
from .forms import *
from .models import Contact


@login_required
def home(request):

    tags = list(request.user.profile.tags.names())
    form = CommentCreateForm()

    # Это проверка нужна была при разработке, в деплое можно убрать (но проверить на всякий случай)
    try:
        mydata = request.user.profile
    except:
        Profile.objects.create(user=request.user)
        mydata = request.user.profile

    posts = request.user.post_created.all().order_by('-created')
    comments = Comment.objects.filter(post__in=posts)
    followers = request.user.followers.all()
    subs = Contact.objects.filter(user_from_id=request.user.id).values_list('id')
    try:

        post_from_subs = Post.objects.all()
            # filter(user__in=[subs[0]])
        # print('lol', post_from_subs)
    except:
        post_from_subs = []

    # if request.method == 'POST':
    #     form = CommentCreateForm(request.POST)
    #     post_id = request.POST.get('postid')
    #
    #     if form.is_valid():
    #         a = form.save(commit=False)
    #         a.nickname = request.user
    #         a.post = Post.objects.get(id=post_id)
    #         a.save()
    #         form = CommentCreateForm()
    #     else:
    #         form = CommentCreateForm()
    #
    #     context = {
    #         'mydata': mydata,
    #         'posts': posts,
    #         'followers': followers,
    #         'subs': subs,
    #         'lenta': post_from_subs,
    #         'tags': tags,
    #         'form': form,
    #         'comments': comments
    #     }


    context = {
        'mydata': mydata,
        'posts': posts,
        'followers': followers,
        'subs': subs,
        'lenta': post_from_subs,
        'tags': tags,
        'form': form,
        'comments': comments,

    }

    return render(request, 'account/home.html', context=context)


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])

            new_user.save()

            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html')
    else:
        form = RegistrationForm()

    context = {
        'form' : form,
    }


    return render(request, 'account/registration.html', context=context)


@login_required
def edit(request):

    tags = request.user.profile.tags.all()

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfilEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Данные профиля успешно обновлены')
    else:
        user_form = UserEditForm(instance=request.user)
        try:
            profile_form = ProfilEditForm(instance=request.user.profile)
        except:
            Profile.objects.create(user=request.user)
            profile_form = ProfilEditForm(instance=request.user.profile)

    context = {
        'user_form' : user_form,
        'profile_form' : profile_form,
        'tags' : tags
    }

    return render(request, 'account/edit.html', context=context)


@login_required
def follower_list(request):

    users = request.user.followers.all()
    title = 'Ваши подписчики'

    context = {
        'users' : users,
         'title' : title
    }
    return render(request, 'account/follower_list.html', context = context)

@login_required
def subs_list(request):

    users = Contact.objects.filter(user_from_id=request.user.id)
    print(users)
    # users = request.user.followers.all()
    title = 'Ваши подписки'

    context = {
        'users' : users,
        'title': title
    }

    return render(request, 'account/follower_list.html', context = context)



def user_profile(request, id):

    profile_user = User.objects.get(id=id)
    posts = profile_user.post_created.all()
    comments = Comment.objects.filter(post__in=posts)
    form = CommentCreateForm()

    # if request.user in profile_user.following.all():
    try:
        a = Contact.objects.get(user_from=request.user, user_to=profile_user)
    except:
        a = None

    if a:
        sign = True
        print(111)
    else:
        sign = None
        print(222)


    context = {
        'profil_user' : profile_user,
        'sign' : sign,
        'form' : form,
        'comments' : comments
    }


    return render(request, 'account/user/user_profile.html' , context=context)


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True).exclude(id=request.user.id)

    context = {
        'users' : users
    }
    return render(request, 'account/user_list.html', context=context)


@login_required
@require_POST
def do_follow(request):

    follow_id = request.POST.get('id')
    action = request.POST.get('action')
    print(999, follow_id, action)
    profile_user = User.objects.get(id=follow_id)

    try:
        a = Contact.objects.get(user_from=request.user, user_to=profile_user)
    except:
        a = None

    if a:
        sign = True
    else:
        sign = None

    if follow_id and action:
        try:
            profile_user = User.objects.get(id=follow_id)
            if action == 'sign':
                Contact.objects.get_or_create(user_from=request.user, user_to=profile_user)
                print('sub', 33)
            else:
                Contact.objects.filter(user_from=request.user, user_to=profile_user).delete()
                print('unsub', 33)
            return JsonResponse({'status': 'ok', 'sign' : sign})
        except:
            pass
    return JsonResponse({'status': 'ok', 'sign' : sign})




    context = {
        'profil_user': profile_user,
        'sign': sign,
    }

    return render(request, 'account/user/user_profile.html', context=context)



# def user_profil_lenta(request)

