from django.shortcuts import render, get_object_or_404


from .models import Post


# Create your views here.
def index(request):
    posts = Post.published.all()
    return render(
        request,
        "posts/index.html",
        {"posts": posts},
    )


def post_detail(request, pk):
    post = get_object_or_404(
        Post,
        pk=pk,
        status=Post.Status.PUBLISHED,
    )
    return render(
        request,
        "posts/post_detail.html",
        {"post": post},
    )
