import os

from celery import shared_task
from django.contrib.auth import get_user_model
from newsapi import NewsApiClient

from .models import Article, UserArticle

User = get_user_model()
newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY", "news-api-key"))


@shared_task
def fetch_news_for_all_users():
    user_ids = list(User.objects.filter(is_active=True).values_list("id", flat=True))

    chunk_size = 10
    for i in range(0, len(user_ids), chunk_size):
        chunk = user_ids[i : i + chunk_size]
        fetch_news_for_user_batch.delay(chunk)


@shared_task
def fetch_news_for_user_batch(user_ids):
    users = User.objects.filter(id__in=user_ids)

    for user in users:
        query = ",".join(user.keywords) if user.keywords else None
        sources = ",".join(user.sources) if user.sources else None
        country = user.countries[0] if user.countries else None

        try:
            # NOTE: country and sources are not executed together in the API call
            if sources:
                top_headlines = newsapi.get_top_headlines(
                    q=query,
                    sources=sources,
                    language="en",
                    page_size=10,
                )
            elif country:
                top_headlines = newsapi.get_top_headlines(
                    q=query,
                    country=country,
                    language="en",
                    page_size=10,
                )
            else:
                top_headlines = newsapi.get_top_headlines(
                    q=query,
                    language="en",
                    page_size=10,
                )
        except Exception as e:
            print(f"Error for {user.email}: {e}")
            continue

        articles_data = top_headlines.get("articles", [])
        if not articles_data:
            continue

        urls = [item["url"] for item in articles_data]

        existing_articles = Article.objects.filter(url__in=urls)
        existing_urls = set(existing_articles.values_list("url", flat=True))

        articles_to_create = []

        for item in articles_data:
            if item["url"] not in existing_urls:
                articles_to_create.append(
                    Article(
                        url=item["url"],
                        source_id=item["source"].get("id"),
                        source_name=item["source"].get("name"),
                        author=item.get("author"),
                        title=item["title"],
                        description=item.get("description"),
                        content=item.get("content"),
                        url_to_image=item.get("urlToImage"),
                        published_at=item.get("publishedAt"),
                    )
                )
        Article.objects.bulk_create(articles_to_create)

        all_articles = Article.objects.filter(url__in=urls)
        article_map = {article.url: article for article in all_articles}

        existing_user_articles = UserArticle.objects.filter(
            user=user, article__in=all_articles
        )
        existing_article_ids = set(
            existing_user_articles.values_list("article_id", flat=True)
        )

        user_articles_to_create = []

        for item in articles_data:
            article = article_map[item["url"]]
            if article.id not in existing_article_ids:
                user_articles_to_create.append(UserArticle(user=user, article=article))

        UserArticle.objects.bulk_create(user_articles_to_create)
