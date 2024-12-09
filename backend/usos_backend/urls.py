from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .usos_api.views import (
    StudentViewSet, TeacherViewSet, ParentViewSet, GradeViewSet,
    CurrentUserView, UserInfoView, GradeColumnView,
    GradeListCreateView, GradeDetailView, ScheduleView, 
    ConsentTemplateView, FeedView, MeetingViewSet, GradeColumnDetailView, SchoolSubjectViewSet
    ,GradeListCreateView, GradeDetailView, GradeColumnView, GradeColumnDetailView, SchoolSubjectViewSet,
    StudentGroupViewSet, ScheduledMeetingViewSet, AttendanceViewSet, 
    ConsentTemplateViewSet, ParentConsentViewSet, MessageViewSet,GradeColumnViewSet,
    StudentGroupsView, StudentSubjectsView,
    ParentChildrenView, TeacherGroupsView, TeacherSubjectsView,UserViewSet
)

     
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import datetime

router = DefaultRouter()
router.register('students', StudentViewSet, basename='student')
router.register('teachers', TeacherViewSet, basename='teacher')
router.register('parents', ParentViewSet, basename='parent')
router.register('grades', GradeViewSet, basename='grade')
router.register('users', UserViewSet, basename='user')
router.register('meetings', MeetingViewSet, basename='meeting')
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
    
    path('meetings/schedule/', ScheduleView.as_view(), name='schedule'),
    path('econsent/templates/<int:template_consent_id>/', ConsentTemplateView.as_view(), name='consent_template_detail'),
    path('feed/<int:user_id>/', FeedView.as_view(), name='user_feed'),
]
