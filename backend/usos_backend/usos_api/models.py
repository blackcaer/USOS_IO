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
"""class CategoryStudentGroup(models.Model):
    # Unique, stable code
    code = models.CharField(max_length=30, unique=True)
    # Human friendly name
    name = models.CharField(max_length=63, blank=True)

    def __str__(self):
        return f"{self.code} {self.name}"
"""


class CategoryGradeValue(models.Model):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=63, blank=True)

    def __str__(self):
        return f"{self.code} {self.name}"


class CategoryAttendanceStatus(models.Model):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=63, blank=True)

    def __str__(self):
        return f"{self.code} {self.name}"

# Main models:

# Helper model for User


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
    """ Username is user's unique identifier (inherited from AbstractUser) """
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('parent', 'Parent'),
        ('teacher', 'Teacher'),
    ]
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, editable=False,)
    first_name = models.CharField(max_length=255, default="first_name")
    last_name = models.CharField(max_length=255, default="last_name")
    email = models.EmailField(unique=True, default="email@example.com")
    birth_date = models.DateField(default=datetime.date(2010, 1, 1))
    sex = models.CharField(max_length=15, choices=[(
        "M", "Male"), ("F", "Female")], default="M")
    status = models.CharField(max_length=31, choices=[(
        "A", "Active"), ("U", "Inactive")], default="A")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    photo_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name} role:{self.role}"


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    parents = models.ManyToManyField(
        "Parent", related_name="children", blank=True)
    
    class Meta:
        ordering = ['user']
        
    def __str__(self):
        return f"Student: {self.user.username}"


class Teacher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        ordering = ['user']
        
    def __str__(self):
        return f"Teacher: {self.user.username}"


class Parent(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        ordering = ['user']
        
    def __str__(self):
        return f"Parent: {self.user.username}"


class StudentGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    #category = models.ForeignKey(
    #    CategoryStudentGroup, on_delete=models.SET_NULL, null=True)
    level = models.IntegerField()
    section = models.CharField(max_length=50, blank=True, null=True)
    students = models.ManyToManyField(Student, related_name="student_groups")

    def __str__(self):
        return self.name


class SchoolSubject(models.Model):
    subject_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    is_mandatory = models.BooleanField(default=False)
    student_group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject_name} for {self.student_group}"


class Grade(models.Model):
    value = models.ForeignKey(
        CategoryGradeValue, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade_column = models.ForeignKey("GradeColumn", on_delete=models.CASCADE)
    count_to_avg = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.value} for {self.student}"


class GradeColumn(models.Model):
    title = models.CharField(max_length=255)
    weight = models.IntegerField(default=1)
    description = models.TextField(blank=True, default="")
    school_subject = models.ForeignKey(SchoolSubject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} for {self.school_subject}"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),    # Obecny
        ('A', 'Absent'),     # Nieobecny
        ('L', 'Late'),       # Spóźniony
        ('E', 'Excused'),    # Usprawiedliwiony
    ]

    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='attendances')
    meeting = models.ForeignKey('Meeting', on_delete=models.CASCADE, related_name='attendances')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    absence_reason = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('meeting', 'student') 

    def __str__(self):
        return f"{self.student.user.username} - {self.status} at {self.meeting.title}"


class ConsentTemplate(models.Model):
    author = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    end_date = models.DateField()
    students = models.ManyToManyField(
        Student, related_name="consent_templates")

    def time_to_end(self):
        return (self.end_date - timezone.now().date()).days

    def is_active(self):
        return timezone.now().date() <= self.end_date

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
    DAYS_OF_WEEK = [
        (1, "Poniedziałek"),
        (2, "Wtorek"),
        (3, "Środa"),
        (4, "Czwartek"),
        (5, "Piątek")
    ]
    LESSON_SLOTS = [
    (1, "08:00 - 08:45"),
    (2, "08:55 - 09:40"),
    (3, "09:50 - 10:35"),
    (4, "10:45 - 11:30"),
    (5, "11:40 - 12:25"),
    (6, "12:45 - 13:30"),
    (7, "13:40 - 14:25"),
    (8, "14:35 - 15:20")
    ]

    PLACES = [
    (10, "Sala 10"),
    (11, "Sala 11"),
    (12, "Sala 12"),
    (13, "Sala 13"),
    (14, "Sala 14"),
    (15, "Sala 15"),
    (16, "Sala 16"),
    (17, "Sala 17"),
    (18, "Sala 18"),
    (19, "Sala 19"),
    (20, "Sala 20")
]

    description = models.TextField(blank=True, default="")
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    slot = models.IntegerField(choices=LESSON_SLOTS)  # "slots" for lessons
    teacher = models.ForeignKey(
        'Teacher', on_delete=models.CASCADE, related_name='scheduled_meetings'
    )
    school_subject = models.ForeignKey(
        'SchoolSubject', on_delete=models.CASCADE
    )
    place = models.IntegerField(choices=PLACES)
    
    class Meta:
        unique_together = [['day_of_week', 'slot', 'school_subject'],['day_of_week', 'slot', 'teacher'],['day_of_week', 'slot', 'place']]
        
    def __str__(self):
        return f"{self.school_subject.subject_name} (Day: {self.day_of_week}, Slot: {self.slot} Place: {self.place})"


class Meeting(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    start_time = models.DateTimeField()
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    school_subject = models.ForeignKey(
        'SchoolSubject', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Message(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    sender = models.ForeignKey(
        User, related_name='sent_messages', on_delete=models.CASCADE)
    recipients = models.ManyToManyField(User, related_name='received_messages')

    def __str__(self):
        return f"{self.title} (from {self.sender})"
