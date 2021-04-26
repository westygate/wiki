from django.shortcuts import render
from django  import forms
from . import util
import markdown2
from django.urls import reverse
from django.http import HttpResponseRedirect
import random

class CreateForm(forms.Form):
    title=forms.CharField(label=False,widget=forms.TextInput(attrs={'placeholder': 'Title', "size":100, "id": 'text'}))
    content= forms.CharField(label=False,widget=forms.Textarea(
        attrs={"rows":3, "cols":1, "placeholder": "Enter you text here"}))
    
class EditForm(forms.Form):
    content= forms.CharField(label=False,widget=forms.Textarea(
        attrs={"rows":3, "cols":1, "placeholder": "Enter you text here"}))
    

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
    entry=util.get_entry(title)
    if entry==None:
        entry='Requested page was not found'
    return render(request, "encyclopedia/page.html", {
        "entry": markdown2.markdown(entry), "title": title.capitalize()
        })
    
def search(request):
    entries=util.list_entries()
    if request.method=="POST":
        text=request.POST.__getitem__('q')
        lst = [x.lower() for x in entries] 
        if text.lower() in lst:
            return HttpResponseRedirect(reverse('page', args=(text,)))
        else:
            result=[]
            for entry in entries:
                if text.lower() in entry.lower():
                    result.append(entry)
            return render(request, "encyclopedia/search.html", {
        "entries": result
    })
        
def create(request):
    if request.method=="POST":
        form=CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            entries=util.list_entries()
            lst = [x.lower() for x in entries] 
            if title.lower() in lst:
                return render(request, "encyclopedia/create.html",{
        "form": None
            })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('page', args=(title,)))
        else:
            return render(request, "encyclopedia/create.html",{
        "form": form
            })
    return render(request, "encyclopedia/create.html",{
        "form": CreateForm()
        })
 
def edit(request,title):
    content=util.get_entry(title)
    if request.method=="POST":
        form=EditForm(request.POST, initial={"content":content})
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title,content)
            return HttpResponseRedirect(reverse('page', args=(title,)))
        else:
            return render(request, "encyclopedia/edit.html",{
        "form": form, "title":title
            })
    return render(request, "encyclopedia/edit.html",{
        "form": EditForm(initial={"content":content}), "title":title
        })

def rand(request):
     return HttpResponseRedirect(reverse('page', args=(random.choice(util.list_entries()),)))
