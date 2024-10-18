from audioop import reverse

from django.shortcuts import render, get_object_or_404

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


class PostDetailView(DetailView):
    model = Post


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


class CommentCreateView(CreateView):
    template_name = "post/comment.html"
    model = Comment
    form_class = CommentForm
