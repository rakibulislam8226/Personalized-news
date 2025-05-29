from django.urls import path

from ..views.articles import UserArticlesListView, UserArticlesSourcesListView


urlpatterns = [
    path(
        "sources/",
        UserArticlesSourcesListView.as_view(),
        name="user-articles-sources-list",
    ),
    path("", UserArticlesListView.as_view(), name="user-articles-list"),
]
