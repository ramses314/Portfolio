from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .forms import *


# Create your views here.

@login_required
def create_post(request):

    if request.method == 'POST':
        form = PostCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_items = form.save(commit=False)
            new_items.user = request.user
            new_items.save()
            return redirect('/')
    else:
        form = PostCreateForm()

    context = {
        'form' : form,
    }
    return render(request, 'posts/create_post.html', context=context)


def post_detail(request, id):

    post = Post.objects.get(id=id)

    context = {
        'post' : post,
    }

    return render(request, 'posts/post_detail.html', context=context)


@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    loop = request.POST.get('loop')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status' : 'ok', 'loop' : loop})
        except:
            pass
    return JsonResponse({'status' : 'ok', 'loop' : loop})

@login_required
@require_POST
def save_comment(request):
    post_id = request.POST.get('id')
    query = request.POST.get('query')
    user = request.POST.get('user')

    if len(query) == 0:
        return JsonResponse({'status' : 'no'})

    form = CommentCreateForm()
    a = form.save(commit=False)
    a.nickname = request.user
    a.post = Post.objects.get(id=post_id)
    a.body = query
    a.save()
    time = a.created

    return JsonResponse({'status' : 'ok', 'query' : query, 'time' : time})
