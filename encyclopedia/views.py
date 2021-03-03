from django.shortcuts import render
import markdown

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
    

