from django.urls import path

from book import views

app_name="book"

urlpatterns = [
    path("", views.library, name="index"),
    path("feedback", views.feedback, name="feedback"),
    path("<slug:book>/", views.book_detail, name="book_detail"),
    path('like_dislike', views.like_dislike, name='like_dislike'),
]


