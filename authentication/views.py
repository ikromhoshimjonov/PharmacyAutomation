from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication.models import User
from authentication.serializers import UserModelSerializer, CustomTokenObtainPairSerializer, \
    UserParametersModelSerializers
from django.contrib.auth import authenticate, login, logout


@extend_schema(tags=["register"])
class RegisterCreateOperator(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


@extend_schema(tags=["login"])
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"detail": "Email yoki parol noto'g'ri"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.user

        if user:
            login(request, user)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


@extend_schema(tags=["login"])
class CustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(tags=["user parameters"])
class UserParameters(ModelViewSet):
    serializer_class = UserParametersModelSerializers
    authentication_classes = [JWTAuthentication,SessionAuthentication]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

@csrf_exempt
def admin_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            return JsonResponse({
                "success": True,
                "is_superuser": user.is_superuser
            })

    return JsonResponse({"success": False})


def site_logout(request):
        logout(request)
        return redirect('/login/')


class MeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
            u = request.user
            return Response({
                "id": u.id,
                "email": u.email,
                "is_superuser":u.is_superuser,
                "first_name": getattr(u, "first_name", ""),
                "last_name": getattr(u, "last_name", ""),
                "role":getattr(u, "role", ""),
            })
