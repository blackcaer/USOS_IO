from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.test import APITestCase
from .models import Teacher, Meeting, SchoolSubject, StudentGroup, Student,  Attendance, CategoryAttendanceStatus, CategoryGradeValue, User, Parent, Grade, ScheduledMeeting, ParentConsent, ConsentTemplate, StudentGroup, SchoolSubject, Meeting, Message, GradeColumn

class MeetingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher_user = User.objects.create_user(
            username="teacher_test", first_name="John", last_name="Doe", role="teacher", email="teacher@example.com", password="password")
        self.teacher = Teacher.objects.create(user=self.teacher_user)
        self.student_user = User.objects.create_user(
            username="student_test", first_name="Jane", last_name="Doe", role="student", email="student@example.com", password="password")
        self.student = Student.objects.create(user=self.student_user)
        self.student_group = StudentGroup.objects.create(
            name="Group 1", level=1)
        self.student_group.students.add(self.student)
        self.school_subject = SchoolSubject.objects.create(
            subject_name="Math", student_group=self.student_group)
        self.meeting = Meeting.objects.create(school_subject=self.school_subject, title="Meeting 1",
                                              description="Description 1", start_time="2023-10-10T10:00:00Z", teacher=self.teacher)

        # Authenticate the client
        self.client.force_authenticate(user=self.teacher_user)

    def test_create_meeting(self):
        url = reverse('meeting-list-create')
        data = {
            'title': 'New Meeting',
            'description': 'New Description',
            'start_time': '2023-10-11T10:00:00Z',
            'school_subject': self.school_subject.id,
            'teacher': self.teacher_user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Meeting.objects.count(), 2)
        self.assertEqual(Meeting.objects.get(
            id=response.data['id']).title, 'New Meeting')

    def test_get_meeting(self):
        url = reverse('meeting-detail', args=[self.meeting.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.meeting.title)

    def test_delete_meeting(self):
        url = reverse('meeting-detail', args=[self.meeting.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Meeting.objects.count(), 0)

    def test_create_attendance(self):
        url = reverse('meeting-attendance', args=[self.meeting.id])
        data = [
            {'student': self.student.user_id, 'status': 'P'}
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attendance.objects.count(), 1)
        self.assertEqual(Attendance.objects.get().student, self.student)

    def test_create_attendance_invalid_student(self):
        url = reverse('meeting-attendance', args=[self.meeting.id])
        data = [
            {'student': 999, 'status': 'P'}  # Invalid student ID
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_create_attendance_invalid_status(self):
        url = reverse('meeting-attendance', args=[self.meeting.id])
        data = [
            {'student': self.student.user_id, 'status': 'X'}  # Invalid status
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status', response.data[0])
        self.assertEqual(response.data[0]['status'][0].code, 'invalid_choice')


class UserEndpointTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass', role='student', email="student@student.pl")
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
        self.user = User.objects.create_user(
            username='student_test', password='testpass', role='student', email="student@student.pl")
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
        self.user = User.objects.create_user(
            username='teacher_test', password='testpass', role='teacher', email="teacher@teacher.pl")
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
        self.user = User.objects.create_user(
            username='parent_test', password='testpass', role='parent', email="parent@parent.pl")
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
        self.user = User.objects.create_user(
            username='student_test', password='testpass', role='student', email="student@student.pl")
        self.student = Student.objects.create(user=self.user)
        self.grade_column = GradeColumn.objects.create(title="Test Column", school_subject=SchoolSubject.objects.create(
            subject_name="Math", student_group=StudentGroup.objects.create(name="Group 1", level=1)))
        self.grade = Grade.objects.create(student=self.student, grade_column=self.grade_column,
                                          value=CategoryGradeValue.objects.create(code="A", name="Excellent"))
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
        self.user = User.objects.create_user(
            username='teacher_test', password='testpass', role='teacher', email="teacher@teacher.pl")
        self.teacher = Teacher.objects.create(user=self.user)
        self.student_group = StudentGroup.objects.create(name="Group 1", level=1)
        self.school_subject = SchoolSubject.objects.create(subject_name="Math", student_group=self.student_group)
        self.scheduled_meeting = ScheduledMeeting.objects.create(
            description="Test Description",
            day_of_week=1,  # Poniedziałek
            slot=1,  # 08:00 - 08:45
            teacher=self.teacher,
            school_subject=self.school_subject,
            place=10  # Sala 10
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
        self.assertEqual(response.data['title'], self.scheduled_meeting.title)
        self.assertEqual(response.data['description'], self.scheduled_meeting.description)
        self.assertEqual(response.data['day_of_week'], self.scheduled_meeting.day_of_week)
        self.assertEqual(response.data['slot'], self.scheduled_meeting.slot)
        self.assertEqual(response.data['place'], self.scheduled_meeting.place)


class AttendanceEndpointTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='student_test', password='testpass', role='student', email="student@student.pl")
        self.student = Student.objects.create(user=self.user)
        self.meeting = Meeting.objects.create(
            title="Test Meeting",
            teacher=Teacher.objects.create(user=User.objects.create_user(
                username='teacher_test', password='testpass', role='teacher', email="teacher@teacher.pl")),
            school_subject=SchoolSubject.objects.create(
                subject_name="Math", student_group=StudentGroup.objects.create(name="Group 1", level=1)),
            start_time=timezone.now() + timedelta(days=1)
        )
        self.attendance = Attendance.objects.create(
            student=self.student, meeting=self.meeting, status=CategoryAttendanceStatus.objects.create(code="P", name="Present"))
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
        self.user = User.objects.create_user(
            username='parent_test', password='testpass', role='parent', email="parent@parent.pl")
        self.parent = Parent.objects.create(user=self.user)
        self.student = Student.objects.create(user=User.objects.create_user(
            username='student_test', password='testpass', role='student', email="student@student.pl"))
        self.consent_template = ConsentTemplate.objects.create(title="Test Consent", author=Teacher.objects.create(user=User.objects.create_user(
            username='teacher_test', password='testpass', role='teacher', email="teacher@teacher.pl")), end_date=timezone.now().date() + timedelta(days=10))
        self.parent_consent = ParentConsent.objects.create(
            parent_user=self.parent, child_user=self.student, consent=self.consent_template)
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
        self.user = User.objects.create_user(
            username='teacher_test', password='testpass', role='teacher', email="teacher@teacher.pl")
        self.teacher = Teacher.objects.create(user=self.user)
        self.consent_template = ConsentTemplate.objects.create(
            title="Test Consent", author=self.teacher, end_date=timezone.now().date() + timedelta(days=10))
        self.client.login(username='teacher_test', password='testpass')

    def test_consent_template_list_endpoint(self):
        url = reverse('consenttemplate-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_consent_template_detail_endpoint(self):
        url = reverse('consenttemplate-detail',
                      args=[self.consent_template.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StudentGroupEndpointTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='teacher_test', password='testpass', role='teacher', email="teacher@teacher.pl")
        self.teacher = Teacher.objects.create(user=self.user)
        self.student_group = StudentGroup.objects.create(
            name="Group 1", level=1)
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
        self.user = User.objects.create_user(
            username='teacher_test', password='testpass', role='teacher', email="teacher@teacher.pl")
        self.teacher = Teacher.objects.create(user=self.user)
        self.student_group = StudentGroup.objects.create(
            name="Group 1", level=1)
        self.school_subject = SchoolSubject.objects.create(
            subject_name="Math", student_group=self.student_group)
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
        self.user = User.objects.create_user(
            username='teacher_test', password='testpass', role='teacher', email="teacher@teacher.pl")
        self.teacher = Teacher.objects.create(user=self.user)
        self.school_subject = SchoolSubject.objects.create(
            subject_name="Math", student_group=StudentGroup.objects.create(name="Group 1", level=1))
        self.meeting = Meeting.objects.create(
            title="Test Meeting",
            teacher=self.teacher,
            school_subject=self.school_subject,
            start_time=timezone.now() + timedelta(days=1)
        )
        self.client.login(username='teacher_test', password='testpass')

    def test_meeting_detail_endpoint(self):
        url = reverse('meeting-detail', args=[self.meeting.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class MessageEndpointTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass', role='student', email="student@student.pl")
        self.message = Message.objects.create(
            title="Test Message", content="This is a test message.", sender=self.user)
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
        self.user = User.objects.create_user(
            username='teacher_test', password='testpass', role='teacher', email="teacher@teacher.pl")
        self.teacher = Teacher.objects.create(user=self.user)
        self.school_subject = SchoolSubject.objects.create(
            subject_name="Math", student_group=StudentGroup.objects.create(name="Group 1", level=1))
        self.grade_column = GradeColumn.objects.create(
            title="Test Column", school_subject=self.school_subject)
        self.client.login(username='teacher_test', password='testpass')

    def test_grade_column_list_endpoint(self):
        url = reverse('gradecolumn-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_grade_column_detail_endpoint(self):
        url = reverse('gradecolumn-detail', args=[self.grade_column.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
