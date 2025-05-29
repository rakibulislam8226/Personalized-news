from django.db import models
from django.contrib.auth import get_user_model

from autoslug import AutoSlugField

from apps.common.models import BaseModelWithUID

User = get_user_model()


class Article(BaseModelWithUID):
    source_id = models.CharField(max_length=255, null=True, blank=True)
    source_name = models.CharField(max_length=255)
    slug = AutoSlugField(
        populate_from="title",
        null=True,
        blank=True,
        max_length=255,
    )
    author = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=512)
    description = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    url = models.URLField(unique=True)
    url_to_image = models.URLField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title


class UserArticle(BaseModelWithUID):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="user_articles"
    )
    is_read = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "article")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} → {self.article.title}"
