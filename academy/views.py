# academy/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Sum

from .models import Courses, PaymentCheck, Teacher, Group, Student
from .serializers import (
    TeacherSerializer, GroupSerializer, StudentSerializer,
    PaymentCheckSerializer, CourseSerializer
)
from .permissions import IsAdminUser

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all().order_by('full_name')
    serializer_class = TeacherSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('full_name')
    serializer_class = StudentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        group_id = self.request.query_params.get('group_id')
        if group_id:
            queryset = queryset.filter(group_id=group_id)
        return queryset

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.select_related('teacher').all()
    serializer_class = GroupSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'], url_path='students', serializer_class=StudentSerializer)
    def students_list(self, request, pk=None):
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)

        group = self.get_object()
        students = group.students.all()
        
        page = self.paginate_queryset(students)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)

class PaymentCheckViewSet(viewsets.ModelViewSet):
    queryset = PaymentCheck.objects.select_related('student', 'teacher').all().order_by('-date')
    serializer_class = PaymentCheckSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = PaymentCheck.objects.select_related('student', 'teacher').all().order_by('-date')

        if not self.request.user.is_authenticated:
            return queryset.none()

        student_id = self.request.query_params.get('student_id')
        teacher_id = self.request.query_params.get('teacher_id')
        payment_type = self.request.query_params.get('payment_type')
        date_param = self.request.query_params.get('date')

        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)
        if payment_type:
            queryset = queryset.filter(payment_type=payment_type)
        if date_param:
            try:
                from datetime import datetime
                valid_date = datetime.strptime(date_param, "%Y-%m-%d").date()
                queryset = queryset.filter(date=valid_date)
            except ValueError:
                pass

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        total_sum = queryset.aggregate(sum_price=Sum('price'))['sum_price'] or 0.00

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = self.get_paginated_response(serializer.data).data
            response_data['total_sum'] = total_sum
            return Response(response_data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'total_sum': total_sum,
            'results': serializer.data
        })

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Courses.objects.all().order_by('name')
    serializer_class = CourseSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

