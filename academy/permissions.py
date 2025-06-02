# academy/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS
from academy.models import PaymentCheck
from accounts.models import User # User modelini import qilish
from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Faqat 'admin' rolidagi foydalanuvchilarga ruxsat beradi.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'

class IsTeacherUser(BasePermission):
    """
    Faqat 'teacher' rolidagi foydalanuvchilarga ruxsat beradi.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == User.Role.TEACHER)

class IsStudentUser(BasePermission):
    """
    Faqat 'student' rolidagi foydalanuvchilarga ruxsat beradi.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == User.Role.STUDENT)

class IsOwnerOrAdmin(BasePermission):
    """
    Obyekt egasi yoki 'admin' rolidagi foydalanuvchilarga ruxsat beradi.
    GET, HEAD, OPTIONS so'rovlariga barcha autentifikatsiyadan o'tganlarga ruxsat.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS: # O'qish uchun
            return request.user.is_authenticated

        # Yozish (PUT, PATCH, DELETE) uchun
        # Agar obyektda 'user' atributi bo'lsa va u request.user ga teng bo'lsa
        if hasattr(obj, 'user') and obj.user == request.user:
            return True
        # Agar obyektda 'teacher' atributi bo'lsa, 'teacher' da 'user' atributi bo'lsa va u request.user ga teng bo'lsa
        if hasattr(obj, 'teacher') and obj.teacher and hasattr(obj.teacher, 'user') and obj.teacher.user == request.user:
            return True
        
        return request.user.role == User.Role.ADMIN

class IsTeacherOfGroupOrAdmin(BasePermission):
    """
    Guruh o'qituvchisi yoki adminlarga ruxsat.
    """
    def has_object_permission(self, request, view, obj): # obj bu Group instansi
        if request.user.role == User.Role.ADMIN:
            return True
        if request.user.role == User.Role.TEACHER and obj.teacher and hasattr(obj.teacher, 'user') and obj.teacher.user == request.user:
            return True
        return False

# StudentViewSet uchun qo'shimcha permission
class IsTeacherOfStudentOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj): # obj bu Student instansi
        # Agar Student obyektining user atributi request.user ga teng bo'lsa (o'zini ko'rishi/tahrirlashi)
        if hasattr(obj, 'user') and obj.user == request.user:
            return True
        if request.user.role == User.Role.ADMIN:
            return True
        if request.user.role == User.Role.TEACHER:
            # O'qituvchining profilini olish
            teacher_profile = getattr(request.user, 'teacher_profile', None)
            # Agar o'qituvchi profili mavjud bo'lsa VA student guruhga biriktirilgan bo'lsa VA guruhning o'qituvchisi shu o'qituvchi bo'lsa
            if teacher_profile and obj.group and obj.group.teacher == teacher_profile:
                return True
        return False

class IsPaymentOwnerOrAdmin(BasePermission):
    """
    Allows access only to admin users or to the teacher who created the payment.
    """
    def has_object_permission(self, request, view, obj: PaymentCheck):
        if request.user.role == User.Role.ADMIN:
            return True
        if request.user.role == User.Role.TEACHER:
            teacher_profile = getattr(request.user, 'teacher_profile', None)
            # obj.teacher bu PaymentCheck dagi teacher fieldi
            return teacher_profile is not None and obj.teacher == teacher_profile
        return False