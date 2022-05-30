import random
import markdown2
from django.shortcuts import redirect
from distutils.command.sdist import sdist
from django import forms
from django.shortcuts import render

from . import util

class CreateForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)

class EditForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'readonly':True}))
    content = forms.CharField(label="Content", widget=forms.Textarea)
# CreateForm에서 edit function 안에서만 title readonly 설정하는법을 모르겠어서 새로운 object 하나 만듬

def index(request):
    if request.method =="POST":
        # print(request.POST.get('q'))

        if util.get_entry(request.POST.get('q')):
            return render(request, "encyclopedia/title.html", {
        "title": request.POST.get('q'), "content": markdown2.markdown(util.get_entry(request.POST.get('q'))), "random" : random.choice(util.list_entries())
        })
        elif any(s for s in util.list_entries() if request.POST.get('q').lower() in s.lower()):
            matches=[s for s in util.list_entries() if request.POST.get('q').lower() in s.lower()]
            return render(request, "encyclopedia/search.html",{
                "matches": matches, "random" : random.choice(util.list_entries())
            }) 
        else:
            return render(request, "encyclopedia/error.html", {"random" : random.choice(util.list_entries())})

    else:    #if request method is "GET"
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "random" : random.choice(util.list_entries())
            })

def title(request, title):
    if util.get_entry(title):
        content = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/title.html", {
        "title": title, "content": content, "random" : random.choice(util.list_entries())
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "random" : random.choice(util.list_entries())
        })


def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if request.POST.get('delete'):
            util.delete_entry(title)
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(), "random" : random.choice(util.list_entries())
            })
        elif not form.is_valid():
            return render(request, "encyclopedia/error_create.html", {
                "message" : "Invalid input!", "random" : random.choice(util.list_entries())
            })
        elif request.POST.get('save'): #Create 랑 똑같이 함. save_entry가 기존파일 있으면 지우고 새로 저장하기 때문에 문제없음
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect(f'/wiki/{title}')
            # redirect /wiki/css 하면 8000/wiki/css로 보내고 wiki/css 하면 8000/wiki/edit/wiki/css 로 보냄. 
            # f'/wiki/{title} 으로 해결됨   
    else:
        form = EditForm(initial = {'title': title, 'content': util.get_entry(title)})
# 나머지는 content attribute 없다는 오류 생기거나 variable data 설정 못하거나 문제 생기므로 이 방법이 가장 단순
        return render(request, "encyclopedia/edit.html" , {
            "title" : title, "content" : util.get_entry(title),
            "form" : form, "random" : random.choice(util.list_entries())
        })


def create(request):
    if request.method == "POST":
        # form = CreateForm(request.POST.get('title'), request.POST.get('content')) 이렇게 하니까 안되고 request.POST로 해야됨. value name따라 알아서 찾아가는듯 하다.
        form = CreateForm(request.POST)

        if util.get_entry(request.POST.get('title')):   #해당 entry 이미 존재하면
            return render(request, "encyclopedia/error_create.html", {
                "message" : "Entry already exists!", "random" : random.choice(util.list_entries())
            })
        # elif not form.is_valid(): 
        #     return render(request, "encyclopedia.error_create.html", {
        #         "message" : "Invalid input!"
        #     })
        elif form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect(f'/wiki/{title}')
    else:
        return render(request, "encyclopedia/create.html",{
        "form": CreateForm(), "random" : random.choice(util.list_entries())
    })

    ## random page 기능
    ## layout에 있기 때문에 title, create, edit 모든 페이지에 random을 넣어줘야 오류 안생김, 더 좋은방법이 있을 거 같은데 모르겠음
    ## index에만 있기 때문에 문제생기는 거였다. 
    # 그리고 페이지 새로고침 해도 random.choice()변하지 않는 이유는  x = random.choice() 이런식으로 했기 때문에