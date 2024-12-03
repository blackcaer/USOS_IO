# from django.shortcuts import render
from datetime import timedelta
from .models import Student, Teacher, Parent
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Group  # , User
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from django.utils import timezone

from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.http import JsonResponse
import json

from usos_backend.usos_api.serializers import GroupSerializer

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import (
    User, Grade, GradeColumn, ScheduledMeeting, ParentConsent, ConsentTemplate, StudentGroup, SchoolSubject, Meeting, Attendance
)
from .serializers import (
    UserSerializer, GradeSerializer, GradeColumnSerializer, ScheduledMeetingSerializer,
    ParentConsentSerializer, ConsentTemplateSerializer, StudentGroupSerializer, SchoolSubjectSerializer,
    StudentSerializer,TeacherSerializer,ParentSerializer, MeetingSerializer, AttendanceSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class GroupViewSet(viewsets.ModelViewSet):
    """
    FOR BACKEND DEVELOPMENT ONLY! (probably won't be supported)
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class StudentViewSet(viewsets.ModelViewSet):
    """
    FOR BACKEND DEVELOPMENT ONLY! (probably won't be supported)
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

class TeacherViewSet(viewsets.ModelViewSet):
    """
    FOR BACKEND DEVELOPMENT ONLY! (probably won't be supported)
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]


class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [IsAuthenticated]


class GradeViewSet(ModelViewSet):
    """
    FOR BACKEND DEVELOPMENT ONLY! (probably won't be supported)
    """
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]

class GradeViewSet(ModelViewSet):
    """
    FOR BACKEND DEVELOPMENT ONLY! (probably won't be supported)
    """
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]

class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'teacher'):
            return Meeting.objects.filter(teacher=user.teacher)
        return Meeting.objects.none()

    def list(self, request):
        now = timezone.now()
        past_meetings = self.get_queryset().filter(start_time__lt=now - timedelta(minutes=45))
        serializer = self.get_serializer(past_meetings, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(teacher=request.user.teacher)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        meeting = self.get_object()
        serializer = self.get_serializer(meeting)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        meeting = self.get_object()
        meeting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['put'], url_path='update-attendance')
    def update_attendance(self, request, pk=None):
        meeting = self.get_object()
        attendance_data = request.data.get('attendance')
        for attendance in attendance_data:
            attendance_instance, created = Attendance.objects.update_or_create(
                meeting=meeting,
                student_id=attendance['student_id'],
                defaults={'status': attendance['status'], 'absence_reason': attendance.get('absence_reason')}
            )
        return Response({'status': 'attendance updated'})

    @action(detail=False, methods=['get'], url_path='schedule')
    def get_schedule(self, request):
        start_of_week = timezone.now().date() - timezone.timedelta(days=timezone.now().date().weekday())
        end_of_week = start_of_week + timezone.timedelta(days=6)
        meetings = self.get_queryset().filter(start_time__date__range=[start_of_week, end_of_week])
        serializer = self.get_serializer(meetings, many=True)
        return Response(serializer.data)

class UserCreateViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# APIViews
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class GradeListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, subject_id):
        grades = Grade.objects.filter(student_id=user_id, grade_column__school_subject_id=subject_id)
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)

    def post(self, request, user_id, subject_id):
        serializer = GradeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student_id=user_id, grade_column__school_subject_id=subject_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GradeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, grade_id):
        grade = get_object_or_404(Grade, id=grade_id)
        serializer = GradeSerializer(grade)
        return Response(serializer.data)

    def put(self, request, grade_id):
        grade = get_object_or_404(Grade, id=grade_id)
        serializer = GradeSerializer(grade, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, grade_id):
        grade = get_object_or_404(Grade, id=grade_id)
        grade.delete()
        return Response(status=204)


class ScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        meetings = ScheduledMeeting.objects.filter(teacher=request.user)
        serializer = ScheduledMeetingSerializer(meetings, many=True)
        return Response(serializer.data)


class ConsentTemplateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, template_consent_id):
        template = get_object_or_404(ConsentTemplate, id=template_consent_id)
        serializer = ConsentTemplateSerializer(template)
        return Response(serializer.data)

    def delete(self, request, template_consent_id):
        template = get_object_or_404(ConsentTemplate, id=template_consent_id)
        template.delete()
        return Response(status=204)


class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        # Logika generowania feeda dla użytkownika
        return Response({"feed": "Example feed data"})


class GradeColumnView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, subject_id):
        columns = GradeColumn.objects.filter(school_subject_id=subject_id)
        serializer = GradeColumnSerializer(columns, many=True)
        return Response(serializer.data)

    def post(self, request, subject_id):
        serializer = GradeColumnSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(school_subject_id=subject_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, subject_id):
        columns = GradeColumn.objects.filter(school_subject_id=subject_id)
        columns.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GradeColumnDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, column_id):
        grades = Grade.objects.filter(grade_column_id=column_id)
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)

    def put(self, request, column_id):
        column = get_object_or_404(GradeColumn, id=column_id)
        serializer = GradeColumnSerializer(column, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, column_id):
        column = get_object_or_404(GradeColumn, id=column_id)
        column.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SchoolSubjectViewSet(viewsets.ModelViewSet):
    queryset = SchoolSubject.objects.all()
    serializer_class = SchoolSubjectSerializer
    permission_classes = [IsAuthenticated]
