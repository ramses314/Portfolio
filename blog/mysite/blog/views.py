from django.contrib.postgres.search import SearchVector
from django.core.checks import Tags
from django.db.models import Q
from django.shortcuts import render

from taggit.models import Tag

from .forms import CommentForm, SearchForm
from .models import Post, Comment, Blogger



# Главная страница
def home(request, tag=None):

    posts = Post.objects.filter(status=True)[:12]
    posts_for_lenta = Post.objects.filter(tags__name__in=['retro'])
    news = Post.objects.filter(status=True).exclude(id__in=posts_for_lenta).order_by('?')[:6]
    tags = Tag.objects.all()

    if tag:
        posts = Post.objects.filter(tags__name__in=[f'{tag}'])

    # Для обработки формы поиска (который находиться в футере)
    form = SearchForm()
    if 'query' in request.GET:
        query = None
        results = []
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            # results = Post.objects.annotate(search=SearchVector('title', 'body')).filter(search=query)
            results = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
            return render(request, 'blog/search.html', {'form': search_form, 'query': query, 'results': results,
                                                            'tags': tags, 'search_form': search_form})
    context = {
        'posts' : posts,
        'news' : news,
        'tags' : tags,
        'tag' : tag,
        'search_form' : form,
        'post_for_lenta' : posts_for_lenta,
    }
    return render(request, 'blog/home.html', context=context)


# Для отображения статей по тегам
def collect_tag(request, tag=None):

    posts = Post.objects.all()
    tags = Tag.objects.all()

    if tag:
        posts = Post.objects.filter(tags__name__in=[f'{tag}'])

    form = SearchForm()

    if 'query' in request.GET:
        query = None
        results = []
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            # results = Post.objects.annotate(search=SearchVector('title', 'body')).filter(search=query)
            results = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
            return render(request, 'blog/search.html', {'form': search_form, 'query': query, 'results': results,
                                                            'tags': tags, 'search_form': search_form})
    context = {
        'posts' : posts,
        'tags' : tags,
        'tag' : tag,
        'search_form' : form,
    }
    return render(request, 'blog/collect_tag.html', context=context)


# Отображение отдельной взятой статьи
def detail(request, slug):

    post = Post.objects.get(slug=slug)
    comments = Comment.objects.filter(post=post).order_by('-created')
    tags = Tag.objects.all()

    mytags = post.tags.values_list('name', flat=True)
    recommendations = Post.objects.filter(tags__name__in=[mytags]).exclude(slug=slug)

    search_form = SearchForm()

    if 'query' in request.GET:
        query = None
        results = []
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            # results = Post.objects.annotate(search=SearchVector('title', 'body')).filter(search=query)
            results = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
            return render(request, 'blog/search.html', {'form': search_form, 'query': query, 'results': results,
                                                        'tags': tags, 'search_form': search_form})

    # Для сохранения комментариев
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
            # results = Post.objects.annotate(search=SearchVector('title', 'body')).filter(search=query)
            results = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))

            return render(request, 'blog/search.html', {'form': search_form, 'query': query, 'results': results,
                                                         'search_form': search_form})

    return render(request, 'blog/search.html', {'form': search_form, 'query': query, 'results': results,
                                                         'search_form': search_form})


# Вкладка "Что на ютуб?"
def tab_for_youtube(request):

    posts = Blogger.objects.all()
    search_form = SearchForm()

    if 'query' in request.GET:
        query = None
        results = []
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            results = Post.objects.annotate(search=SearchVector('title', 'body')).filter(search=query)
            results = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
            return render(request, 'blog/search.html', {'form': search_form, 'query': query, 'results': results,
                                                         'search_form': search_form})
    context = {
        'posts': posts,
        'search_form' : search_form,
    }
    return render(request, 'blog/youtube.html', context=context)