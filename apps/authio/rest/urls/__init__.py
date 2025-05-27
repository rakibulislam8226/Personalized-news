from django.urls import path, include

urlpatterns = [
    path("", include("apps.authio.rest.urls.auth")),
]
