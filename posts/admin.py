from django.contrib import admin
from posts.models import Post, Category, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "rate")
    search_fields = ("title", "content")
    list_filter = ("category", "tags")
    ordering = ("-created_at",)
    list_editable = ("author",)

admin.site.register(Category)
admin.site.register(Tag)