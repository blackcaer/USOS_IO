from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import (
    User, Student, Parent, Teacher, Grade, GradeColumn, ScheduledMeeting, ParentConsent,
    ConsentTemplate, Attendance, SchoolSubject, StudentGroup, CategoryGradeValue
)

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','first_name', 'last_name', 'email', 'status', 'birth_date','sex','phone_number', 'photo_url']


class StudentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGroup
        fields = ['id', 'name', 'category', 'level', 'section']


class SchoolSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolSubject
        fields = ['id', 'subject_name', 'description', 'is_mandatory', 'student_group']


class GradeSerializer(serializers.ModelSerializer):
    value = serializers.SlugRelatedField(
        queryset=CategoryGradeValue.objects.all(),
        slug_field="code"
    )
    class Meta:
        model = Grade
        fields = ['id', 'value', 'weight', 'timestamp', 'student', 'grade_column', 'count_to_avg']


class GradeColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeColumn
        fields = ['id', 'title', 'description', 'default_weight', 'school_subject']


class ScheduledMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledMeeting
        fields = ['id', 'title', 'description', 'start_time', 'end_time', 'teacher', 'school_subject']


class ParentConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentConsent
        fields = ['id', 'parent_user', 'child_user', 'consent', 'is_consent', 'url']


class ConsentTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsentTemplate
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'recipients', 'expiry_date']




class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user', 'groups']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'user']


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['id', 'user', 'children']

