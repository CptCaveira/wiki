from django.shortcuts import redirect, render

import markdown, random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, article):
    md = markdown.Markdown()
    text = util.get_entry(article)
    split = text.split()
    title = split[1]  
    return render(request, "encyclopedia/wiki.html", {
        "text": md.convert(text),
        "title" : title
    }) 
    

def search(request):
    if request.method == "POST":
        entries = util.list_entries()
        query = request.POST
        if query["q"].lower() in (entry.lower() for entry in entries):
            md = markdown.Markdown()
            text = util.get_entry(query["q"])
            split = text.split()
            title = split[1]  
            return redirect( "wiki", title)
        elif query["q"].lower() not in (entry.lower() for entry in entries):
            matches = []
            for entry in entries:
                if query["q"].lower() in entry.lower():
                    matches.append(entry)
            return render(request, "encyclopedia/search.html",{
                "matches" : matches
            })

def randompage(request):
    entries = util.list_entries()
    randomnum = random.randrange(len(entries))
    title = entries[randomnum]
    return redirect( "wiki", title)
