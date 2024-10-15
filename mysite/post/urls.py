from django.urls import path

from . import views

app_name = "post"

urlpatterns = [
    path("", views.index, name="posts_index"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.post_detail,
        name="post_detail",
    ),
]
