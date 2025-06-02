# academy/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, PaymentCheckViewSet, TeacherViewSet, GroupViewSet, StudentViewSet

router = DefaultRouter()
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'payment-checks', PaymentCheckViewSet, basename='paymentcheck') # Yangi URL
router.register(r'courses', CourseViewSet, basename='course') # Yangi URL

urlpatterns = [
    path('', include(router.urls)),
]