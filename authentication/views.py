from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import User
from .serializers import (
    UserSignupSerializer,
    UserSigninSerializer,
    UserProfileSerializer,
)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


# Signup View
@api_view(["POST"])
def signup(request):
    serializer = UserSignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Signin View
@api_view(["POST"])
def signin(request):
    serializer = UserSigninSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data["user_email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, user_email=email, password=password)

        if user:
            user_data = UserProfileSerializer(user).data
            print('user_data.....', user_data)
            tokens = get_tokens_for_user(user)
            response_data = {
                "access": tokens["access"],
                "refresh": tokens["refresh"],
                "user": user_data["user_id"]
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Signout View (Blacklist refresh token)
@api_view(["POST"])
# @permission_classes([permissions.IsAuthenticated])
def signout(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Signed out successfully"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Profile View
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def profile(request):
    user = request.user
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)
