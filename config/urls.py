from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # apps
    path("api/v1/", include("apps.articlesio.rest.urls")),
    path("api/v1/", include("apps.authio.rest.urls")),
]
