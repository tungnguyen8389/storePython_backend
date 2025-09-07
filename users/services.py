from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

def get_all_users():
    return User.objects.all()

def get_user_by_id(user_id):
    return User.objects.filter(id=user_id).first()

def create_user(validated_data):
    return User.objects.create_user(**validated_data)

def update_user(user, validated_data):
    for attr, value in validated_data.items():
        if attr == "password":
            user.set_password(value)
        else:
            setattr(user, attr, value)
    user.save()
    return user

def delete_user(user):
    user.delete()
    
class AuthService:
    @staticmethod
    def authenticate_user(username, password):
        user = authenticate(username=username, password=password)
        if not user:
            return None
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
