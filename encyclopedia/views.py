from django.shortcuts import render
from django.http import HttpResponseNotFound
from django import forms
from random import choice
from . import util
import markdown


class CreateEntryForm(forms.Form):
    new_title = forms.CharField(label='Title')
    new_definition = forms.CharField(widget=forms.Textarea, label='Markdown definition')
    

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })

# Returns the title's corresponding markdown content translated to HTML
def show_entry(request, title):
    entry = util.get_entry(title)
    # if entry is not existing, sends to error page
    if entry is None:
        return HttpResponseNotFound(render(request, "encyclopedia/error.html", {
            "error": "Error: Entry not found",
        }))
    else:
        return render(request, "encyclopedia/entry.html", {
            'title': title,
            'entry': md(entry),
        })

# Converts markdown syntax text into HTML content 
def md(markdown_content):
    html_content = markdown.markdown(markdown_content)
    return html_content

# Enable search function to allow user to get pages results matching the input
def search(request):
    if request.method == "POST":
        query = request.POST.get("q").lower()
        matches = []
        entry = util.get_entry(query)
        if entry is not None:
            return render(request, "encyclopedia/entry.html", {
            'title': query,
            'entry': md(entry),
            })
        else:
            for match in util.list_entries():
                if query.lower() in match.lower():
                    matches.append(match)
            return render(request, "encyclopedia/results.html",{
                "results" : matches,
                "query": query
                })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })
        
# Create new entry into encyclopedia
def create(request):
    if request.method == "POST":
        form = CreateEntryForm(request.POST)
        if form.is_valid():
                title = form.cleaned_data["new_title"]
                description = form.cleaned_data["new_definition"]
                if title.lower() in (_.lower() for _ in util.list_entries()):
                    return HttpResponseNotFound(render(request, "encyclopedia/error.html", {
                        "error": "Error: This entry already exists.",
                    }))
                else: 
                    content = f'# {title} \n {description}'
                    util.save_entry(title, content)
                    return render(request, "encyclopedia/entry.html", {
                        'title': title,
                        'entry': md(util.get_entry(title)),
                    })
        else:
            return render(request,"create.html", {
                "form": form
            })
    return render(request, "encyclopedia/create.html", {
        "form": CreateEntryForm()
    })


def edit(request, title):
    if request.method =="GET":
        if util.get_entry(title) == None:
                return HttpResponseNotFound(render(request, "encyclopedia/error.html", {
                    "error": "Error: This entry does not exist. Please create it first.",
                }))
        else:
            return render(request, "encyclopedia/edit.html", {
                'title': title,
                'entry':util.get_entry(title),
        })
    if request.method == "POST":
        content = request.POST["current"]
        if content:
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                        'title': title,
                        'entry': md(util.get_entry(title)),
                    })
        
def random(request):
    random_page = choice(util.list_entries())
    return render(request, "encyclopedia/entry.html", {
        "title": random_page,
        "entry": md(util.get_entry(random_page)),
    })

def error(request, exception): 
    return render(request, "error.html")