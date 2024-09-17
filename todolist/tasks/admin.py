from django.contrib import admin
from .models import Task, Category

# Настройка отображения модели Task в админке
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'completed', 'id')
    list_filter = ('completed', 'category', 'user')
    search_fields = ('title', 'description')
    list_editable = ('completed',)
    ordering = ('completed', 'title')
    readonly_fields = ('id',)

# Настройка отображения модели Category в админке
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)
    readonly_fields = ('id',)