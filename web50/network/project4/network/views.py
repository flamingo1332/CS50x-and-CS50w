import json
from django.core.serializers import serialize
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import models
from django.forms import ModelForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django import template
from django.contrib.auth.decorators import login_required

from .models import User, Post, Comment, Like, Follow


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['username', 'content']


# register = template.Library()
# # html template에서 variable value 바꿀 수 있게 해주는 기능
# @register.simple_tag
# def update_value(value):
#     return value
# register.filter('update_value', update_value)

def index(request):
    username = request.user
    if request.method == "POST":
        if "post" in request.POST:
            content = request.POST['content']
            post = Post(username=username, content=content)
            post.save()
            return HttpResponseRedirect(reverse("index"))
        
        elif "like" in request.POST:
            post_id = request.POST['like']
            print(post_id)
            post = Post.objects.get(id=post_id)
            print(post.liker.all())
            print(request.user.pk)
            if post.liker.filter(pk=request.user.pk).exists():
                # pk는 primary key를 말한다. 현재 유저의 username 말고 primary key인 id로 찾아내는 것
                # username으로 찾으면 안찾아짐
                # 이렇게 하면 쉬운데 javascript이용해서 하려니 너무 어렵다...
                post.liker.remove(request.user)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                post.liker.add(request.user)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

                # request.META.get('HTTP_REFERER')를 사용하면 현재 template에서 벗어나지 않는다. reverse index/html하면
                # like 기능 후에 index로 보내져서 문제 생겼음
            
            # return render(request, "network/index.html")

    #  pagination 페이지 만들기 기본 틀이라고 보면 된다.
    else:
        postform = PostForm(request.POST)
        # reverse order
        posts = Post.objects.all().order_by('-date')

        # print(posts.first())
        # print(posts.first().liker.all())
        # manytomanyfield 사용하면 이렇게 쉽다. 이거 몰라서 하루넘게날린듯
        
        page = request.GET.get('page', 1)

        paginator = Paginator(posts, 10)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
     

        return render(request, "network/index.html", {
            "postform" : postform, "posts": posts, 'user':username
        })

def profile(request, username):
    user = request.user
    print(user)
    print(username)
    if request.method == 'POST':
        if 'follow' in request.POST:
            Follow(followedby=user, followingto=username).save()
            return HttpResponseRedirect(reverse('profile', args=(username)))
        elif 'unfollow' in request.POST:
            Follow.objects.get(followedby=user, followingto=username).delete()
            return HttpResponseRedirect(reverse('profile', args=(username)))
    
    else:
        # print(username)
        postform = PostForm(request.POST)
        profile = User.objects.get(username=username)
        posts = Post.objects.filter(username__username=username).order_by('-date')
        # model에 username이라는 이름으로 foreign key 넣어놨는데 적용안되는듯
        # username__username으로 해야 제대로 된다. username= 하면 User model 의 primarykey인 id 요구함.
        
        # profile pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(posts, 10)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        followers = Follow.objects.filter(followingto=username)
        followings = Follow.objects.filter(followedby=username)
        num_followers = len(Follow.objects.filter(followingto=username))
        num_followings = len(Follow.objects.filter(followedby=username))
        
        if Follow.objects.filter(followedby=user, followingto=username).exists():
            followed=True
        else:
            followed=False
        return render(request, "network/profile.html",{
            "profile": profile, "user":user, 'posts': posts,
            'followers': followers, 'followings': followings, "num_followers":num_followers,"num_followings":num_followings,
            'followed': followed, 'user' : user, "postform" : postform, 'username' : username
        })


# 두개의 model 이용해서 crosscheck?하는 느낌인데 복잡해보였는데 어쩌다 됨
@login_required
def following(request, username):
    user = request.user 
    followings = Follow.objects.filter(followedby=username).values_list('followingto')
    # username으로 filter한다음에 .value_list로 한 column데이터만 추출

    # print(followings)
    posts = Post.objects.filter(username__username__in=followings)
    # filter에서 __in 사용하여 followings 리스트 안에 있다면 ~ 가능
    # print(posts)
    postform = PostForm(request.POST)
    # profile pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, "network/following.html",{
        'posts':posts,"user" : user, "postform" : postform

    })



# csrf 면제
@csrf_exempt
def edit(request, id):
    try:
        post= Post.objects.get(username__username=request.user, id=id)
    except Post.DoesNotExist:
        return JsonResponse({"error":"Post does not exist"}, status=404)

    if request.method=="GET":
        post= Post.objects.filter(username__username=request.user, id=id)
        return JsonResponse(post.serialize())

    elif request.method =="PUT":
        data = json.loads(request.body)
        # content 바꿔주기
        if data.get("content") is not None:
            post.content = data["content"]
            post.save()
        return HttpResponse(status=204)
    

    else:
        return JsonResponse({"error": "GET or PUT request required."}, status=400)



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
