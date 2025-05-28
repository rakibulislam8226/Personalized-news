from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from ...models import User
from ..serializers.auth import (
    UserProfileDetailSerializer,
    UserRegistrationListSerializer,
)


class UserRegistrationListView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationListSerializer
    queryset = User.objects.all()
    http_method_names = ["post"]


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileDetailSerializer
    http_method_names = ["get", "put", "patch"]

    def get_object(self):
        user = self.request.user
        if not user.is_authenticated:
            return Response(
                {"message": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return user


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"refresh": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT
            )
        except TokenError:
            return Response(
                {"message": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )
