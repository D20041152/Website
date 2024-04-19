from django.contrib import admin

from users.models import User

# Register your models here.
@admin.register(User)
class BookAdmin(admin.ModelAdmin):
    list_display=["id", "email", "username", "password"]
