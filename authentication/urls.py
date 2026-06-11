from authentication.views import RegisterCreateOperator, CustomTokenObtainPairView, CustomTokenRefreshView, admin_login, \
    site_logout, MeView
from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()

urlpatterns = [
    path("register/",RegisterCreateOperator.as_view(),name="register"),
    path("site-login/", admin_login),
    path("logout/", site_logout),
    path("api/me/", MeView.as_view(), name="me")
]

# JWT
urlpatterns += [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
