from django.shortcuts import get_object_or_404, render, redirect
from .forms import UserForm
from .models import Book, Like
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Sum
import json
from users.models import User
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required



def library(request):
    books = Book.objects.all()
    
    context = {
        "title": "MIET books",
        "books": books
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
    }

    return render(request, 'feedback.html', context)
    
def book_detail(request, book):
    book = get_object_or_404(Book, 
                            slug = book)
    return render(request, "book/bookProfile.html", {"book": book})


def book_detail_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    user_liked = book.like_set.filter(id=request.user.id).exists() if request.user.is_authenticated else False
    context = {
        'book': book,
        'user_liked': user_liked,
    }
    return render(request, 'bookProfile.html', context)

def is_liked(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'You must be logged in to like.'})
    book_id = request.POST.get('id')
    action = request.POST.get('action')

    try:
        book = Book.objects.get(id=book_id)
        if user in book.like_set.all:
            print(True)
            return True
        else:
            return False        
        #return book.like_set.filter(id=request.user.id).exists() if request.user.is_authenticated else False
    except Book.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Book not found.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
@require_POST
@csrf_exempt
def like_dislike(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'You must be logged in to like.'})

    book_id = request.POST.get('id')
    action = request.POST.get('action')

    try:
        book = Book.objects.get(id=book_id)
        if action == 'like':
            book.likes.add(request.user)
            #Like.objects.get_or_create(user=user, book=book)
        else:
            book.likes.remove(request.user)
            #Like.objects.filter(user=user, book=book).delete()

        total_likes = book.likes.count()
        lis = (u for u in str(book.likes))

        return JsonResponse({'status': 'ok', 'total_likes': total_likes})
    except Book.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Book not found.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
