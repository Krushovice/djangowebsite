from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from .models import CustomUser as User


# Create your views here.
def index(request):
    users_list = User.objects.all()
    paginator = Paginator(users_list, 3)
    page_number = request.GET.get("page", 1)
    try:
        users = paginator.get_page(page_number)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(
        request,
        "user/index.html",
        {"users": users},
    )


def get_profile(request, pk: int):
    user = User.objects.get(pk=pk)
    return render(
        request,
        "user/profile.html",
        context={"user": user},
    )
