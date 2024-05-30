from django.shortcuts import get_object_or_404, render, redirect
from .forms import UserForm, SearchForm
from .models import Book, Like
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Sum
import json
from users.models import User
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import TrigramSimilarity



def library(request):
    books = Book.objects.all()
    
    context = {
        "title": "MIET books",
        "books": books,
        "header_bool": 1
    }

    return render(request, "book/index.html", context=context)


def feedback(request):
    submitbutton= request.POST.get("submit")
    firstname=''
    email=''
    comment=''
    if request.method == "POST":
        form = UserForm(request.POST or None)
        if form.is_valid():
            firstname= form.cleaned_data.get("first_name")
            email= form.cleaned_data.get("email")
            comment= form.cleaned_data.get("comments")
        url = "https://api.telegram.org/bot7079047712:AAHDhyunKU_Oe3p-5ZvVtEYZLPshFefdwO8/sendMessage"
        params={"chat_id": "1093577177", "parse_mode": "html", "text": f"{email}\n\n{firstname}:\n\n{comment}" }
        requests.get(url, params=params)
    else:
        form = UserForm()
    context = {
        "title": "Home - Авторизация",
        "form": form,
        "header_bool": 1
    }

    return render(request, 'feedback.html', context)


def book_detail(request, book):
    book = get_object_or_404(Book, 
                            slug = book)
    user_liked = book.like_set.filter(id=request.user.id).exists() if request.user.is_authenticated else False

    if book.likes.filter(id=request.user.id).exists():
        is_liked = True

    else:
        is_liked = False

    context = {
        'book': book,
        'user_liked': user_liked,
        "is_liked": is_liked,
        "header_bool": 1
    }

    return render(request, "book/bookProfile.html", context=context)

@login_required
@require_POST
@csrf_exempt
def like_dislike(request):
    user = request.user
    is_liked = None
    if not user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'You must be logged in to like.'})

    book_id = request.POST.get('id')
    action = request.POST.get('action')

    try:
        book = Book.objects.get(id=book_id)


        if action == 'like':
            book.likes.add(request.user)
            is_liked = True
        else:
            book.likes.remove(request.user)
            is_liked = False

        total_likes = book.likes.count()
        return JsonResponse({'status': 'ok', 'total_likes': total_likes, "is_liked": True})
    except Book.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Book not found.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    

def book_search(request):
    form = SearchForm()
    query = None
    results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            if query:
                results = Book.objects.annotate(similarity=TrigramSimilarity("title", query),).filter(similarity__gt=0.1).order_by("-similarity")
    return render (request, "book/search.html",
                   {"form_s": form,
                    "query": query,
                    "results": results,
                    "header_bool": 1,})
