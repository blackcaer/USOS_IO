# from django.shortcuts import render
from datetime import timedelta
from .models import Student, Teacher, Parent
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Group  # , User
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from django.utils import timezone

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.http import JsonResponse, HttpResponse
import json

from usos_backend.usos_api.serializers import GroupSerializer

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import (
    User, Grade, GradeColumn, ScheduledMeeting, ParentConsent, ConsentTemplate, StudentGroup, SchoolSubject, Meeting, Attendance, Message
)
from .serializers import (
    UserSerializer, GradeSerializer, GradeColumnSerializer, ScheduledMeetingSerializer,
    ParentConsentSerializer, ConsentTemplateSerializer, StudentGroupSerializer, SchoolSubjectSerializer,
    StudentSerializer, TeacherSerializer, ParentSerializer, MeetingSerializer, AttendanceSerializer, MessageSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    Be careful xd
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


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
    """
    FOR BACKEND DEVELOPMENT ONLY! (probably won't be supported)
    """
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [IsAuthenticated]


class GradeViewSet(ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
                defaults={'status': attendance['status'], 'absence_reason': attendance.get(
                    'absence_reason')}
            )
        return Response({'status': 'attendance updated'})

    @action(detail=False, methods=['get'], url_path='schedule')
    def get_schedule(self, request):
        start_of_week = timezone.now().date(
        ) - timezone.timedelta(days=timezone.now().date().weekday())
        end_of_week = start_of_week + timezone.timedelta(days=6)
        meetings = self.get_queryset().filter(
            start_time__date__range=[start_of_week, end_of_week])
        serializer = self.get_serializer(meetings, many=True)
        return Response(serializer.data)


"""class UserCreateViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)"""

# APIViews


@csrf_exempt
def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('current_user')
            else:
                return HttpResponse('Invalid login credentials', status=401)
        else:
            return HttpResponse('Invalid form data', status=400)
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@csrf_exempt
def custom_logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'method not allowed'}, status=405)

@method_decorator(csrf_exempt, name='dispatch')
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    """def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""


class GradeListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GradeSerializer

    def get(self, request, user_id, subject_id):
        student = get_object_or_404(Student, user_id=user_id)
        subject = get_object_or_404(SchoolSubject, id=subject_id)

        grades = Grade.objects.filter(
            student=student, grade_column__school_subject=subject)
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)

    def post(self, request, user_id, subject_id):
        student = get_object_or_404(Student, user_id=user_id)
        subject = get_object_or_404(SchoolSubject, id=subject_id)

        data = request.data.copy()
        data['student'] = student.user_id  # Użyj user_id zamiast id
        serializer = GradeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GradeDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GradeSerializer

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
    serializer_class = ScheduledMeetingSerializer

    def get(self, request):
        meetings = ScheduledMeeting.objects.filter(teacher=request.user)
        serializer = ScheduledMeetingSerializer(meetings, many=True)
        return Response(serializer.data)


class ConsentTemplateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConsentTemplateSerializer

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
    serializer_class = None  # No serializer needed for this view

    def get(self, request, user_id):
        # Logika generowania feeda dla użytkownika
        return Response({"feed": "Example feed data"})


class GradeColumnView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GradeColumnSerializer

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
    serializer_class = GradeColumnSerializer

    def get(self, request, subject_id, column_id):
        column = get_object_or_404(GradeColumn, id=column_id)
        grades = Grade.objects.filter(grade_column_id=column_id)
        column_serializer = GradeColumnSerializer(column)
        grade_serializer = GradeSerializer(grades, many=True)
        return Response({
            'column': column_serializer.data,
            'grades': grade_serializer.data
        })

    def put(self, request, subject_id, column_id):
        column = get_object_or_404(GradeColumn, id=column_id)
        serializer = GradeColumnSerializer(
            column, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, subject_id, column_id):
        column = get_object_or_404(GradeColumn, id=column_id)
        column.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SchoolSubjectViewSet(viewsets.ModelViewSet):
    queryset = SchoolSubject.objects.all()
    serializer_class = SchoolSubjectSerializer
    permission_classes = [IsAuthenticated]


class StudentGroupViewSet(viewsets.ModelViewSet):
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer
    permission_classes = [IsAuthenticated]


class ScheduledMeetingViewSet(viewsets.ModelViewSet):
    queryset = ScheduledMeeting.objects.all()
    serializer_class = ScheduledMeetingSerializer
    permission_classes = [IsAuthenticated]


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]


class ConsentTemplateViewSet(viewsets.ModelViewSet):
    queryset = ConsentTemplate.objects.all()
    serializer_class = ConsentTemplateSerializer
    permission_classes = [IsAuthenticated]


class ParentConsentViewSet(viewsets.ModelViewSet):
    queryset = ParentConsent.objects.all()
    serializer_class = ParentConsentSerializer
    permission_classes = [IsAuthenticated]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]


class GradeColumnViewSet(viewsets.ModelViewSet):
    queryset = GradeColumn.objects.all()
    serializer_class = GradeColumnSerializer
    permission_classes = [IsAuthenticated]


class StudentGroupsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentGroupSerializer

    def get(self, request, user_id):
        student = get_object_or_404(Student, user_id=user_id)
        groups = student.student_groups.all()
        serializer = StudentGroupSerializer(groups, many=True)
        return Response(serializer.data)


class StudentSubjectsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SchoolSubjectSerializer

    def get(self, request, user_id, group_id):
        student = get_object_or_404(Student, user_id=user_id)
        group = get_object_or_404(StudentGroup, id=group_id, students=student)
        subjects = group.schoolsubject_set.all()
        serializer = SchoolSubjectSerializer(subjects, many=True)
        return Response(serializer.data)


class ParentChildrenView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer

    def get(self, request, user_id):
        parent = get_object_or_404(Parent, user_id=user_id)
        children = parent.children.all()
        serializer = StudentSerializer(children, many=True)
        return Response(serializer.data)


class TeacherGroupsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentGroupSerializer

    def get(self, request, user_id):
        teacher = get_object_or_404(Teacher, user_id=user_id)
        groups = teacher.groups.all()
        serializer = StudentGroupSerializer(groups, many=True)
        return Response(serializer.data)


class TeacherSubjectsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SchoolSubjectSerializer

    def get(self, request, user_id, group_id):
        teacher = get_object_or_404(Teacher, user_id=user_id)
        group = get_object_or_404(StudentGroup, id=group_id, teacher=teacher)
        subjects = group.schoolsubject_set.all()
        serializer = SchoolSubjectSerializer(subjects, many=True)
        return Response(serializer.data)
