from datetime import datetime, timedelta
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CategoryAttendanceStatus, CategoryGradeValue, User, Student, Teacher, Parent, Grade, ScheduledMeeting, Attendance, ParentConsent, ConsentTemplate, StudentGroup, SchoolSubject, Meeting, Message, GradeColumn

class UserEndpointTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', role='student', email="student@student.pl")
        self.client.login(username='testuser', password='testpass')

    def test_user_list_endpoint(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_detail_endpoint(self):
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StudentEndpointTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='student_test', password='testpass', role='student', email="student@student.pl")
        self.student = Student.objects.create(user=self.user)
        self.client.login(username='student_test', password='testpass')

    def test_student_list_endpoint(self):
        url = reverse('student-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_detail_endpoint(self):
        url = reverse('student-detail', args=[self.student.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TeacherEndpointTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='teacher_test', password='testpass', role='teacher', email="teacher@teacher.pl")
        self.teacher = Teacher.objects.create(user=self.user)
        self.client.login(username='teacher_test', password='testpass')

    def test_teacher_list_endpoint(self):
        url = reverse('teacher-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_teacher_detail_endpoint(self):
        url = reverse('teacher-detail', args=[self.teacher.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ParentEndpointTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='parent_test', password='testpass', role='parent', email="parent@parent.pl")
        self.parent = Parent.objects.create(user=self.user)
        self.client.login(username='parent_test', password='testpass')

    def test_parent_list_endpoint(self):
        url = reverse('parent-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_parent_detail_endpoint(self):
        url = reverse('parent-detail', args=[self.parent.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GradeEndpointTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='student_test', password='testpass', role='student', email="student@student.pl")
        self.student = Student.objects.create(user=self.user)
        self.grade_column = GradeColumn.objects.create(title="Test Column", school_subject=SchoolSubject.objects.create(subject_name="Math", student_group=StudentGroup.objects.create(name="Group 1", level=1)))
        self.grade = Grade.objects.create(student=self.student, grade_column=self.grade_column, value=CategoryGradeValue.objects.create(code="A", name="Excellent"))
        self.client.login(username='student_test', password='testpass')

    def test_grade_list_endpoint(self):
        url = reverse('grade-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_grade_detail_endpoint(self):
        url = reverse('grade-detail', args=[self.grade.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ScheduledMeetingEndpointTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='teacher_test', password='testpass', role='teacher', email="teacher@teacher.pl")
        self.teacher = Teacher.objects.create(user=self.user)
        self.scheduled_meeting = ScheduledMeeting.objects.create(
            title="Test Meeting",
            teacher=self.teacher,
            school_subject=SchoolSubject.objects.create(subject_name="Math", student_group=StudentGroup.objects.create(name="Group 1", level=1)),
            start_time=timezone.now() + timedelta(days=1)
        )
        self.client.login(username='teacher_test', password='testpass')

    def test_scheduled_meeting_list_endpoint(self):
        url = reverse('scheduledmeeting-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_scheduled_meeting_detail_endpoint(self):
        url = reverse('scheduledmeeting-detail', args=[self.scheduled_meeting.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AttendanceEndpointTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='student_test', password='testpass', role='student', email="student@student.pl")
        self.student = Student.objects.create(user=self.user)
        self.meeting = Meeting.objects.create(
            title="Test Meeting",
            teacher=Teacher.objects.create(user=User.objects.create_user(username='teacher_test', password='testpass', role='teacher', email="teacher@teacher.pl")),
            school_subject=SchoolSubject.objects.create(subject_name="Math", student_group=StudentGroup.objects.create(name="Group 1", level=1)),
            start_time=timezone.now() + timedelta(days=1)
        )
        self.attendance = Attendance.objects.create(student=self.student, meeting=self.meeting, status=CategoryAttendanceStatus.objects.create(code="P", name="Present"))
        self.client.login(username='student_test', password='testpass')

    def test_attendance_list_endpoint(self):
        url = reverse('attendance-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_attendance_detail_endpoint(self):
        url = reverse('attendance-detail', args=[self.attendance.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ParentConsentEndpointTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='parent_test', password='testpass', role='parent', email="parent@parent.pl")
        self.parent = Parent.objects.create(user=self.user)
        self.student = Student.objects.create(user=User.objects.create_user(username='student_test', password='testpass', role='student', email="student@student.pl"))
        self.consent_template = ConsentTemplate.objects.create(title="Test Consent", author=Teacher.objects.create(user=User.objects.create_user(username='teacher_test', password='testpass', role='teacher', email="teacher@teacher.pl")), end_date=timezone.now().date() + timedelta(days=10))
        self.parent_consent = ParentConsent.objects.create(parent_user=self.parent, child_user=self.student, consent=self.consent_template)
        self.client.login(username='parent_test', password='testpass')

    def test_parent_consent_list_endpoint(self):
        url = reverse('parentconsent-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_parent_consent_detail_endpoint(self):
        url = reverse('parentconsent-detail', args=[self.parent_consent.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ConsentTemplateEndpointTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='teacher_test', password='testpass', role='teacher', email="teacher@teacher.pl")
        self.teacher = Teacher.objects.create(user=self.user)
        self.consent_template = ConsentTemplate.objects.create(title="Test Consent", author=self.teacher, end_date=timezone.now().date() + timedelta(days=10))
        self.client.login(username='teacher_test', password='testpass')

    def test_consent_template_list_endpoint(self):
        url = reverse('consenttemplate-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_consent_template_detail_endpoint(self):
        url = reverse('consenttemplate-detail', args=[self.consent_template.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StudentGroupEndpointTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='teacher_test', password='testpass', role='teacher', email="teacher@teacher.pl")
        self.teacher = Teacher.objects.create(user=self.user)
        self.student_group = StudentGroup.objects.create(name="Group 1", level=1)
        self.client.login(username='teacher_test', password='testpass')

    def test_student_group_list_endpoint(self):
        url = reverse('studentgroup-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_group_detail_endpoint(self):
        url = reverse('studentgroup-detail', args=[self.student_group.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SchoolSubjectEndpointTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='teacher_test', password='testpass', role='teacher', email="teacher@teacher.pl")
        self.teacher = Teacher.objects.create(user=self.user)
        self.student_group = StudentGroup.objects.create(name="Group 1", level=1)
        self.school_subject = SchoolSubject.objects.create(subject_name="Math", student_group=self.student_group)
        self.client.login(username='teacher_test', password='testpass')

    def test_school_subject_list_endpoint(self):
        url = reverse('subject-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_school_subject_detail_endpoint(self):
        url = reverse('subject-detail', args=[self.school_subject.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MeetingEndpointTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='teacher_test', password='testpass', role='teacher', email="teacher@teacher.pl")
        self.teacher = Teacher.objects.create(user=self.user)
        self.school_subject = SchoolSubject.objects.create(subject_name="Math", student_group=StudentGroup.objects.create(name="Group 1", level=1))
        self.meeting = Meeting.objects.create(
            title="Test Meeting",
            teacher=self.teacher,
            school_subject=self.school_subject,
            start_time=timezone.now() + timedelta(days=1)
        )
        self.client.login(username='teacher_test', password='testpass')

    def test_meeting_list_endpoint(self):
        url = reverse('meeting-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_meeting_detail_endpoint(self):
        url = reverse('meeting-detail', args=[self.meeting.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MessageEndpointTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', role='student', email="student@student.pl")
        self.message = Message.objects.create(title="Test Message", content="This is a test message.", sender=self.user)
        self.message.recipients.add(self.user)
        self.client.login(username='testuser', password='testpass')

    def test_message_list_endpoint(self):
        url = reverse('message-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_message_detail_endpoint(self):
        url = reverse('message-detail', args=[self.message.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GradeColumnEndpointTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='teacher_test', password='testpass', role='teacher', email="teacher@teacher.pl")
        self.teacher = Teacher.objects.create(user=self.user)
        self.school_subject = SchoolSubject.objects.create(subject_name="Math", student_group=StudentGroup.objects.create(name="Group 1", level=1))
        self.grade_column = GradeColumn.objects.create(title="Test Column", school_subject=self.school_subject)
        self.client.login(username='teacher_test', password='testpass')

    def test_grade_column_list_endpoint(self):
        url = reverse('gradecolumn-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_grade_column_detail_endpoint(self):
        url = reverse('gradecolumn-detail', args=[self.grade_column.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
