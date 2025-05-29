from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.custom_paginator import CustomPagination

from ...models import UserArticle
from ..serializers.articles import UserArticlesListSerializer


class UserArticlesListView(ListAPIView):
    serializer_class = UserArticlesListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        qs = UserArticle.objects.select_related("user").filter(user=user)
        search = self.request.query_params.get("search", None)
        source = self.request.query_params.get("source", None)
        published_after = self.request.query_params.get("published_after", None)

        if source:
            qs = qs.filter(article__source_name__icontains=source)
        if published_after:
            qs = qs.filter(article__published_at__date__gte=published_after)
        if search:
            qs = qs.filter(article__title__icontains=search)

        return qs


class UserArticlesSourcesListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        sources = UserArticle.objects.filter(user=user).values_list(
            "article__source_name", flat=True
        )
        stripped_sources = set(s.strip() for s in sources if s and s.strip())

        return Response({"sources": sorted(stripped_sources)}, status=200)
