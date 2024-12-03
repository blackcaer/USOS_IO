from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import (
    Meeting, User, Student, Parent, Teacher, Grade, GradeColumn, ScheduledMeeting, ParentConsent,
    ConsentTemplate, Attendance, SchoolSubject, StudentGroup, CategoryGradeValue, Message
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

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Student
        fields = ['user_id', 'user', 'groups', 'parents']

class ParentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Parent
        fields = ['user_id', 'user', 'children']

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Teacher
        fields = ['user_id', 'user', 'groups']

class StudentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGroup
        fields = ['id', 'name', 'description', 'category', 'level', 'section', 'students']

class SchoolSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolSubject
        fields = ['id', 'subject_name', 'description', 'is_mandatory', 'student_group']

class GradeSerializer(serializers.ModelSerializer):
    value = serializers.SlugRelatedField(
        queryset=CategoryGradeValue.objects.all(),
        slug_field="code"
    )
    count_to_avg = serializers.BooleanField(default=True)
    grade_column = serializers.PrimaryKeyRelatedField(queryset=GradeColumn.objects.all())

    class Meta:
        model = Grade
        fields = ['id', 'value', 'timestamp', 'student', 'grade_column', 'count_to_avg']

    def create(self, validated_data):
        grade = Grade.objects.create(grade_column=validated_data.pop('grade_column'), **validated_data)
        return grade

class GradeColumnSerializer(serializers.ModelSerializer):
    weight = serializers.IntegerField(default=1)

    class Meta:
        model = GradeColumn
        fields = ['id', 'title', 'weight', 'description', 'school_subject']

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

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'title', 'content', 'timestamp', 'is_read', 'sender', 'recipients']
