# academy/models.py
from django.db import models
import uuid


class Courses(models.Model):
    COURSES_CHOICES = [
        ('fan', 'Fan'),
        ('kurslar', 'Kurslar')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    course_type = models.CharField(max_length=20, choices=COURSES_CHOICES, default='fan') # Fan yoki Kurslar
    duration = models.IntegerField(help_text="Kurs davomiyligi soatlarda", blank=True, null=True) # Kurs davomiyligi soatlarda
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100)
    subject = models.ForeignKey(Courses, on_delete=models.SET_NULL, null=True, blank=True, related_name='teachers') # O'qituvchi qaysi fan bo'yicha
    work_days = models.JSONField(default=list) # Misol: ["Monday", "Wednesday"]
    phone = models.CharField(max_length=20, blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True) # Yillarda
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_name = models.CharField(max_length=50, unique=True)
    course_name = models.CharField(max_length=100)
    lesson_days = models.JSONField(default=list) # Misol: ["Tuesday", "Thursday"]
    start_time = models.TimeField()
    end_time = models.TimeField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='groups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group_name

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    phone = models.CharField(max_length=20, blank=True, null=True)
    birth_day = models.IntegerField(null=True, blank=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    father_number = models.CharField(max_length=20, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    mother_number = models.CharField(max_length=20, blank=True, null=True)
    school_name = models.CharField(max_length=150, blank=True, null=True)
    school_class = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

class PaymentCheck(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, related_name='student_payments')
    price = models.DecimalField(max_digits=10, decimal_places=2) # To'lov miqdori
    payment_type = models.CharField(max_length=50, choices=[('naqd', 'Naqd'), ('click', 'Click'), ('terminal', 'Terminal')], default='naqd')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'teacher', 'date') # Bir kunda bir talaba uchun bitta yozuv

    def __str__(self):
        student_name = self.student.full_name if self.student else "Noma'lum student"
        teacher_name = self.teacher.full_name if self.teacher else "Noma'lum o'qituvchi"
        return f"{student_name} - {teacher_name} - {self.date}"