from django.urls import path, include

urlpatterns = [
    path("articles/", include("apps.articlesio.rest.urls.articles")),
]
