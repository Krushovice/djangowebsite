from audioop import reverse

from django.shortcuts import render, get_object_or_404

from django.views.decorators.http import require_POST

from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    FormView,
)

from django.core.mail import send_mail

from .models import Post, Comment

from .forms import EmailPostForm, PostForm, CommentForm


# Create your views here.
# def index(request):
#     posts_list = Post.published.all()
#     paginator = Paginator(posts_list, 1)
#     page_number = request.GET.get("page", 3)
#     try:
#         posts = paginator.get_page(page_number)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     return render(
#         request,
#         "post/index.html",
#         {"posts": posts},
#     )


class PostListView(ListView):
    model = Post
    template_name = "post/index.html"
    context_object_name = "posts"
    paginate_by = 5


class CreatePostView(CreateView):
    model = Post
    form_class = PostForm


def post_detail(request, pk: int):
    post = get_object_or_404(
        Post,
        pk=pk,
        status=Post.Status.PUBLISHED,
    )
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    return render(
        request,
        "post/detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
        },
    )


class PostEmailView(FormView):
    template_name = "post/email_share.html"
    form_class = EmailPostForm
    success_url = "/thanks"

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get("pk"))
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (
                f"{cd['name']} ({cd['email']}) " f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd["to"]],
            )
            sent = True
            return render(
                request,
                self.template_name,
                {
                    "post": post,
                    "form": form,
                    "sent": sent,
                },
            )

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get("pk"))
        sent = False
        return render(
            request,
            self.template_name,
            {
                "post": post,
                "form": self.form_class,
                "sent": sent,
            },
        )


# class CommentCreateView(CreateView):
#     template_name = "post/comment.html"
#     model = Comment
#     form_class = CommentForm


@require_POST
def post_comment_create(request, pk: int):
    post = get_object_or_404(
        Post,
        pk=pk,
        status=Post.Status.PUBLISHED,
    )
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request,
        "post/comment.html",
        context={
            "post": post,
            "form": form,
            "comment": comment,
        },
    )
