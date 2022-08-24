from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import random
from markdown2 import Markdown
from . import util
import encyclopedia


markdowner = Markdown()

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)

def index(request):
    form = SearchForm()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "form": form
    })

def entry(request, title):
     # checking if particular page is present or not
     flag = util.get_entry(title)
     if flag is None:
        form = SearchForm()
        # showing the error page
        content = "the page is not available"
        return render(request, "encyclopedia/error.html", {"form": form, "content": content})
     else:
        form = SearchForm()
        mdcontent = util.get_entry(title)
        #converting markdown content into html
        htmlcontent = markdowner.convert(mdcontent)
        return render(request, "encyclopedia/entry.html", {"title": title, "content": htmlcontent, "form": form})
        
    

