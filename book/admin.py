from django.contrib import admin
from .models import Author, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display=["id", "surname", "name", "patronymic"]
    search_fields = ["surname", "name", "id"]
    ordering=["surname", "name"]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=["id", "title","slug", "created"]
    search_fields =["title", "id"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author",)
    ordering = ["title"]

