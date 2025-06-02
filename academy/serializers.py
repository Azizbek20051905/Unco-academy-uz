# academy/serializers.py
from rest_framework import serializers
from .models import Courses, PaymentCheck, Teacher, Group, Student

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            'id', 'full_name', 'subject', 'work_days', 'phone', 'experience',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class StudentSerializer(serializers.ModelSerializer):
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        source='group',
        allow_null=True,
        required=False,
        write_only=True
    )

    class Meta:
        model = Student
        fields = [
            'id', 'full_name', 'group', 'group_id', 'phone', 'birth_day',
            'father_name', 'father_number', 'mother_name', 'mother_number',
            'school_name', 'school_class', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'group']

class MinimalTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'full_name', 'subject']

class GroupSerializer(serializers.ModelSerializer):
    teacher_details = MinimalTeacherSerializer(source='teacher', read_only=True)
    teacher = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(),
        allow_null=True,
        required=False,
        write_only=True
    )

    class Meta:
        model = Group
        fields = [
            'id', 'group_name', 'course_name', 'lesson_days', 'start_time', 'end_time',
            'teacher', 'teacher_details', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'teacher_details']

class PaymentCheckSerializer(serializers.ModelSerializer):
    student_details = StudentSerializer(source='student', read_only=True)
    teacher_details = TeacherSerializer(source='teacher', read_only=True)

    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        allow_null=True,
        required=False,
        write_only=True
    )
    teacher = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(),
        write_only=True
    )

    class Meta:
        model = PaymentCheck
        fields = [
            'id',
            'student', 'student_details',
            'price',
            'payment_type',
            'teacher', 'teacher_details',
            'date',
        ]
        read_only_fields = ['id', 'date', 'student_details', 'teacher_details']

    def validate(self, data):
        if not self.instance:
            student = data.get('student')
            teacher = data.get('teacher')
            from django.utils import timezone
            current_date = timezone.now().date()
            if student and teacher:
                if PaymentCheck.objects.filter(student=student, teacher=teacher, date=current_date).exists():
                    raise serializers.ValidationError(
                        {"detail": "A payment check for this student with this teacher already exists for today."}
                    )
        return data

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = [
            'id',
            'name',
            'description',
            'course_type',
            'duration',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


