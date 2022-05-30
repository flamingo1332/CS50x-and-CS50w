from django.urls import path

from . import views

app_name="wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("create", views.create, name="create"),
    path("wiki/edit/<str:title>", views.edit, name="edit")
]
