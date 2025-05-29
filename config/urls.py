from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [
    # admin
    path("admin/", admin.site.urls),
    # rest_framework
    path("api-auth/", include("rest_framework.urls")),
    # drf-spectacular
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # simple-jwt
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # apps
    path("api/v1/", include("apps.articlesio.rest.urls")),
    path("api/v1/", include("apps.authio.rest.urls")),
]

urlpatterns += (
    re_path(
        r"^(?!api|media|static/).*", TemplateView.as_view(template_name="app.html")
    ),
)
