from django.shortcuts import redirect, render

import markdown, random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, article):
    # error message for wrong url TO DO
    md = markdown.Markdown()
    text = util.get_entry(article)
    f = open("entries/" + article + ".md", "r")
    title = f.readline()
    f.close()
    title = title.strip("#")
    title = title.replace(" ","") 
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

def mod(request, title):
    if title == "new":
        new = True
    else:
        new = False
    if request.method == "POST":
        if new == False:
            content = request.POST.get("content")
            f = open("entries/" + title + ".md", "w")
            f.write(content)
            f.close()
            return redirect( "wiki", title)
        else:
            article = request.POST.get("title")
            articlename = article.replace(" ","")
            entries = util.list_entries()
            if article in entries:
                pass
            content = request.POST.get("content")
            f = open("entries/" + articlename + ".md", "w")
            f.write("# " + article + "\n" + content)
            f.close()
            print(article)
            return redirect( "wiki", articlename)
    else:
        if new == False:
            entries = util.list_entries()
            title = title.rstrip("\n")
            if title in entries:
                article = util.get_entry(title)
                return render(request, "encyclopedia/mod.html",{
                    "title" : title,
                    "article" : article
                })
        else:
            print(new)
            return render(request, "encyclopedia/mod.html",{
                "new" : new,
                "title" : "new"
            })