from rest_framework import serializers

from ...models import Article, UserArticle


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "id",
            "source_id",
            "source_name",
            "author",
            "title",
            "description",
            "content",
            "url",
            "url_to_image",
            "published_at",
        ]


class UserArticlesListSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()

    class Meta:
        model = UserArticle
        fields = [
            "id",
            "article",
            "user",
            "is_read",
        ]
