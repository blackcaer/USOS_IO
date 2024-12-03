from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import (
    Meeting, User, Student, Parent, Teacher, Grade, GradeColumn, ScheduledMeeting, ParentConsent,
    ConsentTemplate, Attendance, SchoolSubject, StudentGroup, CategoryGradeValue
)

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=['student', 'parent', 'teacher'], write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'status', 'birth_date', 'sex', 'phone_number', 'photo_url', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(**validated_data)
        if role == 'student':
            Student.objects.create(user=user)
        elif role == 'parent':
            Parent.objects.create(user=user)
        elif role == 'teacher':
            Teacher.objects.create(user=user)
        else:
            raise serializers.ValidationError("Invalid role")
        return user
"""
class UserCreateSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=['student', 'parent', 'teacher'], write_only=True)

    class Meta:
        model = User
        fields = ['id', 'role', 'username', 'password', 'first_name', 'last_name', 'email', 'status', 'birth_date', 'sex', 'phone_number', 'photo_url']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(**validated_data)
        if role == 'student':
            Student.objects.create(user=user)
        elif role == 'parent':
            Parent.objects.create(user=user)
        elif role == 'teacher':
            Teacher.objects.create(user=user)
        else:
            raise serializers.ValidationError("Invalid role")
        return user"""

class StudentSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'user', 'groups', 'parents']

    def get_id(self, obj):
        return obj.user.id

class ParentSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Parent
        fields = ['id', 'user', 'children']

    def get_id(self, obj):
        return obj.user.id

class TeacherSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'groups']

    def get_id(self, obj):
        return obj.user.id

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


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['id', 'title', 'description', 'start_time', 'duration', 'teacher', 'school_subject']

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'status', 'absence_reason', 'meeting']
