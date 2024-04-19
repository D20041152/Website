from django.db import models
from django.urls import reverse

class Author(models.Model):
    surname = models.CharField(max_length=80, verbose_name="Фамилия")
    name = models.CharField(max_length=80, verbose_name="Имя")
    patronymic = models.CharField(max_length=80, verbose_name="Отчество", blank=True)


    def __str__(self):
        return f"{self.surname} {self.name[0]}. {self.patronymic[0]}."
    

    class Meta:
        ordering=["surname"]
        verbose_name = "Автор"
        verbose_name_plural = "Авторы" 


class Book(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название")
    slug = models.SlugField(max_length=150, unique_for_date="created")
    author = models.ManyToManyField(to=Author, verbose_name="Автор", related_name="books")
    image = models.ImageField(upload_to="books_images", blank=True, null=True, verbose_name="Изображение")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=["title"]
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        indexes=[
            models.Index(fields=["title"])
        ]

    def get_absolute_url(self):
        return reverse("book:book_detail", args=[
            self.slug,
        ])
    
