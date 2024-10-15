from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post


# Create your views here.
def index(request):
    posts_list = Post.published.all()
    paginator = Paginator(posts_list, 5)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.get_page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        "posts/index.html",
        {"posts": posts},
    )


def post_detail(
    request,
    year,
    month,
    day,
    post,
):
    post = get_object_or_404(
        Post,
        slug=post,
        status=Post.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(
        request,
        "posts/post_detail.html",
        {"post": post},
    )
