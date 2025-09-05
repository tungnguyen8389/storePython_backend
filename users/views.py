from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, UserSerializer
from .services import AuthService
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test

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

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data)
