from django.contrib import admin
from .models import Plant, Image, Comment, PlantTag, PlantTagCategory


@admin.register(PlantTagCategory)
class PlantTagCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'emoji', 'color']
    search_fields = ['name']


@admin.register(PlantTag)
class PlantTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_category_emoji', 'get_category_color']
    search_fields = ['name']
    list_filter = ['category']
    
    def get_category_emoji(self, obj):
        return obj.category.emoji if obj.category else ''
    get_category_emoji.short_description = 'Emoji'
    
    def get_category_color(self, obj):
        return obj.category.color if obj.category else ''
    get_category_color.short_description = 'Color'


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

