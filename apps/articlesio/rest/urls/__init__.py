from django.urls import path, include

urlpatterns = [
    path("", include("apps.articlesio.rest.urls.articles")),
]
