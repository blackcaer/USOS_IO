# from django.shortcuts import render
from .models import Student, Teacher, Parent
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Group  # , User
from rest_framework import permissions, viewsets

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
    User, Grade, GradeColumn, ScheduledMeeting, ParentConsent, ConsentTemplate, StudentGroup, SchoolSubject
)
from .serializers import (
    UserSerializer, GradeSerializer, GradeColumnSerializer, ScheduledMeetingSerializer,
    ParentConsentSerializer, ConsentTemplateSerializer, StudentGroupSerializer, SchoolSubjectSerializer,
    StudentSerializer,TeacherSerializer,ParentSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


# ViewSets dla prostych CRUD operacji
class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]


class ParentViewSet(ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [IsAuthenticated]


class GradeViewSet(ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]


# Widoki dla bardziej specyficznych funkcji
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
        grades = Grade.objects.filter(
            student_id=user_id, subject_id=subject_id)
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)

    def post(self, request, user_id, subject_id):
        serializer = GradeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student_id=user_id, subject_id=subject_id)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


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
        return Response(serializer.errors, status=400)

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
