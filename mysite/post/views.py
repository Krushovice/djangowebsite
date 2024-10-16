from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post

from .forms import EmailPostForm


# Create your views here.
def index(request):
    posts_list = Post.published.all()
    paginator = Paginator(posts_list, 1)
    page_number = request.GET.get("page", 3)
    try:
        posts = paginator.get_page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        "post/index.html",
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
        "post/post_detail.html",
        {"post": post},
    )


def post_share(request, post_pk):
    # Retrieve post by id
    post = get_object_or_404(
        Post,
        id=post_pk,
        status=Post.Status.PUBLISHED,
    )
    if request.method == "POST":
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
    else:
        form = EmailPostForm()
    return render(
        request,
        "post/share.html",
        {
            "post": post,
            "form": form,
        },
    )
