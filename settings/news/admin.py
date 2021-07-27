from django.contrib import admin
from .models import Article

@admin.register(Article)
class EuroAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'image']