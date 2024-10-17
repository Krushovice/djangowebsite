from django.urls import path

from . import views

app_name = "post"

urlpatterns = [
    path("", views.PostListView.as_view(), name="index"),
    path(
        "<int:pk>/",
        views.PostDetailView.as_view(),
        name="detail",
    ),
    path("create/", views.CreatePostView.as_view(), name="create"),
    path("<int:pk>/share/", views.PostEmailView.as_view(), name="share"),
]
