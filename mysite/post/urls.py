from django.urls import path

from . import views

app_name = "post"

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "tag/<slug:tag_slug>/",
        views.index,
        name="index_by_tag",
    ),
    path(
        "<int:pk>/",
        views.post_detail,
        name="detail",
    ),
    path(
        "<int:pk>/comment/",
        views.post_comment_create,
        name="comment",
    ),
    path(
        "<int:pk>/share/",
        views.PostEmailView.as_view(),
        name="share",
    ),
    path(
        "create/",
        views.CreatePostView.as_view(),
        name="create",
    ),
]
