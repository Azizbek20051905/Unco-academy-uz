# accounts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogoutView, UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user') # Agar UserViewSet kerak bo'lsa

urlpatterns = [
    path('', include(router.urls)), # Agar UserViewSet ishlatilsa
    # path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
]