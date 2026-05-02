from django.shortcuts import render
from .models import Post


def post_list(request):
    posts = Post.objects.filter(
        is_published=True,
        rate__gt=5
    )

    return render(request, 'posts/post_list.html', {
        'posts': posts
    })