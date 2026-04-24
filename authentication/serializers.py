from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import Serializer, ModelSerializer
from authentication.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "email", "password"

    def validate_password(self, value):
        password = make_password(value)
        return password

User = get_user_model()
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def get_token(cls, user):
        token = super().get_token(user)

        token["is_superuser"] = user.is_superuser
        token["email"] = user.email

        return token

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise AuthenticationFailed("Email va password kerak")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed("Login xato. Email/parolni tekshiring.")

        if not user.check_password(password):
            raise AuthenticationFailed("Login xato. Email/parolni tekshiring.")

        # --- MANA BU QATORNI QO'SHING ---
        # Djangoga ushbu foydalanuvchi standart backend orqali kirganini bildiramiz
        user.backend = 'django.contrib.auth.backends.ModelBackend'

        self.user = user  # View uchun saqlab qo'yamiz

        refresh = self.get_token(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }


class UserParametersModelSerializers(ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True
    )

    class Meta:
        model = User
        fields = "id","email", "password" , "first_name" , "role" ,"image","phone_number","last_name"

    def validate_password(self, value):
        password = make_password(value)
        return password
