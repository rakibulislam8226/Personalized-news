from django.urls import path

from ..views.auth import (
    UserRegistrationListView,
    UserProfileDetailView,
    LogoutAPIView,
)

urlpatterns = [
    path("register/", UserRegistrationListView.as_view(), name="user-registration"),
    path("logout/", LogoutAPIView.as_view(), name="user-logout"),
    path("profile/", UserProfileDetailView.as_view(), name="user-profile"),
]
