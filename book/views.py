from django.shortcuts import get_object_or_404, render
from .forms import UserForm
from book.models import Book
import requests


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
    context = {"book": book}
    return render(request, "book/bookProfile.html", context=context)

