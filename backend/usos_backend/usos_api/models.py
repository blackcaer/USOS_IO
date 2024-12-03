from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
import datetime
from django.core.exceptions import ValidationError
from datetime import timedelta

def validate_duration(value):
    if value > timedelta(minutes=120):
        raise ValidationError('Duration cannot exceed 120 minutes.')


    
# Categories
class CategoryStudentGroup(models.Model):
    code = models.CharField(max_length=30, unique=True)     # Unique, stable code
    name = models.CharField(max_length=63,blank=True)       # Human friendly name
    
    def __str__(self):
        return f"{self.code} {self.name}"


class CategoryGradeValue(models.Model):
    code = models.CharField(max_length=30, unique=True)  
    name = models.CharField(max_length=63,blank=True)

    def __str__(self):
        return f"{self.code} {self.name}"


class CategoryAttendanceStatus(models.Model):
    code = models.CharField(max_length=30, unique=True)  
    name = models.CharField(max_length=63,blank=True)

    def __str__(self):
        return f"{self.code} {self.name}"

# Main models

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    """ 
    Username is user's identifier
    """
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('parent', 'Parent'),
        ('teacher', 'Teacher'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=255, default="name_example")
    last_name = models.CharField(max_length=255, default="Lname_example")
    email = models.EmailField(unique=True, default="example@example.com")
    birth_date = models.DateField(default=datetime.date(2010, 1, 1))
    sex = models.CharField(max_length=15, choices=[("M", "Male"), ("F", "Female")],default="M")
    status = models.CharField(max_length=31, choices=[("A", "Active"), ("U", "Inactive")],default="A")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    photo_url = models.URLField(blank=True, null=True)

    objects = UserManager()

    def __str__(self):
        return f"{self.username}({self.id}): {self.first_name} {self.last_name}"


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    groups = models.ManyToManyField('StudentGroup', blank=True)

    def __str__(self):
        return f"Teacher: {self.user.username}"

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"Parent: {self.user.username}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    groups = models.ManyToManyField('StudentGroup', blank=True)
    parents = models.ManyToManyField(Parent, related_name="children", blank=True)

    def __str__(self):
        return f"Student: {self.user.username}"


class StudentGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True,default="")
    category = models.ForeignKey(CategoryStudentGroup, on_delete=models.SET_NULL, null=True)
    level = models.IntegerField()
    section = models.CharField(max_length=50, blank=True, null=True)
    students = models.ManyToManyField(Student, related_name="student_groups")

    def __str__(self):
        return self.name


class SchoolSubject(models.Model):
    subject_name = models.CharField(max_length=255)
    description = models.TextField(blank=True,default="")
    is_mandatory = models.BooleanField(default=False)
    student_group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject_name} for {self.student_group}"


class Grade(models.Model):
    value = models.ForeignKey(CategoryGradeValue, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade_column = models.ForeignKey("GradeColumn", on_delete=models.CASCADE)
    count_to_avg = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.value} for {self.student}"


class GradeColumn(models.Model):
    title = models.CharField(max_length=255)
    weight = models.IntegerField(default=1)
    description = models.TextField(blank=True,default="")
    school_subject = models.ForeignKey(SchoolSubject, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.ForeignKey(CategoryAttendanceStatus, on_delete=models.SET_NULL, null=True)
    meeting = models.ForeignKey("Meeting", on_delete=models.CASCADE)
    absence_reason = models.TextField(blank=False, null=True)

    def __str__(self):
        return f"{self.status} for meeting {self.meeting}"


class Meeting(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    start_time = models.DateTimeField()
    duration = models.DurationField(default=timedelta(minutes=45), validators=[validate_duration])
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    school_subject = models.ForeignKey('SchoolSubject', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class ConsentTemplate(models.Model):
    author = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    start_date = models.DateField()
    end_date = models.DateField()
    recipients = models.ManyToManyField('StudentGroup')
    expiry_date = models.DateField()
    duration = models.IntegerField()

    def is_active(self):
        return (timezone.now().date() - self.creation_date).days <= self.duration

    def __str__(self):
        return f"ConsentTemplate {self.title} by {self.author} (Active: {self.is_active()})"


class ParentConsent(models.Model):
    parent_user = models.ForeignKey('Parent', on_delete=models.CASCADE)
    child_user = models.ForeignKey('Student', on_delete=models.CASCADE)
    consent = models.ForeignKey(ConsentTemplate, on_delete=models.CASCADE)
    is_consent = models.BooleanField(default=False)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Consent by {self.parent_user} for {self.child_user}"


class ScheduledMeeting(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    start_time = models.DateTimeField()
    duration = models.DurationField(default=timedelta(minutes=45), validators=[validate_duration])
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='scheduled_meetings')
    school_subject = models.ForeignKey('SchoolSubject', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Message(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipients = models.ManyToManyField(User, related_name='received_messages')

    def __str__(self):
        return f"{self.title} (from {self.sender})"