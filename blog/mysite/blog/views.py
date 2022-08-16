from django.contrib.postgres.search import SearchVector
from django.core.checks import Tags
from django.shortcuts import render

# Create your views here.
from taggit.models import Tag

from .forms import CommentForm, SearchForm
from .models import Post, Comment, Blogger


def home(request, tag=None):

    print(8888)

    posts = Post.objects.filter(status=True)
    posts_for_lenta = posts[:3]
    # post = Post.objects.get(pk=1)
    tags = Tag.objects.all()

    if tag:
        print(111, tag)
        posts = Post.objects.filter(tags__name__in=[f'{tag}'])

    form = SearchForm()

    if 'query' in request.GET:
        # form = SearchForm(request.GET)
        query = None
        results = []
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            results = Post.objects.annotate(
                search=SearchVector('title', 'body')).filter(search=query)
            return render(request, 'blog/search.html', {'form': search_form, 'query': query, 'results': results,
                                                            'tags': tags, 'search_form': search_form})


    context = {
        'posts' : posts,
        # 'post' : post,
        'tags' : tags,
        'tag' : tag,
        'search_form' : form,
        'post_for_lenta' : posts_for_lenta,
    }

    return render(request, 'blog/home.html', context=context)


def collect_tag(request, tag=None):

    posts = Post.objects.all()
    posts_for_lenta = posts[:3]
    # post = Post.objects.get(pk=1)
    tags = Tag.objects.all()

    if tag:
        posts = Post.objects.filter(tags__name__in=[f'{tag}'])

    form = SearchForm()

    if 'query' in request.GET:
        # form = SearchForm(request.GET)
        query = None
        results = []
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            results = Post.objects.annotate(
                search=SearchVector('title', 'body')).filter(search=query)
            return render(request, 'blog/search.html', {'form': search_form, 'query': query, 'results': results,
                                                            'tags': tags, 'search_form': search_form})


    context = {
        'posts' : posts,
        # 'post' : post,
        'tags' : tags,
        'tag' : tag,
        'search_form' : form,
        'post_for_lenta' : posts_for_lenta,
    }

    return render(request, 'blog/collect_tag.html', context=context)

def detail(request, slug):

    post = Post.objects.get(slug=slug)
    comments = Comment.objects.filter(post=post).order_by('-created')
    tags = Tag.objects.all()

    mytags = post.tags.values_list('name', flat=True)
    recommendations = Post.objects.filter(tags__name__in=[mytags]).exclude(slug=slug)



    search_form = SearchForm()

    if 'query' in request.GET:
        # form = SearchForm(request.GET)
        query = None
        results = []
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            results = Post.objects.annotate(
                search=SearchVector('title', 'body')).filter(search=query)
            return render(request, 'blog/search.html', {'form': search_form, 'query': query, 'results': results,
                                                        'tags': tags, 'search_form': search_form})


    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            a = form.save(commit=False)
            a.post = post
            a.save()
        else:
            form = CommentForm(request.POST)
    else:
        form = CommentForm()


    form = CommentForm()
    context = {
        'post' : post,
        'form' : form,
        'comments' : comments,
        'tags' : tags,
        'recommendations' : recommendations,
        'search_form' : search_form,
    }
    return render(request, 'blog/detail.html', context=context)


def search(request):

    search_form = SearchForm(request.GET)
    query = None
    results = []

    if 'query' in request.GET:

        results = []
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            results = Post.objects.annotate(
                search=SearchVector('title', 'body')).filter(search=query)
            return render(request, 'blog/search.html', {'form': search_form, 'query': query, 'results': results,
                                                         'search_form': search_form})


    return render(request, 'blog/search.html', {'form': search_form, 'query': query, 'results': results,
                                                         'search_form': search_form})


def tab_for_youtube(request):

    posts = Blogger.objects.all()
    search_form = SearchForm()

    if 'query' in request.GET:
        # form = SearchForm(request.GET)
        query = None
        results = []
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            results = Post.objects.annotate(
                search=SearchVector('title', 'body')).filter(search=query)
            return render(request, 'blog/search.html', {'form': search_form, 'query': query, 'results': results,
                                                         'search_form': search_form})

    context = {
        'posts': posts,
        'search_form' : search_form,
    }

    return render(request, 'blog/youtube.html', context=context)