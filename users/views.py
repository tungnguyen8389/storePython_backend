from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .serializers import RegisterSerializer, UserSerializer, UserAdminSerializer
from .services import AuthService
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from .services import get_all_users, get_user_by_id, create_user, update_user, delete_user
from users.permissions import IsAdmin
from rest_framework import status

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Đăng ký thành công", "user": UserSerializer(user).data})
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        tokens = AuthService.authenticate_user(username, password)
        if not tokens:
            return Response({"error": "Sai tài khoản hoặc mật khẩu"}, status=400)
        return Response(tokens)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"detail": "Refresh token required."}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data)

class UserListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = get_all_users()
        serializer = UserAdminSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserAdminSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserAdminSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, pk):
        user = get_user_by_id(pk)
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserAdminSerializer(user).data)

    def put(self, request, pk):
        user = get_user_by_id(pk)
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserAdminSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            updated_user = serializer.save()
            return Response(UserAdminSerializer(updated_user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_user_by_id(pk)
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        delete_user(user)
        return Response(status=status.HTTP_204_NO_CONTENT)