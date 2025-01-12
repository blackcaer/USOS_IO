from datetime import timedelta
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
    role = serializers.ChoiceField(
        choices=['student', 'parent', 'teacher'], write_only=True)
    first_name = serializers.CharField(default="first_name")
    last_name = serializers.CharField(default="last_name")
    # email = serializers.EmailField(default="email@example.com")#unique
    birth_date = serializers.DateField(default="2010-01-01")
    sex = serializers.ChoiceField(
        choices=[("M", "Male"), ("F", "Female")], default="M")
    status = serializers.ChoiceField(
        choices=[("A", "Active"), ("U", "Inactive")], default="A")
    phone_number = serializers.CharField(
        default="", allow_blank=True, allow_null=True)
    photo_url = serializers.URLField(
        default="", allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email',
                  'status', 'birth_date', 'sex', 'phone_number', 'photo_url', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(**validated_data)
        user.role = role
        user.save()
        if role == 'student':
            Student.objects.create(user=user)
        elif role == 'parent':
            Parent.objects.create(user=user)
        elif role == 'teacher':
            Teacher.objects.create(user=user)
        else:
            raise serializers.ValidationError("Invalid role")
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['role'] = instance.role
        return representation

    def update(self, instance, validated_data):
        validated_data.pop('role', None)  # Prevent role from being updated
        return super().update(instance, validated_data)


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    student_groups_string = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['user_id', 'user', 'parents', 'student_groups_string']

    def get_student_groups_string(self, obj):
        return ", ".join([group.name for group in obj.student_groups.all()])

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        parents_data = validated_data.pop('parents', [])
        user = User.objects.create_user(**user_data)
        student = Student.objects.create(user=user, **validated_data)
        student.parents.set(parents_data)
        return student


class ParentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Parent
        fields = ['user_id', 'user', 'children']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        children_data = validated_data.pop('children', [])
        user = User.objects.create_user(**user_data)
        parent = Parent.objects.create(user=user, **validated_data)
        parent.children.set(children_data)
        return parent


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ['user_id', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher


class StudentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGroup
        fields = ['id', 'name', 'description',
                  'level', 'section', 'students']


class SchoolSubjectSerializer(serializers.ModelSerializer):
    student_group = StudentGroupSerializer()

    class Meta:
        model = SchoolSubject
        fields = ['id', 'subject_name', 'description',
                  'is_mandatory', 'student_group']


class GradeSerializer(serializers.ModelSerializer):
    value = serializers.SlugRelatedField(
        queryset=CategoryGradeValue.objects.all(),
        slug_field="code"
    )
    count_to_avg = serializers.BooleanField(default=True)
    grade_column = serializers.PrimaryKeyRelatedField(
        queryset=GradeColumn.objects.all())

    class Meta:
        model = Grade
        fields = ['id', 'value', 'timestamp',
                  'student', 'grade_column', 'count_to_avg']

    def create(self, validated_data):
        grade = Grade.objects.create(
            grade_column=validated_data.pop('grade_column'), **validated_data)
        return grade


class GradeColumnSerializer(serializers.ModelSerializer):
    weight = serializers.IntegerField(default=1)

    class Meta:
        model = GradeColumn
        fields = ['id', 'title', 'weight', 'description', 'school_subject']


class GradeColumnDetailSerializer(serializers.ModelSerializer):
    grades = GradeSerializer(many=True, read_only=True, source='grade_set')

    class Meta:
        model = GradeColumn
        fields = ['id', 'title', 'weight',
                  'description', 'school_subject', 'grades']


class ScheduledMeetingSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    school_subject = SchoolSubjectSerializer()

    class Meta:
        model = ScheduledMeeting
        fields = ['id', 'day_of_week', 'slot',
                  'teacher', 'school_subject', 'place']


class ParentConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentConsent
        fields = ['id', 'parent_user', 'child_user',
                  'consent', 'is_consent', 'file']


class ConsentTemplateSerializer(serializers.ModelSerializer):
    parent_consents = ParentConsentSerializer(many=True, read_only=True)
    parent_submission = serializers.SerializerMethodField()
    author = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())

    class Meta:
        model = ConsentTemplate
        fields = ['id', 'title', 'description', 'end_date',
                  'students', 'parent_consents', 'author', 'parent_submission']

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_parent_submission(self, obj):
        request = self.context.get('request')
        if request and request.user.role == 'parent':
            parent = Parent.objects.get(user=request.user)
            return obj.what_parent_submitted(parent)
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = TeacherSerializer(instance.author).data
        return representation


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['id', 'title', 'description',
                  'start_time', 'teacher', 'school_subject']


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'status', 'absence_reason', 'meeting']


class BulkAttendanceSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        attendance_mapping = {att.id: att for att in instance}
        updated_attendances = []
        for item in validated_data:
            attendance = attendance_mapping.get(item['id'])
            if attendance:
                for attr, value in item.items():
                    setattr(attendance, attr, value)
                updated_attendances.append(attendance)
        Attendance.objects.bulk_update(
            updated_attendances, ['status', 'absence_reason'])
        return updated_attendances


class AttendanceBulkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
        list_serializer_class = BulkAttendanceSerializer


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'title', 'content', 'timestamp',
                  'is_read', 'sender', 'recipients']
