import imp
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from markdown2 import Markdown
from . import util
import random

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
     # checking if particular page is present or not
     html_content = convert_md_to_html(title)
     if html_content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist",
            "title": title
        })
     else:
        return render(request, "encyclopedia/entry.html", {
            "content": html_content,
            "title": title
        })
            
def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_md_to_html(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
               "content": html_content,
               "title": entry_search
            })
        else:
            allentries = util.list_entries()
            recommendation = []
            for entry in allentries:
                if entry_search.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendation": recommendation
            })

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/error.html",{
                "message": "entry page already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = convert_md_to_html(title)
            return render(request, "encyclopedia/entry.html",{
                "title": title,
                "content": html_content
            })

def edit(request):
    if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "content": content
        })

def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html",{
           "title": title,
            "content": html_content
        })
    
def rand(request):
    allEntries = util.list_entries()
    rand_entry = random.choice(allEntries)
    html_content = convert_md_to_html(rand_entry)
    return render(request, "encyclopedia/entry.html",{
           "title": rand_entry,
            "content": html_content
    })   