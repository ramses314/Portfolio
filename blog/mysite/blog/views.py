from django.shortcuts import render

# Create your views here.
from .models import Post


def home(request):

    posts = Post.objects.all()
    post = Post.objects.get(pk=1)

    context = {
        'posts' : posts,
        'post' : post,
    }

    return render(request, 'blog/home.html', context=context)

def detail(request, slug):

    post = Post.objects.get(slug=slug)

    context = {
        'post' : post
    }
    return render(request, 'blog/detail.html', context=context)