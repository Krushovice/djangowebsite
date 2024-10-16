from django.urls import path

from . import views

app_name = "user"

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<int:pk>", views.get_profile, name="profile"),
]
