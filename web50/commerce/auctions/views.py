from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import models
from django.forms import ModelForm
from .models import User, Listing, Bids, Comments, Watchlist, categories

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title','description','starting_bid','image','category']
        # widgets = { 
        #     'title': Textinput(attrs={
        #         "required: True"
        #     })
        # }


def index(request):

    listings = Listing.objects.all()
    bids = Bids.objects.all()
    return render(request, "auctions/index.html", {
        "listings" : listings, "username": request.user, "bids": bids
    })
def watchlist(request, username):
    username=request.user
    watchlists=Watchlist.objects.filter(username=username)
    bids = Bids.objects.all()
    return render(request, "auctions/watchlist.html",{
        "username": username, "watchlists": watchlists,"bids": bids
    })
def categoryname(request, category):
    if not category in dict(categories):
        # 어떤 단어가 list of tuple 안에 있는지 보기 위한 방법이다. 원리는 정확히 모르겠다. dict(listoftuple)하면 key, value 가진 dict로 바뀌는걸 이용하는거 같다.
        # if any(a[0] == 'check' for a  in alist) 이런 방법도 있음.
        return render(request, "auctions/categoryname.html",{
            "message": "Category does not exist!", "category": category, "username": request.user
        })
    else:    
        bids = Bids.objects.all()
        return render(request, "auctions/categoryname.html",{
                "category": category, "username": request.user,
                "categorylistings": Listing.objects.filter(category=category), "bids": bids
            })  

	# 할 것. bidding꽤 어렵 , comment 쉬울듯 , styling 귀찮


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image = request.FILES.get("image")
        # 시간 많이잡아먹음
        #첫번째 : models.py에서 imagefield(upload_to= " ") 하면 MEDIA ROOT 로 간다는걸 몰라서
        #두번쨰 : enctype="multipart/form-data" form에 이거 안넣으면 이미지 업로드가 안된다. 처음엔 없어도 됐는데 이유 모르겠음
        #세번쨰 : image파일을 request.POST[] 으로 받으니까 Multivaluedictkeyerror 생겨서 위처럼 바꿔줌

        category = request.POST["category"]
            
        try:
            listing = Listing(title=title, user=request.user, description=description ,starting_bid=starting_bid, image=image, category=category)
            listing.save()
    # listing model 의 id 에서 default=0으로 되어있던거 없애주니 정상적으로 id autoincrement되면서 저장됨
    # defualt값 있었을때는 id = 0 인것 하나밖에 없었다.

        except IntegrityError:
            return render(request, "auctions/create.html" ,{
                "message": "Invalid", "username": request.user
            })
        # try:
        #     listing = Listing(title=title ,description=description  ,starting_bid=starting_bid  ,image=image  , category=category)
        #     listing.save()
        # except IntegrityError:
        #     return render(request, "auctions/create.html" ,{
        #         "message": "Invalid"
        #     })
        return HttpResponseRedirect(reverse("index"))

    else:
        form = ListingForm(request.POST)
        return render(request, "auctions/create.html", {
            "form": form, "username": request.user
        })

# User model 의 primary key는 Username이다. id 아니다. 
def listing(request, title):
    username = request.user
    listing_id = Listing.objects.get(title = title).id
    # Listing.objects.filter 로 Query 찾아내고 first()기능으로 List로 바꿈.
    # first()없이 .id 하면 Queryset은 id attribute 없다는 오류 발생함

    comments = Comments.objects.filter(listing=listing_id)

    if Watchlist.objects.filter(username=username, listing=Listing.objects.get(title=title)).exists():
        watchlist = Watchlist.objects.get(username=username, listing=Listing.objects.get(title=title))
        # if문에서 exists() function 사용할떈 filter로 하고 밑에선 사용하기 쉽게 get으로
    else:
        watchlist = None


    if Bids.objects.filter(listing=listing_id).exists():
        closed = Bids.objects.filter(listing=listing_id).last().closed
        
    else:
        closed = False
       
    if Bids.objects.filter(listing=listing_id).exists():
        bids = Bids.objects.get(listing=listing_id)
        
    else:
        bids = None
       

    # .get을 쓰면 query를 거쳐서 바로 list 가져올 수 있다. .first()쓰는것보다 나은방법
    if request.method=="POST":

        # ##############
        # watchlist function
        # ##############
        if 'watchlist' in request.POST:
            if Watchlist.objects.filter(listing=listing_id, username=username).exists():  #이미 watchlist에 있다면 --> exists() 사용해야 함
                Watchlist.objects.get(listing=listing_id, username=username).delete()
                return HttpResponseRedirect(reverse("watchlist", args=[username]))
            ## save 와는 달리 delete는 이미 있는 것을 지우기 때문에 foreign key라 발생하는 특이사항이 없다. 다른경우와 같다.

            elif not Watchlist.objects.filter(listing=listing_id, username=username).exists():  # watchlist에 없다면 새로 저장
                Watchlist(listing=Listing.objects.get(title=title), username=User.objects.get(username=request.user)).save()
                return HttpResponseRedirect(reverse("watchlist", args=[username]))
            ## foreign key밖에 없는 모델이라 값 지정하는 방식으로 save 하면 문제생김
            ## 해결방법 = foreign key가 primary key로 있는 모델 objects의 리스트를 불러내면 알아서 값 적용됨. get() 하거나 .first()하거나 둘중하나.

        # ##############
        # comment function
        # ##############
        elif 'comment' in request.POST:  ## template 하나에 여러 request.post 있을 때 이렇게 하면 된다. 
            comment = request.POST["comment"]
            Comments(listing=Listing.objects.get(title=title), username=User.objects.get(username=request.user), comment=comment).save()
            return HttpResponseRedirect(reverse("listing", args=[title]))

        # ##############
        # bid function
        # ##############
        elif 'bid' in request.POST:
            bid=float(request.POST["bid"])
            # print("######################################")
            # print(type(bid))
            # print(bid)
            # print(type(Listing.objects.get(title=title).starting_bid))
            # print(Bids.objects.filter(listing=listing_id).order_by('date').last().bid)
            # print(Bids.objects.filter(listing=listing_id).exists())

            if Bids.objects.filter(listing=listing_id).exists()==False:        # 첫 bid. starting_bid보다 크면 가능
                if bid > Listing.objects.get(title=title).starting_bid:
                    Bids(listing=Listing.objects.get(title=title), username=User.objects.get(username=request.user), bid=bid).save()
                    bids = Bids.objects.get(listing=listing_id)
                    print(bids)
                    return render(request,"auctions/listing.html",{
                "listing": Listing.objects.get(title=title),
                 "username" : username, "title": title,
                "comments" : comments, "bids": bids, "closed": closed,"watchlist":watchlist
                })       
                    
                else:
                    # get()은 object에만 사용가능하다. get()한다음 .field 이렇게 사용함
                    # filter는 Queryset을 가져오고 get은 objects 가져옴
                    return render(request,"auctions/listing.html",{
                "listing": Listing.objects.get(title=title),
                "username" : username, "title": title,
                "comments" : comments, "message":"Must be greater than any other bids", "bids": bids, "closed": closed,"watchlist":watchlist})

            else:    #첫 bid 아니면..
                if bid > Bids.objects.filter(listing=listing_id).order_by('date').last().bid:
                    Bids.objects.filter(listing=Listing.objects.get(title=title)).delete()
                    Bids(listing=Listing.objects.get(title=title), username=User.objects.get(username=request.user), bid=bid).save()
                    ## 계속 Cannot resolve keyword 'user' into field. choices are ~ 에러발생했는데 User를 user로 입력해서 발생.. 오타 잘 확인

                    bids = Bids.objects.get(listing=listing_id)
                    return render(request,"auctions/listing.html",{
                "listing": Listing.objects.get(title=title),
                "username" : username, "title": title,
                "comments" : comments, "bids": bids, "closed": closed
                ,"watchlist":watchlist})
                
                else:
                    return render(request,"auctions/listing.html",{
                "listing": Listing.objects.get(title=title),
                "username" : username, "title": title,
                "comments" : comments, "message":"Must be greater than any other bids", "bids": bids, "closed": closed,"watchlist":watchlist})

        # ##############
        # bid close function
        # ##############
        elif 'close' in request.POST:
            if  not Bids.objects.filter(listing=listing_id):
                return render(request,"auctions/listing.html",{
                "listing": Listing.objects.get(title=title),
                "username" : username, "title": title,
                "comments" : comments, "message":"There are no bids", "bids": bids, "closed": closed
                ,"watchlist":watchlist})
            
            else:
                Bids.objects.filter(listing=listing_id).update(closed=True)
                closed = Bids.objects.filter(listing=listing_id).first().closed

                print(username)
                print(Bids.objects.get(listing=listing_id))
                
                print(closed)
            return render(request,"auctions/listing.html",{
                "listing": Listing.objects.get(title=title),
                 "username" : username, "title": title,
                "comments" : comments, "bids": bids, "closed": closed
                ,"watchlist":watchlist})

    elif Watchlist.objects.filter(listing=listing_id, username=username).exists():
        return render(request,"auctions/listing.html",{
                "listing": Listing.objects.get(title=title),
                 "username" : username, "title": title,
                "comments" : comments, "bids": bids, "closed": closed
                ,"watchlist":watchlist})
    else:
        return render(request,"auctions/listing.html",{
                "listing": Listing.objects.get(title=title),
                 "username" : username, "title": title, 
                "comments" : comments, "bids": bids, "closed": closed
                ,"watchlist":watchlist})



def category(request):
    # print(categories)
    # print(Listing.objects.all())
    return render(request, "auctions/category.html",{
            "categories": categories, "username": request.user
        })
