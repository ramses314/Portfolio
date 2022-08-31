from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

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
            return render(request, 'account/home.html')
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

    return render(request, 'posts/post_deyail.html', context=context)