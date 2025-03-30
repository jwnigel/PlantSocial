from django.contrib import admin
from .models import Plant, Image, Comment

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ['genus', 'species', 'common_name', 'family', 'zones', 'light', 'moisture', 'form', 'form_size', 'description']
    list_filter = ['common_name', 'light', 'form', 'moisture']
    search_fields = ['genus', 'species', 'common_name', 'description']
    prepopulated_fields = {'slug': ('genus', 'species')}
    ordering = ['common_name']
    inlines = [ImageInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'plant', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['user_profile.user.username', 'body']

