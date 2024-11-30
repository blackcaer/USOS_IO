from django.db import models
from django.contrib.auth.models import AbstractUser


# Categories
class CategoryUserStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CategoryStudentGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CategoryGradeValue(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class CategoryAttendanceStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Main models

class User(AbstractUser):
    name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    birth_date = models.DateField()
    sex = models.CharField(max_length=10, choices=[("M", "Male"), ("F", "Female")])
    status = models.ForeignKey(CategoryUserStatus, on_delete=models.SET_NULL, null=True)    #TODO maybe default to something?
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    photo_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Parent: {self.user}"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groups = models.ManyToManyField("StudentGroup")
    parents = models.ManyToManyField(Parent, related_name="children")

    def __str__(self):
        return f"Student: {self.user}"


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groups = models.ManyToManyField("StudentGroup", blank=True)

    def __str__(self):
        return f"Teacher: {self.user}"


class StudentGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(CategoryStudentGroup, on_delete=models.SET_NULL, null=True)
    level = models.IntegerField()
    section = models.CharField(max_length=50, blank=True, null=True)
    students = models.ManyToManyField(Student, related_name="student_groups")

    def __str__(self):
        return self.name


class SchoolSubject(models.Model):
    subject_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_mandatory = models.BooleanField(default=False)
    student_group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject_name


class Grade(models.Model):
    value = models.ForeignKey(CategoryGradeValue, on_delete=models.SET_NULL, null=True)
    weight = models.IntegerField()
    timestamp = models.DateField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade_column = models.ForeignKey("GradeColumn", on_delete=models.CASCADE)
    count_to_avg = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.value} for {self.student}"


class GradeColumn(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    default_weight = models.IntegerField()
    school_subject = models.ForeignKey(SchoolSubject, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Attendance(models.Model):
    status = models.ForeignKey(CategoryAttendanceStatus, on_delete=models.SET_NULL, null=True)
    meeting = models.ForeignKey("Meeting", on_delete=models.CASCADE)
    absence_reason = models.CharField(max_length=1023, blank=True, null=True)

    def __str__(self):
        return f"{self.status} for meeting {self.meeting}"


class Meeting(models.Model):
    topic = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    school_subject = models.ForeignKey(SchoolSubject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.topic
