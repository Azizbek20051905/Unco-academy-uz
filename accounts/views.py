# accounts/views.py
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, UserRegistrationSerializer
from .models import User
from academy.permissions import IsAdminUser # Agar Userlarni faqat admin boshqaradigan bo'lsa
from rest_framework.decorators import action


class UserViewSet(viewsets.ReadOnlyModelViewSet): # Yoki ModelViewSet agar CRUD kerak bo'lsa
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser] # Faqat admin ko'rishi/o'zgartirishi uchun

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='me')
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

# class UserRegistrationView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (AllowAny,) # Ro'yxatdan o'tish hammaga ochiq
#     serializer_class = UserRegistrationSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save() # create metodi serializerda chaqiriladi
#         # Foydalanuvchi yaratilgandan keyin token berish mumkin
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             "user": UserSerializer(user, context=self.get_serializer_context()).data,
#             "refresh": str(refresh),
#             "access": str(refresh.access_token),
#         }, status=status.HTTP_201_CREATED)


class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# simplejwt'ning standart view'larini ham ishlatsa bo'ladi, lekin xohlasangiz o'zgartirishingiz mumkin
# class CustomTokenObtainPairView(TokenObtainPairView):
#     # pass # Agar qo'shimcha logika kerak bo'lsa