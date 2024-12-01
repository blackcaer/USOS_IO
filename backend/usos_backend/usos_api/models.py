from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.timezone import now


# Categories
class CategoryUserStatus(models.Model):
    code = models.CharField(max_length=30, unique=True)     # Unique, stable code
    name = models.CharField(max_length=63,blank=True)                  # Human friendly name

    def __str__(self):
        return f"{self.code} {self.name}"


class CategoryStudentGroup(models.Model):
    code = models.CharField(max_length=30, unique=True)  
    name = models.CharField(max_length=63,blank=True)
    
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

class User(AbstractUser):
    """ 
    Username is user's identifier
    """
    first_name = models.CharField(max_length=255, default="name_example")
    last_name = models.CharField(max_length=255, default="Lname_example")
    email = models.EmailField(unique=True, default="example@example.com")  # Przykładowy adres e-mail
    birth_date = models.DateField(default="2010-01-01")  # Przykładowa data urodzenia
    sex = models.CharField(max_length=15, choices=[("M", "Male"), ("F", "Female")],default="M")
    status = models.CharField(max_length=31, choices=[("A", "Active"), ("U", "Unactive")],default="A")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    photo_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} {self.username}: {self.first_name} {self.last_name}"    


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Parent: {self.user}"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groups = models.ManyToManyField("StudentGroup", blank=True)
    parents = models.ManyToManyField(Parent, related_name="children", blank=True)

    def __str__(self):
        return f"{self.id} Student: {self.user}"


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groups = models.ManyToManyField("StudentGroup", blank=True)

    def __str__(self):
        return f"{self.id} Teacher: {self.user}"


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
    description = models.TextField(blank=True,default="")
    default_weight = models.IntegerField()
    school_subject = models.ForeignKey(SchoolSubject, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Attendance(models.Model):
    status = models.ForeignKey(CategoryAttendanceStatus, on_delete=models.SET_NULL, null=True)
    meeting = models.ForeignKey("Meeting", on_delete=models.CASCADE)
    absence_reason = models.TextField(blank=False, null=True)

    def __str__(self):
        return f"{self.status} for meeting {self.meeting}"


class Meeting(models.Model):
    topic = models.CharField(max_length=255)
    description = models.TextField(blank=True,default="")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    school_subject = models.ForeignKey(SchoolSubject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.topic

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
    end_time = models.DateTimeField()
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    school_subject = models.ForeignKey('SchoolSubject', on_delete=models.CASCADE)

    def __str__(self):
        return self.title