from django.shortcuts import render
from django.http import HttpResponse
from . import util
import markdown2
import random
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect


def index(request):
    return render(request, "encyclopedia/layout.html")

def greet(request, title):
    entries = util.list_entries()
    content = util.get_entry(title)
    if content == None:
        content = "Sorry!"
    clean = markdown2.markdown(content)

    return render(request, "encyclopedia/content.html",
    {
        "entries": entries, "clean": clean
    })


class NewTaskForm(forms.Form):
    title = forms.CharField(label="Title here")
    Entry = forms.CharField(widget=forms.Textarea)



def add(request):
    entries = util.list_entries()
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            newtitle = form.cleaned_data["title"]
            newguy = form.cleaned_data["Entry"]
            if newtitle in entries:
                return render(request, "encyclopedia/fail.html")
            save = util.save_entry(newtitle, newguy)
            return HttpResponseRedirect(reverse("encyclopedia:add"))
        else:
            return render(request, "encyclopedia/add.html", {
             "form": NewTaskForm(), "entries": entries
        })

    return render(request, "encyclopedia/add.html",
    {
        "entries": entries, "form": NewTaskForm()
    })


def randomy(request):
    entries = util.list_entries()
    randompage = random.choice(entries)
    return greet(request, randompage)

def edit(request, title):
    content = util.get_entry(title.strip())
    print(content)
    return render(request, "encyclopedia/chad.html", {'content': content, 'title': title})


def search(request):
    q = request.GET.get('q').strip()
    if q in util.list_entries():
        return greet(request, q)
    return render(request, "encyclopedia/searchtry.html")
