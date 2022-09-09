from distutils.log import error
import random
from tkinter import Widget
from django.shortcuts import render

from markdown2 import markdown

from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util


error_entry = "This requested page was not found 😔"
entries = util.list_entries()


# creating form class

class NewTitleForm(forms.Form):
    title = forms.CharField(label="New Wiki Title", max_length=20, widget=forms.TextInput(attrs = {'class':'form-control col-md-8 col-lg-8','required': True}))
    contents = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control col-md-8 col-lg-8','required': True}))

class EditForm(forms.Form):
    editcontents = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control col-md-8 col-lg-8'}))
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def titleName(request, title):

    if util.get_entry(title):
        get_entry = markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html",{
            "title":title,
            "body":get_entry,
            "success":True
        })
    else:
        return render(request, "encyclopedia/entry.html",{
            "title":"Request Error!",
            "error_query":"We Couldn't find your Query: ",
            "query":title,
            "body":error_entry,
            "success":False
        })


def search(request):

    query = request.GET.get('q').lower()
    similar_entries = []
    
    for entry in entries:
        entry = entry.lower()
        if query == entry:
            return render(request, "encyclopedia/entry.html",{
            "title":query,
            "body": markdown(util.get_entry(query)),
            "success":True
            })
            
        if query in entry:
            similar_entries.append(entry)
    
    return render(request, "encyclopedia/search.html",{
                    "query": query,
                    "match":similar_entries,
                    "failed":error_entry
                })        

def create(request):
    if request.method == "POST":
        form = NewTitleForm(request.POST)

        if form.is_valid():

            title = form.cleaned_data["title"]
            contents = form.cleaned_data["contents"]

            if title not in entries:

                entry = util.save_entry(title,contents)
                new_entry = markdown(util.get_entry(title))

                return HttpResponseRedirect(reverse('encyclopedia:title', args=[title]))
            
            else:

                return render(request,'encyclopedia/entry.html',{

                    "title": "Error !!!",
                    "error_query":"We Couldn't Create New Wiki: ",
                    "body": "The Given file name already exists in the system",
                    "query": title,
                    "success":False

                })
        else:
            return render(request, 'encyclopedia/create.html',{
                'form':form
            })

    return render(request, "encyclopedia/create.html",{
        "form": NewTitleForm
    })


def edit(request,title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["editcontents"]
            util.save_entry(title,content)
            body = markdown(util.get_entry(title))
          
            return render(request, "encyclopedia/entry.html", {
                "title": title, 
                "body": body,
                "success": True
            })
    else:
        body = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            'title':title,
            'form': EditForm(initial={'editcontents':body})
        })

def random_request(request):
    ran_entry = random.choice(list(entries))
    ran_body = markdown(util.get_entry(ran_entry))

    return render(request, "encyclopedia/entry.html",{
        'title':ran_entry,
        'body':ran_body,
        'success':True
    })


