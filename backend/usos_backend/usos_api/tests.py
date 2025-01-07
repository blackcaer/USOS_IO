from .utils import get_scheduled_meetings
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
        url = reverse('student-detail', args=[self.student.user_id])
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
        url = reverse('teacher-detail', args=[self.teacher.user_id])
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
        url = reverse('parent-detail', args=[self.parent.user_id])
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


class ScheduledMeetingEndpointTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Create users
        self.teacher_user = User.objects.create_user(
            username="teacher_test", role="teacher", email="teacher@example.com", password="password")
        self.teacher = Teacher.objects.create(user=self.teacher_user)

        self.student_user = User.objects.create_user(
            username="student_test", role="student", email="student@example.com", password="password")
        self.student = Student.objects.create(user=self.student_user)

        self.parent_user = User.objects.create_user(
            username="parent_test", role="parent", email="parent@example.com", password="password")
        self.parent = Parent.objects.create(user=self.parent_user)
        self.parent.children.add(self.student)

        self.student_group = StudentGroup.objects.create(
            name="Group 1", level=1)
        self.student_group.students.add(self.student)

        self.school_subject = SchoolSubject.objects.create(
            subject_name="Math", student_group=self.student_group)

        self.scheduled_meeting = ScheduledMeeting.objects.create(
            day_of_week=1,  # Poniedziałek
            slot=1,  # 08:00 - 08:45
            teacher=self.teacher,
            school_subject=self.school_subject,
            place=10  # Sala 10
        )

        # Create additional users and groups
        self.other_teacher_user = User.objects.create_user(
            username="other_teacher_test", role="teacher", email="other_teacher@example.com", password="password")
        self.other_teacher = Teacher.objects.create(
            user=self.other_teacher_user)

        self.other_student_user = User.objects.create_user(
            username="other_student_test", role="student", email="other_student@example.com", password="password")
        self.other_student = Student.objects.create(
            user=self.other_student_user)

        self.other_parent_user = User.objects.create_user(
            username="other_parent_test", role="parent", email="other_parent@example.com", password="password")

        self.other_parent = Parent.objects.create(user=self.other_parent_user)
        self.other_parent.children.add(self.other_student)

        self.other_student_group = StudentGroup.objects.create(
            name="Group 2", level=2)
        self.other_student_group.students.add(self.other_student)

        self.other_school_subject = SchoolSubject.objects.create(
            subject_name="Science", student_group=self.other_student_group)

        self.other_scheduled_meeting = ScheduledMeeting.objects.create(
            day_of_week=2,  # Wtorek
            slot=2,  # 08:55 - 09:40
            teacher=self.other_teacher,
            school_subject=self.other_school_subject,
            place=11  # Sala 11
        )

        self.client.login(username='teacher_test', password='password')

    def test_scheduled_meeting_detail_endpoint(self):
        url = reverse('meeting-schedule')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]['day_of_week'], self.scheduled_meeting.day_of_week)
        self.assertEqual(response.data[0]['slot'], self.scheduled_meeting.slot)
        self.assertEqual(response.data[0]['place'],
                         self.scheduled_meeting.place)

    def test_get_scheduled_meetings_for_student(self):
        meetings = get_scheduled_meetings(self.student_user, None, None)
        self.assertIn(self.scheduled_meeting, meetings)
        self.assertNotIn(self.other_scheduled_meeting, meetings)

    def test_get_scheduled_meetings_for_parent(self):
        meetings = get_scheduled_meetings(self.parent_user, None, None)
        self.assertIn(self.scheduled_meeting, meetings)
        self.assertNotIn(self.other_scheduled_meeting, meetings)

    def test_get_scheduled_meetings_for_teacher(self):
        meetings = get_scheduled_meetings(self.teacher_user, None, None)
        self.assertIn(self.scheduled_meeting, meetings)
        self.assertNotIn(self.other_scheduled_meeting, meetings)

    def test_get_scheduled_meetings_for_other_student(self):
        meetings = get_scheduled_meetings(self.other_student_user, None, None)
        self.assertIn(self.other_scheduled_meeting, meetings)
        self.assertNotIn(self.scheduled_meeting, meetings)

    def test_get_scheduled_meetings_for_other_parent(self):
        meetings = get_scheduled_meetings(self.other_parent_user, None, None)
        self.assertIn(self.other_scheduled_meeting, meetings)
        self.assertNotIn(self.scheduled_meeting, meetings)

    def test_get_scheduled_meetings_for_other_teacher(self):
        meetings = get_scheduled_meetings(self.other_teacher_user, None, None)
        self.assertIn(self.other_scheduled_meeting, meetings)
        self.assertNotIn(self.scheduled_meeting, meetings)


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
            parent_user=self.parent, child_user=self.student, consent=self.consent_template, is_consent=True)
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


class UserViewSetTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin', password='adminpass', email='admin@admin.com')
        self.client.login(username='admin', password='adminpass')

    def test_create_user(self):
        url = reverse('user-list')
        data = {
            'username': 'newuser',
            'password': 'newpass',
            'email': 'newuser@example.com',
            'role': 'student'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_update_user(self):
        user = User.objects.create_user(
            username='testuser', password='testpass', email='testuser@example.com', role='student')
        url = reverse('user-detail', args=[user.id])
        data = {
            'first_name': 'UpdatedName'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'UpdatedName')


class GradeListCreateViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.student_user = User.objects.create_user(
            username='student_test', password='testpass', role='student', email="student@student.pl")
        self.student = Student.objects.create(user=self.student_user)
        self.teacher_user = User.objects.create_user(
            username='teacher_test', password='testpass', role='teacher', email="teacher@teacher.pl")
        self.teacher = Teacher.objects.create(user=self.teacher_user)
        self.student_group = StudentGroup.objects.create(
            name="Group 1", level=1)
        self.student_group.students.add(self.student)
        self.school_subject = SchoolSubject.objects.create(
            subject_name="Math", student_group=self.student_group)
        self.grade_column = GradeColumn.objects.create(
            title="Test Column", school_subject=self.school_subject)
        self.grade_value = CategoryGradeValue.objects.create(
            code="A", name="Excellent")
        self.client.login(username='teacher_test', password='testpass')

    def test_create_grade(self):
        url = reverse('user_subject_grades', args=[
                      self.student.user_id, self.school_subject.id])
        data = {
            'value': self.grade_value.code,
            'grade_column': self.grade_column.id,
            'count_to_avg': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Grade.objects.count(), 1)

    def test_get_grades(self):
        Grade.objects.create(
            student=self.student, grade_column=self.grade_column, value=self.grade_value)
        url = reverse('user_subject_grades', args=[
                      self.student.user_id, self.school_subject.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ScheduledMeetingViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.teacher_user = User.objects.create_user(
            username='teacher_test', password='testpass', role='teacher', email="teacher@teacher.pl")
        self.teacher = Teacher.objects.create(user=self.teacher_user)
        self.student_user = User.objects.create_user(
            username='student_test', password='testpass', role='student', email="student@student.pl")
        self.student = Student.objects.create(user=self.student_user)
        self.student_group = StudentGroup.objects.create(
            name="Group 1", level=1)
        self.student_group.students.add(self.student)
        self.school_subject = SchoolSubject.objects.create(
            subject_name="Math", student_group=self.student_group)
        self.scheduled_meeting = ScheduledMeeting.objects.create(
            day_of_week=1, slot=1, teacher=self.teacher, school_subject=self.school_subject, place=10)
        self.client.login(username='teacher_test', password='testpass')

    def test_get_scheduled_meetings(self):
        url = reverse('meeting-schedule')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ParentChildrenViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.parent_user = User.objects.create_user(
            username='parent_test', password='testpass', role='parent', email="parent@parent.pl")
        self.parent = Parent.objects.create(user=self.parent_user)
        self.student_user = User.objects.create_user(
            username='student_test', password='testpass', role='student', email="student@student.pl")
        self.student = Student.objects.create(user=self.student_user)
        self.parent.children.add(self.student)
        self.client.login(username='parent_test', password='testpass')

    def test_get_children(self):
        url = reverse('parent_children', args=[self.parent.user_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ElectronicConsentTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.parent_user = User.objects.create_user(
            username='parent_test', password='testpass', role='parent', email="parent@parent.pl")
        self.parent = Parent.objects.create(user=self.parent_user)
        self.student_user = User.objects.create_user(
            username='student_test', password='testpass', role='student', email="student@student.pl")
        self.student = Student.objects.create(user=self.student_user)
        self.parent.children.add(self.student)
        self.teacher_user = User.objects.create_user(
            username='teacher_test', password='testpass', role='teacher', email="teacher@teacher.pl")
        self.teacher = Teacher.objects.create(user=self.teacher_user)
        self.consent_template = ConsentTemplate.objects.create(
            title="Test Consent", author=self.teacher, end_date=timezone.now().date() + timedelta(days=10))
        self.client.login(username='parent_test', password='testpass')
        self.consent_template.students.set([self.student])

    def test_get_pending_consents(self):
        url = reverse('pending_consents')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('parent_submission', response.data[0])
        self.assertIsNone(response.data[0]['parent_submission'])

    def test_get_pending_consents_with_submission(self):
        ParentConsent.objects.create(
            parent_user=self.parent, child_user=self.student, consent=self.consent_template, is_consent=True)
        url = reverse('pending_consents')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('parent_submission', response.data[0])
        self.assertTrue(response.data[0]['parent_submission'])

    def test_get_parent_consent_detail(self):
        parent_consent = ParentConsent.objects.create(
            parent_user=self.parent, child_user=self.student, consent=self.consent_template, is_consent=True)
        url = reverse('parent_consent_detail', args=[parent_consent.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], parent_consent.id)

    def test_create_parent_consent(self):
        url = reverse('parent_consent_submit', args=[self.consent_template.id])
        data = {
            'child_user': self.student.user_id,
            'is_consent': True
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ParentConsent.objects.count(), 1)
        self.assertEqual(ParentConsent.objects.get().is_consent, True)

    def test_get_consent_templates(self):
        self.client.login(username='teacher_test', password='testpass')
        url = reverse('consent_template_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_consent_template(self):
        self.client.login(username='teacher_test', password='testpass')
        url = reverse('consent_template_list')
        data = {
            'title': 'New Consent',
            'description': 'New Description',
            'end_date': (timezone.now().date() + timedelta(days=10)).isoformat(),
            'students': [self.student.user_id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ConsentTemplate.objects.count(), 2)

    def test_get_consent_template_detail_teacher(self):
        self.client.login(username='teacher_test', password='testpass')
        url = reverse('consent_template_detail',
                      args=[self.consent_template.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('parent_consents', response.data)

    def test_get_consent_template_detail_parent(self):
        url = reverse('consent_template_detail',
                      args=[self.consent_template.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('parent_consents', response.data)

    def test_delete_consent_template(self):
        self.client.login(username='teacher_test', password='testpass')
        url = reverse('consent_template_detail',
                      args=[self.consent_template.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ConsentTemplate.objects.count(), 0)

    def test_parent_cannot_create_consent_template(self):
        url = reverse('consent_template_list')
        data = {
            'title': 'New Consent',
            'description': 'New Description',
            'end_date': (timezone.now().date() + timedelta(days=10)).isoformat(),
            'students': [self.student.user_id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_cannot_create_consent_template(self):
        self.client.login(username='student_test', password='testpass')
        url = reverse('consent_template_list')
        data = {
            'title': 'New Consent',
            'description': 'New Description',
            'end_date': (timezone.now().date() + timedelta(days=10)).isoformat(),
            'students': [self.student.user_id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_can_create_consent_template(self):
        self.client.login(username='teacher_test', password='testpass')
        url = reverse('consent_template_list')
        data = {
            'title': 'New Consent',
            'description': 'New Description',
            'end_date': (timezone.now().date() + timedelta(days=10)).isoformat(),
            'students': [self.student.user_id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ConsentTemplate.objects.count(), 2)

    def test_teacher_can_get_consent_template_list(self):
        self.client.login(username='teacher_test', password='testpass')
        url = reverse('consent_template_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_parent_cannot_get_consent_template_list(self):
        url = reverse('consent_template_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_cannot_get_consent_template_list(self):
        self.client.login(username='student_test', password='testpass')
        url = reverse('consent_template_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_can_delete_consent_template(self):
        self.client.login(username='teacher_test', password='testpass')
        url = reverse('consent_template_detail',
                      args=[self.consent_template.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ConsentTemplate.objects.count(), 0)

    def test_parent_cannot_delete_consent_template(self):
        url = reverse('consent_template_detail',
                      args=[self.consent_template.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_cannot_delete_consent_template(self):
        self.client.login(username='student_test', password='testpass')
        url = reverse('consent_template_detail',
                      args=[self.consent_template.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ConsentTemplateModelTests(TestCase):

    def setUp(self):
        self.teacher_user = User.objects.create_user(
            username='teacher_test', password='testpass', role='teacher', email="teacher@teacher.pl")
        self.teacher = Teacher.objects.create(user=self.teacher_user)
        self.parent_user = User.objects.create_user(
            username='parent_test', password='testpass', role='parent', email="parent@parent.pl")
        self.parent = Parent.objects.create(user=self.parent_user)
        self.student_user = User.objects.create_user(
            username='student_test', password='testpass', role='student', email="student@student.pl")
        self.student = Student.objects.create(user=self.student_user)
        self.parent.children.add(self.student)
        self.consent_template = ConsentTemplate.objects.create(
            title="Test Consent", author=self.teacher, end_date=timezone.now().date() + timedelta(days=10))
        self.consent_template.students.add(self.student)

    def test_what_parent_submitted_no_consent(self):
        result = self.consent_template.what_parent_submitted(self.parent)
        self.assertIsNone(result)

    def test_what_parent_submitted_with_consent(self):
        ParentConsent.objects.create(
            parent_user=self.parent, child_user=self.student, consent=self.consent_template, is_consent=True)
        result = self.consent_template.what_parent_submitted(self.parent)
        self.assertTrue(result)

    def test_what_parent_submitted_with_rejection(self):
        ParentConsent.objects.create(
            parent_user=self.parent, child_user=self.student, consent=self.consent_template, is_consent=False)
        result = self.consent_template.what_parent_submitted(self.parent)
        self.assertFalse(result)


class StudentGroupsAPITests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpass', role='teacher', email="teacher@teacher.pl")
        self.teacher = Teacher.objects.create(user=self.user)
        self.student_group = StudentGroup.objects.create(name="Group 1", level=1)
        self.student = Student.objects.create(user=User.objects.create_user(
            username='student_test', password='testpass', role='student', email="student@student.pl"))
        self.student_group.students.add(self.student)
        self.subject = SchoolSubject.objects.create(subject_name="Math", student_group=self.student_group)
        self.client.login(username='testuser', password='testpass')

    def test_get_all_student_groups(self):
        url = reverse('student_group_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_student_group_info(self):
        url = reverse('student_group_detail', args=[self.student_group.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.student_group.name)

    def test_get_students_for_student_group(self):
        url = reverse('student_group_students', args=[self.student_group.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['username'], self.student.user.username)

    def test_get_subjects_for_student_group(self):
        url = reverse('student_group_subjects', args=[self.student_group.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['subject_name'], self.subject.subject_name)


class GetScheduledMeetingsTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Create users
        self.teacher_user = User.objects.create_user(
            username="teacher_test", role="teacher", email="teacher@example.com", password="password")
        self.teacher = Teacher.objects.create(user=self.teacher_user)

        self.student_user = User.objects.create_user(
            username="student_test", role="student", email="student@example.com", password="password")
        self.student = Student.objects.create(user=self.student_user)

        self.parent_user = User.objects.create_user(
            username="parent_test", role="parent", email="parent@example.com", password="password")
        self.parent = Parent.objects.create(user=self.parent_user)
        self.parent.children.add(self.student)

        self.student_group = StudentGroup.objects.create(
            name="Group 1", level=1)
        self.student_group.students.add(self.student)

        self.school_subject = SchoolSubject.objects.create(
            subject_name="Math", student_group=self.student_group)

        self.scheduled_meeting = ScheduledMeeting.objects.create(
            day_of_week=1,  # Poniedziałek
            slot=1,  # 08:00 - 08:45
            teacher=self.teacher,
            school_subject=self.school_subject,
            place=10  # Sala 10
        )

    def test_get_scheduled_meetings_for_student(self):
        meetings = get_scheduled_meetings(self.student_user, None, None)
        self.assertIn(self.scheduled_meeting, meetings)

    def test_get_scheduled_meetings_for_teacher(self):
        meetings = get_scheduled_meetings(self.teacher_user, None, None)
        self.assertIn(self.scheduled_meeting, meetings)

    def test_get_scheduled_meetings_for_parent(self):
        meetings = get_scheduled_meetings(self.parent_user, None, None)
        self.assertIn(self.scheduled_meeting, meetings)

    def test_get_scheduled_meetings_for_student_with_date_range(self):
        start_of_week = timezone.now().date() - timedelta(days=timezone.now().weekday())
        end_of_week = start_of_week + timedelta(days=7)
        meetings = get_scheduled_meetings(self.student_user, start_of_week, end_of_week)
        self.assertIn(self.scheduled_meeting, meetings)

    def test_get_scheduled_meetings_for_teacher_with_date_range(self):
        start_of_week = timezone.now().date() - timedelta(days=timezone.now().weekday())
        end_of_week = start_of_week + timedelta(days=7)
        meetings = get_scheduled_meetings(self.teacher_user, start_of_week, end_of_week)
        self.assertIn(self.scheduled_meeting, meetings)

    def test_get_scheduled_meetings_for_parent_with_date_range(self):
        start_of_week = timezone.now().date() - timedelta(days=timezone.now().weekday())
        end_of_week = start_of_week + timedelta(days=7)
        meetings = get_scheduled_meetings(self.parent_user, start_of_week, end_of_week)
        self.assertIn(self.scheduled_meeting, meetings)
