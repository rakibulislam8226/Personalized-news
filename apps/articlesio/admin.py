from django.contrib import admin

from .models import Article, UserArticle

# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "source_name",
    )
    search_fields = ("title", "source_name")
    list_filter = ("source_name",)
    ordering = ("-published_at",)
    date_hierarchy = "published_at"
    list_per_page = 50
    readonly_fields = ("slug", "published_at")


@admin.register(UserArticle)
class UserArticleAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "article",
        "is_read",
    )
    search_fields = ("user__username", "article__title")
    list_filter = ("is_read",)
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_per_page = 50
    raw_id_fields = ("user", "article")
