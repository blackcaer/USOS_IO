from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from usos_backend.usos_api.views import (
    MeetingAttendanceView, MeetingDetailView, MeetingListCreateView, MeetingScheduleView, custom_login_view, custom_logout_view, CurrentUserView, UserInfoView,
    StudentViewSet, TeacherViewSet, ParentViewSet, GradeViewSet,
    GradeColumnView, GradeListCreateView, GradeDetailView, ScheduleView, 
    ConsentTemplateView, FeedView, GradeColumnDetailView, SchoolSubjectViewSet,
    StudentGroupViewSet, ScheduledMeetingViewSet, AttendanceViewSet, 
    ConsentTemplateViewSet, ParentConsentViewSet, MessageViewSet, GradeColumnViewSet,
    StudentGroupsView, StudentSubjectsView, ParentChildrenView, TeacherGroupsView, TeacherSubjectsView, UserViewSet
)

router = DefaultRouter()
router.register('students', StudentViewSet, basename='student')
router.register('teachers', TeacherViewSet, basename='teacher')
router.register('parents', ParentViewSet, basename='parent')
router.register('grades', GradeViewSet, basename='grade')
router.register('users', UserViewSet, basename='user')

router.register('subjects', SchoolSubjectViewSet, basename='subject')
router.register('student-groups', StudentGroupViewSet, basename='studentgroup')
router.register('scheduled-meetings', ScheduledMeetingViewSet, basename='scheduledmeeting')
router.register('attendances', AttendanceViewSet, basename='attendance')
router.register('consent-templates', ConsentTemplateViewSet, basename='consenttemplate')
router.register('parent-consents', ParentConsentViewSet, basename='parentconsent')
router.register('messages', MessageViewSet, basename='message')
router.register('grade-columns', GradeColumnViewSet, basename='gradecolumn')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('auth/login/', custom_login_view, name='login'),
    path('auth/logout/', custom_logout_view, name='logout'),
    path('auth/', include('rest_framework.urls')),
    
    path('user/', CurrentUserView.as_view(), name='current_user'),
    path('user/<int:user_id>/info/', UserInfoView.as_view(), name='user_info'),
    
    path('user/<int:user_id>/student/groups/', StudentGroupsView.as_view(), name='student_groups'),
    path('user/<int:user_id>/student/groups/<int:group_id>/subjects/', StudentSubjectsView.as_view(), name='student_subjects'),
    path('user/<int:user_id>/parent/children/', ParentChildrenView.as_view(), name='parent_children'),
    path('user/<int:user_id>/teacher/groups/', TeacherGroupsView.as_view(), name='teacher_groups'),
    path('user/<int:user_id>/teacher/groups/<int:group_id>/subjects/', TeacherSubjectsView.as_view(), name='teacher_subjects'),
    
    path('grades/<int:user_id>/<int:subject_id>/', GradeListCreateView.as_view(), name='user_subject_grades'),
    path('grades/<int:grade_id>/', GradeDetailView.as_view(), name='grade_detail'),
    path('grades/columns/<int:subject_id>/', GradeColumnView.as_view(), name='grade_columns'),
    path('grades/columns/<int:subject_id>/<int:column_id>/', GradeColumnDetailView.as_view(), name='grade_column_detail'),
    
    path('meetings/', MeetingListCreateView.as_view(), name='meeting-list-create'),
    path('meetings/<int:meeting_id>/', MeetingDetailView.as_view(), name='meeting-detail'),
    path('meetings/schedule/', MeetingScheduleView.as_view(), name='meeting-schedule'),
    path('meetings/<int:meeting_id>/attendance/', MeetingAttendanceView.as_view(), name='meeting-attendance'),
    
    path('econsent/templates/<int:template_consent_id>/', ConsentTemplateView.as_view(), name='consent_template_detail'),
    path('feed/<int:user_id>/', FeedView.as_view(), name='user_feed'),
]
