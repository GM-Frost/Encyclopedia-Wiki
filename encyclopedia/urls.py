from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.titleName, name="title"),
    path("search", views.search, name="search"),
    path("create",views.create, name="create"),
    path("edit/<str:title>",views.edit, name="edit"),
    path("random", views.random_request, name="random")
]
