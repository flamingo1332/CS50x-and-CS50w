from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<str:title>", views.listing, name="listing"),
    path("watchlist/<str:username>", views.watchlist, name="watchlist"),
    path("category", views.category, name="category"),
    path("category/<str:category>", views.categoryname, name="categoryname")
]
# category/<str:categoryname> 에서 category/<str:category>로 바꿔줌
# def categoryname(reqeust, category) 에서 매치 안되서 그런듯
