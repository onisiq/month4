from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm, PostForm, RegisterForm
from .models import Post


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = RegisterForm()

    return render(request, 'blog/register.html', {'form': form})


def category_create(request):
    next_url = request.POST.get('next') or request.GET.get('next')

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            if next_url == 'post_create':
                return redirect('post_create')
            return redirect('post_list')
    else:
        form = CategoryForm()

    return render(request, 'blog/category_form.html', {
        'form': form,
        'next_url': next_url,
    })


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    return render(request, 'blog/post_confirm_delete.html', {'post': post})


def post_list(request):
    posts = Post.objects.select_related('category').filter(is_published=True, rate__gte=5)
    return render(request, 'blog/post_list.html', {'posts': posts})


def create_post(request):

    if request.method == 'POST':

        form = PostForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('home')

    else:

        form = PostForm()

    return render(request, 'create_post.html', {'form': form})
