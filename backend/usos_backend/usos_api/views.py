from datetime import timedelta

from usos_backend.usos_api.utils import get_scheduled_meetings
from .models import Student, Teacher, Parent
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, viewsets, status
from django.utils import timezone

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse

from django.http import JsonResponse, HttpResponse

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import (
    User, Grade, GradeColumn, ScheduledMeeting, ParentConsent, ConsentTemplate, StudentGroup, SchoolSubject, Meeting, Attendance, Message
)
from .serializers import (
    AttendanceBulkSerializer, UserSerializer, GradeSerializer, GradeColumnSerializer, ScheduledMeetingSerializer,
    ParentConsentSerializer, ConsentTemplateSerializer, StudentGroupSerializer, SchoolSubjectSerializer,
    StudentSerializer, TeacherSerializer, ParentSerializer, MeetingSerializer, AttendanceSerializer, MessageSerializer
)


from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


def get_consent_template_serializer(request, consent_template, many=False):
    context = {'request': request}
    if request.user.role == 'teacher':
        return ConsentTemplateSerializer(consent_template, fields=['id', 'title', 'description', 'end_date',
                                                                   'students', 'parent_consents', 'author'], many=many, context=context)
    if request.user.role == 'parent':
        return ConsentTemplateSerializer(consent_template, fields=['id', 'title', 'description', 'end_date', 'parent_submission', 'author'], many=many, context=context)
    else:
        raise PermissionError("User role not supported for this view")


class IsParent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'parent'


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'teacher'


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'student'


class IsParentOrTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['parent', 'teacher']


class UserViewSet(viewsets.ModelViewSet):
    """
    IT IS NOT PART OF THE API, IT IS USED FOR TESTING PURPOSES ONLY
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
    IT IS NOT PART OF THE API, IT IS USED FOR TESTING PURPOSES ONLY
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class TeacherViewSet(viewsets.ModelViewSet):
    """
    IT IS NOT PART OF THE API, IT IS USED FOR TESTING PURPOSES ONLY
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]


class ParentViewSet(viewsets.ModelViewSet):
    """
    IT IS NOT PART OF THE API, IT IS USED FOR TESTING PURPOSES ONLY
    """
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [IsAuthenticated]


class GradeViewSet(ModelViewSet):
    """
    IT IS NOT PART OF THE API, IT IS USED FOR TESTING PURPOSES ONLY
    """
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]


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


@method_decorator(csrf_exempt, name='dispatch')
class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class GradeListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GradeSerializer
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, user_id, subject_id):
        student = get_object_or_404(Student, user_id=user_id)
        subject = get_object_or_404(SchoolSubject, id=subject_id)

        grades = Grade.objects.filter(
            student=student, grade_column__school_subject=subject)
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request, user_id, subject_id):
        student = get_object_or_404(Student, user_id=user_id)
        subject = get_object_or_404(SchoolSubject, id=subject_id)

        data = request.data.copy()
        data['student'] = student.user_id
        serializer = GradeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class GradeDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GradeSerializer
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

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

    @csrf_exempt
    def delete(self, request, grade_id):
        grade = get_object_or_404(Grade, id=grade_id)
        grade.delete()
        return Response(status=204)


@method_decorator(csrf_exempt, name='dispatch')
class ScheduleView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ScheduledMeetingSerializer
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        meetings = ScheduledMeeting.objects.filter(teacher=request.user)
        serializer = ScheduledMeetingSerializer(meetings, many=True)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class ConsentTemplateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConsentTemplateSerializer

    def get(self, request, template_consent_id):
        template = get_object_or_404(ConsentTemplate, id=template_consent_id)
        serializer = ConsentTemplateSerializer(template)
        return Response(serializer.data)

    @csrf_exempt
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


@method_decorator(csrf_exempt, name='dispatch')
class GradeColumnView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GradeColumnSerializer
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, subject_id):
        columns = GradeColumn.objects.filter(school_subject_id=subject_id)
        serializer = GradeColumnSerializer(columns, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request, subject_id):
        serializer = GradeColumnSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(school_subject_id=subject_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def delete(self, request, subject_id):
        columns = GradeColumn.objects.filter(school_subject_id=subject_id)
        columns.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GradeColumnDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GradeColumnSerializer
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

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

    @csrf_exempt
    def delete(self, request, subject_id, column_id):
        column = get_object_or_404(GradeColumn, id=column_id)
        column.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SchoolSubjectViewSet(viewsets.ModelViewSet):
    """
    IT IS NOT PART OF THE API, IT IS USED FOR TESTING PURPOSES ONLY
    """
    queryset = SchoolSubject.objects.all()
    serializer_class = SchoolSubjectSerializer
    permission_classes = [IsAuthenticated]


class StudentGroupViewSet(viewsets.ModelViewSet):
    """
    IT IS NOT PART OF THE API, IT IS USED FOR TESTING PURPOSES ONLY
    """
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer
    permission_classes = [IsAuthenticated]


class ScheduledMeetingViewSet(viewsets.ModelViewSet):
    """
    IT IS NOT PART OF THE API, IT IS USED FOR TESTING PURPOSES ONLY
    """
    queryset = ScheduledMeeting.objects.all()
    serializer_class = ScheduledMeetingSerializer
    permission_classes = [IsAuthenticated]


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    IT IS NOT PART OF THE API, IT IS USED FOR TESTING PURPOSES ONLY
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]


class ConsentTemplateViewSet(viewsets.ModelViewSet):
    """
    IT IS NOT PART OF THE API, IT IS USED FOR TESTING PURPOSES ONLY
    """
    queryset = ConsentTemplate.objects.all()
    serializer_class = ConsentTemplateSerializer
    permission_classes = [IsAuthenticated]


class ParentConsentViewSet(viewsets.ModelViewSet):
    """
    IT IS NOT PART OF THE API, IT IS USED FOR TESTING PURPOSES ONLY
    """
    queryset = ParentConsent.objects.all()
    serializer_class = ParentConsentSerializer
    permission_classes = [IsAuthenticated]


class MessageViewSet(viewsets.ModelViewSet):
    """
    IT IS NOT PART OF THE API, IT IS USED FOR TESTING PURPOSES ONLY
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]


class GradeColumnViewSet(viewsets.ModelViewSet):
    """
    IT IS NOT PART OF THE API, IT IS USED FOR TESTING PURPOSES ONLY
    """
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


class MeetingListCreateView(APIView):
    """
    GET - Zwraca listę wszystkich spotkań
    POST - Tworzy nowe spotkanie
    """
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        past_meetings = Meeting.objects.all()
        serializer = MeetingSerializer(past_meetings, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request):
        serializer = MeetingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# /meetings/{meeting_id}/ (GET, DELETE)
class MeetingDetailView(APIView):
    """
    GET - Szczegóły spotkania
    DELETE - Usuwa spotkanie
    """
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, meeting_id):
        meeting = get_object_or_404(Meeting, pk=meeting_id)
        serializer = MeetingSerializer(meeting)
        return Response(serializer.data)

    @csrf_exempt
    def delete(self, request, meeting_id):
        meeting = get_object_or_404(Meeting, pk=meeting_id)
        meeting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# /meetings/{meeting_id}/attendance (GET, POST, PUT)
class MeetingAttendanceView(APIView):
    """
    POST - Tworzy listę obecności dla spotkania (bulk create)
    np. [{"student": 1, "status": "P"}, {"student": 2, "status": "A"}]
    Ważne żeby studenci byli z grupy która faktycznie ma te zajęcia, inaczej error "Student not in the valid student group"
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, meeting_id):
        meeting = get_object_or_404(Meeting, pk=meeting_id)
        attendances = Attendance.objects.filter(meeting=meeting)
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request, meeting_id):
        meeting = get_object_or_404(Meeting, pk=meeting_id)

        student_group = meeting.school_subject.student_group
        valid_student_ids = student_group.students.values_list(
            'user_id', flat=True)

        for item in request.data:
            item['meeting'] = meeting_id
            if item['student'] not in valid_student_ids:
                return Response({'error': 'Student not in the valid student group'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AttendanceSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# /meetings/schedule/ (GET)


class ScheduledMeetingView(APIView):
    """
    GET - Zwraca harmonogram spotkań na bieżący tydzień
    """
    serializer_class = ScheduledMeetingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_of_week = timezone.now().date() - timedelta(days=timezone.now().weekday())
        end_of_week = start_of_week + timedelta(days=7)

        scheduled_meetings = get_scheduled_meetings(
            request.user, start_of_week, end_of_week)

        serializer = ScheduledMeetingSerializer(scheduled_meetings, many=True)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class PendingConsentsView(APIView):
    permission_classes = [IsAuthenticated, IsParent]

    def get(self, request):
        parent = get_object_or_404(Parent, user=request.user)
        pending_consents = ConsentTemplate.objects.filter(
            students__parents=parent, end_date__gte=timezone.now().date())
        serializer = get_consent_template_serializer(
            request, pending_consents, many=True)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class ParentConsentDetailView(APIView):
    permission_classes = [IsAuthenticated, IsParentOrTeacher]
    serializer_class = ParentConsentSerializer

    def get(self, request, parent_consent_id):
        parent_consent = get_object_or_404(ParentConsent, id=parent_consent_id)
        if not parent_consent.consent.is_active():
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ParentConsentSerializer(parent_consent)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class ConsentTemplateListView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = ConsentTemplateSerializer

    def get(self, request):
        teacher = get_object_or_404(Teacher, user=request.user)
        consent_templates = ConsentTemplate.objects.filter(
            author=teacher, end_date__gte=timezone.now().date())
        serializer = ConsentTemplateSerializer(consent_templates, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request):
        teacher = get_object_or_404(Teacher, user=request.user)
        data = request.data.copy()
        data['author'] = teacher.user_id

        serializer = ConsentTemplateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class ConsentTemplateDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConsentTemplateSerializer
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, consent_template_id):
        consent_template = get_object_or_404(
            ConsentTemplate, id=consent_template_id)
        if not consent_template.is_active():
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = get_consent_template_serializer(request, consent_template)
        return Response(serializer.data)

    @csrf_exempt
    def delete(self, request, consent_template_id):
        print(request.user.role)
        if request.user.role != 'teacher':
            return Response(status=status.HTTP_403_FORBIDDEN, data={'error': 'Only teacher can delete consent templates'})
        consent_template = get_object_or_404(
            ConsentTemplate, id=consent_template_id)
        consent_template.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(csrf_exempt, name='dispatch')
class ParentConsentSubmitView(APIView):
    permission_classes = [IsAuthenticated, IsParent]
    serializer_class = ParentConsentSerializer
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    @csrf_exempt
    def post(self, request, consent_template_id):
        parent = get_object_or_404(Parent, user=request.user)
        consent_template = get_object_or_404(
            ConsentTemplate, id=consent_template_id)
        data = {
            'parent_user': parent.user.id,
            'child_user': request.data.get('child_user'),
            'consent': consent_template.id,
            'is_consent': request.data.get('is_consent'),
            'file': request.FILES.get('file') if 'file' in request.FILES else None
        }
        serializer = ParentConsentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class StudentGroupListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentGroupSerializer

    def get(self, request):
        student_groups = StudentGroup.objects.all()
        serializer = StudentGroupSerializer(student_groups, many=True)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class StudentGroupDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentGroupSerializer

    def get(self, request, student_group_id):
        student_group = get_object_or_404(StudentGroup, id=student_group_id)
        serializer = StudentGroupSerializer(student_group)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class StudentGroupStudentsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer

    def get(self, request, student_group_id):
        student_group = get_object_or_404(StudentGroup, id=student_group_id)
        students = student_group.students.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class StudentGroupSubjectsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SchoolSubjectSerializer

    def get(self, request, student_group_id):
        student_group = get_object_or_404(StudentGroup, id=student_group_id)
        subjects = student_group.schoolsubject_set.all()
        serializer = SchoolSubjectSerializer(subjects, many=True)
        return Response(serializer.data)
